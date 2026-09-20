"""E-2 health check + E-1 baseline freeze + E-2b gate coverage (WS-C, Phase X).

Every cadence re-runs the **frozen subset** against `_eval_out/baselines.json`
with variance-aware thresholds (design rules #2/#3 in
`docs/design/self-evolution-mechanism.md`):

  - mock regression (deterministic, hard gate)          → `test_pipeline mock` 34/34
  - judge sanity on frozen proxy manuscripts (P-A/B/C)  → |Δ Total| ≥ 2σ FAIL · ≥ 1σ WARN
  - pool-coverage re-scan + arXiv reachability probe    → −10% of recorded = WARN
  - L6 gate-coverage mutation check (E-2b, zero-LLM)    → ≥20 mutants, 100% kill rate

Exit code: `0` GREEN · `1` WARN · `2` FAIL.

Usage:
  python -m tools.eval.health_check --freeze   # (re)write baselines.json only, zero-LLM
  python -m tools.eval.health_check --quick    # skip the LLM judge step (mock+pool+gate)
  python -m tools.eval.health_check            # full cycle (adds ~1.5 min judge step)

The judge step re-scores the *already-rendered* proxy manuscripts (fixed
artifacts) rather than re-running the pipeline, so a cadence measures
judge/backend drift without re-paying full pipeline cost (still <10 min).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from tools.eval.bench_eval import SCENARIOS, score_survey, _family_avgs
from tools.llm.client import LLMClient

REPO_ROOT = Path(__file__).resolve().parent.parents[1]
EVAL_OUT = REPO_ROOT / "_eval_out"
BASELINES = EVAL_OUT / "baselines.json"
REPORT = EVAL_OUT / "health_check.md"
MANUSCRIPTS = EVAL_OUT / "manuscripts"
SOURCE_MD = REPO_ROOT / "_demo_downloads/mineru_out_ds0509/liang2023_test/auto/liang2023_test.md"

GOOD_CITE = "arXiv:2304.02819"  # Liang et al. 2023 — well-formed control cite

FROZEN_PROXY = ["P-A", "P-B", "P-C"]
ARXIV_PROBE = "https://export.arxiv.org/api/query?search_query=all:electron&max_results=1"

# Thresholds in judge-noise units (baseline σ per proxy comes from
# variance_runs.json at freeze time; P-A ≈ 0.53 → 2σ ≈ ±1.06 on Total).
FAIL_SIGMA = 2.0
WARN_SIGMA = 1.0
POOL_WARN_FRAC = 0.10  # −10% of recorded coverage = WARN

# Recorded constants (as of 2026-09-20, PROGRESS Session 19b); files take
# precedence at freeze time when present.
DOC_MOCK = {"assertions": 34, "failures": 0}
DOC_PANEL = {"n": 31, "correctness": 4.23, "groundedness": 4.45, "pass": "24/31"}


def _load(name: str):
    p = EVAL_OUT / name
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _proxy_variances() -> dict:
    """Per-proxy mean/sd/n from variance_runs.json (the only LLM-measured noise).

    Only the SINGLE-CALL population (median=1) is the baseline: L-3 median-of-3
    rounds (median=3) are a different measurement protocol and must not shift
    the σ the cadence compares against.
    """
    recs = _load("variance_runs.json") or []
    by: dict = {}
    for r in recs:
        if r.get("median", 1) != 1:
            continue
        by.setdefault(r["topic_id"], []).append(r.get("total"))
    out = {}
    for tid in FROZEN_PROXY:
        tots = [t for t in by.get(tid, []) if t is not None]
        if not tots:
            continue
        out[tid] = {
            "mean": round(statistics.mean(tots), 2),
            "sd": round(statistics.stdev(tots), 2) if len(tots) > 1 else 0.0,
            "n": len(tots),
        }
    return out


def _pool_coverage() -> dict:
    pools = _load("pools_30.json") or {}
    total = len(pools)
    covered = partial = full = 0
    for v in pools.values():
        papers = v.get("papers") or []
        n = len(papers)
        if n >= 1:
            covered += 1
        if n >= 3:
            full += 1
        elif n >= 1:
            partial += 1
    return {"total": total, "covered": covered,
            "full": full, "partial": partial, "empty": total - covered}


def _gate_mutants() -> list:
    """E-2b: L6 mutation corpus (zero-LLM). Each entry: (name, result_dict,
    expected_reject). ``result_dict`` is passed to the L6 ``validate`` whole —
    which is how structure-drop mutants (missing ``draft``/``taxonomy``) are
    expressed faithfully.

    Reject-class designers (all deterministic — no reliance on source content):
    - **gap-1 interleave** — a unique never-in-source token inserted before
      every word, so every 5-content-token window contains the filler ⇒ zero
      shared 5-grams with the source regardless of text. Verbatim sentences are
      the base so the mutation is *specifically* about contiguity, not about
      the sentence being foreign.
    - **synthetic negatives** — fabricated claims/numbers/cites with no source
      ȧoverlap (5-gram set disjoint by construction).
    - **structure drops** — the result dict literally lacks ``draft`` (or
      ``taxonomy``), exercising the structure hard check.

    Keep-controls must NOT reject: verbatim quote · one-word paraphrase (fuzzy
    tolerance) · empty quote (informational) · Latin-only draft (bilingual is
    a warning, not a hard gate).
    """
    src = SOURCE_MD.read_text(encoding="utf-8") if SOURCE_MD.is_file() else ""
    sentences = [s for s in src.replace("\n", " ").split(".") if len(s.split()) >= 12]
    if len(sentences) < 6:
        sentences += [
            "GPT detectors can wrongly flag non-native English writing as AI-generated",
            "Bias in detectors skews toward false positives for second-language writers",
            "Watermarking and statistical detection differ in robustness and deployment cost",
        ]
    filler = "__fl__"

    def _killed_gap1(sentence: str) -> str:
        # interleave at TOKEN level (post _toks): a descendant word like
        # `<sup>1,2,3,+</sup>` expands to several tokens, so a raw-word join
        # would leave a run without the filler → shared 5-gram survives. Token-
        # level expansion guarantees every 5-content-token window has filler.
        from tools.pipeline.validate import _toks as _tk
        return " ".join(f"{filler} {t}" for t in _tk(sentence))

    base = {
        "output": "x" * 200,
        "claims": [{"claim": "text", "cite": GOOD_CITE}],
        "taxonomy": {"topics": []},
        "draft": "reasoning underpins this summary 中文 双语",
    }

    mutants: list = []

    # -- gap-1 interleave rejects (verbatim sentences, contiguity broken)
    for i, s in enumerate(sentences[:8]):
        claims = [{"claim": "text", "quote": _killed_gap1(s), "cite": GOOD_CITE}]
        mutants.append((f"interleave gap1 s{i}", dict(base, claims=claims), True))

    # -- synthetic negatives (no source overlap by construction)
    for j, q in enumerate([
        "97.4% of all detectors achieve perfect accuracy on Korean corpora",
        "Photosynthesis converts light into chemical energy inside plant cells",
        "The quantum engine accelerated past the outer ring of the orbital station",
        "维生素 C deficiency impairs collagen synthesis 这是错误的翻译示例",
    ]):
        mutants.append((f"synthetic negative {j}", dict(base, claims=[
            {"claim": "text", "quote": q, "cite": GOOD_CITE}]), True))

    # -- structure drops (validate requires output/claims/taxonomy/draft)
    mutants.append(("structure no draft",
                    {"output": "x" * 200, "claims": [{"claim": "text", "cite": GOOD_CITE}],
                     "taxonomy": {"topics": []}}, True))
    mutants.append(("structure no taxonomy",
                    {"output": "x" * 200, "claims": [{"claim": "text", "cite": GOOD_CITE}],
                     "draft": "d"}, True))
    mutants.append(("structure no claims",
                    {"output": "x" * 200, "taxonomy": {"topics": []}, "draft": "d"}, True))

    # -- malformed-cite rejects
    for k, cite in enumerate(["arXiv:2304", "arXiv:23", "please cite this", "  "]):
        mutants.append((f"bad cite {k}", dict(base, claims=[
            {"claim": "text", "quote": sentences[0], "cite": cite}]), True))

    # -- keep-controls (must NOT reject)
    base_claims_g = lambda q: dict(base,  # noqa: E731
                                   claims=[{"claim": "text", "quote": q, "cite": GOOD_CITE}])
    mutants += [
        ("verbatim quote", base_claims_g(sentences[0]), False),
        ("one-word paraphrase", base_claims_g(_swap_word(sentences[0])), False),
        ("empty quote (informational)", base_claims_g(""), False),
        ("latin-only draft (bilingual=warn only)", dict(base_claims_g(sentences[0]),
                                                        draft="english only draft no chinese"), False),
    ]
    return mutants


def _swap_word(sentence: str) -> str:
    """Paraphrase-tolerant mutant: swap one filler-safe word inside a verbatim
    sentence. 5-grams around the swap are still mostly shared, so the gate must
    NOT reject it (fuzzy grounding tolerance)."""
    words = sentence.split()
    for i in range(len(words) - 1, -1, -1):
        w = words[i].strip("(),.;:")
        if len(w) >= 5 and w.lower() not in {"these", "those", "which", "their"}:
            words[i] = words[i].replace(w, "bigger")
            break
    return " ".join(words)


def _gate_coverage() -> dict:
    """Run the L6 validate() over the mutant corpus; report kill rate."""
    from tools.pipeline.validate import validate

    mutants = _gate_mutants()
    if len(mutants) < 20:
        return {"mutants": len(mutants), "passed": 0, "kill_rate": 0.0,
                "results": {}, "error": f"only {len(mutants)} mutants (need >=20)"}
    src = SOURCE_MD.read_text(encoding="utf-8") if SOURCE_MD.is_file() else ""
    rejected = 0
    results = {}
    for name, result, expect_reject in mutants:
        rep = validate(result, src)
        got_reject = not rep["passed"]
        results[name] = {"expected_reject": expect_reject, "got_reject": got_reject,
                         "score": round(rep["score"], 2),
                         "fails": list(k for k, v in rep["checks"].items() if not v["ok"])}
        if got_reject == expect_reject:
            rejected += 1
    return {
        "mutants": len(mutants),
        "passed": rejected,
        "kill_rate": round(rejected / len(mutants), 3) if mutants else 0.0,
        "results": results,
    }


def _arxiv_reachable(timeout: float = 12.0) -> bool:
    try:
        req = urllib.request.Request(ARXIV_PROBE, headers={"User-Agent": "research_foodie/0.1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def _mock_regression():
    """Run `test_pipeline mock` (deterministic); parse verdict from stdout."""
    try:
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "tools.pipeline.test_pipeline", "mock"],
            capture_output=True, text=True, encoding="utf-8", timeout=240,
        )
    except subprocess.TimeoutExpired:
        return {"completed": False, "reason": "timeout>240s", "rc": None}
    out = (proc.stdout or "") + (proc.stderr or "")
    m = re.search(r"==== (\d+) FAILED ====", out)
    all_pass = "==== ALL PASS ====" in out
    n_fail = int(m.group(1)) if m else (0 if all_pass else -1)
    return {"completed": proc.returncode == 0, "rc": proc.returncode,
            "all_pass": all_pass, "failed": n_fail > 0, "n_failed": n_fail}


def _judge_sanity(client: LLMClient):
    """Re-score frozen proxy manuscripts; return per-proxy totals."""
    scored = {}
    for tid in FROZEN_PROXY:
        topic = next((s["topic"] for s in SCENARIOS if s["topic_id"] == tid),
                     f"proxy {tid}")
        md_p = MANUSCRIPTS / f"{tid}_manuscript.md"
        if not md_p.is_file():
            scored[tid] = {"ok": False, "reason": "no manuscript artifact"}
            continue
        artifact = md_p.read_text(encoding="utf-8")
        if "\n## Sources (" in artifact:
            artifact = artifact.split("\n## Sources (", 1)[0].rstrip()
        bench = score_survey(client, topic, artifact)
        vals = [v for v in bench["scores"].values()]
        scored[tid] = {
            "ok": bool(vals),
            "total": round(statistics.mean(vals), 2) if vals else None,
            "coverage": bench["coverage"],
            "judge_model": bench.get("judge_model", "?"),
        }
    return scored


def _diff(current: dict) -> dict:
    """Compare current measurements vs baselines; produce verdicts."""
    base = current.pop("_baseline", {})
    verdicts = []

    mock = current["mock"]
    b_mock = base.get("mock", DOC_MOCK)
    if not mock.get("completed") or not mock.get("all_pass"):
        verdicts.append({"level": "FAIL", "check": "mock",
                         "detail": f"mock regression failed: {mock}"})
    else:
        verdicts.append({"level": "PASS", "check": "mock",
                         "detail": f"mock 34/34 (baseline {b_mock.get('assertions')}/{b_mock.get('failures')})"})

    pool = current["pools"]
    b_pool = base.get("pools", {})
    cover = pool["covered"] / pool["total"] if pool["total"] else 0
    b_cover = b_pool.get("covered", 0) / b_pool.get("total", 1) if b_pool.get("total") else 0
    if b_cover and cover < b_cover * (1 - POOL_WARN_FRAC):
        verdicts.append({"level": "WARN", "check": "pools",
                         "detail": f"coverage {pool['covered']}/{pool['total']} = {cover:.0%} vs baseline {b_cover:.0%} (−{POOL_WARN_FRAC:.0%} threshold)"})
    else:
        verdicts.append({"level": "PASS", "check": "pools",
                         "detail": f"coverage {pool['covered']}/{pool['total']} (full {pool['full']})"})

    probe = current["arxiv_reachable"]
    if not probe:
        verdicts.append({"level": "WARN", "check": "arxiv_probe",
                         "detail": f"{ARXIV_PROBE} unreachable (network/live rail)"})
    else:
        verdicts.append({"level": "PASS", "check": "arxiv_probe", "detail": "reachable"})

    gc = current["gate_coverage"]
    if gc["kill_rate"] >= 1.0 and gc["mutants"] >= 20:
        verdicts.append({"level": "PASS", "check": "gate_coverage",
                         "detail": f"{gc['passed']}/{gc['mutants']} mutants killed (100%)"})
    else:
        survivors = [k for k, v in gc["results"].items() if v["got_reject"] != v["expected_reject"]]
        verdicts.append({"level": "WARN", "check": "gate_coverage",
                         "detail": f"kill_rate={gc['kill_rate']} ({gc['passed']}/{gc['mutants']}); survivors={survivors} → fix the gate, not the prompt"})

    for tid in FROZEN_PROXY:
        cur_t = current["judge"].get(tid) or {}
        b_t = (base.get("judge_variance") or {}).get(tid) or {}
        if not cur_t.get("ok"):
            verdicts.append({"level": "SKIP", "check": f"judge:{tid}",
                             "detail": f"no current score ({cur_t.get('reason', 'n/a')})"})
            continue
        b_mean = b_t.get("mean")
        if b_mean is None:
            verdicts.append({"level": "SKIP", "check": f"judge:{tid}",
                             "detail": "no baseline mean"})
            continue
        # σ floor: a recorded sd=0.00 (e.g. P-B: two identical rounds) must not
        # freeze the comparison — treat it as at least one meaningful unit.
        sigma = b_t.get("sd", 0.0) or 0.10
        delta = abs(cur_t["total"] - b_mean)
        sig = delta / sigma
        if sig >= FAIL_SIGMA:
            lvl = "FAIL"
        elif sig >= WARN_SIGMA:
            lvl = "WARN"
        else:
            lvl = "PASS"
        verdicts.append({"level": lvl, "check": f"judge:{tid}",
                         "detail": f"current {cur_t['total']} vs baseline {b_mean} "
                                   f"(σ={sigma}) → Δ={delta:.2f} = {sig:.1f}σ "
                                   f"(FAIL≥{FAIL_SIGMA}σ, WARN≥{WARN_SIGMA}σ)"})

    levels = {"FAIL": 2, "WARN": 1, "SKIP": 0, "PASS": 0}
    exit_code = max((levels[v["level"]] for v in verdicts), default=0)
    return {"verdicts": verdicts, "exit_code": exit_code}


def _freeze() -> dict:
    from tools.llm.profiles import load_profile, profile_header, ProfileError
    try:
        prof = load_profile()
    except ProfileError:
        prof = None
    base = {
        "as_of": "2026-09-20",
        "backend": {"llm": "opencode/big-pickle (free, directional)",
                    "profile": profile_header(prof) if prof else "profile N/A"},
        "mock": DOC_MOCK,
        "qa_panel": DOC_PANEL,
        "judge_variance": _proxy_variances(),
        "pools": {k: v for k, v in _pool_coverage().items()},
        "thresholds": {"fail_sigma": FAIL_SIGMA, "warn_sigma": WARN_SIGMA,
                       "warn_sigma_units": "on judge Total (proxy manuscripts×1 round)"},
    }
    return base


def _fmt_report(rep: dict, judge: dict, base: dict, elapsed: float,
                provenance: str = "") -> str:
    jm = next(iter((
        v.get("judge_model") for v in judge.values()
        if isinstance(v, dict) and v.get("judge_model"))), "skipped (--quick)")
    L = ["# Health check / 健康检查 (WS-C E-2)", "",
         f"> Updated: 2026-09-20 · elapsed {elapsed:.0f}s · frozen subset = mock "
         f"34/34 + judge sanity {FROZEN_PROXY} + pools re-scan + L6 gate coverage",
         f"> Judge: {jm}  ·  thresholds: 2σ FAIL / 1σ WARN "
         f"(σ per proxy from baselines.json)"]
    if provenance:
        L.append(f"> Provenance (D-4): {provenance}")
    L.append("")
    for v in rep["verdicts"]:
        L.append(f"- **[{v['level']}]** `{v['check']}` — {v['detail']}")
    L += ["", "## Baselines (frozen at freeze time)", ""]
    jv = base.get("judge_variance", {})
    L.append("| proxy | baseline mean | σ | n | 2σ |")
    L.append("|---|---|---|---|---|")
    for tid in FROZEN_PROXY:
        b = jv.get(tid)
        if b:
            L.append(f"| {tid} | {b['mean']} | {b['sd']} | {b['n']} | {2 * b['sd']:.2f} |")
        else:
            L.append(f"| {tid} | - | - | - | - |")
    L += ["", f"- qa_panel: {DOC_PANEL}", f"- pools: {base.get('pools', {})}",
          f"- gate_coverage: {rep.get('gc', {})}", ""]
    return "\n".join(L)


def run_cycle(quick: bool = False, profile_name: str | None = None,
              backend: str | None = None, model: str | None = None) -> dict:
    """One full frozen-subset cycle (importable — E-3 evolution_sprint wraps
    this; `main()` is the argv front end). Returns verdicts + exit code."""
    EVAL_OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    base = _load("baselines.json")
    if not base or not base.get("judge_variance"):
        print("[health] no baselines.json — freezing now (E-1 implements first)")
        base = _freeze()
        BASELINES.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")

    mock = _mock_regression()
    gc = _gate_coverage()
    pools = _pool_coverage()
    probe = _arxiv_reachable()

    judge = {}
    provenance = "judge skipped (--quick)"
    if not quick:
        from tools.llm.profiles import load_profile, clients_for, profile_header, ProfileError
        try:
            profile = load_profile(profile_name)
        except ProfileError as e:
            print(f"[health] profile error: {e}")
            return {"exit_code": 2, "verdicts": [{"level": "FAIL", "check": "profile",
                                                  "detail": str(e)}],
                    "rep": {}, "current": {}, "base": base, "judge": {},
                    "elapsed": time.time() - t0, "provenance": f"profile error: {e}"}
        print(f"[health] {profile_header(profile)}")
        _, judge_client = clients_for(profile)
        provenance = profile_header(profile)
        # explicit CLI overrides beat the profile (ad hoc judging vantage)
        if backend or model:
            judge_client = LLMClient(backend=backend or "opencode", model=model)
        judge = _judge_sanity(judge_client)
    else:
        for tid in FROZEN_PROXY:
            judge[tid] = {"ok": False, "reason": "skipped (--quick)"}

    current = {"mock": mock, "pools": pools, "arxiv_reachable": probe,
               "gate_coverage": gc, "judge": judge, "_baseline": base}
    rep = _diff(current)
    rep["gc"] = gc
    elapsed = time.time() - t0
    report_txt = _fmt_report(rep, judge, base, elapsed, provenance)
    REPORT.write_text(report_txt, encoding="utf-8")
    print(f"\n[health] wrote {REPORT}")
    for v in rep["verdicts"]:
        print(f"  [{v['level']:<4}] {v['check']:<14} {v['detail']}")
    print(f"\n[health] exit_code={rep['exit_code']} "
          f"({('GREEN','WARN','FAIL')[rep['exit_code']] if rep['exit_code'] < 3 else '?'})")
    return {"exit_code": rep["exit_code"], "verdicts": rep["verdicts"],
            "rep": rep, "current": current, "base": base, "judge": judge,
            "elapsed": elapsed, "provenance": provenance}


def main() -> int:
    ap = argparse.ArgumentParser(description="E-2 health check + E-1 baseline freeze")
    ap.add_argument("--freeze", action="store_true",
                    help="(re)write baselines.json from current artifacts (zero-LLM) and exit")
    ap.add_argument("--quick", action="store_true",
                    help="skip the LLM judge sanity step (mock + pools + gate coverage only)")
    ap.add_argument("--backend", default=None,
                    help="override judge backend (default: from profile)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--profile", default=None,
                    help="named profile from tools.llm.profiles (default: env LLM_PROFILE)")
    a = ap.parse_args()

    EVAL_OUT.mkdir(parents=True, exist_ok=True)

    if a.freeze:
        base = _freeze()
        BASELINES.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[health] baselines frozen → {BASELINES} (judge_variance={base['judge_variance']})")
        return 0

    return run_cycle(a.quick, a.profile, a.backend, a.model)["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())