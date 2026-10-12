import json
import unittest
from pathlib import Path

from harness_factory.collect import iter_entities

SOURCES = Path(__file__).resolve().parent.parent / "src" / "harness_factory" / "data" / "sources.json"
KINDS = {"paper", "repo", "doc", "post", "video", "podcast", "newsletter", "other"}


class SourcesDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCES.read_text(encoding="utf-8"))

    def test_groups_present(self):
        for group in ("projects", "harnesses", "venues", "people", "media"):
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


if __name__ == "__main__":
    unittest.main()
