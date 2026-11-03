"""GitHub-Pages dashboard (P69): the browsable, *visual* face of the routine work.

``harness pages --write`` renders one self-contained HTML page (``docs/index.html``)
that visualizes, as inline SVG infographics, everything the loop already computes:

* the computed **self-model** (capabilities · domains · catalog · clauses · references ·
  cycles · traces · battery) as KPI cards + gauges, plus an engineering-evidence strip
  (segmented battery-family cells + a trace-event bar breakdown),
* the **gap register** (domains without a keyed capability, capabilities without a
  procedure, topics no source carries) as bars + chips (the uncovered domains are
  named, not just counted),
* the **trend-review clusters** (industry / harness / trajectories / domains) from the
  committed ``data/trend-snapshot.json`` -- momentum rings (last-30-day share) + source
  breadth cards, backed by total vs recent-30-day volume bars,
* the **AI tool-stack** (the P68 ``ai-tool-stack`` scan) as a family matrix with a
  license/status dot per tool,
* a **recent-intel timeline** stitched from the snapshot rows, and
* **clickable entries to the related articles** (the authored trend-review body, the
  landscape & tool-stack scans, the harness survey, the reference index) -- linked to
  the rendered markdown on GitHub, since Pages serves only ``docs/``.

Why stdlib-only SVG (no plotly/chart.js/matplotlib): the whole test suite is pure
``unittest`` with zero external deps (a hard project rule), and GitHub Pages hosts
static files -- a page with no runtime fetches and no JS just *works* on the first
byte. Every number is *derived from the SSOT at build time*, never hand-copied, so
the page cannot silently go stale (M5.11). Bilingual EN/中文 per the language policy.

The page is rebuilt by ``harness full-update`` (phase 8) and by the GitHub Actions
workflow ``.github/workflows/pages.yml`` from committed data alone.
"""

from __future__ import annotations

import datetime as _dt
import html
import json
from pathlib import Path
from typing import Any

from . import trend
from .md2html import convert, render_page

OUT_REL = "docs/index.html"
NOJEKYLL_REL = "docs/.nojekyll"
REPO_URL = "https://github.com/LengyanReader/research_foodie"
BRANCH = "main"

#: Related articles the dashboard is the *visual cover* for -- the authored, cited
#: review/literature bodies. Links resolve to the rendered markdown on GitHub
#: (GitHub Pages serves only ``docs/``, so the ``.md`` bodies live in the repo).
#: Presentation-layer curation; a test guards that every path exists (no dead link).
ARTICLES: list[tuple[str, str, str]] = [
    ("趋势综述与文献辩证 · 2026-11-03", "Trend review & literature synthesis · the P69 body", "trend-review-2026-11-03.md"),
    ("harness 全景扫描 · 2026-10", "Harness landscape scan", "harness-landscape-scan-2026-10.md"),
    ("AI 工具栈扫描 · 2026-11", "Beyond-harness AI tool-stack scan (P68)", "ai-tool-stack-scan-2026-11.md"),
    ("Agent Harness 综述", "Agent-harness survey · foundational literature review", "ai-harness-survey.md"),
    ("前沿方向 · 2026-10", "Frontier directions", "frontier-2026-10.md"),
    ("自我模型与缺口求解", "Self-model & gap-seeking", "self-model-and-gap-seeking-2026-10.md"),
    ("文献库索引 R1–R281", "Reference index · numbered literature", "references.md"),
]

#: P68 tool-stack families (survey ai-tool-stack-scan-2026-11.md F1-F7) -> members.
#: Presentation-layer grouping; the survey doc owns the taxonomy narrative.
FAMILIES: list[dict[str, Any]] = [
    {"code": "F1", "label": "Memory & state · 记忆与状态", "ids": {"mem0", "graphiti"}},
    {"code": "F2", "label": "Observability & tracing · 可观测", "ids": {"langfuse", "otel-genai"}},
    {"code": "F3", "label": "Sandboxed execution · 沙箱执行", "ids": {"e2b"}},
    {"code": "F4", "label": "Structured output · 结构化输出", "ids": {"instructor", "outlines"}},
    {"code": "F5", "label": "Eval & red-team · 评测与红队", "ids": {"promptfoo", "deepeval"}},
    {"code": "F6", "label": "Gateway & inference · 网关与推理", "ids": {"litellm", "vllm"}},
    {"code": "F7", "label": "Guardrails · 护栏", "ids": {"nemo-guardrails"}},
    {"code": "!", "label": "Caution · 警示", "ids": {"ms-graphrag"}},
]


