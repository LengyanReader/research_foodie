"""FastAPI app for the local observation dashboard (WS-B, Phase F).

Serves four pages over the CLI pipeline + `_eval_out/` artifacts:
  /            runs — trigger bench/QA/variance/pools/pipeline runs, live SSE tail, cancel
  /dashboard   overview — measured numbers, latest reports, manuscripts
  /manuscripts PDFs — rendered-article review (L6 human gate surface)
  /feedback    append JSONL feedback rows (E-5 ingestion; read-only page)

Design rules (PLAN Phase F, D-4/D-5):
  * binds 127.0.0.1 only; no auth (explicit scope boundary)
  * the server owns env (`LLM_BACKEND`/`OPENAI_*`); the browser never sees keys
  * every run records its profile name; reports keep `judge_model` provenance
  * read-only fallback: `/dashboard` and `/manuscripts` work even if uvicorn
    deps are pinned by anything else — they never touch the LLM
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .run_manager import manager, REPO_ROOT

WEB_DIR = Path(__file__).resolve().parent
EVAL_OUT = REPO_ROOT / "_eval_out"
MANUSCRIPTS = EVAL_OUT / "manuscripts"
MOCK_MANUSCRIPTS = EVAL_OUT / "mock_manuscripts"

app = FastAPI(title="research_foodie — local observation dashboard", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")

# ---------------------------------------------------------------------------
# Templates (no external JS; inline CSS — zero network deps, K1/K2-safe)
# ---------------------------------------------------------------------------

HTML_HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>research_foodie · {title}</title><style>
:root{{
  --paper:#f4f5ef; --card:#fcfcfa; --ink:#20211c; --ink-soft:#56584e; --ink-faint:#8b8d80;
  --rule:#d7d8cd; --rule-strong:#20211c; --mark:#b0432e; --pass:#2c6b4e; --warn:#96680f;
  --link:#35506b;
  --serif:Georgia,'Times New Roman',serif; --sans:system-ui,'Segoe UI','PingFang SC',sans-serif;
  --mono:Consolas,'Cascadia Mono',monospace;
}}
*{{box-sizing:border-box}}
html{{scrollbar-gutter:stable}}
body{{margin:0;padding:26px clamp(16px,5vw,56px) 80px;color:var(--ink);
  background:var(--paper);font:15px/1.65 var(--sans)}}
h1,h2,h3{{font-family:var(--serif);line-height:1.2;font-weight:600}}
h1{{font-size:clamp(25px,3.6vw,33px);margin:.1em 0 .25em}}
h2{{font-size:17px;margin:0;letter-spacing:.01em}}
h2 .en{{font-family:var(--sans);font-size:12.5px;color:var(--ink-faint);font-weight:400;margin-left:8px}}
a{{color:var(--link);text-decoration:none}}
a:hover{{text-decoration:underline;color:var(--ink)}}
code{{font-family:var(--mono);font-size:12px}}
pre{{font-family:var(--mono);font-size:12px;background:transparent;margin:0}}

/* nav */
.nav{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;
  padding-bottom:14px;border-bottom:1px solid var(--rule);margin-bottom:4px}}
.brand{{font-family:var(--serif);font-weight:700;font-size:16px;color:var(--ink)}}
.brand .zh{{font-family:var(--sans);font-weight:400;color:var(--ink-faint);font-size:12.5px;margin-left:8px}}
nav a{{margin-left:20px;color:var(--ink-soft);font-size:14px}}
nav a.cur{{color:var(--ink);border-bottom:1px solid var(--mark)}}

/* masthead */
.mast{{border-bottom:2px solid var(--ink);padding:14px 0 14px;margin-bottom:6px}}
.mast-meta{{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint)}}
.lede{{color:var(--ink-soft);max-width:66ch;font-family:var(--serif);font-size:15.5px;line-height:1.6;margin:.5em 0 0}}

/* sections */
.sect{{margin:30px 0 0}}
.sect-head{{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;
  border-bottom:1px solid var(--rule-strong);padding-bottom:5px;margin-bottom:16px}}
.sect-head .side{{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint)}}

/* probe form */
.probe{{background:var(--card);border:1px solid var(--rule);padding:18px 20px 16px}}
.probe label.fl{{display:block;font-size:13px;color:var(--ink-soft);margin-bottom:8px}}
.qfield{{width:100%;padding:10px 12px;font:14.5px var(--sans);color:var(--ink);
  border:1px solid var(--ink);border-radius:0;background:var(--paper)}}
.qfield:focus{{outline:2px solid var(--link);outline-offset:2px}}
.seg{{display:inline-flex;border:1px solid var(--ink);margin:0}}
.seg label{{display:flex;align-items:baseline;gap:8px;margin:0;padding:8px 14px;font-size:13px;
  color:var(--ink-soft);cursor:pointer;border-right:1px solid var(--rule)}}
.seg label:last-child{{border-right:0}}
.seg input{{position:absolute;opacity:0;pointer-events:none}}
.seg b{{font-weight:600;color:var(--ink)}}
.seg small{{display:block;font-size:11.5px;color:var(--ink-faint)}}
.seg label:has(input:checked){{background:var(--paper)}}
.probe-row{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:14px}}
.hint{{margin:12px 0 0;font-size:12.5px;color:var(--ink-faint)}}

/* buttons */
.btn{{font:13px var(--sans);color:var(--ink);background:transparent;border:1px solid var(--ink);
  padding:8px 18px;cursor:pointer;border-radius:0}}
.btn:hover{{background:var(--ink);color:var(--paper)}}
.btn:focus-visible{{outline:2px solid var(--link);outline-offset:2px}}
.btn.primary{{background:var(--ink);color:var(--paper)}}
.btn.primary:hover{{background:var(--mark);border-color:var(--mark)}}
.btn.danger{{border-color:var(--mark);color:var(--mark)}}
.btn.danger:hover{{background:var(--mark);color:var(--paper)}}
.btn.mini{{padding:4px 10px;font-size:12px;border-color:var(--rule);color:var(--ink-soft)}}
.btn.mini:hover{{border-color:var(--ink);color:var(--ink)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}

/* mission — the numbered stage sequence */
.mission{{display:flex;flex-direction:column}}
.progress{{height:3px;background:var(--rule);margin:2px 0 6px}}
.progress i{{display:block;height:3px;background:var(--pass);transition:width .4s ease}}
.stg{{display:grid;grid-template-columns:46px 1fr;padding:12px 0;border-bottom:1px solid var(--rule)}}
.stg:last-child{{border-bottom:0}}
.stg-no{{padding-top:3px;font-family:var(--serif);color:var(--ink-faint)}}
.stg-title{{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;font-family:var(--serif);font-weight:600;font-size:15.5px}}
.stg-title .zh{{font-family:var(--sans);font-weight:400;color:var(--ink-faint);font-size:12.5px}}
.stg-title .tick{{font-family:var(--mono);font-size:11.5px;color:var(--pass);margin-left:auto}}
.stg-what{{margin:4px 0 1px}}
.stg-why{{margin:0 0 5px;color:var(--ink-soft);font-family:var(--serif);font-size:14px}}
.stg-note{{font-family:var(--mono);font-size:12px;color:var(--ink)}}
.stg-tech{{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint);margin-top:2px}}
.stg.live .stg-no{{color:var(--mark);font-weight:700}}
.stg.live .stg-title{{border-left:3px solid var(--mark);padding-left:10px}}
.stg.live .stg-title .tick{{color:var(--mark)}}
.stg.off{{opacity:.55}}
.stg.done .stg-no{{color:var(--pass)}}

/* raw tail */
details.rawtail{{border:1px solid var(--rule);margin-top:6px}}
details.rawtail summary{{cursor:pointer;padding:8px 12px;font-size:12.5px;color:var(--ink-soft);list-style:none}}
details.rawtail summary:before{{content:'▸ ';color:var(--ink-faint)}}
details.rawtail[open] summary:before{{content:'▾ '}}
#tail{{margin:0;padding:10px 12px;height:230px;overflow:auto;border-top:1px solid var(--rule);
  font-family:var(--mono);font-size:12px;color:#c9d1d9;background:#191a10;white-space:pre-wrap}}

/* run archive */
.runs{{display:flex;flex-direction:column;gap:12px}}
.run-card{{background:var(--card);border:1px solid var(--rule);padding:12px 16px}}
.run-top{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
.run-top strong{{font-family:var(--serif);font-size:15.5px}}
.run-card .cmd{{margin-top:8px;font-size:11.5px;color:var(--ink-faint);word-break:break-all}}
.run-card .q{{margin-top:6px;font-family:var(--serif);font-style:italic;color:var(--ink-soft)}}
.run-card .res{{margin-top:4px;font-size:13px;color:var(--ink-soft)}}
.mono{{font-family:var(--mono)}}
.id{{color:var(--ink-faint);font-size:12px}}
.badge{{font-size:11px;padding:1px 8px;border:1px solid var(--rule-strong);white-space:nowrap}}
.badge.ok{{border-color:var(--pass);color:var(--pass)}}
.badge.fail{{border-color:var(--mark);color:var(--mark)}}
.badge.run{{border-color:var(--mark);color:var(--mark)}}
.badge.cancel{{border-color:var(--warn);color:var(--warn)}}
.badge.muted{{border-color:var(--rule);color:var(--ink-faint)}}

/* generic utilities & tables */
table{{border-collapse:collapse;width:100%;font-size:13px}}
td,th{{border:1px solid var(--rule);padding:6px 10px;text-align:left}}
th{{background:var(--card);font-weight:600}}
ul{{margin:.4em 0}}li{{margin:.15em 0}}
.muted{{color:var(--ink-faint)}}.green{{color:var(--pass)}}.red{{color:var(--mark)}}.amber{{color:var(--warn)}}
.mission-empty{{color:var(--ink-faint);font-family:var(--serif);font-style:italic;padding:10px 0}}

@media (max-width:700px){{
  .stg{{grid-template-columns:32px 1fr}}
  .stg-title .tick{{margin-left:0}}
  nav a{{margin-left:12px;font-size:13px}}
}}
@media (prefers-reduced-motion: reduce){{
  *{{transition:none!important;animation:none!important}}
}}
</style></head><body>
<nav class="nav"><span class="brand">Research Foodie<span class="zh">本地科研综述工作台</span></span>
<span><a class="{cur_workbench}" href="/">Workbench</a><a class="{cur_dash}" href="/dashboard">Numbers</a><a class="{cur_ms}" href="/manuscripts">Manuscripts</a><a class="{cur_fb}" href="/feedback">Feedback</a></span></nav>
"""

