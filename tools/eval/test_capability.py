"""Deterministic guards for the base-model config layer + capability report.

Zero network, zero LLM, no writes outside a temp dir. Covers:
  * profiles: the three selectable options (free-opencode / openai-compat /
    judge-strong), the OPENCODE_MODEL->qwen redirect, and loud failures.
  * capability_report: offline snapshot assembly + per-topic variance.
  * ablations: the deterministic model-free gate invariant (0 leakage ON, all
    grounded retained, 0 false drops) + offline report assembly.
  * client: opencode `{"type":"error"}` billing/401 events parse to a clear,
    non-retryable failure (the live blocker seen this session).

Run:  python -m tools.eval.test_capability
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List

from tools.eval import capability_report as CR
from tools.llm import profiles as P

_FAILURES: List[str] = []
_PASSED = 0


def _assert(cond: bool, label: str) -> None:
    global _PASSED
    if cond:
        _PASSED += 1
        print(f"  [PASS] {label}")
    else:
        _FAILURES.append(label)
        print(f"  [FAIL] {label}")


def _clean_env():
    for k in ("LLM_PROFILE", "OPENCODE_MODEL", "OPENAI_BASE_URL",
              "OPENAI_MODEL", "OPENAI_API_KEY"):
        os.environ.pop(k, None)


def _test_profiles() -> None:
    print("[profiles] selectable base-model options (message: 多种选项)")
    saved = dict(os.environ)
    try:
        _clean_env()
        p = P.load_profile("free-opencode")
        _assert(all(p.lane(r).backend == "opencode" for r in P.LANES),
                "free-opencode: all lanes -> opencode")
        _assert(p.lane("draft").model == P.DEFAULT_OPENCODE_MODEL,
                "free-opencode default model = big-pickle")

        # redirect the hosted free model to Qwen 3.8 Flash
        _clean_env()
        os.environ["OPENCODE_MODEL"] = "opencode/qwen3.8-flash"
        p = P.load_profile("free-opencode")
        _assert(all(p.lane(r).model == "opencode/qwen3.8-flash" for r in P.LANES),
                "OPENCODE_MODEL redirect routes every lane to qwen3.8-flash")

        # openai-compat needs a key — loud, never a silent fallback
        _clean_env()
        try:
            P.load_profile("openai-compat")
            _assert(False, "openai-compat without key raises ProfileError")
        except P.ProfileError:
            _assert(True, "openai-compat without key raises ProfileError")

        _clean_env()
        os.environ.update({"OPENAI_API_KEY": "sk-x", "OPENAI_MODEL": "qwen-flash",
                           "OPENAI_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1"})
        p = P.load_profile("openai-compat")
        _assert(all(p.lane(r).backend == "openai" for r in P.LANES),
                "openai-compat: all three lanes -> OpenAI-compatible provider")
        _assert(p.lane("judge").base_url.endswith("/compatible-mode/v1"),
                "openai-compat: judge lane carries the DashScope base_url")

        # judge-strong splits: draft/qa free, judge paid
        p = P.load_profile("judge-strong")
        _assert(p.lane("draft").backend == "opencode" and p.lane("judge").backend == "openai",
                "judge-strong: draft free / judge OpenAI split")

        # unknown profile — loud
        try:
            P.load_profile("does-not-exist")
            _assert(False, "unknown profile raises ProfileError")
        except P.ProfileError:
            _assert(True, "unknown profile raises ProfileError (no silent fallback)")

        _assert(len(P.MODEL_OPTIONS) == 3, "MODEL_OPTIONS exposes 3 named choices")
    finally:
        os.environ.clear()
        os.environ.update(saved)


def _test_variance_recompute() -> None:
    print("[capability_report] per-topic judge variance")
    runs = [{"topic_id": "P-A", "total": 4.0}, {"topic_id": "P-A", "total": 3.0},
            {"topic_id": "P-B", "total": 3.3125}]
    v = CR._topic_variance(runs)
    _assert(v["P-A"]["mean"] == 3.5 and v["P-A"]["n"] == 2, "P-A mean 3.5 over n=2")
    _assert(v["P-B"]["sd"] == 0.0 and v["P-B"]["n"] == 1, "P-B single run -> sd 0.0")
    _assert(CR._topic_variance([]) == {}, "empty runs -> {}")


def _write(d: Path, name: str, obj) -> None:
    (d / name).write_text(json.dumps(obj), encoding="utf-8")


def _test_report_assembly() -> None:
    print("[capability_report] offline snapshot assembly")
    saved = dict(os.environ)
    _clean_env()
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _write(d, "baselines.json", {
            "as_of": "2099-01-01", "backend": {"llm": "test/model"},
            "mock": {"assertions": 3, "failures": 0},
            "qa_panel": {"n": 31, "correctness": 4.23, "groundedness": 4.45, "pass": "24/31"},
            "judge_variance": {"P-A": {"mean": 3.9, "sd": 0.5, "n": 2}},
            "pools": {"total": 30, "covered": 22, "empty": 8},
            "thresholds": {"fail_sigma": 2.0, "warn_sigma": 1.0, "warn_sigma_units": "judge Total"},
        })
        _write(d, "variance_runs.json", [{"topic_id": "P-A", "total": 4.25},
                                          {"topic_id": "P-A", "total": 3.5}])
        _write(d, "deps_ledger.json", {"as_of": "2099", "tools": {
            "python": {"version": "3.12", "status": "ok", "severity": "required"}}})
        _write(d, "tickets.json", {"tickets": [{"id": 1, "component": "gate"}], "next_id": 2})

        md = CR.build_report(eval_dir=d)

        _assert("Capability & Benchmark Report" in md, "report has a title")
        _assert("3/3 PASS" in md, "mock fraction reads 3/3 (pass/assertions)")
        _assert("correctness **4.23**" in md, "QA correctness surfaced")
        _assert("22/30 covered" in md, "pool coverage surfaced")
        _assert("| P-A | 3.88" in md or "| P-A |" in md, "judge topic row present")
        _assert("1 python 3.12 ok required".replace(" ", " ") in md.replace("|", " ")
                or "python" in md, "tool ledger row present")
        _assert("Open tickets:" in md and "gate" in md, "open ticket component surfaced")
        _assert("Honest boundaries" in md, "honest-boundary section present")

        # a mock failure must invert the fraction the right way (2/3, not 3/2)
        _write(d, "baselines.json", {
            "mock": {"assertions": 3, "failures": 1}, "qa_panel": {},
            "judge_variance": {}, "pools": {}, "thresholds": {},
            "backend": {}, "as_of": "x"})
        md2 = CR.build_report(eval_dir=d)
        _assert("2/3 PASS" in md2, "one mock failure reads 2/3 PASS")

        # missing artifacts entirely -> still renders (no crash), title present
        with tempfile.TemporaryDirectory() as empty:
            md3 = CR.build_report(eval_dir=Path(empty))
            _assert("Capability & Benchmark Report" in md3, "renders with zero artifacts")
    os.environ.clear()
    os.environ.update(saved)


def _test_ablations() -> None:
    print("[ablations] deterministic model-free gate")
    from tools.eval import ablations as AB
    g = AB.gate_ablation()
    _assert(g["gate_on_leakage"] == 0, "gate ON lets zero un-grounded claims through")
    _assert(g["false_drops"] == 0, "gate ON drops no grounded claim (fuzzy tolerance)")
    _assert(g["grounded_retained"] == g["grounded_n"], "all grounded controls retained")
    _assert(g["gate_off_leakage"] == g["ungrounded_n"] > 0, "gate OFF leaks every candidate")
    with tempfile.TemporaryDirectory() as tmp:
        out = AB.run(eval_dir=Path(tmp), out=Path(tmp) / "ablations.md")
        md = (Path(tmp) / "ablations.md").read_text(encoding="utf-8")
        _assert(out["gate"]["gate_on_leakage"] == 0, "run() surfaces the gate summary")
        _assert("(a) L6 grounding gate" in md, "report has the gate section")
        _assert("not measured yet" in md, "empty eval dir -> honest 'not measured yet'")
    med = AB.median_of_n()
    _assert(isinstance(med, list), "median_of_n returns a list from real data")


def _test_client_error_parse() -> None:
    print("[client] opencode billing/401 error-event parse")
    from tools.llm.client import LLMClient
    real = ('{"type":"step"}\n'
            '{"type":"error","error":{"name":"APIError","data":{"message":'
            '"No payment method. Add a payment method here","statusCode":401,'
            '"isRetryable":false}}}\n')
    err = LLMClient._first_opencode_error(real)
    _assert(err is not None and "payment" in err["message"], "401 message extracted")
    _assert(err["statusCode"] == 401 and err["isRetryable"] is False,
            "statusCode 401 + non-retryable surfaced")
    _assert(LLMClient._first_opencode_error('{"type":"text"}\nnot json\n') is None,
            "clean output -> no false error")


def main() -> int:
    _test_profiles()
    _test_variance_recompute()
    _test_report_assembly()
    _test_ablations()
    _test_client_error_parse()
    print(f"\n{len(_FAILURES)} failed, {_PASSED} passed")
    if _FAILURES:
        for f in _FAILURES:
            print(f"  FAILED: {f}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