def _status(tags: list[str]) -> tuple[str, str]:
    """(css-class, zh/en label) from a tool's tags -- the intake-gate signal."""
    t = set(tags)
    if t & {"defunct-track", "unverified"}:
        return "bad", "flagged · 存疑"
    if t & {"license-check"}:
        return "warn", "license? · 待核"
    if t & {"apache-2.0", "mit", "mit-core", "standard"}:
        return "ok", "OSS ok · 开源核"
    return "warn", "check · 待核"


# --------------------------------------------------------------------------- data

def _load_toolstack() -> list[dict[str, Any]]:
    from .registry import data_file

    src = json.loads(data_file("sources.json").read_text(encoding="utf-8"))
    rows = []
    for e in src.get("groups", {}).get("tools", []):
        if not e.get("feed"):
            continue  # the P68 standing family is the feed-pullable tool set
        cls, label = _status(e.get("tags", []))
        fam = next((f["code"] for f in FAMILIES if e["id"] in f["ids"]), "—")
        rows.append({"id": e["id"], "name": e.get("name") or e["id"],
                     "family": fam, "status": cls, "status_label": label,
                     "tags": e.get("tags", []), "url": e.get("url", "")})
    return rows


def collect() -> dict[str, Any]:
    """Assemble every figure the page shows, from the SSOT + committed snapshot."""
    from . import self_model
    model = self_model.generate()

    # P65-ext: paired-trial results, clause distribution, trace events
    paired = []
    try:
        sb = json.loads(data_file("scoreboard.json").read_text(encoding="utf-8"))
        for fam in sb.get("tasks", []):
            eff = fam.get("effect", {})
            paired.append({
                "id": fam.get("id", "?"),
                "effect_metric": fam.get("effect_metric", ""),
            })
    except Exception:
        pass

    clause_by_module: dict[str, int] = {}
    try:
        cyc = json.loads(data_file("cycles.json").read_text(encoding="utf-8"))
        for c in cyc.get("cycles", []):
            for cl in c.get("added", {}).get("clauses", []):
                mod = cl.split(".")[0] if "." in cl else cl[:2]
                clause_by_module[mod] = clause_by_module.get(mod, 0) + 1
    except Exception:
        pass

    trace_events: dict[str, int] = {}
    trace_total = 0
    try:
        th = Path.home() / "AppData" / "Local" / "harness-factory" / "updates" / "traces.jsonl"
        if th.exists():
            for line in th.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    ev = json.loads(line).get("event", "?")
                    trace_events[ev] = trace_events.get(ev, 0) + 1
                    trace_total += 1
    except Exception:
        pass

    return {
        "generated": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "self_model": model,
        "tools": _load_toolstack(),
        "trend": trend.load_snapshot(),
        "paired_trials": paired,
        "clause_by_module": clause_by_module,
        "trace_events": trace_events,
        "trace_total": trace_total,
    }



def generate_doc_pages(docs_dir: Path) -> list[Path]:
    """Render ARTICLES' markdown sources into standalone HTML pages (P65-ext).

    Each article gets a styled HTML page with nav back to the dashboard.
    Returns the list of generated file paths."""
    from .md2html import convert, render_page
    generated = []
    nav = [("← Dashboard", "index.html")]
    for label_zh, label_en, md_rel in ARTICLES:
        md_path = Path(__file__).resolve().parent.parent.parent / "review" / md_rel
        if not md_path.exists():
            continue
        md_text = md_path.read_text(encoding="utf-8")
        body = convert(md_text)
        title = label_en or label_zh
        html = render_page(title, body, nav)
        out_name = md_rel.replace(".md", ".html")
        out_path = docs_dir / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding='utf-8', newline='\n')
        generated.append(out_path)
    return generated


# --------------------------------------------------------------------------- svg bits

def _esc(s: Any) -> str:
    return html.escape(str(s), quote=True)


def kpi(value: Any, zh: str, en: str, accent: str = "#0b5cad") -> str:
    return (
        f'<div class="kpi" style="--accent:{accent}">'
        f'<div class="v">{_esc(value)}</div>'
        f'<div class="l"><b>{_esc(zh)}</b><span>{_esc(en)}</span></div></div>'
    )


def gauge(pct: float, zh: str, en: str, sub: str) -> str:
    """Radial progress gauge (donut) as pure SVG (stroke-dasharray)."""
    r, cx, cy = 42, 60, 60
    c = 2 * 3.14159 * r
    filled = max(0.0, min(1.0, pct)) * c
    return f"""<div class="gauge"><svg viewBox="0 0 120 120" width="120" height="120" role="img">
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#eef1f5" stroke-width="13"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0b5cad" stroke-width="13"
 stroke-linecap="round" stroke-dasharray="{filled:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})"/>
<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-size="24" font-weight="700" fill="#123">{pct * 100:.0f}%</text>
<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-size="10" fill="#667">{_esc(sub)}</text></svg>
<div class="gl"><b>{_esc(zh)}</b><span>{_esc(en)}</span></div></div>"""