HTML_TAIL = "</body></html>"

def page(title, body: str, cur: str = "wb") -> HTMLResponse:
    kw = dict(
        cur_workbench="cur" if cur == "wb" else "",
        cur_dash="cur" if cur == "dash" else "",
        cur_ms="cur" if cur == "ms" else "",
        cur_fb="cur" if cur == "fb" else "",
    )
    return HTMLResponse(HTML_HEAD.format(title=title, **kw) + body + HTML_TAIL)

# ---------------------------------------------------------------------------
# Read-only data feeds (no LLM)
# ---------------------------------------------------------------------------

def _load_json(name: str):
    p = EVAL_OUT / name
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _variance_summary() -> List[dict]:
    data = _load_json("variance_runs.json") or []
    by_topic: dict = {}
    for r in data:
        by_topic.setdefault(r["topic_id"], []).append(r)
    out = []
    for tid, rows in sorted(by_topic.items()):
        totals = [r.get("total", 0) for r in rows]
        import statistics
        mean = statistics.mean(totals)
        sd = statistics.stdev(totals) if len(totals) > 1 else 0.0
        out.append({"topic_id": tid, "n": len(rows), "mean": mean, "sd": sd,
                    "last_total": rows[-1].get("total")})
    return out


def _pools_summary() -> dict:
    data = _load_json("pools_30.json") or {}
    full = sum(1 for v in data.values() if len(v.get("papers", [])) >= 3)
    partial = sum(1 for v in data.values() if 0 < len(v.get("papers", [])) < 3)
    empty = sum(1 for v in data.values() if not v.get("papers"))
    return {"total": len(data), "full": full, "partial": partial, "empty": empty}


