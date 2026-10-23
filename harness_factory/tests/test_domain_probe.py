"""Guards for the domain probe (P29): the automated finder surfaces unmapped
clusters, stays silent on mapped ones, and proposes without touching the SSOT."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import domain_probe


def _write_intel(kb: Path, items: list[dict]) -> None:
    path = kb / domain_probe.INTEL_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for item in items:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")


class DomainProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_no_intel_is_a_quiet_noop(self):
        self.assertEqual(domain_probe.probe(self.tmp), [])

    def test_unmapped_cluster_surfaces_with_nearest_domain(self):
        items = [
            {"title": "Transcranial ultrasound neurostimulation for memory recall", "brief": "note one"},
            {"title": "Transcranial ultrasound waveform tuning study", "brief": "note two"},
            {"title": "Transcranial ultrasound phased-array calibration", "brief": "note three"},
            # mapped items must not leak into the cluster
            {"title": "A survey of agent memory systems", "brief": "memory survey"},
        ]
        _write_intel(self.tmp, items)
        proposals = domain_probe.probe(self.tmp)
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["keyword"], "transcranial")
        self.assertEqual(proposals[0]["n_items"], 3)
        self.assertIsInstance(proposals[0]["nearest_domain"], str)

    def test_fully_mapped_intel_yields_no_proposals(self):
        items = [
            {"title": "A literature review of agent memory with citations", "brief": "review"},
            {"title": "构建方志人物知识图谱并做检索增强问答，注明来源", "brief": "KG"},
        ]
        _write_intel(self.tmp, items)
        self.assertEqual(domain_probe.probe(self.tmp), [])

    def test_emit_writes_the_report_only(self):
        items = [{"title": f"Glymphatic clearance of brain waste during sleep {i}", "brief": "new"} for i in range(3)]
        _write_intel(self.tmp, items)
        proposals = domain_probe.probe(self.tmp)
        self.assertEqual(len(proposals), 1)
        path = domain_probe.emit(self.tmp, proposals)
        self.assertTrue(path.exists())
        self.assertIn("glymphatic", path.read_text(encoding="utf-8"))
        # proposals never touch the SSOT: only the report exists under updates/
        names = sorted(p.name for p in (self.tmp / "updates").iterdir())
        self.assertEqual(names, ["DOMAIN-PROBES.md", "intel.jsonl"])


if __name__ == "__main__":
    unittest.main()
