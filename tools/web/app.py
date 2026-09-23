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
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response, StreamingResponse
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

HTML_HEAD = """<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">
<title>research_foodie · {title}</title>
<style>
/* ------------------------------------------------------------------
   II    design tokens — a set manuscript with a terminal transcript.
   Serif prose on cold press paper; every figure and footnote set in
   a mono voice. One live heartbeat: the inked block cursor.
   ------------------------------------------------------------------ */
:root{{
  --paper:#f3f1e7; --card:#fbf9f1; --panel:#eceadc;
  --ink:#22231c; --ink-soft:#57584a; --ink-faint:#8b8c7d;
  --rule:#d8d5c2; --rule-strong:#22231c;
  --link:#345b6e; --pass:#3c6b52; --warn:#9a6d10; --mark:#a63a2a;
  --ghost:#c9c6b3; --live-tint:#f6e7de; --mast:#22231c;
  --serif:Georgia,'Iowan Old Style','Source Serif 4','Times New Roman',serif;
  --sans:'Segoe UI','PingFang SC',system-ui,sans-serif;
  --mono:Consolas,'Cascadia Mono','IBM Plex Mono',ui-monospace,monospace;
}}
*{{box-sizing:border-box}}
html{{scrollbar-gutter:stable}}
::selection{{background:#345b6e;color:#fbf9f1}}
body{{margin:0;color:var(--ink);background-color:var(--paper);
  font:15.5px/1.72 var(--serif);
  background-image:repeating-linear-gradient(90deg,transparent 0 68px,
    rgba(34,35,28,.05) 68px 69px),repeating-linear-gradient(90deg,transparent 0 340px,
    rgba(34,35,28,.05) 340px 341px);background-attachment:fixed}}
body::before{{content:'';position:fixed;inset:0 0 auto 0;height:4px;background:var(--mast);z-index:5}}
.frame{{max-width:1080px;margin:0 auto;padding:0 clamp(16px,4vw,44px)}}
h1,h2,h3{{font-family:var(--serif);line-height:1.25;font-weight:600}}
h1{{font-size:clamp(26px,3.8vw,34px);margin:.1em 0 .3em}}
h2{{font-size:18px;margin:0;letter-spacing:.01em}}
h2 .en{{font-family:var(--sans);font-size:12.5px;color:var(--ink-faint);font-weight:400;margin-left:10px}}
a{{color:var(--link);text-decoration:none}}
a:hover{{text-decoration:underline;color:var(--ink)}}
code{{font-family:var(--mono);font-size:12px}}
pre{{font-family:var(--mono);font-size:12px;background:transparent;margin:0}}
.num, .stg-no, .tick, .id, td, th{{font-variant-numeric:tabular-nums}}

/* layout frame */
.frame{{max-width:1080px;margin:0 auto;padding:16px clamp(16px,5vw,60px) 64px}}
.nav{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;
  padding:14px 0;margin-bottom:22px}}
.brand{{font-family:var(--mono);font-size:15px;font-weight:700;letter-spacing:.01em;color:var(--ink)}}
.brand .zh{{font-family:var(--sans);font-weight:400;color:var(--ink-faint);font-size:12px;margin-left:10px}}
.brand .cursor{{display:inline-block;width:.62em;height:1.05em;margin-left:5px;
  background:var(--mark);vertical-align:-.18em;animation:blink 1.1s steps(2,start) 4;
  animation-iteration-count:4;animation-fill-mode:forwards}}
@keyframes blink{{to{{visibility:hidden}}}}
nav a{{margin-left:20px;color:var(--ink-soft);font-size:14px;font-family:var(--sans)}}
nav a.cur{{color:var(--ink);border-bottom:1px solid var(--mark)}}

/* masthead — ink letterpress band */
.mast{{background:var(--mast);color:var(--paper);position:relative;
  padding:30px clamp(20px,4vw,44px) 26px;margin-bottom:6px}}
.mast::after{{content:'';position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--mark)}}
.mast-grid{{display:grid;grid-template-columns:1fr auto;gap:28px;align-items:start}}
.mast-meta{{font-family:var(--mono);font-size:11px;color:#c9cbb8;letter-spacing:.06em;text-transform:none;margin-bottom:10px}}
.mast h1{{margin:.05em 0 .1em;font-variant:small-caps;font-size:clamp(30px,4.6vw,46px);
  letter-spacing:.02em;color:var(--paper);line-height:1.1}}
.mast h1 .cursor{{display:inline-block;width:.28em;height:.9em;margin-left:10px;
  background:var(--mark);vertical-align:.08em;animation:blink 1.1s steps(2,start) 6;
  animation-iteration-count:6;animation-fill-mode:forwards}}
.lede{{max-width:66ch;color:#cdceba;font-size:15.5px;line-height:1.72;margin:.65em 0 0}}
.nostamp{{font-family:var(--mono);font-size:10.5px;line-height:2;color:#b7b9a4;text-align:right;
  border-left:1px solid rgba(205,206,186,.28);padding-left:18px;white-space:nowrap;margin-top:6px}}
.nostamp b{{color:#efefe2;font-weight:700}}
.nostamp .live-dot{{color:var(--mark)}}
@keyframes pulse{{50%{{opacity:.25}}}}

/* sections */
.sect{{margin:34px 0 0}}
.sect-head{{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;
  border-bottom:1px solid var(--rule-strong);padding-bottom:6px;margin-bottom:16px}}
.sect-head h2 .idx{{font-family:var(--mono);font-weight:700;color:var(--mark);margin-right:10px;
  font-variant-numeric:tabular-nums}}
.sect-head .side{{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint);letter-spacing:.02em}}

/* probe — the paper form */
.probe{{background:var(--card);border:1px solid var(--rule);padding:22px 24px 18px;position:relative}}
.probe::before{{content:'';position:absolute;inset:0 0 auto 0;height:2px;background:var(--rule)}}
.probe label.fl{{display:block;font-size:12.5px;font-family:var(--mono);color:var(--ink-soft);margin-bottom:9px;letter-spacing:.02em}}
.probe label.fl::before{{content:'§ ';color:var(--mark);font-weight:700}}
.qfield{{width:100%;padding:12px 14px;font:15px/1.5 var(--serif);color:var(--ink);
  border:1px solid var(--rule-strong);border-radius:0;background:var(--panel);caret-color:var(--mark)}}
.qfield::placeholder{{font-style:italic;color:var(--ink-faint)}}
.qfield:focus{{outline:2px solid var(--link);outline-offset:1px;border-color:var(--link);background:var(--card)}}
.seg{{display:inline-flex;border:1px solid var(--rule-strong);margin:0}}
.seg label{{display:flex;align-items:baseline;gap:8px;margin:0;padding:9px 15px;font:12.5px var(--mono);
  color:var(--ink-soft);cursor:pointer;border-right:1px solid var(--rule)}}
.seg label:last-child{{border-right:0}}
.seg input{{position:absolute;opacity:0;pointer-events:none}}
.seg b{{font-weight:700;color:var(--ink)}}
.seg small{{display:block;font-size:10px;color:var(--ink-faint);letter-spacing:.01em}}
.seg label:has(input:checked){{background:var(--ink);color:var(--paper)}}
.seg label:has(input:checked) b{{color:var(--paper)}}
.seg label:has(input:checked) small{{color:var(--rule)}}
.seg label:has(input:checked)::before{{content:'▮ ';color:var(--mark)}}
.seg label:has(input:focus-visible){{outline:2px solid var(--link);outline-offset:1px}}
.probe-row{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:15px}}
.hint{{margin:13px 0 0;font-family:var(--mono);font-size:11.5px;color:var(--ink-faint)}}
.hint b{{font-weight:700;color:var(--ink-soft)}}

/* buttons — inked controls */
.btn{{font:12.5px/1 var(--mono);color:var(--ink);background:transparent;border:1px solid var(--rule-strong);
  padding:0 18px;min-height:36px;cursor:pointer;border-radius:0;letter-spacing:.02em}}
.btn:hover:not(:disabled){{background:var(--ink);color:var(--paper)}}
.btn:disabled{{opacity:.55;cursor:wait}}
.btn:focus-visible{{outline:2px solid var(--link);outline-offset:2px}}
.btn.primary{{background:var(--ink);color:var(--paper)}}
.btn.primary:hover:not(:disabled){{background:var(--mark);border-color:var(--mark)}}
.btn.danger{{border-color:var(--mark);color:var(--mark)}}
.btn.danger:hover:not(:disabled){{background:var(--mark);color:var(--paper)}}
.btn.mini{{padding:0 11px;min-height:28px;font-size:11px;border-color:var(--rule);color:var(--ink-soft)}}
.btn.mini:hover:not(:disabled){{border-color:var(--ink);color:var(--ink)}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;counter-reset:chip}}
.chips .btn{{min-height:30px;border-color:var(--rule);color:var(--ink-soft);font-size:11.5px;background:var(--card)}}
.chips .btn::before{{counter-increment:chip;content:'#' counter(chip,decimal-leading-zero) ' ';color:var(--mark);font-weight:700}}
.chips .btn:hover:not(:disabled){{background:var(--ink);border-color:var(--ink);color:var(--paper)}}
.chips .btn:hover:not(:disabled)::before{{color:var(--paper)}}

/* mission — folio + numbered stage sequence */
.mission{{display:flex;flex-direction:column}}
.folio{{display:flex;gap:3px;align-items:center;margin:0 0 8px}}
.f-tick{{flex:1;height:7px;background:var(--ghost)}}
.f-tick.done{{background:var(--pass)}}
.f-tick.live{{background:var(--mark);animation:pulse 1.4s ease-in-out infinite}}
.f-label{{font:11.5px var(--mono);color:var(--ink-faint);margin-left:12px;letter-spacing:.02em}}
.stg{{display:grid;grid-template-columns:56px 1fr auto;gap:0 14px;padding:15px 8px 14px 4px;
  border-bottom:1px solid var(--rule)}}
.stg:last-child{{border-bottom:0}}
.stg-no{{padding-top:5px;font-family:var(--mono);font-size:11.5px;color:var(--ink-faint);letter-spacing:.02em}}
.stg-title{{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;font-family:var(--serif);font-weight:600;font-size:16px}}
.stg-title .zh{{font-family:var(--sans);font-weight:400;color:var(--ink-faint);font-size:12px}}
.stg-title .tick{{font-family:var(--mono);font-size:11px;color:var(--pass);margin-left:auto;letter-spacing:.02em}}
.stg-meta{{font:11px var(--mono);color:var(--ink-faint);text-align:right;padding-top:6px;
  letter-spacing:.02em;white-space:nowrap}}
.stg-what{{margin:5px 0 1px}}
.stg-why{{margin:0 0 6px;color:var(--ink-soft);font-size:14px}}
.stg-note{{font-family:var(--mono);font-size:11.5px;color:var(--ink)}}
.stg-tech{{font-family:var(--mono);font-size:11px;color:var(--ink-faint);margin-top:2px}}
.stg.live{{background:var(--live-tint);margin:0 -12px;padding-left:16px;padding-right:16px}}
.stg.live .stg-no{{color:var(--mark);font-weight:700}}
.stg.live .stg-title .tick{{color:var(--mark)}}
.stg.live .stg-title .tick::before{{content:'● ';animation:pulse 1.4s ease-in-out infinite}}
.stg.live .stg-meta{{color:var(--mark);font-weight:700}}
.stg.off{{opacity:.62}}
.stg.done .stg-no{{color:var(--pass)}}
.stg.done .stg-meta{{color:var(--pass)}}

/* raw-tail — the transcript drawer */
details.rawtail{{border:1px solid var(--rule);margin-top:8px;background:var(--card)}}
details.rawtail summary{{cursor:pointer;padding:9px 13px;font:11.5px var(--mono);color:var(--ink-soft);list-style:none;letter-spacing:.02em}}
details.rawtail summary::before{{content:'▸ ';color:var(--mark)}}
details.rawtail[open] summary::before{{content:'▾ '}}
#tail{{margin:0;padding:12px 14px;height:240px;overflow:auto;border-top:1px solid var(--rule);
  font-family:var(--mono);font-size:12px;line-height:1.5;color:#dbe2c9;background:#16180f;white-space:pre-wrap}}

/* run archive — index cards with ghost folio numbers */
.runs{{display:flex;flex-direction:column;gap:12px}}
.run-card{{position:relative;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--rule);padding:14px 18px 13px;overflow:hidden;transition:border-color .15s ease}}
.run-card:hover{{border-left-color:var(--link)}}
.run-card::after{{content:attr(data-id);position:absolute;right:14px;top:4px;
  font:700 46px/1 var(--mono);color:var(--ghost);opacity:.55;pointer-events:none;letter-spacing:.01em}}
.run-top{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;padding-right:90px;position:relative;z-index:1}}
.run-top strong{{font-family:var(--serif);font-size:16px}}
.run-card .cmd{{margin-top:8px;font-family:var(--mono);font-size:11px;color:var(--ink-faint);word-break:break-all;letter-spacing:.01em}}
.run-card .q{{margin-top:6px;font-family:var(--serif);font-style:italic;color:var(--ink-soft);padding-right:90px}}
.run-card .res{{margin-top:6px;font-family:var(--mono);font-size:11.5px;color:var(--ink-soft)}}
.run-card .res a{{margin-right:14px}}
.mono{{font-family:var(--mono)}}
.id{{color:var(--ink-faint);font-size:11.5px}}
.badge{{font-family:var(--mono);font-size:10.5px;padding:2px 9px;border:1px solid var(--rule-strong);letter-spacing:.03em}}
.badge.ok{{border-color:var(--pass);color:var(--pass)}}
.badge.fail{{border-color:var(--mark);color:var(--mark)}}
.badge.run{{border-color:var(--mark);color:var(--mark)}}
.badge.cancel{{border-color:var(--warn);color:var(--warn)}}
.badge.muted{{border-color:var(--rule);color:var(--ink-faint)}}
.badge.ok, .badge.fail, .badge.run{{background:var(--card)}}

/* tables & utilities */
table{{border-collapse:collapse;width:100%;font-size:13px}}
td,th{{border:1px solid var(--rule);padding:7px 11px;text-align:left}}
th{{background:var(--panel);font-family:var(--mono);font-weight:600;font-size:11.5px}}
tbody tr:nth-child(even){{background:var(--card)}}
ul{{margin:.4em 0}}li{{margin:.15em 0}}
.muted{{color:var(--ink-faint)}}.green{{color:var(--pass)}}.red{{color:var(--mark)}}.amber{{color:var(--warn)}}
.mission-empty{{color:var(--ink-faint);font-family:var(--serif);font-style:italic;padding:10px 0}}

/* colophon */
.colophon{{margin-top:56px;padding-top:12px;border-top:1px solid var(--rule);
  font-family:var(--mono);font-size:10.5px;line-height:1.7;color:var(--ink-faint);letter-spacing:.02em}}

@media (prefers-color-scheme: dark){{
  :root{{
    --paper:#171810; --card:#1e2016; --panel:#24261b; --ink:#e9e4d3; --ink-soft:#bec0ae; --ink-faint:#96988a;
    --rule:#3a3c2e; --rule-strong:#e9e4d3; --link:#9bbccb; --pass:#8ab596; --warn:#c9a35e; --mark:#dc8b7b;
    --ghost:#33352a; --live-tint:#372820; --mast:#0e0f09;
  }}
  body{{background-image:none}}
  .lede{{color:#b7b9a6}}
  .nostamp{{color:#9a9c8a;border-left-color:rgba(233,228,211,.2)}}
  .nostamp b{{color:#e9e4d3}}
  .run-card::after{{color:#2b2d23}}
  ::selection{{background:#9bbccb;color:#171810}}
}}

@media (max-width:700px){{
  .mast-grid{{grid-template-columns:1fr}}
  .nostamp{{text-align:left;border-left:0;padding-left:0;margin-top:14px;white-space:normal}}
  .stg{{grid-template-columns:40px 1fr}}
  .stg-meta{{grid-column:2;text-align:left;padding-top:2px}}
  nav a{{margin-left:12px;font-size:13px}}
  .run-card::after{{font-size:32px;top:8px}}
  .run-top{{padding-right:56px}}
}}
@media (prefers-reduced-motion: reduce){{
  *{{transition:none!important;animation:none!important}}
  .brand .cursor, .mast h1 .cursor{{animation:none;visibility:hidden}}
  .stg.live .stg-title .tick::before, .f-tick.live{{animation:none}}
}}
</style></head><body>
<nav class="nav"><span class="brand">research_foodie<span class="zh">本地科研综述工作台</span><span class="cursor" aria-hidden="true"></span></span>
<span><a class="{cur_workbench}" href="/">{ui_nav_workbench}</a><a class="{cur_dash}" href="/dashboard">{ui_nav_dash}</a><a class="{cur_ms}" href="/manuscripts">{ui_nav_ms}</a><a class="{cur_fb}" href="/feedback">{ui_nav_fb}</a></span>
<span class="lang-nav"><a class="{cur_lang_zh}" href="/_lang/zh">中文</a><a class="{cur_lang_en}" href="/_lang/en">EN</a></span></nav>
<div class="frame">
"""