def _manuscript_list() -> List[Path]:
    out = []
    for d in (MANUSCRIPTS, MOCK_MANUSCRIPTS):
        if d.is_dir():
            out.extend(sorted(d.glob("*.pdf")))
    return out


def _scenario_menu() -> List[dict]:
    """Pre-defined run buttons for the Runs page (mirrors bench_eval scenario sets)."""
    return [
        {"id": "proxies", "title": "Bench proxies (P-A, P-B, P-C)",
         "args": ["-m", "tools.eval.bench_eval", "--scenarios", "P-A,P-B,P-C"]},
        {"id": "das", "title": "DAS rows (001, 019 — expect no-evidence on free judge)",
         "args": ["-m", "tools.eval.bench_eval", "--scenarios", "001,019"]},
        {"id": "qa", "title": "Evidence-grounded QA subset (QA-6, QA-7, SQ-1, PQ-1)",
         "args": ["-m", "tools.eval.bench_eval", "--scenarios", "QA-6,QA-7,SQ-1,PQ-1"]},
        {"id": "variance", "title": "Judge variance (P-A,P-B,P-C × 1 round)",
         "args": ["-m", "tools.eval.variance_run", "--rounds", "1"]},
        {"id": "pools", "title": "30-topic pools battery (build, limit 3 — long, network)",
         "args": ["-m", "tools.eval.pools_30", "--step", "build", "--limit", "3"]},
        {"id": "pipe-mock", "title": "Pipeline smoke — mock (deterministic, ~0.1 s)",
         "args": ["-m", "tools.pipeline.test_pipeline", "mock"]},
        {"id": "pipe-real", "title": "Pipeline smoke — real opencode (2–4 min)",
         "args": ["-m", "tools.pipeline.test_pipeline", "real"]},
        {"id": "health", "title": "Health check (E-2, quick — green-light gate)",
         "args": ["-m", "tools.eval.health_check", "--quick"]},
    ]


