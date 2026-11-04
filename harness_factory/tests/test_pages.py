"""P69 simulation tests for the GitHub-Pages dashboard.

The page's job is to *visualize* what the SSOT already says, so these tests lock the
contract that matters for a static, dependency-free GitHub Pages artifact: it is
self-contained (no <script>/<link>/<img>, so it renders on the first byte), it is
bilingual, it escapes untrusted intel titles, it dedupes the timeline, and it builds
offline from committed data alone.
"""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from harness_factory import pages


def _sm(**over):
    base = {
        "capabilities": {"total": 43},
        "domains": {"total": 34},
        "catalog": {"total": 221},
        "clauses": {"anchored_total": 44},
        "references": {"total": 291},
        "cycles": {"total": 64},
        "battery": {"families": 9, "done": 9, "updated": "2026-11-01"},
        "traces": {"total": 24, "events": {}},
        "gaps": {
            "domains_without_capability": ["a-domain", "b-domain"],
            "caps_without_procedure": ["cap-x"],
            "uncovered_topics": ["ambition-and-agency"],
        },
    }
    base.update(over)
    return base


def _tool(id_, name, family, status, tags=("apache-2.0",)):
    return {"id": id_, "name": name, "family": family, "status": status,
            "status_label": "OSS ok · 开源核", "tags": list(tags),
            "url": f"https://github.com/x/{id_}"}


def _snap():
    return {
        "generated": "2026-11-03", "horizon": "2026-10-04",
        "items": 3336, "untracked": 0,
        "clusters": {
            "industry": {"title": "AI industry & adjacent fields · 全行业", "count": 2851,
                          "recent": 648, "sources": 13,
                          "top": [{"rel": 3.5, "date": "2026-10-22", "source": "SW",
                                    "title": "Donating Agent Skills", "url": "https://a/1"}]},
            "harness": {"title": "Harness directions · harness", "count": 3336, "recent": 888,
                         "sources": 11,
                         "top": [{"rel": 3.0, "date": "2026-10-20", "source": "arXiv",
                                   "title": "Self-evolving " + "x" * 90, "url": "https://b/2"}]},
            "trajectories": {"title": "Other promising trajectories · 其他", "count": 0,
                              "recent": 0, "sources": 0, "top": []},
            "domains": {"title": "Field-by-field signals · 学科", "count": 10, "recent": 10,
                         "sources": 2, "top": []},
        },
    }


class StatusMappingTest(unittest.TestCase):
    def test_license_and_flag_tags_map_to_the_intake_gate(self):
        self.assertEqual(pages._status(["apache-2.0"])[0], "ok")
        self.assertEqual(pages._status(["mit"])[0], "ok")
        self.assertEqual(pages._status(["gateway", "license-check"])[0], "warn")
        self.assertEqual(pages._status(["retrieval", "defunct-track"])[0], "bad")
        self.assertEqual(pages._status(["eval", "unverified"])[0], "bad")


class BitsTest(unittest.TestCase):
    def test_hbars_emits_responsive_rows_with_a_visible_sliver_for_small_values(self):
        html = pages.hbars([("Industry", 2851, 648), ("Domains", 10, 10)])
        self.assertIn('class="gbars"', html)
        self.assertEqual(html.count('class="gbar"'), 2)
        # the tiny 10-vs-2851 bar still gets a non-zero width (>=0.8%) so it is never "missing"
        widths = [float(w) for w in re.findall(r'gtotal" style="width:([\d.]+)%', html)]
        self.assertTrue(all(w > 0 for w in widths))

    def test_hbars_empty_is_safe(self):
        self.assertIn("muted", pages.hbars([]))

    def test_timeline_dedupes_by_url_and_flags_nothing_when_empty(self):
        rows = [
            {"date": "2026-10-22", "source": "S", "title": "T1", "url": "https://dup"},
            {"date": "2026-10-22", "source": "S", "title": "T1", "url": "https://dup"},
            {"date": "2026-10-20", "source": "S", "title": "T2", "url": "https/unique"},
        ]
        html = pages.timeline(rows)
        self.assertEqual(html.count('class="tln"'), 2)  # the repeat collapses
        self.assertIn("…", pages.timeline(
            [{"date": "2026-10-01", "source": "S", "title": "y" * 200, "url": "https/long"}]))

    def test_tool_matrix_groups_by_family(self):
        html = pages.tool_matrix([_tool("mem0", "Mem0", "F1", "ok"),
                                  _tool("vllm", "vLLM", "F6", "ok")])
        self.assertIn("F1", html)
        self.assertIn("Mem0", html)
        self.assertIn("vLLM", html)

    def test_ring_encodes_the_momentum_share_as_a_percentage(self):
        self.assertIn("23%", pages.ring(0.227))   # industry 648/2851 rounds to 23%
        self.assertIn("100%", pages.ring(1.0))
        self.assertIn("0%", pages.ring(0.0))
        self.assertIn("<svg", pages.ring(0.5))     # pure inline SVG, no external asset

    def test_trend_cards_one_per_cluster_and_zero_safe(self):
        rows = [("Industry", 2851, 648, 13), ("Harness", 3336, 888, 11),
                ("Trajectories", 0, 0, 0), ("Domains", 10, 10, 2)]
        html = pages.trend_cards(rows)
        self.assertEqual(html.count('class="tcard"'), 4)
        self.assertEqual(html.count('class="ring"'), 4)
        self.assertIn("0%", html)                  # the empty cluster reads 0%, not missing
        self.assertIn("13 sources", html)          # source breadth shown
        self.assertIn("muted", pages.trend_cards([]))

    def test_segmented_marks_done_cells(self):
        full = pages.segmented(9, 9)
        self.assertEqual(full.count('seg on'), 9)
        self.assertEqual(full.count('seg off'), 0)
        part = pages.segmented(2, 5)
        self.assertEqual(part.count('seg on'), 2)
        self.assertEqual(part.count('seg off'), 3)
        self.assertIn("muted", pages.segmented(0, 0))


