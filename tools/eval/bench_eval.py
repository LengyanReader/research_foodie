"""DAS-Bench-style benchmark evaluation for research_foodie.

Uses the *existing* DAS-Bench dataset assets that ship in `external/DAS`
(worktree):
  - `benchmark/topics.json`            — the 30 benchmark topics (ids 001-030)
  - `benchmark/evaluation_protocol.md` — the 16 scoring criteria (4 families:
    BSC, MAR, TSQ, HDQ; each 1-5; family avg = mean of its 4 criteria;
    Total Avg = mean of all 16)
  - `results/main_results_30_topics.csv` — published per-method scores (Human,
    Codex, GPT Deep Research, Gemini Deep Research, Naive RAG) used only as
    *directional context* for our pilot.

NOT full DAS-Bench compliance (see the report's feasibility matrix): the pilot
scorer is our own LLM judge (default `opencode/big-pickle`), not the ≥300B
frozen judge; the DAS-2M candidate-paper metadata pool and gold source PDFs
live on Hugging Face (not fetched here); MAR's rendered-page scoring is
out of reach in this env; proxy topics are paper-anchored, not the vanilla
topic instances. Every number below is therefore labelled a *preview*.

Run (from repo root; mock = deterministic regression via the mock server):
  python -m tools.eval.bench_eval                      # real, opencode default
  python -m tools.eval.bench_eval --backend openai --base-url http://127.0.0.1:8199/v1 --model mock-api   # mock
Reports: `_eval_out/bench_pilot_das.md`, plus a console summary.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.llm.client import LLMClient, Message
from tools.pipeline.graph import Pipeline
from tools.pipeline.validate import parse_json_dict

DAS_BENCH_DIR = Path("external/DAS/DAS-Bench")
TOPICS_JSON = DAS_BENCH_DIR / "benchmark" / "topics.json"
RESULTS_CSV = DAS_BENCH_DIR / "results" / "main_results_30_topics.csv"
DEFAULT_OUT = Path("_eval_out") / "bench_pilot_das.md"

# 16 criteria, verbatim from benchmark/evaluation_protocol.md (as of 2026-09-16).
DAS_16: List[Tuple[str, str]] = [
    ("BSC", "Claim-Level Citation Support"),
    ("BSC", "Reference Faithfulness and Attribution Accuracy"),
    ("BSC", "Multi-Reference Synthesis Coverage and Quality"),
    ("BSC", "Citation Distribution Balance and Non-Redundancy"),
    ("MAR", "Citation and Reference Presentation Integrity"),
    ("MAR", "Figure/Table Quality and Textual Integration"),
    ("MAR", "Layout and Formatting Professionalism"),
    ("MAR", "Manuscript Component Completeness"),
    ("TSQ", "Research-Space Coverage"),
    ("TSQ", "Taxonomy Clarity and Boundary Control"),
    ("TSQ", "Survey Organization and Functional Coherence"),
    ("TSQ", "Synthesis Insight and Gap Analysis"),
    ("HDQ", "Multi-Level Goal Alignment"),
    ("HDQ", "Paragraph Argument Progression"),
    ("HDQ", "Atomic Claim Specificity and Technical Concreteness"),
    ("HDQ", "Local Synthesis and Non-Enumerative Writing"),
]

_RUBRIC_LINES = "\n".join(f"{f}: {c}" for f, c in DAS_16)

_BENCH_RUBRIC_PROMPT = (
    "You are a benchmark scorer for academic-survey generation. Score the "
    "artifact below on the DAS-Bench rubric (16 criteria, 1-5 integer each, "
    "5 = human-survey level). The artifact may be a single-paper grounded "
    "summary rather than a multi-paper survey; score strictly by what the "
    "artifact contains.\n"
    f"The 16 criteria:\n{_RUBRIC_LINES}\n"
    "Respond ONLY as JSON {\"scores\": {\"<criterion>\": int}} — one key per "
    "criterion, using the criterion names above exactly."
)

# Topics we evaluate: two paper-anchored *proxy* topics (evidence available in
# the local corpus) + two verbatim DAS-Bench topics (to probe the evidence gap).
SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "proxy",
        "topic_id": "P-A",
        "topic": "Proxy · AI-generated text detection (paper-anchored)",
        "question": "How reliable are automatic detection tools for AI-generated text?",
    },
    {
        "kind": "proxy",
        "topic_id": "P-B",
        "topic": "Proxy · Detection-tool bias against non-native writers (paper-anchored)",
        "question": "Are GPT detectors biased against non-native English writers?",
    },
    {
        "kind": "proxy",
        "topic_id": "P-C",
        "topic": "Proxy · Methods taxonomy: detect AIGC (statistical, watermark, human)",
        "question": "Which methods for detecting AI-generated text — statistical detection, watermarking, classifiers, human judgment — are documented, and what are their relative limitations?",
    },
    {
        "kind": "das",
        "topic_id": "001",
        "topic": "Tool Learning and Function Calling for LLM Agents",
        "question": "Tool Learning and Function Calling for LLM Agents",
    },
    {
        "kind": "das",
        "topic_id": "019",
        "topic": "Human-AI Collaboration in Scientific Writing and Research Workflows",
        "question": "Human-AI Collaboration in Scientific Writing and Research Workflows",
    },
]


def load_topics() -> List[Dict[str, str]]:
    """Return the 30 DAS-Bench topics from the local topics.json (for reference)."""
    if not TOPICS_JSON.is_file():
        return []
    with TOPICS_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def reference_means() -> Dict[str, Dict[str, float]]:
    """Published DAS-Bench main results (Total Avg + family avgs), directional."""
    if not RESULTS_CSV.is_file():
        return {}
    out: Dict[str, Dict[str, float]] = {}
    with RESULTS_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        method = " ".join((row.get("Category", "") or "").split()).strip()
        name = " ".join((row.get("Method", "") or "").split()).strip()
        key = name or method
        vals: Dict[str, float] = {}
        for col, short in (("BSC_Avg", "BSC"), ("MAR_Avg", "MAR"),
                           ("TSQ_Avg", "TSQ"), ("HDQ_Avg", "HDQ"),
                           ("Total_Avg", "Total")):
            try:
                vals[short] = float(row.get(col, "") or "nan")
            except ValueError:
                continue
        if vals:
            out[key] = vals
    return out


_MAX_ARTIFACT_CHARS = 40_000  # full manuscript (abstract+sections+table+refs) must be viewable


def score_survey(client: LLMClient, topic: str, artifact: str) -> Dict[str, Any]:
    """Ask an LLM judge to score `artifact` on the 16 DAS-Bench criteria.

    Returns {"scores": {criterion: int}, "coverage": n/16, "error": str?}.
    Never raises: parse/network failures degrade to a low-coverage dict.
    """
    r = client.chat(
        [
            Message(role="system", content=_BENCH_RUBRIC_PROMPT),
            Message(role="user",
                    content=f"Topic: {topic}\n\nArtifact:\n{artifact[:_MAX_ARTIFACT_CHARS]}"),
        ],
        json_mode=True,
        max_tokens=700,
    )
    obj = parse_json_dict(r.text)
    raw = obj.get("scores") if isinstance(obj, dict) else None
    if not isinstance(raw, dict):
        return {"scores": {}, "coverage": 0, "error": f"unparseable: {r.text[:120]!r}"}

    scores: Dict[str, int] = {}
    norm = {str(k).split(": ", 1)[-1].strip(): v for k, v in raw.items()}
    for family, criterion in DAS_16:
        v = norm.get(criterion)
        if v is None:  # tolerate "BSC: <criterion>" / "<criterion>" variants
            v = raw.get(f"{family}: {criterion}")
        try:
            scores[criterion] = int(v)
        except (TypeError, ValueError):
            continue
    return {
        "scores": scores,
        "coverage": len(scores),
        "judge_model": getattr(client, "model", "?"),
    }


def _family_avgs(scores: Dict[str, int]) -> Dict[str, Optional[float]]:
    avgs: Dict[str, Optional[float]] = {}
    for family in ("BSC", "MAR", "TSQ", "HDQ"):
        vals = [scores[c] for f, c in DAS_16 if f == family and c in scores]
        avgs[family] = statistics.mean(vals) if vals else None
    return avgs


def run_scenarios(client: LLMClient, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for s in scenarios:
        row: Dict[str, Any] = {"scenario": s}
        p = Pipeline(client)
        res = p.run(question=s["question"])
        row["candidates"] = res.get("candidates", [])
        row["elapsed"] = res.get("_elapsed", 0.0)
        row["paper_id"] = res.get("paper_id", "")
        row["papers"] = res.get("papers", [])
        row["n_cited"] = (res.get("validation") or {}).get("n_papers_cited", 0)
        row["l6"] = dict(res.get("validation") or {})
        artifact = res.get("output", "") or ""
        if artifact and "\n## Sources (" in artifact:
            artifact = artifact.split("\n## Sources (", 1)[0].rstrip()
        row["artifact_chars"] = len(artifact)
        if not artifact:
            row["status"] = "no-evidence"
        else:
            row["status"] = "scored"
            row["pdf"] = _render_manuscript(s, artifact)
            row["bench"] = score_survey(client, s["topic"], artifact)
        out.append(row)
    return out


def _render_manuscript(scenario: Dict[str, Any], artifact: str) -> Dict[str, Any]:
    """Best-effort render of the Markdown manuscript to PDF for MAR scoring.

    Returns {"pdf": str, "pages": int} (pages = 0 when rendering unavailable).
    """
    from pathlib import Path
    from tools.eval.render_manuscript import render_to_pdf

    md_dir = Path(DEFAULT_OUT).parent / "manuscripts"
    md_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{scenario.get('topic_id', 'manu')}_manuscript"
    md_path = md_dir / f"{stem}.md"
    pdf_path = md_dir / f"{stem}.pdf"
    try:
        md_path.write_text(artifact, encoding="utf-8")
    except OSError:
        return {"pdf": "", "pages": 0}
    pages = render_to_pdf(md_path, pdf_path, title=str(scenario.get("question", ""))[:80])
    return {"pdf": str(pdf_path), "pages": pages}


def format_report(rows: List[Dict[str, Any]], ref: Dict[str, Dict[str, float]]) -> str:
    L: List[str] = []
    add = L.append
    add("# DAS-Bench-style evaluation pilot — research_foodie preview")
    add("")
    add("> Updated: 2026-09-16 · scorer = this repo's LLM judge (default "
        "`opencode/big-pickle`), NOT DAS-Bench's frozen ≥300B judge")
    add(">")
    add("> Status: **preview / directional only**. Full DAS-Bench compliance is "
        "out of reach in this env (see feasibility matrix at the end).")
    add("")

    scored = [r for r in rows if r["status"] == "scored"]
    add(f"## Run summary")
    add("")
    add("| id | kind | paper | candidates | papers | cited | out chars | pdf pg | L6 | internal judge | DAS-16 cov. |")
    add("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        paper = r.get("paper_id") or "-"
        cands = ",".join(c.get("arxiv_id", "?") for c in r.get("candidates", [])) or "-"
        np = len(r.get("papers") or [])
        nc = r.get("n_cited", 0)
        pages = (r.get("pdf") or {}).get("pages", "-") if r.get("pdf") else "-"
        l6 = (_fmt(r["l6"].get("score")) if r.get("l6") else "-")
        j = (r["l6"].get("judge") or {}) if r.get("l6") else {}
        ji = f"{j.get('label','-')}@{_fmt(j.get('score'))}" if j else "-"
        cov = (f"{r['bench']['coverage']}/16" if r.get("bench") else "-")
        add(f"| {r['scenario']['topic_id']} | {r['scenario']['kind']} | {paper} | "
            f"{cands} | {np} | {nc} | {r.get('artifact_chars','-')} | {pages} | {l6} | {ji} | {cov} |")
    if not scored:
        add("\nAll scenarios produced **no evidence** (no parsed corpus match).")
    add("")

    for r in scored:
        s = r["scenario"]
        add(f"## {s['topic_id']} · {s['topic']}")
        add("")
        add(f"- paper_id: {r.get('paper_id')} · evidence chars: {r.get('artifact_chars')} · "
            f"elapsed: {r.get('elapsed', 0):.1f}s" + (" · **cached (vintage run)**" if r.get("cached") else ""))
        pdfi = r.get("pdf") or {}
        if pdfi.get("pdf"):
            add(f"- rendered manuscript (MAR): `{pdfi['pdf']}` · **{pdfi.get('pages', 0)} pages**")
        add(f"- L6 gate: score {_fmt(r['l6'].get('score'))} passed={r['l6'].get('passed')} · "
            f"internal P3 judge: {r['l6'].get('judge', {}).get('label')}@{_fmt(r['l6'].get('judge', {}).get('score'))}")
        b = r["bench"]
        for family in ("BSC", "MAR", "TSQ", "HDQ"):
            line = " · ".join(
                f"{c}: {b['scores'].get(c, '-')}" for f2, c in DAS_16 if f2 == family
            )
            add(f"- **{family}** — {line}  (avg {_fmt(_family_avgs(b['scores']).get(family))})")
        tot = [v for v in b["scores"].values()]
        total = statistics.mean(tot) if tot else None
        add(f"- **Total Avg**: {_fmt(total)}  (coverage {b['coverage']}/16, "
            f"judge={b.get('judge_model')})")
        if b.get("error"):
            add(f"- ⚠ judge error: {b['error']}")
        add("")

    if scored:
        add("## Family means across scored scenarios (preview)")
        add("")
        add("| method | BSC | MAR | TSQ | HDQ | Total |")
        add("|---|---|---|---|---|---|")
        # our pilot row
        fams: Dict[str, List[float]] = {f: [] for f in ("BSC", "MAR", "TSQ", "HDQ")}
        totals: List[float] = []
        for r in scored:
            fa = _family_avgs(r["bench"]["scores"])
            for f in fams:
                if fa.get(f) is not None:
                    fams[f].append(fa[f])
            tot = [v for v in r["bench"]["scores"].values()]
            if tot:
                totals.append(statistics.mean(tot))
        m = lambda xs: statistics.mean(xs) if xs else None  # noqa: E731
        add(f"| research_foodie (preview, n={len(scored)}) | {_fmt(m(fams['BSC']))} | "
            f"{_fmt(m(fams['MAR']))} | {_fmt(m(fams['TSQ']))} | {_fmt(m(fams['HDQ']))} | "
            f"{_fmt(m(totals))} |")
        for name, v in ref.items():
            if v.get("Total") is None:
                continue
            add(f"| {name} (published) | {_fmt(v.get('BSC'))} | {_fmt(v.get('MAR'))} | "
                f"{_fmt(v.get('TSQ'))} | {_fmt(v.get('HDQ'))} | {_fmt(v.get('Total'))} |")
        add("")
        add("> ⚠ Directional only: published rows used a multi-paper survey "
            "artifact, a ≥300B frozen judge, rendered pages (MAR) and DAS-2M "
            "pools; our preview artifacts are single-paper grounded summaries "
            "scored by the local judge. Not comparable head-to-head.")
        add("")

    add("## Feasibility matrix — is DAS-Bench usable in this env?")
    add("")
    add("| asset | status | notes |")
    add("|---|---|---|")
    add("| `benchmark/topics.json` (30 topics) | ✅ local | used verbatim (001, 019 probed) |")
    add("| `benchmark/evaluation_protocol.md` (16 criteria) | ✅ local | re-implemented here (frozen judge prompt is not public) |")
    add("| `results/main_results_30_topics.csv` | ✅ local | benchmark published scores (context only) |")
    add("| `evaluation/*.py` + `run_eval_all.sh` | ✅ local | full harness present (BSC/MAR/TSQ/HDQ) |")
    add("| DAS-2M candidate-paper metadata pool | ⛔ Hugging Face | not fetched (network); task pools are the benchmark input |")
    add("| gold source PDFs / reference surveys | ⛔ Hugging Face | not fetched |")
    add("| ≥300B-class frozen judge | ⛔ keys/GPU | config.json also supports a local OpenAI-compatible judge endpoint |")
    add("| MAR rendered-page scoring (dpi/binary) | ⛔ env | needs PDF page rendering + binary scoring |")
    add("| multi-paper evidence per topic | 🟡 2/30 | corpus has 2 parsed papers; DAS topics map to neither → no-evidence rows |")
    add("| `external/DAS/DAS-Bench` worktree | ✅ | read-only reference harness |")
    add("")
    add("## Full-compliance checklist (to actually *run* DAS-Bench)")
    add("")
    add("1. Fetch DAS-2M metadata + topic pools (Hugging Face) and the gold surveys/PDFs.")
    add("2. Build multi-paper evidence per topic (extend S_lit to fetch + parse top-k full texts).")
    add("3. Run the released `run_eval_all.sh` evaluators (needs PDF rendering for MAR).")
    add("4. Use a ≥300B judge (cloud key or a local OpenAI-compatible endpoint).")
    add("5. Report frozen-judge prompt, model id, temperature, aggregation — per protocol.")
    return "\n".join(L)


def _fmt(x: Optional[float], nd: int = 2) -> str:
    return "-" if x is None else f"{x:.{nd}f}"


def _serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-safe copy of a scenario row (for the sidecar cache)."""
    safe = dict(row)
    safe["scenario"] = dict(row["scenario"])
    safe["papers"] = [dict(p) for p in row.get("papers") or []]
    safe["candidates"] = [dict(c) for c in row.get("candidates") or []]
    safe["l6"] = dict(row.get("l6") or {})
    return safe