# ---------------------------------------------------------------------------
# Research-workflow narration (application-domain view of the pipeline stages)
# ---------------------------------------------------------------------------
# Each stage is described in *business* language (what is happening to the
# research) + *technical* key points (how it is implemented), so the dashboard
# answers "what stage is the research at / how / why". The same metadata drives
# the live mission panel, the mission page, and the run-card summary.
SURVEY_STAGES: List[dict] = [
    {"id": "discover", "label": "Discover sources", "zh": "检索文献",
     "what": "Search for the papers that are worth reading for this question",
     "how": "Three discovery rails (seed / arXiv / orx) with the free arXiv API",
     "why": "A survey is only as good as the papers it considers",
     "key": "backend · candidates", "icon": "search"},
    {"id": "evidence", "label": "Build evidence pool", "zh": "解析证据",
     "what": "Turn selected PDFs into searchable, quotable text",
     "how": "MinerU windowed parse (≤6 pages) + resolved_evidence() pool",
     "why": "Only retrievable full text can back verbatim grounding later",
     "key": "pool_size papers", "icon": "archive"},
    {"id": "synthesize", "label": "Synthesise literature", "zh": "文献综合",
     "what": "Distil each paper into the claims and facts it can actually support",
     "how": "S_lit node — per-paper extraction, tagged with its paper_id",
     "why": "Drafting builds on verified content instead of memory",
     "key": "model lane · paper_id tags", "icon": "book"},
    {"id": "outline", "label": "Plan the article", "zh": "制定大纲",
     "what": "Break the question into a section structure and argument flow",
     "how": "S_org node — STORM-style multi-perspective outline on LangGraph",
     "why": "Outline decides coverage before a single sentence is written",
     "key": "reader perspectives · sections", "icon": "list"},
    {"id": "write", "label": "Write grounded sections", "zh": "接地写作",
     "what": "Write each section so every claim is bound to its verbatim source",
     "how": "S_write + review — BM25 source windows + 5-gram verbatim filter",
     "why": "Kills hallucination at write time; un-grounded claims are dropped",
     "key": "claims · BM25 windows · 5-gram", "icon": "pencil"},
    {"id": "finalize", "label": "Assemble manuscript", "zh": "装配成稿",
     "what": "Merge abstract, evidence table, references, and audit annex",
     "how": "_finalize node — deterministic assembly of the artifact",
     "why": "Produces a single reviewable deliverable with provenance",
     "key": "chars · evidence table · annex", "icon": "layers"},
    {"id": "gate", "label": "Deterministic gate", "zh": "机械门禁",
     "what": "Zero-LLM quality checks: structure, citation form, grounding, bilingual",
     "how": "validate.py L6 — deterministic rules, no model call",
     "why": "A hard floor that never relies on the model's self-report",
     "key": "L6 · 5-gram overlap · arXiv/DOI form", "icon": "shield"},
    {"id": "judge", "label": "Academic judgement", "zh": "AI 判题",
     "what": "Score the manuscript against a scholarly rubric",
     "how": "P3 judge — DAS-Bench 16-axis rubric (BSC·MAR·TSQ·HDQ)",
     "why": "Aligns with an external evaluation protocol, not just internal rules",
     "key": "label · checks", "icon": "scale"},
    {"id": "deliver", "label": "Render deliverables", "zh": "渲染交付",
     "what": "Render the manuscript to PDF for human review",
     "how": "render_manuscript — pandoc + xelatex + YaHei",
     "why": "Human L6 review happens on a rendered artifact",
     "key": "pages · pdf link", "icon": "doc"},
]
_STAGE_ORDER = {s["id"]: i for i, s in enumerate(SURVEY_STAGES)}


def _parse_survey_stages(lines: List[str]) -> List[dict]:
    """Reconstruct a stage plan from `[survey-stage]` JSON lines of a raw run log."""
    plan: dict = {}
    for ln in lines:
        if not ln.startswith("[survey-stage] "):
            continue
        try:
            ev = json.loads(ln[len("[survey-stage] "):].strip())
        except Exception:
            continue
        sid, status = ev.get("id"), ev.get("status")
        if sid not in _STAGE_ORDER:
            continue
        row = plan.setdefault(sid, {"id": sid, "status": "pending",
                                    "dur_s": 0.0, "tech": {}})
        if status == "start":
            row["status"] = "running"
        elif status == "done":
            row["status"] = "done"
            row["dur_s"] = max(row["dur_s"], float(ev.get("dur_s", 0)))
            row["tech"] = ev.get("tech") or row.get("tech") or {}
    ordered = [plan[s["id"]] for s in SURVEY_STAGES if s["id"] in plan]
    return ordered


def _mission_html(stages: List[dict], summary: Optional[dict]) -> str:
    """Render the research-workflow narration block (business + tech)."""
    if not stages:
        return '<p class="muted">No survey mission info recorded for this run.</p>'
    done = sum(1 for s in stages if s["status"] == "done")
    pct = int(100 * done / len(stages)) if stages else 0
    rows = []
    for i, s in enumerate(stages, 1):
        meta = next(m for m in SURVEY_STAGES if m["id"] == s["id"])
        status = s["status"] if s["status"] in ("done", "running", "pending") else "pending"
        mark = {"done": "✓", "running": "●", "pending": "○"}[status]
        dur = f" · {s['dur_s']:.1f}s" if s.get("dur_s") else ""
        tick = {"done": f"done{dur}", "running": "running", "pending": "pending"}[status]
        tech = " · ".join(f"{k}={v}" for k, v in (s.get("tech") or {}).items())
        note = ('<div class="stg-note">how · ' + meta["how"] + '</div>'
                + (f'<div class="stg-tech">{tech}</div>' if tech else ""))
        rows.append(
            f'<article class="stg {status}">'
            f'<div class="stg-no">{i:02d}</div><div>'
            f'<div class="stg-title">{meta["label"]}<span class="zh">{meta["zh"]}</span>'
            f'<span class="tick">{mark} {tick}</span></div>'
            f'<p class="stg-what">{meta["what"]}</p>'
            f'<p class="stg-why">{meta["why"]}</p>'
            f'{note}'
            f'</div></article>')
    summary_html = ""
    if summary:
        links = " ".join(
            f'<a href="/manuscripts/{Path(x).name}">{label}</a>'
            for label, x in (("manuscript", summary.get("manuscript")),
                             ("pdf 干货稿", summary.get("pdf")),
                             ("preprint 出版化稿", summary.get("pdf_pub")))
            if x)
        verdict = "pass" if summary.get("gate_passed") else "fail"
        summary_html = (f'<div class="run-card">'
                        f'<span class="badge {"ok" if summary.get("gate_passed") else "fail"}">'
                        f'L6 {verdict}</span> '
                        f'<span class="res">judge={summary.get("judge_label")} · '
                        f'{summary.get("claims", 0)} claims · '
                        f'{summary.get("n_papers_cited", 0)} papers · '
                        f'{summary.get("elapsed_s", 0)}s</span> '
                        f'{links}</div>')
    return (f'<div class="progress"><i style="width:{pct}%"></i></div>'
            f'<div class="muted" style="font-size:12px">{done}/{len(stages)} '
            f'research stages · {pct}%</div>'
            + summary_html + "".join(rows))


