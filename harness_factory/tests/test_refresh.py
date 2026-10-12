from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory.collect import Candidate, collect, file_provider, llm_provider
from harness_factory.curate import extract_keys, known_keys
from harness_factory.refresh import apply_accepted, run_refresh


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class CollectTest(unittest.TestCase):
    def test_extract_keys(self):
        keys = extract_keys("see arXiv:2408.08435 and https://x.y/z and doi 10.1234/abcd")
        self.assertIn("2408.08435", keys)
        self.assertIn("https://x.y/z", keys)
        self.assertIn("10.1234/abcd", keys)

    def test_file_provider_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox.jsonl"
            _write(
                inbox,
                json.dumps({"title": "T", "url": "https://a.b/c", "topics": ["agent-memory"]}) + "\n",
            )
            cands = collect([file_provider(inbox)], {"topics": []})
            self.assertEqual(len(cands), 1)
            self.assertEqual(cands[0].url, "https://a.b/c")
            self.assertEqual(cands[0].topics, ["agent-memory"])

    def test_llm_provider_uses_injected_discover(self):
        def fake_discover(topics, since=None, max_items=10):
            return [{"title": "New", "external_id": "2601.00001", "kind": "paper"}]

        cands = collect(
            [llm_provider(discover=fake_discover)],
            {"topics": [{"id": "x", "queries": ["q"]}], "frontier_probes": []},
        )
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0].source_kind, "llm")


class RefreshTest(unittest.TestCase):
    def _root(self) -> Path:
        tmp = Path(tempfile.mkdtemp())
        _write(tmp / "review" / "references.md", "R1. Something (arXiv:2408.08435).\n")
        _write(
            tmp / "updates" / "inbox.jsonl",
            "\n".join(
                [
                    json.dumps({"title": "Dup", "external_id": "2408.08435", "kind": "paper"}),
                    json.dumps(
                        {
                            "title": "Fresh agent memory paper",
                            "url": "https://arxiv.org/abs/2601.12345",
                            "kind": "paper",
                            "topics": ["agent-memory"],
                            "published": "2026-01-05",
                        }
                    ),
                    json.dumps({"title": "No ref", "summary": "untraceable"}),
                ]
            )
            + "\n",
        )
        return tmp

    def test_run_refresh_dedupes_and_reports(self):
        root = self._root()
        summary = run_refresh(root, providers=[file_provider(root / "updates" / "inbox.jsonl")])
        self.assertEqual(summary["collected"], 3)
        self.assertEqual(summary["accepted"], 1)
        self.assertEqual(summary["rejected"], 2)
        self.assertTrue((root / "updates" / "REPORT.md").exists())
        queue = (root / "updates" / "queue.jsonl").read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(queue), 1)
        self.assertIn("agent-memory", json.loads(queue[0])["topics"])
        journal = (root / "updates" / "JOURNAL.md").read_text(encoding="utf-8")
        self.assertIn("refresh", journal)

    def test_dry_run_writes_nothing(self):
        root = self._root()
        summary = run_refresh(
            root,
            providers=[file_provider(root / "updates" / "inbox.jsonl")],
            dry_run=True,
        )
        self.assertEqual(summary["accepted"], 1)
        self.assertFalse((root / "updates" / "REPORT.md").exists())

    def test_apply_accepts_by_index_and_writes_proposal(self):
        root = self._root()
        run_refresh(root, providers=[file_provider(root / "updates" / "inbox.jsonl")])
        applied = apply_accepted(root, ["0"])
        self.assertEqual(len(applied), 1)
        proposals = list((root / "updates" / "proposals").glob("*.md"))
        self.assertEqual(len(proposals), 1)
        row = json.loads((root / "updates" / "queue.jsonl").read_text(encoding="utf-8"))
        self.assertEqual(row["status"], "accepted")

    def test_known_keys_from_corpus(self):
        root = self._root()
        keys = known_keys([root / "review" / "references.md"])
        self.assertIn("2408.08435", keys)

    def test_run_persists_watermark(self):
        root = self._root()
        run_refresh(root, providers=[file_provider(root / "updates" / "inbox.jsonl")])
        state = json.loads((root / "updates" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["since"], "2026-01-05")
        self.assertIn("last_run", state)

    def test_watermark_resumes_as_default_since(self):
        root = self._root()
        run_refresh(root, providers=[file_provider(root / "updates" / "inbox.jsonl")])
        summary = run_refresh(root, providers=[])
        self.assertEqual(summary["since"], "2026-01-05")


if __name__ == "__main__":
    unittest.main()