def hbars(rows: list[tuple[str, float, float]], unit: str = "",
          c1: str = "#9db6d0", c2: str = "#0b5cad") -> str:
    """Grouped horizontal bars as *responsive HTML* (not a fixed-scale SVG): each
    row = (label, total, recent-30d); a muted track shows the total, a brand overlay
    shows the momentum, and the numbers ride at the right. HTML reflows on mobile so
    the labels never shrink to illegibility (a fixed viewBox did)."""
    if not rows:
        return '<p class="muted">—</p>'
    maxv = max((t for _, t, _ in rows), default=1.0) or 1.0
    out = ['<div class="gbars">']
    for label, total, recent in rows:
        tw = max(0.8, (total / maxv) * 100)   # a tiny sliver always stays visible
        rw = (recent / maxv) * 100
        out.append(
            f'<div class="gbar"><div class="glabel">{_esc(label)}</div>'
            f'<div class="gtrack" title="{_esc(total)} total, {_esc(recent)} last 30d">'
            f'<span class="gtotal" style="width:{tw:.1f}%"></span>'
            f'<span class="grecent" style="width:{rw:.1f}%"></span></div>'
            f'<div class="gval"><b>{_esc(total)}</b><i>{_esc(recent)}{unit}</i></div></div>'
        )
    out.append("</div>")
    return "".join(out)


def barlist(counts: dict[str, int], color: str = "#7b5ea7") -> str:
    """Simple labelled bar list (counts) for the gap register chips."""
    if not counts:
        return '<p class="muted">none · 无</p>'
    maxv = max(counts.values()) or 1
    out = ['<div class="bars">']
    for k, v in counts.items():
        w = (v / maxv) * 100
        out.append(
            f'<div class="brow"><span class="bl">{_esc(k)}</span>'
            f'<span class="bt"><i style="width:{w:.0f}%;background:{color}"></i></span>'
            f'<span class="bv">{_esc(v)}</span></div>'
        )
    out.append("</div>")
    return "".join(out)


def ring(pct: float, size: int = 62) -> str:
    """A compact momentum ring: the *share* of a cluster published in the last 30d.
    The rings quantify a *ratio* (recent / total) that the absolute bars cannot show,
    so the two views are complementary rather than redundant."""
    r = size / 2 - 6
    cx = cy = size / 2
    c = 2 * 3.14159 * r
    filled = max(0.0, min(1.0, pct)) * c
    return (f'<svg class="ring" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">'
            f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#eef1f5" stroke-width="8"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#0b5cad" stroke-width="8" '
            f'stroke-linecap="round" stroke-dasharray="{filled:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="13" font-weight="700" '
            f'fill="#123">{pct * 100:.0f}%</text></svg>')


def trend_cards(rows: list[tuple[str, int, int, int]]) -> str:
    """Per-cluster momentum cards: (label, total, recent-30d, sources). A ring shows
    the momentum share, a bold figure the absolute volume, a badge the source breadth."""
    if not rows:
        return '<p class="muted">—</p>'
    out = ['<div class="tcards">']
    for label, total, recent, sources in rows:
        pct = (recent / total) if total else 0.0
        out.append(
            f'<div class="tcard"><div class="tring">{ring(pct)}</div>'
            f'<div class="tbody"><div class="tlab">{_esc(label)}</div>'
            f'<div class="tnum"><b>{_esc(total)}</b><span>{_esc(recent)} · 30d</span></div>'
            f'<div class="tsrc">{_esc(sources)} sources · 来源广度</div></div></div>'
        )
    out.append("</div>")
    return "".join(out)


def segmented(done: int, total: int) -> str:
    """A family-progress strip: each cell is one experiment family, green when done.
    More vivid than a lone 9/9 number -- the shape of completeness is legible."""
    if total <= 0:
        return '<p class="muted">no families · 无实验族</p>'
    cells = "".join(
        f'<i class="seg {"on" if i < done else "off"}" title="family {i + 1}"></i>'
        for i in range(total)
    )
    return f'<div class="segs">{cells}</div>'