def _survey_summary(run) -> Optional[dict]:
    """Parse the `[survey-result]` JSON line written by run_survey, if any."""
    for ln in reversed(run.lines):
        if ln.startswith("[survey-result] "):
            try:
                return json.loads(ln[len("[survey-result] "):].strip())
            except Exception:
                return None
    return None


def _run_card(run) -> str:
    """HTML card for one run (list page)."""
    from tools.eval.run_ledger import ResumeLedger
    status_badge = {
        "done": 'ok', "running": 'run', "pending": 'run',
        "failed": 'fail', "cancelled": 'cancel', "interrupted": 'cancel',
    }.get(run.status, 'muted')
    logf = f'<a class="muted" href="/runs/{run.id}/log" target="_blank">log</a>'
    greeting = ''
    survey = _survey_summary(run)
    mission_link = ''
    if survey or any(ln.startswith("[survey-stage]") for ln in run.lines):
        mission_link = (f'<a class="muted" href="/runs/{run.id}/mission" target="_blank">'
                        f'research view</a> ')
    if survey:
        mode = survey.get("mode", "real")
        badge_cls = "ok" if survey.get("gate_passed") else "fail"
        mode_badge = (f'<span class="badge {"muted" if mode == "mock" else "run"}">'
                      f'{"MOCK demo" if mode == "mock" else "REAL run"}</span>')
        links = []
        if survey.get("manuscript"):
            links.append(f'<a href="/manuscripts/{Path(survey["manuscript"]).name}">manuscript</a>')
        if survey.get("pdf"):
            links.append(f'<a href="/manuscripts/{Path(survey["pdf"]).name}">pdf 干货稿</a>')
        if survey.get("pdf_pub"):
            links.append(f'<a href="/manuscripts/{Path(survey["pdf_pub"]).name}">preprint 出版化稿</a>')
        links_html = " · ".join(links) if links else ""
        greeting = (f'<div class="q">{survey.get("question", "")}</div>'
                    f'<div class="res">{mode_badge} '
                    f'L6 gate <span class="badge {badge_cls}">{"pass" if survey.get("gate_passed") else "fail"}</span> '
                    f'judge={survey.get("judge_label")} · {survey.get("claims", 0)} claims · '
                    f'{survey.get("n_papers_cited", 0)} papers cited · {survey.get("elapsed_s", 0)}s'
                    + (f' · {links_html}' if links_html else "") + '</div>')
    # ledger progress for bench_eval / variance_run (they persist per-row state)
    progress = ""
    for mod, argv in (("tools.eval.bench_eval", r"bench_eval"),
                      ("tools.eval.variance_run", r"variance_run")):
        search = f"-m {mod}"
        if any(search in str(c) for c in run.cmd):
            led = ResumeLedger._load(argv)
            if led:
                nd = len(led.get("done", {}))
                progress = (f'<span class="muted">· ledger </span>'
                            f'<span class="badge run">{nd} done</span>')
            break
    resume = ""
    if run.status in ("failed", "cancelled", "interrupted"):
        resume = (f'<button class="btn" onclick="resumeRun(\'{run.id}\')">'
                  f'Resume</button> ')
    return (f'<div class="run-card"><div class="run-top">'
            f'<strong>{run.title}</strong> '
            f'<span class="badge {status_badge}">{run.status}</span> '
            f'<span class="id mono">{run.id}</span> {logf} {mission_link}{progress}</div>'
            f'<div class="mono muted" style="font-size:12px">{run.elapsed:.0f}s · '
            f'rc={run.returncode} · {len(run.lines)} lines</div>'
            f'{greeting}'
            f'{resume}'
            f'<div class="cmd">{" ".join(run.cmd)}</div></div>')