HTML_TAIL = ('<footer class="colophon">research_foodie · local-first survey pipeline · '
             'pandoc + xelatex (YaHei) · zero external network on the page · '
             'binds 127.0.0.1 · citations are the lifeline</footer>'
             '</div></body></html>')

UI = {
    "en": {
        "nav_workbench": "Workbench", "nav_dash": "Numbers", "nav_ms": "Manuscripts", "nav_fb": "Feedback",
        "mast_meta": "research_foodie · local-first survey pipeline · citations are the lifeline",
        "mast_title": "Survey workbench",
        "lede": ("Ask a question and get a survey where every sentence is traceable. Each step is "
                 "narrated as it happens — what stage the research is at, how it is done, and why. "
                 "Every survey ships in two tiers: the dry-goods manuscript (default) and an "
                 "arXiv-style preprint."),
        "probe_head": "Start a survey", "probe_head_en": "ask a research question",
        "lane": "Model lane",
        "q_label": "Research question", "q_hint": "what this survey should answer",
        "q_ph": "e.g. GPT detectors bias against non-native English writers",
        "mock_label": "Mock demo", "mock_note": "offline · deterministic · ~1 s · repeatable · not a live result",
        "real_label": "Real run", "real_note": "live free model lane · ~5–8 min · temperature > 0",
        "run_btn": "Run survey", "run_busy": "[ running… ]", "cancel_btn": "Cancel run",
        "resume_hint": ("An interrupted run can be RESUMED from its card — the CLI keeps a per-step "
                        "ledger, so a restart continues from the last finished step."),
        "mission_head": "Live mission", "mission_head_en": "what / how / why as it runs",
        "raw_head": "Raw log", "raw_head_en": "engineering detail, under the narration",
        "no_mission": ("Nothing in flight yet. Ask a question above — progress is narrated stage by "
                       "stage, in research terms."),
        "runs_head": "Recent runs", "runs_head_en": "↘ resume continues an interrupted run",
        "no_runs": "No runs yet this session.",
        "done": "done", "running": "running", "pending": "pending",
        "failed": "failed", "cancelled": "cancelled", "interrupted": "interrupted",
        "l6_pass": "L6 pass", "l6_fail": "L6 fail",
        "judge": "judge", "claims": "claims", "papers": "papers cited", "seconds": "s",
        "stages": "research stages",
        "research_view": "research view",
        "link_manuscript": "manuscript", "link_pdf": "pdf · dry goods", "link_preprint": "preprint · arXiv",
        "link_log": "log", "link_resume": "Resume",
        "started": "submitted — narrating in the mission panel below…",
        "mission_question": "Question:",
        "mission_title": "Research view",
        "mission_not_survey": ("This run is not a survey-pipeline run, so it has no research-workflow "
                               "narration. See the log or the runs page instead."),
        "mission_desc": ("How a survey answer is produced — one stage at a time. Business framing "
                         "(检索文献…) plus each stage's key technical point."),
        "dash_title": "Dashboard",
        "dash_var": "Judge variance (Session 19 baseline)",
        "dash_var_h": ("topic", "rounds", "mean total", "sd"),
        "dash_pools": "30-topic evidence pools",
        "dash_pools_h": ("total", "full (≥3 papers)", "partial", "empty"),
        "dash_ms": "Manuscripts (L6 human review surface)",
        "dash_bench": "Bench report (raw markdown, bench_pilot_das.md)",
        "ms_title": "Manuscripts", "ms_h": ("file", "size", ""),
        "ms_open": "open", "ms_none": "no rendered manuscripts yet — run a survey or a bench scenario first",
        "ms_note": "Rendered from the manuscript source by pandoc + xelatex + YaHei (干货稿) and its arXiv-style preprint variant.",
        "fb_title": "Feedback",
        "log_title": "log",
    },
    "zh": {
        "nav_workbench": "工作台", "nav_dash": "数据", "nav_ms": "手稿", "nav_fb": "反馈",
        "mast_meta": "research_foodie · 本地优先调研管线 · 引用即生命线",
        "mast_title": "调研工作台",
        "lede": ("输入一个问题，得到一份逐句可溯源的综述。每一步研究都在这里直播——做到哪个阶段、"
                 "怎么做、为什么这么做。每次调研都双档交付：干货稿（缺省）与 arXiv 出版化稿。"),
        "probe_head": "投题", "probe_head_en": "输入一个研究问题",
        "lane": "模型通道",
        "q_label": "研究问题", "q_hint": "这份综述要回答的问题",
        "q_ph": "例如：GPT detectors 是否对非母语作者有偏倚",
        "mock_label": "模拟演示", "mock_note": "离线 · 确定性 · ~1 秒 · 可复现 · 非真实结果",
        "real_label": "真实运行", "real_note": "实时免费模型通道 · 约 5–8 分钟 · 有涨落",
        "run_btn": "开始调研", "run_busy": "[ 运行中… ]", "cancel_btn": "取消运行",
        "resume_hint": ("中断的 run 可在卡片上续跑 —— CLI 保留分步台账，重启后从最后已完成的一步继续，"
                        "不重复计费。"),
        "mission_head": "研究进行时", "mission_head_en": "做到哪 / 怎么做 / 为什么",
        "raw_head": "技术日志", "raw_head_en": "工程细节 · 在叙事层之下",
        "no_mission": "还没有研究在跑。在上方投一个题——进度会按研究术语逐阶段讲述。",
        "runs_head": "历次运行", "runs_head_en": "↘ 断点续跑",
        "no_runs": "本次会话还没有运行记录。",
        "done": "完成", "running": "进行中", "pending": "待开始",
        "failed": "已失败", "cancelled": "已取消", "interrupted": "已中断",
        "l6_pass": "门禁通过", "l6_fail": "门禁未过",
        "judge": "判题", "claims": "条声明", "papers": "篇被引", "seconds": "秒",
        "stages": "个研究阶段",
        "research_view": "研究视图",
        "link_manuscript": "干货稿", "link_pdf": "干货 PDF", "link_preprint": "出版化 PDF (arXiv)",
        "link_log": "日志", "link_resume": "续跑",
        "started": "已提交——正在下方「研究进行时」逐阶段讲述…",
        "mission_question": "研究问题：",
        "mission_title": "研究视图",
        "mission_not_survey": ("这不是调研管线 run，没有研究流程叙事。请查看日志或回到工作台。"),
        "mission_desc": "一份综述答案是怎样产生的——逐阶段展开：业务语言（检索文献…）+ 每阶段的关键技术点。",
        "dash_title": "数据总览",
        "dash_var": "判题方差基线（Session 19）",
        "dash_var_h": ("主题", "轮次", "均值总分", "标准差"),
        "dash_pools": "30 主题证据池",
        "dash_pools_h": ("总计", "足量（≥3 篇）", "部分", "空池"),
        "dash_ms": "手稿（L6 人工审读面）",
        "dash_bench": "基准报告（bench_pilot_das.md 原文）",
        "ms_title": "手稿", "ms_h": ("文件", "大小", ""),
        "ms_open": "打开", "ms_none": "还没有已渲染手稿——先跑一次调研或基准场景",
        "ms_note": "从同一份手稿源码渲染：pandoc + xelatex + YaHei（干货稿）与其 arXiv 出版化变体。",
        "fb_title": "反馈",
        "log_title": "日志",
    },
}


