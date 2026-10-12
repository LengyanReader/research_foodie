import contextlib
import io
import json
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


if __name__ == "__main__":
    unittest.main()