def _env_profile() -> dict:
    import os
    return {
        "LLM_BACKEND": os.getenv("LLM_BACKEND", "opencode"),
        "OPENCODE_MODEL": os.getenv("OPENCODE_MODEL", "opencode/big-pickle"),
        "OPENAI_BASE_URL": (os.getenv("OPENAI_BASE_URL") or "— (not set)"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL") or "— (not set)",
        "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "not set",
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def runs_page(request: Request) -> HTMLResponse:
    menu = _scenario_menu()
    rows = manager.list()
    cards = "".join(_run_card(r) for r in rows[:12]) or '<p class="muted">No runs yet this session.</p>'
    menu_html = "".join(
        f'<button class="btn" onclick="startRun(\'{m["id"]}\')">{m["title"]}</button> '
        for m in menu
    )
    # snapshot the most recent survey run so the mission panel survives refresh
    last_survey = None
    for r in rows:
        if any(ln.startswith("[survey-stage]") for ln in r.lines):
            last_survey = r
            break
    mission_init = ""
    if last_survey:
        mission_init = _mission_html(_parse_survey_stages(last_survey.lines),
                                     _survey_summary(last_survey))
    body = f"""
<header class="mast">
  <div class="mast-meta">research_foodie · local-first survey pipeline · citations are the lifeline</div>
  <h1>Survey workbench</h1>
  <p class="lede">输入一个问题，得到一份逐句可溯源的综述。每一步研究都在这里直播——
  做到哪个阶段、怎么做、为什么这么做。结果一律双档交付：干货稿 + arXiv preprint 稿。</p>
</header>

<section class="sect">
  <div class="sect-head"><h2>投题 <span class="en">start a survey</span></h2>
    <div class="side">模型通道 · {_env_profile()['LLM_BACKEND']} / {_env_profile()['OPENCODE_MODEL']}</div></div>
  <div class="probe">
    <form onsubmit="return false">
      <label class="fl" for="q">研究问题 Research question <span class="muted">——这份综述要回答的问题</span></label>
      <input id="q" class="qfield" type="text" autocomplete="off"
             placeholder="e.g. GPT detectors bias against non-native English writers"
             list="q-examples">
      <datalist id="q-examples">
        <option value="GPT detectors bias against non-native English writers">
        <option value="RAG evaluation needs human judgement">
      </datalist>
      <div class="probe-row">
        <div class="seg">
          <label><input type="radio" name="mode" value="mock" checked>
            <span><b>Mock demo</b><small>离线确定性 · ~1 s · 可复现 · 非真实结果</small></span></label>
          <label><input type="radio" name="mode" value="real">
            <span><b>Real run</b><small>免费模型通道 · ~5–8 min · 有涨落</small></span></label>
        </div>
        <button class="btn primary" onclick="startQuestion()">Run survey</button>
        <span class="muted" id="q-msg"></span>
      </div>
      <p class="hint">取消中断的 run 可在卡片上 <b>Resume</b>——CLI 驱动保留断点台账，重启后从已完成的最后一行继续排队。</p>
    </form>
  </div>
  <div style="margin-top:12px" class="chips">{menu_html}</div>
</section>

<section class="sect">
  <div class="sect-head"><h2>研究进行时 <span class="en">live mission · what / how / why</span></h2>
    <div class="side"><button class="btn danger mini" onclick="cancelRun()">Cancel run</button>
    <span id="active-msg" class="muted"></span></div></div>
  <div id="mission">{mission_init or '<p class="mission-empty">还没有研究在跑。投一个题，进度会在这里按研究术语逐阶段讲述。</p>'}</div>
  <details class="rawtail"><summary>技术日志 raw log（工程细节，叙事层之下）</summary>
  <div id="tail">Run something to see progress here.</div></details>
</section>

<section class="sect">
  <div class="sect-head"><h2>历次运行 <span class="en">runs · ↘ 断点续跑</span></h2></div>
  <div id="runs" class="runs">{cards}</div>
</section>
<script>
const menus = {json.dumps({m["id"]: m["args"] for m in menu})};
let currentRun = null, currentStart = 0, es = null;
const stagesMeta = {json.dumps({s["id"]: {"label": s["label"], "zh": s["zh"],
  "why": s["why"], "how": s["how"], "what": s["what"], "key": s["key"]} for s in SURVEY_STAGES})};
const stagePlan = {{}};   // id -> {{status, dur_s, tech}}
function renderMission(){{
  const el = document.getElementById('mission');
  const ids = Object.keys(stagesMeta);
  const doneN = ids.filter(i => stagePlan[i] && stagePlan[i].status === 'done').length;
  const pct = Math.round(100 * doneN / ids.length);
  let rows = '';
  ids.forEach((id, k) => {{
    const m = stagesMeta[id]; const p = stagePlan[id] || {{status:'pending', tech:{{}}}};
    const st = ['done','running','pending'].includes(p.status) ? p.status : 'pending';
    const col = {{done: '#2c6b4e', running: '#b0432e', pending: '#8b8d80'}}[st];
    const mark = {{done:'✓', running:'●', pending:'○'}}[st];
    const doneNote = (st==='done' && p.dur_s) ? ` · ${{p.dur_s.toFixed(1)}}s` : '';
    const tech = Object.entries(p.tech||{{}}).map(([a,b])=>a+'='+b).join(' · ');
    const no = String(k+1).padStart(2, '0');
    rows += `<article class="stg ${{st}} ${{st==='done' ? 'done' : (st==='running' ? 'live' : 'off')}}">
      <div class="stg-no">${{no}}</div><div>
      <div class="stg-title">${{m.label}}<span class="zh">${{m.zh}}</span>
        <span class="tick">${{mark}} ${{st}}${{doneNote}}</span></div>
      <p class="stg-what">${{m.what}}</p>
      <p class="stg-why">${{m.why}}</p>
      <div class="stg-note">how · ${{m.how}}</div>${{tech ? '<div class="stg-tech">'+tech+'</div>' : ''}}
      </div></article>`;
  }});
  el.innerHTML = `<div class="progress"><i style="width:${{pct}}%"></i></div>
    <div class="muted" style="font-size:12px">${{doneN}}/${{ids.length}} research stages · ${{pct}}%
      ${{currentRun ? ' · 完整 what/how/why 见 <a href="/runs/'+currentRun+'/mission">research view</a>' : ''}}</div>`
    + rows;
}}
function handleLine(line){{
  const st = line.match(/^\\[survey-stage\\] (.*)$/);
  if (st){{
    try {{
      const ev = JSON.parse(st[1]);
      const p = stagePlan[ev.id] = stagePlan[ev.id] || {{status:'pending', dur_s:0, tech:{{}}}};
      if (ev.status === 'start'){{ p.status = 'running'; }}
      else if (ev.status === 'done'){{
        p.status = 'done'; p.dur_s = Math.max(p.dur_s||0, ev.dur_s||0);
        for (const k in (ev.tech||{{}})) p.tech[k] = ev.tech[k];
      }}
      renderMission();
    }} catch(_){{}}
    return true;
  }}
  return false;
}}
function attachSSE(id){{
  currentRun = id; currentStart = 0;
  es && es.close();
  es = new EventSource(`/runs/${{id}}/events`);
  es.onmessage = (e) => {{
    const payload = JSON.parse(e.data);
    if (payload.type === 'line'){{
      if (!handleLine(payload.data)){{
        document.getElementById('tail').textContent += payload.data + '\\n';
        document.getElementById('tail').scrollTop = 1e9;
      }}
    }}
    else if (payload.type === 'status'){{
      document.getElementById('active-msg').textContent = `run ${{currentRun}} → ${{payload.status}} (rc=${{payload.rc}})`;
      location.reload(); }}
  }};
}}
async function startRun(id){{
  const args = menus[id];
  const resp = await fetch('/runs', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{title:id, args}})}});
  const data = await resp.json();
  if (data.error){{ alert(data.error); return; }}
  attachSSE(data.id);
}}
async function startQuestion(){{
  const question = document.getElementById('q').value.trim();
  const mode = document.querySelector('input[name="mode"]:checked').value;
  let msg = document.getElementById('q-msg');
  if (!question){{ msg.textContent = 'type a research question first'; return; }}
  const args = ['-m', 'tools.pipeline.run_survey', '--question', question];
  if (mode === 'mock') args.push('--mock');
  msg.textContent = (mode === 'mock' ? 'mock demo' : 'real run') + ' started — tail below…';
  const resp = await fetch('/runs', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{title: 'survey (' + mode + ')', args}})}});
  const data = await resp.json();
  if (data.error){{ msg.textContent = data.error; return; }}
  attachSSE(data.id);
}}
async function resumeRun(id){{
  const resp = await fetch(`/runs/${{id}}/resume`, {{method:'POST'}});
  const data = await resp.json();
  if (data.error){{ alert(data.error); return; }}
  attachSSE(data.id);
}}
async function cancelRun(){{
  if (!currentRun) return; await fetch(`/runs/${{currentRun}}`, {{method:'DELETE'}}); }}
setInterval(() => {{ if (currentRun){{
  fetch(`/runs/${{currentRun}}/status`).then(r=>r.json()).then(d=>{{
    document.getElementById('active-msg').textContent = `run ${{d.id}} ${{d.status}} elapsed=${{d.elapsed.toFixed(1)}}s rc=${{d.rc}} lines=${{d.lines}}`; }});
}}}}, 2500);
</script>
"""
    return page("Runs", body, cur="cur")


@app.post("/runs", response_class=JSONResponse)
def start_run(payload: dict):
    title = payload.get("title", "run")
    args = payload.get("args")
    if not isinstance(args, list) or not args:
        return JSONResponse({"error": "need 'args' list"}, status_code=400)
    run = manager.start(title, args, env_profile="env-default")
    return {"id": run.id, "status": run.status}


@app.post("/runs/{run_id}/resume", response_class=JSONResponse)
def resume_run(run_id: str):
    """Re-issue an interrupted/cancelled run. CLI drivers with a per-row ledger
    (bench_eval, variance_run) continue from the last completed row."""
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    if run.status not in ("failed", "cancelled", "interrupted"):
        return JSONResponse({"error": f"run is {run.status} — nothing to resume"},
                            status_code=400)
    if not run.cmd or len(run.cmd) < 3:
        return JSONResponse({"error": "run has no CLI command to replay"},
                            status_code=400)
    new = manager.resume(run)
    return {"id": new.id, "status": new.status, "original": run_id}


@app.get("/runs/{run_id}/log", response_class=HTMLResponse)
def run_log(run_id: str):
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    text = ""
    if run.log_path.is_file():
        text = run.log_path.read_text(encoding="utf-8", errors="replace")[-60000:]
    return page(f"log {run_id}",
                f"<h1>log · {run_id} · <span class=badge>{run.status}</span></h1>"
                f"<pre>{text}</pre>")


@app.get("/runs/{run_id}/mission", response_class=HTMLResponse)
def run_mission(run_id: str):
    """Read-only 'research view' of a survey run: what stage, how, why —
    business language with the key technical points, plus the result links.
    This is the application-scenario answer to 'what is the tool doing'."""
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    stages = _parse_survey_stages(run.lines)
    summary = _survey_summary(run)
    if not stages and not summary:
        return page(f"mission {run_id}",
                    f"<h1>Research view · {run_id}</h1>"
                    f'<p class="muted">This run is not a survey pipeline run, so it has no '
                    f'research-workflow narration. See <a href="/runs/{run_id}/log">the log</a> '
                    f'or <a href="/">the runs page</a>.</p>')
    q = (summary or {}).get("question", "")
    head = f"<h1>Research view · {run_id}</h1>"
    if q:
        head += f'<p><strong>Question:</strong> <em>{q}</em></p>'
    head += (f'<p class="muted">How a survey answer is produced — one stage at a time. '
             f'Business framing ({SURVEY_STAGES[0]["zh"]}…) + the key technical point of each stage.</p>')
    return page(f"mission {run_id}", head + _mission_html(stages, summary))


@app.get("/runs/{run_id}/status", response_class=JSONResponse)
def run_status(run_id: str):
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    return {"id": run.id, "status": run.status, "rc": run.returncode,
            "elapsed": run.elapsed, "lines": len(run.lines)}


@app.get("/runs/{run_id}/events")
def run_events(run_id: str):
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)

    def gen():
        start = 0
        while True:
            chunk, start, done = run.tail_from(start)
            for line in chunk:
                yield f"data: {json.dumps({'type': 'line', 'data': line})}\n\n"
            if done and not chunk:
                yield f"data: {json.dumps({'type': 'status', 'status': run.status, 'rc': run.returncode})}\n\n"
                break
            yield ": keep-alive\n\n"
            time.sleep(0.5)

    return StreamingResponse(gen(), media_type="text/event-stream")


@app.delete("/runs/{run_id}")
def cancel_run(run_id: str):
    res = manager.cancel(run_id)
    return {"id": run_id, "cancel": res}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    var = _variance_summary()
    pools = _pools_summary()
    bench_report = EVAL_OUT / "bench_pilot_das.md"
    report_text = bench_report.read_text(encoding="utf-8") if bench_report.is_file() else "no report yet"

    var_rows = "".join(
        f'<tr><td>{t["topic_id"]}</td><td>{t["n"]}</td><td>{t["mean"]:.2f}</td>'
        f'<td>{t["sd"]:.2f}</td></tr>' for t in var) or "<tr><td colspan=4 class=muted>no variance data</td></tr>"
    pools_row = (f'<tr><td>{pools["total"]}</td><td>{pools["full"]}</td>'
                 f'<td>{pools["partial"]}</td><td>{pools["empty"]}</td></tr>')
    m_args = ",".join(f'"{p.name}"' for p in _manuscript_list())
    body = f"""
<h1>Dashboard</h1>
<h2>Judge variance (Session 19 baseline)</h2>
<table><tr><th>topic</th><th>rounds</th><th>mean total</th><th>sd</th></tr>{var_rows}</table>
<h2>30-topic evidence pools</h2>
<table><tr><th>total</th><th>full (≥3 papers)</th><th>partial</th><th>empty</th></tr>{pools_row}</table>
<h2>Manuscripts (L6 human review surface)</h2>
<div>{", ".join(f'<a href="/manuscripts/{p.name}">{p.name}</a>' for p in _manuscript_list()) or "none"}</div>
<h2>Bench report (raw markdown, `bench_pilot_das.md`)</h2>
<pre>{report_text[:4000]}</pre>
"""
    return page("Dashboard", body, cur="dash")


@app.get("/manuscripts", response_class=HTMLResponse)
def manuscripts_page():
    items = _manuscript_list()
    rows = "".join(f'<tr><td>{p.name}</td><td>{p.stat().st_size:,} B</td>'
                   f'<td><a href="/manuscripts/{p.name}">open pdf</a></td></tr>' for p in items) \
        or "<tr><td colspan=3 class=muted>no rendered manuscripts yet (run a bench scenario first)</td></tr>"
    body = (f"<h1>Manuscripts</h1><table><tr><th>file</th><th>size</th><th></th></tr>{rows}</table>"
            f"<p class=muted>Rendered by <code>render_manuscript</code> (pandoc + xelatex + YaHei) during bench runs.</p>")
    return page("Manuscripts", body, cur="ms")


@app.get("/manuscripts/{name}")
def manuscript_file(name: str):
    for d in (MANUSCRIPTS, MOCK_MANUSCRIPTS):
        path = d / name
        if path.is_file():
            media = "application/pdf" if path.suffix.lower() == ".pdf" else "text/markdown"
            return FileResponse(path, media_type=media, filename=name)
    return JSONResponse({"error": "not found"}, status_code=404)


@app.get("/feedback", response_class=HTMLResponse)
def feedback_page():
    fb = EVAL_OUT / "feedback"
    rows_html = ""
    if fb.is_dir():
        lines = []
        for f in sorted(fb.glob("*.jsonl")):
            for ln in f.read_text(encoding="utf-8").splitlines():
                if ln.strip():
                    lines.append(ln)
        rows_html = "".join(f"<tr><td class=mono>{ln[:200]}</td></tr>" for ln in lines[-50:])
    body = f"""
<h1>Feedback → JSONL (self-evolution E-5 ingestion)</h1>
<form method="post"><textarea name="row" rows="4" style="width:100%"
placeholder='{{"feed": "judge too lenient on BSC", "topic": "P-A", "date": "2026-09-20"}}'></textarea>
<button class="btn" type="submit">append row</button></form>
<h2>Last 50 rows</h2><table>{rows_html or '<tr><td class=muted>no feedback rows yet</td></tr>'}</table>
"""
    return page("Feedback", body, cur="fb")


@app.post("/feedback")
def feedback_append(row: str = Form(...)):
    fb = EVAL_OUT / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    with (fb / "feedback.jsonl").open("a", encoding="utf-8") as f:
        f.write(row + "\n")
    body = "<p>appended ✓ <a href='/feedback'>back</a> — note: feedback does not auto-tune anything; it feeds the E-5 corpus reviewed in the weekly cadence.</p>"
    return page("Feedback (appended)", body, cur="fb")