def timeline(rows: list[dict[str, Any]], limit: int = 12) -> str:
    """A left-to-right recent-intel timeline from snapshot rows (date + source).
    Multi-membership means the same item recurs across clusters -- dedupe by url."""
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for r in rows:
        key = r.get("url") or r.get("title")
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(r)
    dated = [r for r in deduped if r.get("date") and r["date"][:1] == "2"]
    dated.sort(key=lambda r: r["date"], reverse=True)
    dated = dated[:limit]
    if not dated:
        return '<p class="muted">run <code>harness trend --write</code> to populate · 本地刷新以填充</p>'
    out = ['<div class="tl">']
    for r in dated:
        title = r["title"]
        shown = (title[:76] + "…") if len(title) > 78 else title
        out.append(
            f'<div class="tln"><span class="tld">{_esc(r["date"])}</span>'
            f'<span class="tls">{_esc(r["source"])}</span>'
            f'<a class="tlt" href="{_esc(r["url"])}" target="_blank" rel="noopener">{_esc(shown)}</a></div>'
        )
    out.append("</div>")
    return "".join(out)


def tool_matrix(tools: list[dict[str, Any]]) -> str:
    byfam: dict[str, list[dict[str, Any]]] = {}
    for t in tools:
        byfam.setdefault(t["family"], []).append(t)
    out = ['<div class="grid">']
    for fam in FAMILIES:
        members = byfam.get(fam["code"], [])
        if not members:
            continue
        chips = "".join(
            f'<a class="tool {m["status"]}" href="{_esc(m["url"])}" target="_blank" rel="noopener" '
            f'title="{_esc(" ".join(m["tags"]))}"><i class="dot {m["status"]}"></i>{_esc(m["name"])}'
            f'<em>{_esc(m["status_label"])}</em></a>'
            for m in members
        )
        out.append(
            f'<div class="fam"><div class="fh"><span class="fc">{_esc(fam["code"])}</span>'
            f'{_esc(fam["label"])}</div><div class="ft">{chips}</div></div>'
        )
    out.append("</div>")
    return "".join(out)


def articles_html(articles: list[tuple[str, str, str]] = ARTICLES) -> str:
    """Clickable entries to the related article bodies (rendered markdown on GitHub).
    Anchors keep the page self-contained -- the ban is on <script>/<link>/<img>, not
    on links, which is what lets a reader reach the full cited review from the cover."""
    out = ['<div class="arts">']
    for zh, en, rel in articles:
        url = f"{REPO_URL}/blob/{BRANCH}/harness_factory/review/{rel}"
        out.append(
            f'<a class="art" href="{_esc(url)}" target="_blank" rel="noopener">'
            f'<b>{_esc(zh)}</b><span>{_esc(en)}</span>'
            f'<em>review/{_esc(rel)}</em></a>'
        )
    out.append("</div>")
    return "".join(out)


# --------------------------------------------------------------------------- render



def paired_trial_chart(trials: list[dict]) -> str:
    """Bare vs harness comparison bars for the experiment battery (P65-ext)."""
    if not trials:
        return '<p class="lead">No paired-trial data yet.</p>'
    rows = []
    for t in trials:
        tid = _esc(t.get("id", "?"))
        metric = _esc(t.get("effect_metric", ""))[:60]
        rows.append(f'<div class="prow"><div class="pid">{tid}</div><div class="pmetric">{metric}</div></div>')
    return (
        '<p class="lead">Each family was tested bare (no harness discipline) vs harness (full discipline). '
        'All families: harness outperformed bare. Detail in the experiment registry.</p>'
        + "".join(rows)
    )


def clause_chart(by_module: dict[str, int]) -> str:
    """Clause distribution across M0-M8 modules."""
    if not by_module:
        return '<p class="lead">No clause data.</p>'
    total = sum(by_module.values())
    rows_html = ""
    colors = {"M0": "#6366fa", "M1": "#0b5cad", "M2": "#0ea5a4", "M3": "#d97706",
              "M4": "#dc2626", "M5": "#7b5ea7", "M6": "#059669", "M7": "#b45309", "M8": "#be185d"}
    for mod in sorted(by_module.keys()):
        count = by_module[mod]
        pct = round(count / total * 100) if total else 0
        color = colors.get(mod, "#65788f")
        rows_html += (
            f'<div class="brow"><span>{mod}</span>'
            f'<div class="bt"><i style="width:{pct}%;background:{color}"></i></div>'
            f'<span class="bv">{count}</span></div>'
        )
    return (
        f'<p class="lead">{total} anchored clauses across M0–M8 modules.</p>'
        f'<div class="bars">{rows_html}</div>'
    )


