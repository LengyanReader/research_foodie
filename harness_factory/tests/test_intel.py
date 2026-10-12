import json
import tempfile
import unittest
from pathlib import Path

from harness_factory import evolution
from harness_factory.collect import (
    Candidate,
    feed_provider,
    iter_entities,
    parse_feed,
    resolve_youtube_feed,
)
from harness_factory.extract import extract_intel, entity_index, write_intel
from harness_factory.refresh import run_refresh

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Feed</title>
<item><title>SEAL self-evolution</title><link>https://x/1</link><guid>x1</guid>
<pubDate>Wed, 01 Oct 2025 00:00:00 GMT</pubDate>
<description>&lt;p&gt;agent &lt;b&gt;harness&lt;/b&gt; design&lt;/p&gt;</description></item>
</channel></rss>"""

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>M</title>
<entry><title>New agent harness</title><link href="https://y/1"/><id>yt:1</id>
<published>2026-01-02T00:00:00+00:00</published><summary>about harness</summary></entry>
</feed>"""

ENTITY = {"id": "v", "name": "Venue", "kind": "paper", "topics": ["evaluation-gates"]}
MEDIA = {
    "id": "m",
    "name": "M",
    "kind": "video",
    "url": "https://youtube.com/@m",
    "feed": None,
    "resolve": "youtube",
    "topics": ["agent-harness"],
}


class FeedTest(unittest.TestCase):
    def test_parse_rss(self):
        items = parse_feed(RSS, ENTITY)
        self.assertEqual(len(items), 1)
        c = items[0]
        self.assertEqual(c.title, "SEAL self-evolution")
        self.assertEqual(c.url, "https://x/1")
        self.assertEqual(c.external_id, "x1")
        self.assertEqual(c.published, "2025-10-01")
        self.assertEqual(c.kind, "paper")
        self.assertEqual(c.entity, "v")
        self.assertEqual(c.source_kind, "feed")
        self.assertNotIn("<b>", c.summary)
        self.assertIn("harness", c.summary)

    def test_parse_atom(self):
        items = parse_feed(ATOM, MEDIA)
        self.assertEqual(len(items), 1)
        c = items[0]
        self.assertEqual(c.title, "New agent harness")
        self.assertEqual(c.url, "https://y/1")
        self.assertEqual(c.external_id, "yt:1")
        self.assertEqual(c.published, "2026-01-02")
        self.assertEqual(c.kind, "video")

    def test_parse_empty_and_malformed(self):
        self.assertEqual(parse_feed("", ENTITY), [])
        self.assertEqual(parse_feed("<not xml", ENTITY), [])

    def test_resolve_youtube(self):
        html = '{"channelId":"UC' + "a" * 22 + '"}'
        url = resolve_youtube_feed("https://youtube.com/@m", lambda _u: html)
        self.assertIn("channel_id=UC", url)
        self.assertIsNone(resolve_youtube_feed("https://youtube.com/@m", lambda _u: "no id"))

    def test_feed_provider_resolves_and_filters_since(self):
        calls = []

        def fake(url):
            calls.append(url)
            if "@m" in url:
                return '{"channelId":"UC' + "a" * 22 + '"}'
            return ATOM

        sources = {"groups": {"media": [MEDIA]}}
        provider = feed_provider(sources, fetcher=fake)
        items = provider({})
        self.assertEqual(len(items), 1)
        self.assertIn("channel_id=UC", calls[1])

        provider_since = feed_provider(sources, fetcher=fake, since="2026-02-01")
        self.assertEqual(provider_since({}), [])

    def test_iter_entities(self):
        sources = {"groups": {"a": [ENTITY], "b": [MEDIA]}}
        self.assertEqual(len(iter_entities(sources)), 2)