def T(lang: str, key: str) -> str:
    return UI.get(lang, UI["en"]).get(key, key)


def lang_of(request: Request) -> str:
    return request.cookies.get("rf_lang", "en") if request.cookies.get("rf_lang") in ("en", "zh") else "en"


def page(title, body: str, cur: str = "wb", lang: str = "en") -> HTMLResponse:
    kw = dict(
        cur_workbench="cur" if cur == "wb" else "",
        cur_dash="cur" if cur == "dash" else "",
        cur_ms="cur" if cur == "ms" else "",
        cur_fb="cur" if cur == "fb" else "",
        cur_lang_zh="cur" if lang == "zh" else "",
        cur_lang_en="cur" if lang == "en" else "",
        html_lang="zh-CN" if lang == "zh" else "en",
        ui_nav_workbench=T(lang, "nav_workbench"),
        ui_nav_dash=T(lang, "nav_dash"),
        ui_nav_ms=T(lang, "nav_ms"),
        ui_nav_fb=T(lang, "nav_fb"),
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
     "key": "backend · candidates", "icon": "search", "est": "≈2–15 s"},
    {"id": "evidence", "label": "Build evidence pool", "zh": "解析证据",
     "what": "Turn selected PDFs into searchable, quotable text",
     "how": "MinerU windowed parse (≤6 pages) + resolved_evidence() pool",
     "why": "Only retrievable full text can back verbatim grounding later",
     "key": "pool_size papers", "icon": "archive", "est": "≈5–30 s"},
    {"id": "synthesize", "label": "Synthesise literature", "zh": "文献综合",
     "what": "Distil each paper into the claims and facts it can actually support",
     "how": "S_lit node — per-paper extraction, tagged with its paper_id",
     "why": "Drafting builds on verified content instead of memory",
     "key": "model lane · paper_id tags", "icon": "book", "est": "≈30–90 s"},
    {"id": "outline", "label": "Plan the article", "zh": "制定大纲",
     "what": "Break the question into a section structure and argument flow",
     "how": "S_org node — STORM-style multi-perspective outline on LangGraph",
     "why": "Outline decides coverage before a single sentence is written",
     "key": "reader perspectives · sections", "icon": "list", "est": "≈30–120 s"},
    {"id": "write", "label": "Write grounded sections", "zh": "接地写作",
     "what": "Write each section so every claim is bound to its verbatim source",
     "how": "S_write + review — BM25 source windows + 5-gram verbatim filter",
     "why": "Kills hallucination at write time; un-grounded claims are dropped",
     "key": "claims · BM25 windows · 5-gram", "icon": "pencil", "est": "≈1–3 min"},
    {"id": "finalize", "label": "Assemble manuscript", "zh": "装配成稿",
     "what": "Merge abstract, evidence table, references, and audit annex",
     "how": "_finalize node — deterministic assembly of the artifact",
     "why": "Produces a single reviewable deliverable with provenance",
     "key": "chars · evidence table · annex", "icon": "layers", "est": "<1 s"},
    {"id": "gate", "label": "Deterministic gate", "zh": "机械门禁",
     "what": "Zero-LLM quality checks: structure, citation form, grounding, bilingual",
     "how": "validate.py L6 — deterministic rules, no model call",
     "why": "A hard floor that never relies on the model's self-report",
     "key": "L6 · 5-gram overlap · arXiv/DOI form", "icon": "shield", "est": "<1 s"},
    {"id": "judge", "label": "Academic judgement", "zh": "AI 判题",
     "what": "Score the manuscript against a scholarly rubric",
     "how": "P3 judge — DAS-Bench 16-axis rubric (BSC·MAR·TSQ·HDQ)",
     "why": "Aligns with an external evaluation protocol, not just internal rules",
     "key": "label · checks", "icon": "scale", "est": "≈1–3 min"},
    {"id": "deliver", "label": "Render deliverables", "zh": "渲染交付",
     "what": "Render the manuscript to PDF for human review",
     "how": "render_manuscript — pandoc + xelatex + YaHei",
     "why": "Human L6 review happens on a rendered artifact",
     "key": "pages · pdf link", "icon": "doc", "est": "≈5–60 s"},
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