def _save_cache(rows: List[Dict[str, Any]], cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        (cache_dir / f"{r['scenario']['topic_id']}.json").write_text(
            json.dumps(_serialize_row(r), ensure_ascii=False), encoding="utf-8")


def _load_cache(ids: List[str], cache_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Load cached rows for `ids`; mark them so the report can flag vintage."""
    out: Dict[str, Dict[str, Any]] = {}
    for tid in ids:
        p = cache_dir / f"{tid}.json"
        if not p.is_file():
            continue
        try:
            row = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        row["cached"] = True
        out[tid] = row
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="DAS-Bench-style benchmark pilot")
    ap.add_argument("--backend", default="opencode")
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--scenarios", default=None,
                    help="comma-separated proxy|das topic ids to run (default: all)")
    args = ap.parse_args()

    client = LLMClient(backend=args.backend, base_url=args.base_url, model=args.model)
    scenarios = SCENARIOS
    run_ids: List[str] = [s["topic_id"] for s in SCENARIOS]
    if args.scenarios:
        run_ids = [x.strip() for x in args.scenarios.split(",")]
        scenarios = [s for s in SCENARIOS if s["topic_id"] in run_ids]

    print(f"[bench] backend={args.backend} running={run_ids}")

    cache_dir = Path(DEFAULT_OUT).parent / "bench_cache"
    rows = run_scenarios(client, scenarios)
    _save_cache(rows, cache_dir)

    # Merge cached rows for scenarios NOT re-run (keeps the report canonical
    # without re-paying the LLM cost; cached rows are flagged vintage).
    if len(run_ids) < len(SCENARIOS):
        cached = _load_cache([s["topic_id"] for s in SCENARIOS if s["topic_id"] not in run_ids], cache_dir)
        if cached:
            print(f"[bench] merged cached rows for {sorted(cached)} (vintage, read-only)")
        merged: List[Dict[str, Any]] = []
        by_id = {r["scenario"]["topic_id"]: r for r in rows}
        for s in SCENARIOS:
            if s["topic_id"] in by_id:
                merged.append(by_id[s["topic_id"]])
            elif s["topic_id"] in cached:
                merged.append(cached[s["topic_id"]])
        rows = merged

    ref = reference_means()
    report = format_report(rows, ref)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"[bench] wrote {out}")

    # console summary
    for r in rows:
        s = r["scenario"]
        if r["status"] == "no-evidence":
            print(f"  {s['topic_id']:>4} {s['kind']:>5}  NO-EVIDENCE "
                  f"cands={[c.get('arxiv_id') for c in r.get('candidates', [])]}")
        else:
            b = r["bench"]
            tot = statistics.mean(b["scores"].values()) if b["scores"] else None
            print(f"  {s['topic_id']:>4} {s['kind']:>5}  paper={r.get('paper_id')} "
                  f"total={_fmt(tot)} cov={b['coverage']}/16 "
                  f"judge={b.get('judge_model')} L6={_fmt(r['l6'].get('score'))} "
                  f"L6pass={r['l6'].get('passed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())