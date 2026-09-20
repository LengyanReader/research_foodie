"""F-3 passive static export — read-only snapshot of ``_eval_out/`` as a
self-contained static site deployable to GitHub Pages.

GitHub Pages is a **static host only** (no server-side execution: Python/Node/PHP
runtimes are not supported). The live FastAPI dashboard (WS-B, SSE/cancel) stays
local on 127.0.0.1; this module generates the deployable mirror:

    <out>/index.html        entry + scope notes
    <out>/dashboard.html    variance mean±sd · pools coverage · bench report head
    <out>/manuscripts.html  list + PDF copies from _eval_out/manuscripts/
    <out/.nojekyll          bypass Jekyll processing on GH Pages

Stdlib only (``html``/``json``/``statistics``) — works even where fastapi/uvicorn
are missing, which is exactly the F-3 degrade-gracefully posture.

Usage:
    $PY -X utf8 -m tools.web.export_static --out gh-pages
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parents[1]
EVAL_OUT = REPO_ROOT / "_eval_out"


_CSS = """
body{font-family:system-ui,'Segoe UI',sans-serif;max-width:1100px;margin:0 auto;padding:16px;color:#1c1c1c;background:#fff}
h1{font-size:20px}h2{font-size:16px;border-bottom:1px solid #ddd;padding-bottom:4px;margin-top:28px}
nav a{margin-right:12px;text-decoration:none;color:#0b5cad}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #ddd;padding:4px 8px;text-align:left}
code{background:#f4f4f4;padding:1px 4px;font-size:12px}pre{background:#f7f7f7;padding:8px;overflow:auto;font-size:12px}
.muted{color:#666;font-size:12px}.mono{font-family:Consolas,monospace;font-size:12px}
"""


def _page(title: str, body: str) -> str:
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>research_foodie · {html.escape(title)}</title>"
        f"<style>{_CSS}</style></head><body>"
        '<nav><a href="index.html">▶ Overview</a> '
        '<a href="dashboard.html">📊 Dashboard</a> '
        '<a href="manuscripts.html">📄 Manuscripts</a> · '
        '<span class="muted">static read-only mirror (F-3)</span></nav>'
        f"{body}</body></html>"
    )


def _table(header, rows, empty="<td class=muted>none</td>") -> str:
    thr = "".join(f"<th>{html.escape(h)}</th>" for h in header)
    body = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in r)}</tr>" for r in rows) or empty
    return f"<table><tr>{thr}</tr>{body}</table>"


def read_json(name: str):
    p = EVAL_OUT / name
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def variance_rows() -> list:
    data = read_json("variance_runs.json") or []
    by: dict = {}
    for r in data:
        by.setdefault(r["topic_id"], []).append(r)
    rows = []
    for tid, rs in sorted(by.items()):
        tots = [r.get("total") for r in rs if r.get("total") is not None]
        if not tots:
            continue
        m = statistics.mean(tots)
        sd = statistics.stdev(tots) if len(tots) > 1 else 0.0
        rows.append([f"<code>{tid}</code>", str(len(tots)), f"{m:.2f}", f"{sd:.2f}",
                     f"{rs[-1].get('total'):.2f}"])
    return rows


def pools_summary() -> dict:
    data = read_json("pools_30.json") or {}
    full = sum(1 for v in data.values() if len(v.get("papers", [])) >= 3)
    partial = sum(1 for v in data.values() if 0 < len(v.get("papers", [])) < 3)
    empty = sum(1 for v in data.values() if not v.get("papers"))
    return {"total": len(data), "full": full, "partial": partial, "empty": empty}


def manuscripts() -> list:
    d = EVAL_OUT / "manuscripts"
    return sorted(d.glob("*.pdf")) if d.is_dir() else []


def _bench_head() -> str:
    p = EVAL_OUT / "bench_pilot_das.md"
    if not p.is_file():
        return '<p class="muted">no report yet — run <code>bench_eval</code> first</p>'
    body = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()][:60]
    return '<pre>' + html.escape("\n".join(body)) + "</pre>"


def render_index() -> str:
    var = variance_rows()
    pools = pools_summary()
    man = manuscripts()
    body = f"""
<h1>research_foodie — static mirror</h1>
<p class="muted">Read-only snapshot of <code>_eval_out/</code>. No backend here — GitHub Pages hosts static
files only; live triggers/SSE/cancel live in the local FastAPI dashboard
(<code>python -m uvicorn tools.web.app:app --host 127.0.0.1 --port 8787</code>).</p>

<h2>Judge variance (mean ± sd)</h2>
{_table(["topic", "rounds", "mean", "sd", "last"], var)}

<h2>30-topic evidence pools</h2>
{_table(["total", "full (≥3 papers)", "partial", "empty"],
        [[str(pools["total"]), str(pools["full"]), str(pools["partial"]), str(pools["empty"])]])}

<h2>Manuscripts ({len(man)})</h2>
<p class="muted"><a href="manuscripts.html">open the manuscripts page</a> for PDFs.</p>

<h2>Bench report (<code>bench_pilot_das.md</code>, head)</h2>
{_bench_head()}
"""
    return _page("Overview", body)


def render_dashboard() -> str:
    var = variance_rows()
    pools = pools_summary()
    man = manuscripts()
    body = f"""
<h1>Dashboard</h1>
<h2>Judge variance (as of last <code>variance_run</code>)</h2>
{_table(["topic", "rounds", "mean total", "sd (≤2σ ≈ judge noise)", "last round"], var)}
<h2>30-topic evidence pools</h2>
{_table(["total", "full (≥3 papers)", "partial", "empty"],
        [[str(pools["total"]), str(pools["full"]), str(pools["partial"]), str(pools["empty"])]])}
<h2>Manuscripts ({len(man)})</h2>
<p class="muted"><a href="manuscripts.html">open PDFs</a></p>
<h2>Bench report (raw head)</h2>
{_bench_head()}
"""
    return _page("Dashboard", body)


def render_manuscripts(man: list) -> str:
    rows = [[f'<a href="manuscripts/{html.escape(p.name)}">{p.name}</a>',
             f"{p.stat().st_size:,} B"] for p in man]
    body = f"""
<h1>Manuscripts</h1>
{_table(["file", "size"], rows, "<td colspan=2 class=muted>no rendered manuscripts yet (run a bench scenario first)</td>")}
<p class="muted">Rendered by <code>render_manuscript</code> (pandoc + xelatex + YaHei) during bench runs.</p>
"""
    return _page("Manuscripts", body)


def export(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    man_dir = out_dir / "manuscripts"
    man_dir.mkdir(exist_ok=True)

    (out_dir / "index.html").write_text(render_index(), encoding="utf-8")
    (out_dir / "dashboard.html").write_text(render_dashboard(), encoding="utf-8")
    (out_dir / "manuscripts.html").write_text(render_manuscripts(manuscripts()), encoding="utf-8")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    man = manuscripts()
    for p in man:
        shutil.copy2(p, man_dir / p.name)

    print(f"[export] wrote {len(list(out_dir.glob('*.html')))} pages + {len(man)} pdfs to {out_dir}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="F-3 static export (GH Pages deployable)")
    ap.add_argument("--out", default="gh-pages", help="output dir (default: ./gh-pages)")
    a = ap.parse_args()
    return export(Path(a.out))


if __name__ == "__main__":
    raise SystemExit(main())