def _mission_html(stages: List[dict], summary: Optional[dict], lang: str = "en") -> str:
    """Render the research-workflow narration block (business + tech)."""
    if not stages:
        return '<p class="muted">No survey mission info recorded for this run.</p>'
    done = sum(1 for s in stages if s["status"] == "done")
    pct = int(100 * done / len(stages)) if stages else 0
    rows = []
    for i, s in enumerate(stages, 1):
        meta = next(m for m in SURVEY_STAGES if m["id"] == s["id"])
        label = meta["label"] if lang == "en" else meta["zh"]
        status = s["status"] if s["status"] in ("done", "running", "pending") else "pending"
        mark = {"done": "✓", "running": "●", "pending": "○"}[status]
        dur = f" · {s['dur_s']:.1f}s" if s.get("dur_s") else ""
        tick = {("done"): T(lang, "done") + dur,
                "running": T(lang, "running"),
                "pending": T(lang, "pending")}[status]
        est = meta.get("est")
        if status == "running" and est:
            tick += f" · {est}"
        meta_text = {"done": (f"{s['dur_s']:.1f}{T(lang, 'seconds')}" if s.get("dur_s") else T(lang, "done")),
                     "running": (est or T(lang, "running")),
                     "pending": (est or "—")}[status]
        tech = " · ".join(f"{k}={v}" for k, v in (s.get("tech") or {}).items())
        note = ('<div class="stg-note">' + meta["how"] + '</div>'
                + (f'<div class="stg-tech">{tech}</div>' if tech else ""))
        rows.append(
            f'<article class="stg {status}">'
            f'<div class="stg-no">{i:02d}</div><div>'
            f'<div class="stg-title">{label}'
            f'<span class="zh">{meta["label"] if lang != "en" else meta["zh"]}</span>'
            f'<span class="tick">{mark} {tick}</span></div>'
            f'<p class="stg-what">{meta["what"]}</p>'
            f'<p class="stg-why">{meta["why"]}</p>'
            f'{note}'
            f'</div><div class="stg-meta">{meta_text}</div></article>')
    summary_html = ""
    if summary:
        links = " ".join(
            f'<a href="/manuscripts/{Path(x).name}">{label}</a>'
            for label, x in ((T(lang, "link_manuscript"), summary.get("manuscript")),
                             (T(lang, "link_pdf"), summary.get("pdf")),
                             (T(lang, "link_preprint"), summary.get("pdf_pub")))
            if x)
        verdict = T(lang, "l6_pass") if summary.get("gate_passed") else T(lang, "l6_fail")
        summary_html = (f'<div class="run-card">'
                        f'<span class="badge {"ok" if summary.get("gate_passed") else "fail"}">'
                        f'{verdict}</span> '
                        f'<span class="res">{T(lang, "judge")}={summary.get("judge_label")} · '
                        f'{summary.get("claims", 0)} {T(lang, "claims")} · '
                        f'{summary.get("n_papers_cited", 0)} {T(lang, "papers")} · '
                        f'{summary.get("elapsed_s", 0)}{T(lang, "seconds")}</span> '
                        f'{links}</div>')
    folio = "".join(
        '<span class="f-tick %s"></span>' % ("done" if s["status"] == "done"
                                             else ("live" if s["status"] == "running" else ""))
        for s in stages)
    return (f'<div class="folio">{folio}'
            f'<span class="f-label">{done:02d}/{len(stages)} · {pct}%</span></div>'
            f'<div class="muted" style="font-size:12px">{done}/{len(stages)} '
            f'{T(lang, "stages")}</div>'
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


def _run_card(run, lang: str = "en") -> str:
    """HTML card for one run (list page)."""
    from tools.eval.run_ledger import ResumeLedger
    status_badge = {
        "done": 'ok', "running": 'run', "pending": 'run',
        "failed": 'fail', "cancelled": 'cancel', "interrupted": 'cancel',
    }.get(run.status, 'muted')
    status_label = T(lang, run.status)
    logf = f'<a class="muted" href="/runs/{run.id}/log" target="_blank">{T(lang, "link_log")}</a>'
    greeting = ''
    survey = _survey_summary(run)
    mission_link = ''
    if survey or any(ln.startswith("[survey-stage]") for ln in run.lines):
        mission_link = (f'<a class="muted" href="/runs/{run.id}/mission" target="_blank">'
                        f'{T(lang, "research_view")}</a> ')
    if survey:
        mode = survey.get("mode", "real")
        badge_cls = "ok" if survey.get("gate_passed") else "fail"
        mode_badge = (f'<span class="badge {"muted" if mode == "mock" else "run"}">'
                      f'{"MOCK demo" if mode == "mock" else "REAL run"}</span>')
        links = []
        if survey.get("manuscript"):
            links.append(f'<a href="/manuscripts/{Path(survey["manuscript"]).name}">'
                         f'{T(lang, "link_manuscript")}</a>')
        if survey.get("pdf"):
            links.append(f'<a href="/manuscripts/{Path(survey["pdf"]).name}">'
                         f'{T(lang, "link_pdf")}</a>')
        if survey.get("pdf_pub"):
            links.append(f'<a href="/manuscripts/{Path(survey["pdf_pub"]).name}">'
                         f'{T(lang, "link_preprint")}</a>')
        links_html = " · ".join(links) if links else ""
        verdict = T(lang, "l6_pass") if survey.get("gate_passed") else T(lang, "l6_fail")
        greeting = (f'<div class="q">{survey.get("question", "")}</div>'
                    f'<div class="res">{mode_badge} '
                    f'<span class="badge {badge_cls}">{verdict}</span> '
                    f'{T(lang, "judge")}={survey.get("judge_label")} · '
                    f'{survey.get("claims", 0)} {T(lang, "claims")} · '
                    f'{survey.get("n_papers_cited", 0)} {T(lang, "papers")} · '
                    f'{survey.get("elapsed_s", 0)}{T(lang, "seconds")}'
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
                progress = (f'<span class="muted">ledger </span>'
                            f'<span class="badge run">{nd} done</span>')
            break
    resume = ""
    if run.status in ("failed", "cancelled", "interrupted"):
        resume = (f'<button class="btn mini" onclick="resumeRun(\'{run.id}\')">'
                  f'{T(lang, "link_resume")}</button> ')
    return (f'<div class="run-card" data-id="{run.id}"><div class="run-top">'
            f'<strong>{run.title}</strong> '
            f'<span class="badge {status_badge}">{status_label}</span> '
            f'<span class="id mono">{run.id}</span> {logf} {mission_link}{progress}</div>'
            f'<div class="mono muted" style="font-size:11.5px;margin-top:6px">{run.elapsed:.0f}s · '
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

@app.get("/_lang/{lang}", response_class=Response)
def set_lang(lang: str, request: Request):
    """Switch UI language: set a long-lived cookie and return to the referring page."""
    if lang not in ("en", "zh"):
        return JSONResponse({"error": "lang must be en|zh"}, status_code=400)
    back = request.headers.get("referer") or "/"
    resp = RedirectResponse(back)
    resp.set_cookie("rf_lang", lang, max_age=31536000, httponly=False, samesite="lax")
    return resp


@app.get("/", response_class=HTMLResponse)
def runs_page(request: Request) -> HTMLResponse:
    lang = lang_of(request)
    menu = _scenario_menu()
    rows = manager.list()
    cards = "".join(_run_card(r, lang) for r in rows[:12]) or \
        f'<p class="muted">{T(lang, "no_runs")}</p>'
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
                                     _survey_summary(last_survey), lang)
    body = f"""
<header class="mast">
  <div class="mast-grid">
    <div>
      <div class="mast-meta">{T(lang, "mast_meta")}</div>
      <h1>{T(lang, "mast_title")}<span class="cursor" aria-hidden="true"></span></h1>
      <p class="lede">{T(lang, "lede")}</p>
    </div>
    <div class="nostamp">edition 2026.09<br>
      lane <b>{_env_profile()['LLM_BACKEND']}</b> / rack <b>{_env_profile()['OPENCODE_MODEL']}</b><br>
      <span class="live-dot">●</span> commit a question &#8594; the flipbook prints here</div>
  </div>
</header>

<section class="sect">
  <div class="sect-head"><h2><span class="idx">I.</span>{T(lang, "probe_head")} <span class="en">{T(lang, "probe_head_en")}</span></h2>
    <div class="side">{T(lang, "lane")} · {_env_profile()['LLM_BACKEND']} / {_env_profile()['OPENCODE_MODEL']}</div></div>
  <div class="probe">
    <form onsubmit="return false">
      <label class="fl" for="q">{T(lang, "q_label")} <span class="muted">· {T(lang, "q_hint")}</span></label>
      <input id="q" class="qfield" type="text" autocomplete="off"
             placeholder="{T(lang, "q_ph")}"
             list="q-examples">
      <datalist id="q-examples">
        <option value="GPT detectors bias against non-native English writers">
        <option value="RAG evaluation needs human judgement">
      </datalist>
      <div class="probe-row">
        <div class="seg">
          <label><input type="radio" name="mode" value="mock" checked>
            <span><b>{T(lang, "mock_label")}</b><small>{T(lang, "mock_note")}</small></span></label>
          <label><input type="radio" name="mode" value="real">
            <span><b>{T(lang, "real_label")}</b><small>{T(lang, "real_note")}</small></span></label>
        </div>
        <button class="btn primary" id="runbtn" onclick="startQuestion()">{T(lang, "run_btn")}</button>
        <span class="muted" id="q-msg"></span>
      </div>
      <p class="hint">{T(lang, "resume_hint")}</p>
    </form>
  </div>
  <div style="margin-top:12px" class="chips">{menu_html}</div>
</section>

<section class="sect">
  <div class="sect-head"><h2><span class="idx">II.</span>{T(lang, "mission_head")} <span class="en">{T(lang, "mission_head_en")}</span></h2>
    <div class="side"><span id="active-msg" class="muted"></span>
    <button class="btn danger mini" onclick="cancelRun()">{T(lang, "cancel_btn")}</button></div></div>
  <div id="mission">{mission_init or f'<p class="mission-empty">{T(lang, "no_mission")}</p>'}</div>
  <details class="rawtail"><summary>{T(lang, "raw_head")} · <span class="muted">{T(lang, "raw_head_en")}</span></summary>
  <div id="tail"></div></details>
</section>

<section class="sect">
  <div class="sect-head"><h2><span class="idx">III.</span>{T(lang, "runs_head")} <span class="en">{T(lang, "runs_head_en")}</span></h2></div>
  <div id="runs" class="runs">{cards}</div>
</section>
<script>
const LANG = {json.dumps(lang)};
const UI = {json.dumps(UI[lang])};
const menus = {json.dumps({m["id"]: m["args"] for m in menu})};
let currentRun = null, currentStart = 0, es = null;
const stagesMeta = {json.dumps({s["id"]: {"label": s["label"], "zh": s["zh"],
  "why": s["why"], "how": s["how"], "what": s["what"], "key": s["key"], "est": s.get("est", "")} for s in SURVEY_STAGES})};
const stagePlan = {{}};   // id -> {{status, dur_s, tech, stageStart}}
const isZh = LANG === 'zh';
const stageLabel = (m) => isZh ? m.zh : m.label;
const stageAlt = (m) => isZh ? m.label : m.zh;
function renderMission(){{
  const el = document.getElementById('mission');
  const ids = Object.keys(stagesMeta);
  const doneN = ids.filter(i => stagePlan[i] && stagePlan[i].status === 'done').length;
  const pct = ids.length ? Math.round(100 * doneN / ids.length) : 0;
  let rows = '';
  ids.forEach((id, k) => {{
    const m = stagesMeta[id]; const p = stagePlan[id] || {{status:'pending', tech:{{}}, dur_s:0}};
    const st = ['done','running','pending'].includes(p.status) ? p.status : 'pending';
    const mark = {{done:'✓', running:'●', pending:'○'}}[st];
    let tickText = {{done: UI.done, running: UI.running, pending: UI.pending}}[st];
    let metaText = st === 'done' ? (p.dur_s ? p.dur_s.toFixed(1) + UI.seconds : UI.done)
      : st === 'running' ? (p.stageStart ? Math.round((Date.now()-p.stageStart)/1000) + UI.seconds : UI.running)
      : (m.est || '—');
    const tech = Object.entries(p.tech||{{}}).map(([a,b])=>a+'='+b).join(' · ');
    const no = String(k+1).padStart(2, '0');
    rows += `<article class="stg ${{st}} ${{st==='done' ? 'done' : (st==='running' ? 'live' : 'off')}}">
      <div class="stg-no">${{no}}</div><div>
      <div class="stg-title">${{stageLabel(m)}}<span class="zh">${{stageAlt(m)}}</span>
        <span class="tick">${{mark}} ${{tickText}}</span></div>
      <p class="stg-what">${{m.what}}</p>
      <p class="stg-why">${{m.why}}</p>
      <div class="stg-note">${{m.how}}</div>${{tech ? '<div class="stg-tech">'+tech+'</div>' : ''}}
      </div><div class="stg-meta">${{metaText}}</div></article>`;
  }});
  const folio = ids.map(i => {{
    const p = stagePlan[i] || {{}};
    const cls = p.status === 'done' ? 'done' : (p.status === 'running' ? 'live' : '');
    return `<span class="f-tick ${{cls}}"></span>`;
  }}).join('');
  el.innerHTML = `<div class="folio">${{folio}}<span class="f-label">${{String(doneN).padStart(2,'0')}}/${{ids.length}} · ${{pct}}%</span></div>
    <div class="muted" style="font-size:12px">${{UI.stages}}
      ${{currentRun ? ' · <a href="/runs/'+currentRun+'/mission">'+UI.research_view+'</a>' : ''}}</div>`
    + rows;
}}
function handleLine(line){{
  const st = line.match(/^\\[survey-stage\\] (.*)$/);
  if (st){{
    try {{
      const ev = JSON.parse(st[1]);
      const p = stagePlan[ev.id] = stagePlan[ev.id] || {{status:'pending', dur_s:0, tech:{{}}, stageStart:0}};
      if (ev.status === 'start'){{ p.status = 'running'; p.stageStart = Date.now(); }}
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
      const btn = document.getElementById('runbtn');
      if (btn){{ btn.disabled = false; btn.textContent = UI.run_btn; }}
      if (payload.status === 'done'){{ document.getElementById('q-msg').textContent = UI.link_pdf + ' …'; }}
      else {{ document.getElementById('q-msg').textContent = payload.status + ' rc=' + payload.rc; }}
      location.reload(); }}
  }};
}} 
async function startRun(id){{
  const args = menus[id];
  const btn = document.getElementById('runbtn');
  if (btn){{ btn.disabled = true; btn.textContent = UI.run_busy; }}
  const resp = await fetch('/runs', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{title:id, args}})}});
  const data = await resp.json();
  if (data.error){{ alert(data.error); if (btn){{ btn.disabled = false; btn.textContent = UI.run_btn; }} return; }}
  attachSSE(data.id);
}}
async function startQuestion(){{
  const question = document.getElementById('q').value.trim();
  const mode = document.querySelector('input[name="mode"]:checked').value;
  let msg = document.getElementById('q-msg');
  const btn = document.getElementById('runbtn');
  if (!question){{ msg.textContent = isZh ? '请先输入一个研究问题' : 'type a research question first'; document.getElementById('q').focus(); return; }}
  const args = ['-m', 'tools.pipeline.run_survey', '--question', question];
  if (mode === 'mock') args.push('--mock');
  if (btn){{ btn.disabled = true; btn.textContent = UI.run_busy; }}
  msg.textContent = UI.started;
  const resp = await fetch('/runs', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{title: 'survey (' + mode + ')', args}})}});
  const data = await resp.json();
  if (data.error){{ msg.textContent = data.error; if (btn) btn.disabled = false; return; }}
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
setInterval(() => {{
  if (currentRun){{
    fetch(`/runs/${{currentRun}}/status`).then(r=>r.json()).then(d=>{{
      let s = isZh ? ({{done:'完成', running:'进行中', failed:'失败', cancelled:'已取消'}}[d.status]||d.status) : d.status;
      document.getElementById('active-msg').textContent =
        currentRun + ' · ' + s + ' · ' + d.elapsed.toFixed(0) + UI.seconds;
      if (Object.values(stagePlan).some(p => p.status==='running')) renderMission();
    }});
  }}
}}, 1500);
</script>
"""
    return page(T(lang, "probe_head"), body, cur="wb", lang=lang)


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
def run_log(run_id: str, request: Request):
    lang = lang_of(request)
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    text = ""
    if run.log_path.is_file():
        text = run.log_path.read_text(encoding="utf-8", errors="replace")[-60000:]
    cls = {"done": 'ok', "running": 'run', "failed": 'fail',
           "cancelled": 'cancel', "interrupted": 'cancel'}.get(run.status, 'muted')
    return page(f"{T(lang, 'log_title')} {run_id}",
                f"<h1>{T(lang, 'log_title')} · {run_id} · "
                f"<span class='badge {cls}'>{T(lang, run.status)}</span></h1>"
                f"<pre>{text}</pre>", lang=lang)


@app.get("/runs/{run_id}/mission", response_class=HTMLResponse)
def run_mission(run_id: str, request: Request):
    """Read-only 'research view' of a survey run: what stage, how, why —
    business language with the key technical points, plus the result links.
    This is the application-scenario answer to 'what is the tool doing'."""
    lang = lang_of(request)
    run = manager.get(run_id)
    if not run:
        return JSONResponse({"error": "not found"}, status_code=404)
    stages = _parse_survey_stages(run.lines)
    summary = _survey_summary(run)
    if not stages and not summary:
        return page(f"{T(lang, 'mission_title')} {run_id}",
                    f"<h1>{T(lang, 'mission_title')} · {run_id}</h1>"
                    f"<p class=\"muted\">{T(lang, 'mission_not_survey')}</p>", lang=lang)
    q = (summary or {}).get("question", "")
    head = f"<h1>{T(lang, 'mission_title')} · {run_id}</h1>"
    if q:
        head += f"<p><strong>{T(lang, 'mission_question')}</strong> <em>{q}</em></p>"
    head += f"<p class=\"muted\">{T(lang, 'mission_desc')}</p>"
    return page(f"{T(lang, 'mission_title')} {run_id}",
                head + _mission_html(stages, summary, lang), lang=lang)


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
def dashboard(request: Request):
    lang = lang_of(request)
    var = _variance_summary()
    pools = _pools_summary()
    bench_report = EVAL_OUT / "bench_pilot_das.md"
    report_text = bench_report.read_text(encoding="utf-8") if bench_report.is_file() else "no report yet"

    vh = T(lang, "dash_var_h")
    ph = T(lang, "dash_pools_h")
    var_rows = "".join(
        f'<tr><td>{t["topic_id"]}</td><td>{t["n"]}</td><td>{t["mean"]:.2f}</td>'
        f'<td>{t["sd"]:.2f}</td></tr>' for t in var) or \
        f'<tr><td colspan=4 class=muted>—</td></tr>'
    pools_row = (f'<tr><td>{pools["total"]}</td><td>{pools["full"]}</td>'
                 f'<td>{pools["partial"]}</td><td>{pools["empty"]}</td></tr>')
    body = f"""
<h1>{T(lang, "dash_title")}</h1>
<h2>{T(lang, "dash_var")}</h2>
<table><tr><th>{vh[0]}</th><th>{vh[1]}</th><th>{vh[2]}</th><th>{vh[3]}</th></tr>{var_rows}</table>
<h2>{T(lang, "dash_pools")}</h2>
<table><tr><th>{ph[0]}</th><th>{ph[1]}</th><th>{ph[2]}</th><th>{ph[3]}</th></tr>{pools_row}</table>
<h2>{T(lang, "dash_ms")}</h2>
<div>{", ".join(f'<a href="/manuscripts/{p.name}">{p.name}</a>' for p in _manuscript_list()) or "—"}</div>
<h2>{T(lang, "dash_bench")}</h2>
<pre>{report_text[:4000]}</pre>
"""
    return page(T(lang, "dash_title"), body, cur="dash", lang=lang)


@app.get("/manuscripts", response_class=HTMLResponse)
def manuscripts_page(request: Request):
    lang = lang_of(request)
    items = _manuscript_list()
    mh = T(lang, "ms_h")
    rows = "".join(
        f'<tr><td>{p.name}</td><td>{p.stat().st_size:,} B</td>'
        f'<td><a href="/manuscripts/{p.name}">{T(lang, "ms_open")} pdf</a></td></tr>' for p in items) \
        or f'<tr><td colspan=3 class=muted>{T(lang, "ms_none")}</td></tr>'
    body = (f"<h1>{T(lang, 'ms_title')}</h1><table><tr><th>{mh[0]}</th><th>{mh[1]}</th><th>{mh[2]}</th>"
            f"</tr>{rows}</table>"
            f"<p class=muted>{T(lang, 'ms_note')}</p>")
    return page(T(lang, "ms_title"), body, cur="ms", lang=lang)


@app.get("/manuscripts/{name}")
def manuscript_file(name: str):
    for d in (MANUSCRIPTS, MOCK_MANUSCRIPTS):
        path = d / name
        if path.is_file():
            media = "application/pdf" if path.suffix.lower() == ".pdf" else "text/markdown"
            return FileResponse(path, media_type=media, filename=name)
    return JSONResponse({"error": "not found"}, status_code=404)


@app.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    lang = lang_of(request)
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
<h1>{T(lang, "fb_title")} → JSONL (self-evolution E-5 ingestion)</h1>
<form method="post"><textarea name="row" rows="4" style="width:100%"
placeholder='{{"feed": "judge too lenient on BSC", "topic": "P-A", "date": "2026-09-20"}}'></textarea>
<button class="btn" type="submit">append row</button></form>
<h2>Last 50 rows</h2><table>{rows_html or '<tr><td class=muted>—</td></tr>'}</table>
"""
    return page(f"{T(lang, 'fb_title')}", body, cur="fb", lang=lang)


@app.post("/feedback")
def feedback_append(request: Request, row: str = Form(...)):
    lang = lang_of(request)
    fb = EVAL_OUT / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    with (fb / "feedback.jsonl").open("a", encoding="utf-8") as f:
        f.write(row + "\n")
    body = ("<p>appended ✓ <a href='/feedback'>back</a> — feedback does not auto-tune anything; "
            "it feeds the E-5 corpus reviewed in the weekly cadence.</p>")
    return page("Feedback (appended)", body, cur="fb", lang=lang)