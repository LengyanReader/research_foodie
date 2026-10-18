import unittest
from pathlib import Path

from harness_factory.catalog import (
    class_ids,
    filter_rows,
    find,
    items,
    kind_ids,
    render_markdown,
    search,
    validate,
)

ROOT = Path(__file__).resolve().parent.parent
INDEX_DOC = ROOT / "review" / "harness-index.md"


class CatalogDataTest(unittest.TestCase):
    def test_validate_is_clean(self):
        self.assertEqual(validate(), [])

    def test_size_and_vocab(self):
        self.assertGreaterEqual(len(items()), 40)
        self.assertGreaterEqual(len(class_ids()), 6)
        self.assertGreaterEqual(len(kind_ids()), 8)

    def test_ids_unique(self):
        ids = [e["id"] for e in items()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_find(self):
        entry = find("godel-agent")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["class"], "self-evolution")
        self.assertIsNone(find("no-such-harness"))

    def test_search(self):
        hits = search("voyager")
        self.assertTrue(any(e["id"] == "voyager" for e in hits))
        self.assertGreaterEqual(len(search("memory")), 3)

    def test_filter_by_class_and_module(self):
        rows = filter_rows(klass="self-evolution")
        self.assertTrue(rows)
        self.assertTrue(all(e["class"] == "self-evolution" for e in rows))
        m5 = filter_rows(module="M5")
        self.assertTrue(m5)
        self.assertTrue(all("M5" in e["maps_to"] for e in m5))

    def test_tracked_cross_links_are_real(self):
        tracked = filter_rows(tracked_only=True)
        self.assertGreaterEqual(len(tracked), 10)
        self.assertTrue(all(e["tracked"] for e in tracked))


class InstrumentCatalogTest(unittest.TestCase):
    """`instruments` carries the evidence tools the discipline capabilities name (M3.10)."""

    def test_instruments_class_is_populated(self):
        rows = [e for e in items() if e["class"] == "instruments"]
        self.assertGreaterEqual(len(rows), 20)
        self.assertGreaterEqual(len({e["kind"] for e in rows}), 8)

    def test_every_instrument_has_url_module_and_verified_flag(self):
        for e in (e for e in items() if e["class"] == "instruments"):
            with self.subTest(e["id"]):
                self.assertTrue(e.get("url"), e["id"])
                self.assertTrue(e.get("maps_to"), e["id"])
                self.assertTrue({"M3", "M4"} & set(e["maps_to"]), f"{e['id']}: instruments must carry evidence-bearing modules")
                self.assertIsInstance(e.get("verified"), bool)

    def test_formal_and_empirical_instruments_are_present(self):
        ids = {e["id"] for e in items() if e["class"] == "instruments"}
        for expected in ("lean4", "rocq", "isabelle", "agda", "dafny", "z3", "tla-plus",
                         "pint", "uncertainties", "rdkit", "rcsb-pdb", "uniprot",
                         "universal-dependencies", "psychopy", "osf", "lme4", "stan", "snakemake"):
            self.assertIn(expected, ids)


class CatalogIndexDriftTest(unittest.TestCase):
    def test_index_doc_matches_generated(self):
        self.assertTrue(INDEX_DOC.exists(), "run `harness catalog --write`")
        on_disk = INDEX_DOC.read_text(encoding="utf-8")
        self.assertEqual(on_disk, render_markdown(), "review/harness-index.md is stale; regenerate")

    def test_index_marks_generated(self):
        self.assertIn("do not edit by hand", render_markdown())


if __name__ == "__main__":
    unittest.main()
