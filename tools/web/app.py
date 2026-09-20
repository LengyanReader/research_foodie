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

app = FastAPI(title="research_foodie — local observation dashboard", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")

# ---------------------------------------------------------------------------
# Templates (no external JS; inline CSS — zero network deps, K1/K2-safe)
# ---------------------------------------------------------------------------

HTML_HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>research_foodie · {title}</title><style>
body{{font-family:system-ui,'Segoe UI',sans-serif;max-width:1100px;margin:0 auto;padding:16px;color:#1c1c1c;background:#fff}}
h1{{font-size:20px}}h2{{font-size:16px;border-bottom:1px solid #ddd;padding-bottom:4px;margin-top:28px}}
nav a{{margin-right:12px;text-decoration:none;color:#0b5cad}}
table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border:1px solid #ddd;padding:4px 8px;text-align:left}}
code{{background:#f4f4f4;padding:1px 4px;font-size:12px}}pre{{background:#f7f7f7;padding:8px;overflow:auto;font-size:12px}}
.btn{{background:#0b5cad;color:#fff;border:0;padding:6px 12px;cursor:pointer;border-radius:4px}}
.btn.danger{{background:#b03030}}.run-card{{border:1px solid #ccc;border-radius:6px;padding:8px 12px;margin:8px 0}}
.green{{color:#1a7f37}}.red{{color:#b03030}}.amber{{color:#a96400}}.mono{{font-family:Consolas,monospace;font-size:12px}}
.muted{{color:#666;font-size:12px}}#tail{{background:#0d1117;color:#c9d1d9;padding:10px;border-radius:6px;
height:300px;overflow:auto;font-family:Consolas,monospace;font-size:12px;white-space:pre-wrap}}
.badge{{font-size:11px;padding:1px 6px;border-radius:10px}}.badge.ok{{background:#dafbe1;color:#1a7f37}}
.badge.run{{background:#ddf4ff;color:#0b5cad}}.badge.fail{{background:#ffebe9;color:#b03030}}.badge.cancel{{background:#fff1e5;color:#a96400}}
</style></head><body>
<nav><a href="/">▶ Runs</a> <a href="/dashboard">📊 Dashboard</a> <a href="/manuscripts">📄 Manuscripts</a> <a href="/feedback">🐞 Feedback</a></nav>
"""

HTML_TAIL = "</body></html>"

def page(title, body: str) -> HTMLResponse:
    return HTMLResponse(HTML_HEAD.format(title=title) + body + HTML_TAIL)

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
    if not MANUSCRIPTS.is_dir():
        return []
    return sorted(MANUSCRIPTS.glob("*.pdf"))


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
    ]


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
        f'<button class="btn" hx-none onclick="startRun(\'{m["id"]}\')">{m["title"]}</button><br>'
        if False else
        f'<button class="btn" onclick="startRun(\'{m["id"]}\')">{m["title"]}</button> '
        for m in menu
    )
    body = f"""
<h1>Runs</h1>
<p class="muted">Each button spawns the same <code>python -m …</code> command you would run from the terminal —
this page is only a trigger + live tail. Profile (D): judge lane model, if set, routes through the current env.
</p>
<div><strong>Model lane (Phase D):</strong> <code>{_env_profile()}</code></div>
<div style="margin:12px 0">{menu_html}</div>
<h2>Live tail (SSE)</h2>
<div id="tail">Run something to see progress here.</div>
<div style="margin-top:8px"><button class="btn danger" onclick="cancelRun()">Cancel current run</button>
<span id="active-msg" class="muted"></span></div>
<h2>Recent runs</h2>
<div id="runs">{cards}</div>
<script>
const menus = {json.dumps({m["id"]: m["args"] for m in menu})};
let currentRun = null, currentStart = 0, es = null;
async function startRun(id){{
  const args = menus[id];
  const resp = await fetch('/runs', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{title:id, args}})}});
  const data = await resp.json();
  currentRun = data.id; currentStart = 0;
  es && es.close();
  es = new EventSource(`/runs/${{data.id}}/events`);
  es.onmessage = (e) => {{
    const payload = JSON.parse(e.data);
    if (payload.type === 'line'){{ document.getElementById('tail').textContent += payload.data + '\\n';
      document.getElementById('tail').scrollTop = 1e9; }}
    else if (payload.type === 'status'){{
      document.getElementById('active-msg').textContent = `run ${{currentRun}} → ${{payload.status}} (rc=${{payload.rc}})`; }}
  }};
}}
async function cancelRun(){{
  if (!currentRun) return; await fetch(`/runs/${{currentRun}}`, {{method:'DELETE'}}); }}
setInterval(() => {{ if (currentRun){{
  fetch(`/runs/${{currentRun}}/status`).then(r=>r.json()).then(d=>{{
    document.getElementById('active-msg').textContent = `run ${{d.id}} ${{d.status}} elapsed=${{d.elapsed.toFixed(1)}}s rc=${{d.rc}} lines=${{d.lines}}`; }});
}}}}, 2500);
</script>
"""
    return page("Runs", body)


@app.post("/runs", response_class=JSONResponse)
def start_run(payload: dict):
    title = payload.get("title", "run")
    args = payload.get("args")
    if not isinstance(args, list) or not args:
        return JSONResponse({"error": "need 'args' list"}, status_code=400)
    run = manager.start(title, args, env_profile="env-default")
    return {"id": run.id, "status": run.status}


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
    return page("Dashboard", body)


@app.get("/manuscripts", response_class=HTMLResponse)
def manuscripts_page():
    items = _manuscript_list()
    rows = "".join(f'<tr><td>{p.name}</td><td>{p.stat().st_size:,} B</td>'
                   f'<td><a href="/manuscripts/{p.name}">open pdf</a></td></tr>' for p in items) \
        or "<tr><td colspan=3 class=muted>no rendered manuscripts yet (run a bench scenario first)</td></tr>"
    body = (f"<h1>Manuscripts</h1><table><tr><th>file</th><th>size</th><th></th></tr>{rows}</table>"
            f"<p class=muted>Rendered by <code>render_manuscript</code> (pandoc + xelatex + YaHei) during bench runs.</p>")
    return page("Manuscripts", body)


@app.get("/manuscripts/{name}")
def manuscript_file(name: str):
    path = MANUSCRIPTS / name
    if not path.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(path, media_type="application/pdf", filename=name)


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
    return page("Feedback", body)


@app.post("/feedback")
def feedback_append(row: str = Form(...)):
    fb = EVAL_OUT / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    with (fb / "feedback.jsonl").open("a", encoding="utf-8") as f:
        f.write(row + "\n")
    body = "<p>appended ✓ <a href='/feedback'>back</a> — note: feedback does not auto-tune anything; it feeds the E-5 corpus reviewed in the weekly cadence.</p>"
    return page("Feedback (appended)", body)