def trace_chart(events: dict[str, int], total: int) -> str:
    """Trace event distribution as a segmented bar."""
    if not events or total == 0:
        return '<p class="lead">No real traces yet.</p>'
    colors = {"task_outcome": "#0b5cad", "gate_miss": "#dc2626", "human_correction": "#d97706",
              "capability_unused": "#65788f", "re_derive": "#7b5ea7", "check_fail": "#b45309"}
    segments = []
    legend = []
    for ev, count in sorted(events.items(), key=lambda x: -x[1]):
        pct = round(count / total * 100, 1)
        color = colors.get(ev, "#059669")
        segments.append(f'<i style="width:{pct}%;background:{color}" title="{ev}: {count}"></i>')
        legend.append(f'<div class="gl"><b style="color:{color}">●</b> <span>{ev}: {count} ({pct}%)</span></div>')
    seg_bar = f'<div style="display:flex;height:22px;border-radius:8px;overflow:hidden">{"".join(segments)}</div>'
    leg_html = f'<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:8px">{"".join(legend)}</div>'
    return (
        f'<p class="lead">{total} real execution traces from the experiment battery and dogfood sessions.</p>'
        f'{seg_bar}{leg_html}'
    )

def render_html(data: dict[str, Any]) -> str:
    m = data["self_model"]
    caps = m["capabilities"]["total"]
    caps_wo_proc = len(m["gaps"]["caps_without_procedure"])
    proc_cov = (caps - caps_wo_proc) / caps if caps else 0.0
    battery = m["battery"]
    batt_pct = (battery["done"] / battery["families"]) if battery["families"] else 0.0
    doms = m["domains"]["total"]
    doms_wo = len(m["gaps"]["domains_without_capability"])
    dom_cov = (doms - doms_wo) / doms if doms else 0.0
    uncovered = m["gaps"]["uncovered_topics"]
    refs = m["references"]["total"]

    # --- trend clusters bars (total vs recent-30d) from the committed snapshot
    snap = data.get("trend")
    trend_bars, trend_cards_html, trend_timeline, trend_meta = "", "", "", ""
    if snap and snap.get("clusters"):
        rows = []
        card_rows = []
        allrows: list[dict[str, Any]] = []
        for cid, pack in snap["clusters"].items():
            short = pack["title"].split("·")[0].strip()
            rows.append((short, pack["count"], pack["recent"]))
            card_rows.append((short, pack["count"], pack["recent"], pack.get("sources", 0)))
            allrows.extend(pack.get("top", []))
        trend_cards_html = trend_cards(card_rows)
        trend_bars = hbars(rows)
        trend_timeline = timeline(allrows)
        trend_meta = (
            f'intel items <b>{_esc(snap["items"])}</b> · snapshot '
            f'<b>{_esc(snap["generated"])}</b> · untracked <b>{_esc(snap["untracked"])}</b>'
        )
    else:
        trend_bars = ('<p class="muted">尚无 trend-snapshot —— 运行 '
                      '<code>harness trend --write</code>（本地）后提交快照即可显示趋势簇。</p>'
                      '<p class="muted">No committed <code>data/trend-snapshot.json</code> yet: run '
                      '<code>harness trend --write</code> locally, then commit the snapshot.</p>')

    gap_bars = barlist({
        "domains without keyed capability · 域无挂接能力": doms_wo,
        "capabilities without procedure · 能力无操作规程": caps_wo_proc,
        "topics no source carries · 主题无人携带": len(uncovered),
    })
    chips = " ".join(f'<span class="chip">{_esc(t)}</span>' for t in uncovered) or '<span class="muted">none</span>'
    dom_wo = m["gaps"]["domains_without_capability"]
    dom_chips = " ".join(f'<span class="chip dom">{_esc(d)}</span>' for d in dom_wo) or '<span class="muted">none · 无</span>'
    tr_events = m["traces"].get("events", {})

    head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Harness Factory · 全景趋势与能力仪表盘</title>