class RenderTest(unittest.TestCase):
    def _html(self):
        return pages.render_html({
            "generated": "2026-11-03 00:00 UTC", "self_model": _sm(),
            "trend": _snap(),
            "tools": [_tool("mem0", "Mem0", "F1", "ok"),
                      _tool("litellm", "LiteLLM", "F6", "warn", ("license-check",)),
                      _tool("ms-graphrag", "GraphRAG", "!", "bad", ("defunct-track",))],
        })

    def test_page_is_self_contained_no_script_no_external_asset(self):
        html = self._html()
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"))
        self.assertNotRegex(html, r"(?i)<(script|link|img)[ >]")
        self.assertNotIn("<iframe", html.lower())

    def test_page_is_bilingual_and_carries_every_section(self):
        html = self._html()
        for marker in ("全景趋势与能力仪表盘", "Self-model", "Gap register",
                       "Trend-review clusters", "AI tool-stack", "Frontier dialectics"):
            self.assertIn(marker, html)

    def test_page_visualizes_svg_gauges_and_grouped_bars(self):
        html = self._html()
        self.assertIn("<svg", html)                 # gauges
        self.assertEqual(html.count('class="gbar"'), 4)  # four clusters
        self.assertIn("R291", html)
        self.assertIn("9/9", html)

    def test_page_adds_momentum_rings_evidence_strip_and_domain_chips(self):
        html = self._html()
        self.assertEqual(html.count('class="tcard"'), 4)  # one momentum card per cluster
        self.assertEqual(html.count('class="ring"'), 4)   # momentum share rings
        self.assertEqual(html.count('seg on'), 9)         # 9/9 battery families filled
        self.assertEqual(html.count('chip dom'), 2)       # the 2 uncovered domains are named
        self.assertIn("momentum share", html)             # legend explains ring vs bar

    def test_page_escapes_untrusted_intel_titles(self):
        bad = {"generated": "t", "self_model": _sm(),
               "trend": {"generated": "t", "horizon": "h", "items": 1, "untracked": 0,
                         "clusters": {"harness": {"title": "Harness", "count": 1, "recent": 1,
                                                   "sources": 1,
                                                   "top": [{"rel": 2.0, "date": "2026-10-01",
                                                            "source": "S", "title": "<img src=x onerror=alert(1)>",
                                                            "url": "https://x"}]}}},
               "tools": []}
        html = pages.render_html(bad)
        self.assertNotIn("<img src=x", html)
        self.assertIn("&lt;img", html)


class ArticlesTest(unittest.TestCase):
    def test_every_related_article_path_exists_no_dead_link(self):
        base = Path(__file__).resolve().parent.parent / "review"
        self.assertTrue(pages.ARTICLES)
        for _zh, _en, rel in pages.ARTICLES:
            self.assertTrue((base / rel).exists(), f"dead link: review/{rel}")

    def test_articles_link_to_local_html_pages(self):
        """P65-ext: articles link to local rendered .html pages, not GitHub .md blobs."""
        html = pages.render_html({
            "generated": "2026-11-03 00:00 UTC", "self_model": _sm(),
            "trend": _snap(),
            "tools": [_tool("mem0", "Mem0", "F1", "ok")],
        })
        self.assertIn("Related articles", html)
        # every article links to a local .html file, not a GitHub blob URL
        self.assertNotIn(f"{pages.REPO_URL}/blob/", html, "GitHub blob links must not appear")
        self.assertEqual(html.count('class="art"'), len(pages.ARTICLES))
        # check a specific link points to the local page
        self.assertIn('href="trend-review-2026-11-03.html"', html)
        self.assertNotRegex(html, r"(?i)<(script|link|img)[ >]")  # self-contained

    def test_repo_url_points_at_the_real_repo(self):
        self.assertEqual(pages.REPO_URL, "https://github.com/LengyanReader/research_foodie")


class BuildTest(unittest.TestCase):
    def test_default_out_is_docs_index_at_repo_root(self):
        self.assertEqual(pages.default_out().name, "index.html")
        self.assertEqual(pages.default_out().parent.name, "docs")

    def test_collect_reads_the_live_ssot(self):
        data = pages.collect()
        self.assertIn("self_model", data)
        self.assertTrue(data["tools"])  # the 13 feed-pullable P68 tools are present
        self.assertTrue(all("feed" not in t or t["url"] for t in data["tools"]))

    def test_run_write_emits_page_and_nojekyll_into_target_dir(self):
        out = Path(tempfile.mkdtemp()) / "docs" / "index.html"
        res = pages.run(write=True, out=str(out))
        self.assertTrue(out.exists())
        self.assertTrue((out.parent / ".nojekyll").exists())
        self.assertGreater(res["bytes"], 3000)
        self.assertIn("capabilities", res)

    def test_run_offline_without_snapshot_still_builds(self):
        # CI has the committed snapshot, but a fresh checkout with none must not crash.
        from unittest import mock
        with mock.patch.object(pages.trend, "load_snapshot", return_value=None):
            html = pages.render_html({"generated": "t", "self_model": _sm(),
                                       "trend": None, "tools": []})
        self.assertIn("<!doctype html>", html.lower())
        self.assertIn("trend-snapshot", html)  # graceful "run harness trend --write" hint


if __name__ == "__main__":
    unittest.main()
