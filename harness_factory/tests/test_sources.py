import json
import unittest
from pathlib import Path

from harness_factory.collect import iter_entities

SOURCES = Path(__file__).resolve().parent.parent / "src" / "harness_factory" / "data" / "sources.json"
KINDS = {"paper", "repo", "doc", "post", "video", "podcast", "newsletter", "other"}
OUTLET_KINDS = {
    "preprint",
    "journal",
    "publisher",
    "index",
    "database",
    "repository",
    "registry",
    "portal",
    "media",
    "qa",
}
FIELDS = {
    "physics",
    "chemistry",
    "biology",
    "medicine",
    "earth-environment",
    "mathematics",
    "statistics",
    "computer-science",
    "economics-finance",
    "psychology",
    "social-science",
    "law",
    "humanities",
    "education",
    "arts-design",
    "linguistics",
}


class SourcesDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCES.read_text(encoding="utf-8"))

    def test_groups_present(self):
        for group in ("projects", "harnesses", "venues", "people", "media", "outlets"):
            self.assertIn(group, self.data["groups"])
            self.assertIsInstance(self.data["groups"][group], list)

    def test_topic_ids_wellformed(self):
        topic_ids = self.data["topic_ids"]
        self.assertEqual(len(topic_ids), len(set(topic_ids)))

    def test_entities_wellformed_and_topics_known(self):
        topic_ids = set(self.data["topic_ids"])
        ids = []
        for group, entity in iter_entities(self.data):
            eid = entity.get("id", "")
            ids.append(eid)
            self.assertTrue(eid, f"missing id in {group}")
            self.assertTrue(entity.get("name"), f"missing name for {eid}")
            self.assertIn(entity.get("kind", ""), KINDS, f"bad kind for {eid}")
            self.assertTrue(entity.get("url", "").startswith("http"), f"bad url for {eid}")
            topics = entity.get("topics", [])
            self.assertTrue(topics, f"no topics for {eid}")
            for topic in topics:
                self.assertIn(topic, topic_ids, f"unknown topic {topic} on {eid}")
            if entity.get("feed"):
                self.assertTrue(entity["feed"].startswith("http"), f"bad feed for {eid}")
            if entity.get("resolve"):
                self.assertEqual(entity["resolve"], "youtube", f"bad resolve for {eid}")
        self.assertEqual(len(ids), len(set(ids)), "duplicate entity ids")

    def test_feed_coverage(self):
        total = 0
        tracked = 0
        for _group, entity in iter_entities(self.data):
            total += 1
            if entity.get("feed") or entity.get("resolve") == "youtube":
                tracked += 1
        # Guard against accidental feed regressions (currently 47/59).
        self.assertGreaterEqual(tracked, 40)
        self.assertLessEqual(tracked, total)


class OutletDataTest(unittest.TestCase):
    """The `outlets` group is the per-field information landscape (reference,
    not the AI intel feed). Guard its shape and its field coverage."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCES.read_text(encoding="utf-8"))
        cls.outlets = cls.data["groups"]["outlets"]

    def test_group_is_substantial(self):
        self.assertGreaterEqual(len(self.outlets), 40)

    def test_outlet_fields_wellformed(self):
        for o in self.outlets:
            oid = o["id"]
            self.assertIn(o["outlet_kind"], OUTLET_KINDS, oid)
            self.assertIsInstance(o.get("verified"), bool, oid)
            # P27 relaxed this from a pinned date: outlets are verified on different
            # rounds, so the guard checks the date's shape, not one frozen value.
            self.assertRegex(o.get("access") or "", r"^\d{4}-\d{2}-\d{2}$", oid)
            self.assertTrue(o.get("why"), f"no why for {oid}")
            if not o["verified"]:
                self.assertTrue(o.get("note"), f"{oid} not verified but carries no note")

    def test_outlets_cover_every_field(self):
        covered: set[str] = set()
        for o in self.outlets:
            covered |= set(o.get("topics", []))
        self.assertEqual(FIELDS - covered, set())


if __name__ == "__main__":
    unittest.main()
