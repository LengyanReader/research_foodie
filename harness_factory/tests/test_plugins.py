from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from harness_factory import plugins, registry, standard
from harness_factory.assemble import build_files, write_harness
from harness_factory.check import check_harness
from harness_factory.classify import classify
from harness_factory.spec import TaskSpec


def _domain_plugin(pid="aux-domain", **over):
    data = {
        "id": pid,
        "kind": "domain",
        "version": "0.1.0",
        "title_en": "Auxiliary Domain",
        "name_zh": "辅助域",
        "summary": "A test-only plugin domain.",
        "faculty": "general",
        "artifact": "document",
        "grounding": "preferred",
        "workflow": ["step one", "step two"],
        "signals": ["zzz-aux-signal", "辅助测试"],
        "extra_templates": ["aux-appendix"],
        "rubric": {
            "title_en": "Auxiliary rubric",
            "dimensions": [
                {"dim": "clarity", "zh": "清晰", "weight": 0.6},
                {"dim": "rigor", "zh": "严谨", "weight": 0.4},
            ],
        },
    }
    data.update(over)
    return data


def _template_plugin(pid="aux-appendix", **over):
    data = {
        "id": pid,
        "kind": "template",
        "version": "0.1.0",
        "name": pid,
        "target": ".harness/aux-appendix.md",
    }
    data.update(over)
    return data


class PluginTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._old = os.environ.get("HARNESS_PLUGINS_DIR")
        os.environ["HARNESS_PLUGINS_DIR"] = str(self.base)
        plugins.clear_caches()

    def tearDown(self):
        if self._old is None:
            os.environ.pop("HARNESS_PLUGINS_DIR", None)
        else:
            os.environ["HARNESS_PLUGINS_DIR"] = self._old
        plugins.clear_caches()
        self._tmp.cleanup()

    def _write_plugin(self, dirname, data, files=None):
        d = self.base / dirname
        d.mkdir(parents=True, exist_ok=True)
        (d / "plugin.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        for name, content in (files or {}).items():
            (d / name).write_text(content, encoding="utf-8")
        return d


class DiscoverTest(PluginTestBase):
    def test_discovers_domain_and_template(self):
        self._write_plugin("aux-domain", _domain_plugin())
        self._write_plugin(
            "aux-appendix",
            _template_plugin(),
            {"aux-appendix.tmpl": "# Aux appendix for {{ domain }}\n"},
        )
        found = {p.id: p for p in plugins.discover()}
        self.assertEqual(set(found), {"aux-domain", "aux-appendix"})
        self.assertEqual(found["aux-domain"].kind, "domain")
        self.assertEqual(plugins.problems(), [])

    def test_empty_dir_reports_nothing(self):
        self.assertEqual(plugins.discover(), [])
        self.assertEqual(plugins.problems(), [])


class RegistrationTest(PluginTestBase):
    def setUp(self):
        super().setUp()
        self._write_plugin("aux-domain", _domain_plugin())
        self._write_plugin(
            "aux-appendix",
            _template_plugin(),
            {"aux-appendix.tmpl": "# Aux appendix for {{ domain }}\n"},
        )
        plugins.clear_caches()

    def test_domain_entry_and_registry_merge(self):
        self.assertIn("aux-domain", plugins.domain_entries())
        self.assertIn("aux-domain", registry.domains())
        self.assertIn("aux-domain", registry.domain_ids())

    def test_rubric_merge(self):
        self.assertIn("aux-domain", standard.rubrics())
        self.assertEqual(
            standard.dimensions("aux-domain"),
            ["clarity", "rigor"],
        )

    def test_classify_reaches_plugin_domain(self):
        feats = classify(TaskSpec(text="please handle the zzz-aux-signal work"))
        self.assertEqual(feats.domain, "aux-domain")

    def test_assemble_emits_extra_template(self):
        task = TaskSpec(text="aux job", domain="aux-domain")
        feats = classify(task, overrides={"domain": "aux-domain"})
        from harness_factory.derive import derive

        plan = derive(task, feats)
        files = build_files(plan)
        self.assertIn(".harness/aux-appendix.md", files)
        self.assertIn("aux-domain", files[".harness/aux-appendix.md"])
        manifest = json.loads(files[".harness/manifest.json"])
        self.assertIn(".harness/aux-appendix.md", manifest["files"])

    def test_written_harness_passes_check(self):
        task = TaskSpec(text="aux job", domain="aux-domain")
        feats = classify(task, overrides={"domain": "aux-domain"})
        from harness_factory.derive import derive

        plan = derive(task, feats)
        with tempfile.TemporaryDirectory() as out:
            write_harness(plan, out)
            self.assertEqual(check_harness(out), [])


class ValidationTest(PluginTestBase):
    def test_bad_artifact_is_reported(self):
        self._write_plugin("bad-domain", _domain_plugin("bad-domain", artifact="nonsense"))
        problems = plugins.problems()
        self.assertTrue(any("artifact must be" in p for p in problems), problems)
        self.assertNotIn("bad-domain", plugins.domain_entries())

    def test_bad_rubric_weights_reported(self):
        bad = _domain_plugin("bad-rubric")
        bad["rubric"]["dimensions"] = [{"dim": "clarity", "weight": 0.5}]
        self._write_plugin("bad-rubric", bad)
        self.assertTrue(any("sum to ~1.0" in p for p in plugins.problems()))

    def test_missing_template_file_reported(self):
        self._write_plugin("aux-appendix", _template_plugin())  # no .tmpl file
        self.assertTrue(any("missing template file" in p for p in plugins.problems()))

    def test_id_must_match_dir(self):
        self._write_plugin("dir-name", _domain_plugin("other-id"))
        self.assertTrue(any("must match the directory name" in p for p in plugins.problems()))

    def test_cannot_shadow_builtin(self):
        self._write_plugin("research", _domain_plugin("research"))
        self.assertTrue(any("shadows a built-in" in p for p in plugins.problems()))
        # the built-in wins; the shadowing plugin is ignored
        self.assertNotIn("plugin", registry.domains()["research"])

    def test_template_target_rejects_escape(self):
        self._write_plugin(
            "aux-appendix",
            _template_plugin(target="../escape.md"),
            {"aux-appendix.tmpl": "x\n"},
        )
        self.assertTrue(any("relative in-tree path" in p for p in plugins.problems()))


if __name__ == "__main__":
    unittest.main()
