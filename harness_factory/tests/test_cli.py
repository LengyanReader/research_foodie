import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from harness_factory import cli

_FAKE_SOURCES = {
    "groups": {
        "harnesses": [
            {
                "id": "x",
                "name": "X",
                "kind": "repo",
                "url": "https://example.com/x",
                "feed": None,
                "topics": ["agent-harness"],
                "tags": [],
                "why": "test",
            }
        ]
    }
}


def run(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            code = cli.main(args)
        except SystemExit as exc:  # argparse --version / errors
            code = exc.code
    return code, buf.getvalue()


class CliTest(unittest.TestCase):
    def test_version(self):
        code, out = run(["--version"])
        self.assertEqual(code, 0)
        self.assertIn("harness-factory", out)

    def test_derive_json(self):
        code, out = run(["derive", "--task", "write a literature review", "--json"])
        self.assertEqual(code, 0)
        plan = json.loads(out)
        self.assertIn("modules", plan)
        self.assertTrue(any(m["module_id"] == "M0" for m in plan["modules"]))

    def test_init_then_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = str(Path(tmp) / "task")
            code, _ = run(["init", "--task", "add unit tests to the parser", "--out", out_dir])
            self.assertEqual(code, 0)
            self.assertTrue((Path(out_dir) / ".harness" / "manifest.json").exists())
            code, out = run(["check", "--dir", out_dir])
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_sources_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "sources.json"
            src.write_text(json.dumps(_FAKE_SOURCES), encoding="utf-8")
            code, out = run(["sources", "--json", "--sources", str(src)])
            self.assertEqual(code, 0)
            data = json.loads(out)
            self.assertIn("harnesses", data["groups"])

    def test_evolve_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "sources.json"
            src.write_text(json.dumps(_FAKE_SOURCES), encoding="utf-8")
            code, out = run(["evolve", "--dry-run", "--root", tmp, "--sources", str(src)])
            self.assertEqual(code, 0)
            self.assertIn("dry-run", out)
            self.assertFalse((Path(tmp) / "updates").exists())

    def test_gate_passes_on_fresh_harness(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = str(Path(tmp) / "task")
            run(["init", "--task", "add unit tests to the parser", "--out", out_dir])
            code, out = run(["gate", "--dir", out_dir])
            self.assertEqual(code, 0)
            self.assertIn("PASS", out)

    def test_gate_fails_without_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            # D1a: a failed gate run records a gate_miss trace in the tool home; point it at a temp dir.
            old_home = os.environ.get("HARNESS_HOME")
            os.environ["HARNESS_HOME"] = str(Path(tmp) / "home")
            try:
                code, out = run(["gate", "--dir", tmp])
            finally:
                if old_home is None:
                    os.environ.pop("HARNESS_HOME", None)
                else:
                    os.environ["HARNESS_HOME"] = old_home
            self.assertEqual(code, 1)
            self.assertIn("FAIL", out)
            from harness_factory import trace

            lines = trace.read_traces(Path(tmp) / "home" / "updates" / "traces.jsonl")
            self.assertEqual(lines[-1]["event"], "gate_miss")

    def test_harvest_writes_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = str(Path(tmp) / "task")
            run(["init", "--task", "add unit tests to the parser", "--out", out_dir])
            kb = str(Path(tmp) / "kb")
            code, out = run(["harvest", "--dir", out_dir, "--root", kb, "--json"])
            self.assertEqual(code, 0)
            bundle = json.loads(out)
            self.assertTrue(bundle["gates"]["passed"])
            self.assertTrue((Path(kb) / "updates" / "signals.jsonl").exists())

    def test_plugins_empty_dir_validates(self):
        from harness_factory import plugins

        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("HARNESS_PLUGINS_DIR")
            os.environ["HARNESS_PLUGINS_DIR"] = tmp
            plugins.clear_caches()
            try:
                code, out = run(["plugins", "--validate"])
                self.assertEqual(code, 0)
                self.assertIn("validation: OK", out)
            finally:
                if old is None:
                    os.environ.pop("HARNESS_PLUGINS_DIR", None)
                else:
                    os.environ["HARNESS_PLUGINS_DIR"] = old
                plugins.clear_caches()


if __name__ == "__main__":
    unittest.main()