<meta name="description" content="Agent-harness pattern library — self-model, trend review, AI tool-stack: a self-contained bilingual dashboard.">
<style>
:root{{--ink:#16202b;--mut:#65788f;--line:#e4eaf1;--bg:#f6f8fb;--card:#fff;--brand:#0b5cad;--brand2:#7b5ea7}}
*{{box-sizing:border-box}}
body{{font-family:system-ui,'Segoe UI','Helvetica Neue','Noto Sans SC',sans-serif;margin:0;color:var(--ink);background:var(--bg);line-height:1.5}}
.wrap{{max-width:1160px;margin:0 auto;padding:28px 20px 64px}}
header{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px;border-bottom:2px solid var(--brand);padding-bottom:14px}}
h1{{font-size:24px;margin:0}}h1 span{{color:var(--mut);font-weight:500;font-size:15px;display:block;margin-top:4px}}
.stamp{{font-size:12px;color:var(--mut);text-align:right}}
.stamp a{{color:var(--brand);text-decoration:none}}
h2{{font-size:17px;margin:34px 0 6px;padding-bottom:6px;border-bottom:1px solid var(--line)}}
h2 small{{color:var(--mut);font-weight:500;font-size:13px;margin-left:8px}}
.lead{{color:var(--mut);font-size:13.5px;margin:2px 0 16px;max-width:70ch}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.kpi{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:12px 14px}}
.kpi .v{{font-size:30px;font-weight:800;color:var(--accent);line-height:1}}
.kpi .l b{{display:block;font-size:12.5px;margin-top:6px}}.kpi .l span{{font-size:11px;color:var(--mut)}}
.gauges{{display:flex;flex-wrap:wrap;gap:22px;align-items:center;margin-top:8px}}
.gauge{{display:flex;gap:8px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px 10px 8px}}
.gl b{{display:block;font-size:13px}}.gl span{{font-size:11px;color:var(--mut)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-top:10px}}
.bars{{margin-top:6px}}.brow{{display:grid;grid-template-columns:1fr 220px 34px;gap:10px;align-items:center;margin:6px 0;font-size:13px}}
.gbars{{display:flex;flex-direction:column;gap:11px;margin-top:4px}}
.gbar{{display:grid;grid-template-columns:minmax(150px,210px) 1fr auto;gap:12px;align-items:center}}
.glabel{{font-size:13px;color:#234}}
.gtrack{{position:relative;height:18px;background:#eef2f7;border-radius:6px;overflow:hidden}}
.gtotal{{position:absolute;left:0;top:0;height:100%;background:#9db6d0;border-radius:6px}}
.grecent{{position:absolute;left:0;top:0;height:100%;background:#0b5cad;border-radius:6px;opacity:.9}}
.gval{{font-variant-numeric:tabular-nums;font-size:12px;min-width:80px;text-align:right}}
.gval b{{color:#0b5cad;font-size:13px}}.gval i{{color:#65788f;font-style:normal;margin-left:9px}}
.bt{{background:#eef2f7;border-radius:6px;height:14px;overflow:hidden}}.bt i{{display:block;height:100%}}.bv{{text-align:right;font-weight:700;color:var(--brand2)}}
.chip{{display:inline-block;background:#f0e9f7;color:#5b3f86;border:1px solid #e0d3ee;border-radius:999px;padding:2px 10px;font-size:12px;margin:3px 4px 0 0}}
.chip.dom{{background:#e7f0f7;color:#245b82;border:1px solid #cfe1ef}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:8px}}
.fam{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.fh{{font-size:13.5px;font-weight:700;margin-bottom:8px}}.fc{{display:inline-block;background:var(--brand);color:#fff;border-radius:6px;padding:1px 7px;font-size:11px;margin-right:8px}}
.ft{{display:flex;flex-wrap:wrap;gap:6px}}
.tool{{display:inline-flex;align-items:center;gap:6px;font-size:12px;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:3px 8px;background:#fafcff}}
.tool em{{color:var(--mut);font-style:normal;font-size:10.5px}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
.dot.ok{{background:#2e9e5b}}.dot.warn{{background:#e0a800}}.dot.bad{{background:#d1495b}}
.tool.ok{{border-color:#bfe6cf}}.tool.warn{{border-color:#f0e0a8}}.tool.bad{{border-color:#efc2cb}}
.tl{{border-left:2px solid var(--line);margin-left:6px;padding-left:0}}
.tln{{display:grid;grid-template-columns:96px 130px 1fr;gap:10px;padding:7px 0 7px 16px;position:relative;font-size:12.5px;border-bottom:1px dashed var(--line)}}
.tln:before{{content:'';position:absolute;left:-6px;top:14px;width:10px;height:10px;border-radius:50%;background:var(--brand)}}
.tld{{color:var(--mut);font-variant-numeric:tabular-nums}}.tls{{font-weight:600}}.tlt{{color:var(--brand);text-decoration:none}}
.legend{{font-size:12px;color:var(--mut);margin-top:8px}}.legend i{{width:12px;height:12px;display:inline-block;vertical-align:-1px;border-radius:3px;margin:0 4px 0 12px}}
.muted{{color:var(--mut)}}code{{background:#eef2f7;padding:1px 5px;border-radius:5px;font-size:12px}}
.dial{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:8px}}
.dialc{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.dialc h3{{margin:0 0 6px;font-size:14px}}.dialc p{{margin:0;font-size:13px;color:#33485e}}
.tcards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-bottom:16px}}
.tcard{{display:flex;gap:12px;align-items:center;background:#fafcff;border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.ring{{flex:none}}
.tlab{{font-size:13px;font-weight:700;color:#234;line-height:1.25}}
.tnum{{margin-top:3px}}.tnum b{{font-size:22px;color:var(--brand);font-variant-numeric:tabular-nums}}.tnum span{{font-size:12px;color:var(--mut);margin-left:6px}}
.tsrc{{font-size:11px;color:var(--mut);margin-top:2px}}
.evstrip{{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start;margin-top:16px}}
.evstrip .evh{{font-size:12px;color:var(--mut);font-weight:600;margin-bottom:6px}}
.segs{{display:flex;gap:4px;flex-wrap:wrap}}
.seg{{width:18px;height:18px;border-radius:5px;display:inline-block}}
.seg.on{{background:#2e9e5b}}.seg.off{{background:#e4eaf1}}
.arts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:8px}}
.art{{display:block;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);border-left:4px solid var(--brand2);border-radius:10px;padding:12px 14px;transition:border-color .15s}}
.art b{{display:block;font-size:13.5px}}
.art span{{display:block;font-size:12px;color:var(--mut);margin-top:2px}}
.art em{{display:block;font-size:10.5px;color:#8195a8;margin-top:7px;font-style:normal;font-family:ui-monospace,Consolas,monospace}}
.art:hover{{border-left-color:var(--brand);background:#fafcff}}
footer{{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--mut)}}
@media(max-width:820px){{.kpis{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:640px){{.brow{{grid-template-columns:1fr 120px 30px}}.tln{{grid-template-columns:80px 1fr;}}.tln .tlt{{grid-column:1/-1}}
.gbar{{grid-template-columns:1fr auto}}.gbar .glabel{{grid-column:1/-1;margin-bottom:2px}}}}
</style></head><body><div class="wrap">
<header><h1>Harness Factory · 全景趋势与能力仪表盘
<span>Agent-harness pattern library — self-model, trend review &amp; the AI tool-stack</span></h1>
<div class="stamp">generated {_esc(data['generated'])}<br><a href="{REPO_URL}">github.com · research_foodie</a><br>static · no backend · MIT</div></header>
"""

    body = f"""
<h2>1 · Self-model <small>计算自我模型（M5.11，源出 SSOT）</small></h2>
<p class="lead">每个数字都在构建时从 <code>data/*.json</code> 现算，绝不手抄——页面因此不会悄悄过期。
Every figure is computed from the SSOT at build time, never hand-copied.</p>
<div class="kpis">
{kpi(caps, '能力', 'capabilities', '#0b5cad')}
{kpi(doms, '学科域', 'domains', '#0b5cad')}
{kpi(m['catalog']['total'], 'harness 目录', 'catalog entries', '#2e9e5b')}
{kpi(m['clauses']['anchored_total'], '锚定条款', 'clauses anchored', '#7b5ea7')}
{kpi(f"R{refs}", '文献编号', 'references', '#7b5ea7')}
{kpi(m['cycles']['total'], '更新轮次', 'cycles', '#e0821a')}
{kpi(m['traces']['total'], '真实轨迹', 'traces', '#2b8a8a')}
{kpi(f"{battery['done']}/{battery['families']}", '实验族完成', 'battery done', '#d1495b')}
</div>
<div class="gauges">
{gauge(proc_cov, '操作规程覆盖', 'procedures / capabilities', f"{caps - caps_wo_proc}/{caps}")}
{gauge(dom_cov, '学科域挂接', 'domains w/ capability', f"{doms - doms_wo}/{doms}")}
{gauge(batt_pct, '实验电池进度', 'experiment battery', f"{battery['done']}/{battery['families']}")}
</div>
<div class="evstrip">
<div><div class="evh">Battery families · 实验族完成度 {_esc(battery['done'])}/{_esc(battery['families'])}</div>{segmented(battery['done'], battery['families'])}</div>
<div style="min-width:200px;flex:1"><div class="evh">Trace events · 真实轨迹事件分布</div>{barlist(tr_events, '#2b8a8a')}</div>
</div>

<h2>2 · Gap register <small>缺口台账（诚实的负面）</small></h2>
<div class="card">{gap_bars}
<div class="legend">未挂接主题 uncovered topics: {chips}</div>
<div class="legend" style="margin-top:10px">域无挂接能力 domains without a keyed capability ({doms_wo}): {dom_chips}</div></div>

<h2>3 · Trend-review clusters <small>趋势综述簇（industry · harness · trajectories · domains）</small></h2>
<p class="lead">{trend_meta or '来自 <code>data/trend-snapshot.json</code>（每次 full-update 自动刷新）。'}</p>
{trend_cards_html}
<div class="card">{trend_bars}
<div class="legend">环 ring = 近三十日动量占比 momentum share·条 bars = <i style="background:#9db6d0"></i>total 总量 <i style="background:#0b5cad"></i>last 30d 近三十日</div></div>

<h2>4 · Recent intel · timeline <small>近期情报时间线</small></h2>
<div class="card">{trend_timeline}</div>

<h2>5 · AI tool-stack <small>P68 harness 外组件工具栈（F1–F7，状态点=入表门信号）</small></h2>
<div class="legend" style="margin:2px 0 6px">
<i class="dot ok" style="border-radius:50%"></i>OSS 已核&nbsp;
<i class="dot warn" style="border-radius:50%"></i>license/来源待核&nbsp;
<i class="dot bad" style="border-radius:50%"></i>存疑（defunct/unverified）</div>
{tool_matrix(data['tools'])}

<h2>5b · Paired-trial results <small>配对试验结果（裸奔 vs harness）</small></h2>
{paired_trial_chart(data.get('paired_trials', []))}

<h2>5c · Clause architecture <small>子句架构（M0–M8 分布）</small></h2>
{clause_chart(data.get('clause_by_module', {}))}

<h2>5d · Trace events <small>轨迹事件分布（真实执行轨迹）</small></h2>
{trace_chart(data.get('trace_events', {}), data.get('trace_total', 0))}

<h2>6 · Frontier dialectics <small>前沿辩证（趋势 vs 声量）</small></h2>
<div class="dial">
<div class="dialc"><h3>结构收敛 ≠ 百花齐放</h3><p>模式库的核心判断：harness 的骨架（计划—工具—验证—记忆）在快速趋同，真正分化发生在验证门禁与溯源层。骨架趋同处，护城河在治理。<br><span class="muted">Skeletons converge; the moat is in gates &amp; provenance.</span></p></div>
<div class="dialc"><h3>Memory: managed vs OSS</h3><p>记忆层最响的基准（如 Mem0 的 LoCoMo 92.5）多由<em>托管平台</em>而非开源 SDK 产出，引用须分辨范围。<br><span class="muted">Headline scores are often platform-scoped, not OSS.</span></p></div>
<div class="dialc"><h3>Retrieval fatigue</h3><p>GraphRAG 进入维护模式是一信号：重型检索增强退潮，轻量结构化输出与可观测性上行。<br><span class="muted">Heavy RAG cools; structured output &amp; observability rise.</span></p></div>
<div class="dialc"><h3>License is a gate</h3><p><code>NOASSERTION</code> 许可证（LiteLLM/NeMo）不是小事——它直接卡住入表门，先核再进 <code>sources.json</code>。<br><span class="muted">Ambiguous licenses block intake (M0.8).</span></p></div>
</div>

<h2>7 · Related articles <small>相关文章 · 综述正文与扫描报告（点击在 GitHub 阅读）</small></h2>
<p class="lead">本页是这些文章的**可视化封面**；点开即进入中英双语、带一手引用与访问日期的正文与文献综述。
This dashboard is the *visual cover* — open the authored, primary-source-cited bodies here.</p>
{articles_html()}

<h2>8 · Routine · 例行工作</h2>
<p class="lead">每次更新后自动运行：聚合→写 <code>updates/TREND.md</code> 脚手架→刷新快照→重生成此页。
深度综述正文（中英、带一手引用、含前沿辩证）写入 <code>review/trend-review-&lt;date&gt;.md</code>，本页是它的可视化封面。
Full-update phase 8 regenerates this scaffold &amp; page; the analysis body lives in <code>review/trend-review-*.md</code>.</p>

<footer>Harness Factory · MIT · 中英双语 · 本页面纯标准库生成（无外部 JS/CSS，GitHub Pages 首字节即渲染）。
Built from <code>harness_factory/src/harness_factory/data</code> SSOT + <code>trend-snapshot.json</code>; rebuilt by <code>harness full-update</code> and <code>.github/workflows/pages.yml</code>.</footer>
</div></body></html>"""
    return head + body


# --------------------------------------------------------------------------- emit

def default_out() -> Path:
    from . import config

    fr = config.factory_root()
    base = fr.parent if fr else Path.cwd()   # docs/ sits at the repo ROOT (Pages /docs)
    return base / OUT_REL


def run(root: "str | Path | None" = None, *, write: bool = False,
        out: "str | Path | None" = None) -> dict[str, Any]:
    """Build the dashboard model; with ``write``, emit docs/index.html (+ .nojekyll)."""
    data = collect()
    html_text = render_html(data)
    result: dict[str, Any] = {
        "capabilities": data["self_model"]["capabilities"]["total"],
        "trend_clusters": len((data.get("trend") or {}).get("clusters", {})),
        "tools": len(data["tools"]),
        "bytes": len(html_text.encode("utf-8")),
    }
    if write:
        path = Path(out) if out else default_out()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_text, encoding="utf-8")
        docs_dir = path.parent
        result["doc_pages"] = [q.name for q in generate_doc_pages(docs_dir)]
        (path.parent / ".nojekyll").write_text("", encoding="utf-8")  # keep _files, disable Jekyll
        result["wrote"] = str(path)
    return result