class IntelTest(unittest.TestCase):
    def _sources(self):
        return {"groups": {"harnesses": [{"id": "openai-agents-sdk", "name": "OpenAI Agents SDK", "kind": "repo", "topics": ["agent-harness"]}]}}

    def _watchlist(self):
        return {"topics": [{"id": "agent-harness", "keywords": ["harness", "handoff"]}]}

    def test_entity_index(self):
        idx = entity_index(self._sources())
        self.assertIn("openai-agents-sdk", idx)

    def test_extract_scores_keywords_and_entity(self):
        cand = Candidate(
            title="OpenAI Agents SDK adds handoffs",
            url="https://x/1",
            entity="openai-agents-sdk",
            kind="repo",
            published="2026-01-01",
        )
        items = extract_intel([cand], self._sources(), self._watchlist())
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertGreater(item.relevance, 1.0)
        self.assertTrue(any(s.startswith("kw:") for s in item.signals))
        self.assertIn("entity:openai-agents-sdk", item.signals)
        self.assertEqual(item.entity_name, "OpenAI Agents SDK")

    def test_extract_enrich(self):
        cand = Candidate(title="t", entity="openai-agents-sdk")
        items = extract_intel([cand], self._sources(), self._watchlist(), enrich=lambda _t: "summary")
        self.assertEqual(items[0].brief, "summary")

    def test_write_intel(self):
        cand = Candidate(title="t", url="https://x", entity="openai-agents-sdk")
        items = extract_intel([cand], self._sources(), self._watchlist())
        with tempfile.TemporaryDirectory() as tmp:
            write_intel(tmp, items)
            updates = Path(tmp) / "updates"
            self.assertTrue((updates / "INTEL.md").exists())
            rows = [json.loads(l) for l in (updates / "intel.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 1)
            self.assertIn("Vendor harnesses", (updates / "INTEL.md").read_text(encoding="utf-8"))


class EvolutionTest(unittest.TestCase):
    def _sources(self):
        return {
            "groups": {
                "projects": [
                    {"id": "p", "name": "P", "kind": "repo", "topics": ["agent-harness"], "feed": None}
                ],
                "harnesses": [],
            }
        }

    def _watchlist(self):
        return {"cadence": "weekly", "topics": [{"id": "agent-harness"}, {"id": "evaluation-gates"}]}

    def test_snapshot_coverage(self):
        m = evolution.snapshot(self._sources(), self._watchlist())
        self.assertEqual(m["entities"], 1)
        self.assertEqual(m["uncovered_topics"], ["evaluation-gates"])
        self.assertAlmostEqual(m["topic_coverage"], 0.5)

    def test_audit_and_propose(self):
        src, wl = self._sources(), self._watchlist()
        audits = evolution.audit(src, wl, [])
        kinds = {a.kind for a in audits}
        self.assertIn("uncovered_topic", kinds)
        self.assertIn("empty_group", kinds)
        proposals = evolution.propose(audits)
        self.assertEqual({p.action for p in proposals}, {"add_source", "populate_group"})

    def test_run_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = evolution.run_evolution(tmp, self._sources(), self._watchlist())
            self.assertGreaterEqual(summary["n_proposals"], 1)
            updates = Path(tmp) / "updates"
            for name in ("EVOLUTION.md", "evolution.jsonl", "metrics.jsonl", "JOURNAL.md"):
                self.assertTrue((updates / name).exists(), name)

            pid = summary["proposals"][0]["id"]
            applied = evolution.apply_accepted(tmp, [pid])
            self.assertEqual(applied, [pid])
            ledger = json.loads((updates / "accepted.json").read_text(encoding="utf-8"))
            self.assertEqual(ledger[0]["status"], "accepted")

            target = summary["proposals"][1]["target"]
            self.assertEqual(evolution.apply_accepted(tmp, [target]), [summary["proposals"][1]["id"]])

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            evolution.run_evolution(tmp, self._sources(), self._watchlist(), dry_run=True)
            self.assertFalse((Path(tmp) / "updates").exists())


class RefreshIntelTest(unittest.TestCase):
    def test_refresh_writes_intel_under_root(self):
        sources = {
            "groups": {
                "harnesses": [
                    {"id": "op", "name": "OpenAI", "kind": "repo", "url": "https://x", "feed": None, "topics": ["agent-harness"]}
                ]
            }
        }
        watch = {"topics": [{"id": "agent-harness", "keywords": ["harness"]}]}
        cand = Candidate(title="New harness", url="https://x/1", entity="op", kind="repo")

        with tempfile.TemporaryDirectory() as tmp:
            run_refresh(
                tmp,
                providers=[lambda _wl: [cand]],
                provider_names=["feed"],
                watchlist=watch,
                sources=sources,
                intel=True,
            )
            updates = Path(tmp) / "updates"
            self.assertTrue((updates / "INTEL.md").exists())
            self.assertTrue((updates / "intel.jsonl").exists())
            self.assertFalse((updates / "updates").exists())


if __name__ == "__main__":
    unittest.main()
