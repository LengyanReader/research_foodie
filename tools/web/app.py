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

from markdown_it import MarkdownIt

from .run_manager import manager, REPO_ROOT
from . import knowledge

WEB_DIR = Path(__file__).resolve().parent
EVAL_OUT = REPO_ROOT / "_eval_out"
MANUSCRIPTS = EVAL_OUT / "manuscripts"
MOCK_MANUSCRIPTS = EVAL_OUT / "mock_manuscripts"

app = FastAPI(title="research_foodie — local observation dashboard", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")

# Offline markdown→HTML for the in-page reader (html=False → no raw-HTML passthrough)
_md = MarkdownIt("js-default", {"html": False})

# ---------------------------------------------------------------------------
# Templates (no external JS; inline CSS — zero network deps, K1/K2-safe)
# ---------------------------------------------------------------------------

HTML_HEAD = """<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">
<title>research_foodie · {title}</title>
<style>
/* ------------------------------------------------------------------
   II    design tokens — a calm, human-first surface. Humanist sans,
   soft warm paper, rounded cards, one serene blue-green accent.
   The only mono surface is the raw-log drawer.
   ------------------------------------------------------------------ */
:root{{
  --paper:#f6f5f0; --surface:#ffffff; --surface-soft:#f0efea; --surface-soft2:#f7f6f2;
  --ink:#2f3238; --ink-soft:#5b5f66; --ink-faint:#98999f;
  --rule:#e7e5de; --rule-strong:#cfcbc2;
  --accent:#3a6b5f; --accent-strong:#2d554b; --accent-soft:#e8f0ec;
  --ok:#3f7a55; --ok-soft:#eaf1eb; --live:#b0703c; --live-soft:#f7ede2;
  --danger:#b4544c; --danger-soft:#f7ebea; --warn:#a57b1c;
  --sh-sm:0 1px 2px rgba(47,50,55,.05); --sh:0 1px 3px rgba(47,50,55,.06),0 10px 28px rgba(47,50,55,.08);
  --r-lg:16px; --r:12px; --r-sm:9px;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',system-ui,sans-serif;
  --mono:Consolas,'Cascadia Mono',ui-monospace,monospace;
}}
*{{box-sizing:border-box}}
html{{scrollbar-gutter:stable}}
::selection{{background:var(--accent);color:#fff}}
body{{margin:0;color:var(--ink);background:var(--paper);font:15px/1.7 var(--font);
  -webkit-font-smoothing:antialiased}}
.frame{{max-width:1000px;margin:0 auto;padding:0 clamp(16px,4vw,40px)}}
h1,h2,h3{{font-family:var(--font);line-height:1.25;font-weight:700;letter-spacing:-.01em}}
h1{{font-size:clamp(24px,3.4vw,32px);margin:0 0 .2em}}
h2{{font-size:17px;margin:0}}
h2 .en{{font-size:12.5px;color:var(--ink-faint);font-weight:400;margin-left:8px}}
a{{color:var(--accent-strong);text-decoration:none}}
a:hover{{text-decoration:underline}}
code,pre{{font-family:var(--mono);font-size:12.5px}}
pre{{margin:0}}

/* ------------------------------------------------------------------
   III   surface — calm & humane. Warm paper, soft cards, humanist
   sans. Monospace is confined to the raw-log drawer only.
   ------------------------------------------------------------------ */

/* top bar */
.topbar{{background:var(--surface);border-bottom:1px solid var(--rule)}}
.topbar-row{{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:9px 0}}
.brand{{display:inline-flex;align-items:baseline;gap:9px;font-size:15.5px;font-weight:700;color:var(--ink);text-decoration:none}}
.brand:hover{{text-decoration:none}}
.brand-dot{{width:9px;height:9px;border-radius:50%;background:var(--accent);align-self:center}}
.brand-tag{{font-size:12px;font-weight:400;color:var(--ink-faint)}}
.navpills{{display:flex;gap:2px;flex:1;min-width:230px}}
.pill{{padding:6px 13px;border-radius:999px;font-size:13.5px;color:var(--ink-soft);white-space:nowrap}}
.pill:hover{{color:var(--accent-strong);background:var(--surface-soft);text-decoration:none}}
.pill.cur{{background:var(--surface-soft);color:var(--accent-strong);font-weight:600;box-shadow:inset 0 0 0 1px var(--rule)}}
.langseg{{display:inline-flex;gap:2px}}
.main{{padding:26px 0 8px}}

/* sections */
.sect{{margin:28px 0 0}}
.sect-head{{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 14px}}
.sect-head h2{{font-size:16.5px}}
.sect-head .side{{font-size:12.5px;color:var(--ink-faint)}}

/* hero */
.hero{{padding:6px 2px 2px}}
.hero h1{{margin:0 0 8px}}
.hero .lede{{color:var(--ink-soft);max-width:64ch;font-size:15.5px;margin:0 0 16px}}
.trust{{display:flex;flex-wrap:wrap;gap:8px}}
.trust span{{font-size:12.5px;color:var(--ink-soft);background:var(--surface-soft);border:1px solid var(--rule);border-radius:999px;padding:5px 13px}}

/* probe form */
.probe{{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r-lg);box-shadow:var(--sh);padding:20px 22px}}
.probe-head{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:12px}}
.probe-head h2{{font-size:16.5px}}
.probe-head .en{{font-size:12px;color:var(--ink-faint)}}
.probe label.fl{{display:block;font-size:13px;font-weight:600;margin-bottom:9px;color:var(--ink-soft)}}
.qfield{{width:100%;padding:13px 16px;font:16px/1.5 var(--font);color:var(--ink);
  border:1px solid var(--rule-strong);border-radius:var(--r);background:var(--surface);
  transition:border-color .15s ease, box-shadow .15s ease}}
.qfield::placeholder{{color:var(--ink-faint)}}
.qfield:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}}
.probe-row{{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:16px}}
.seg{{display:inline-flex;border:1px solid var(--rule);border-radius:999px;padding:3px;gap:2px}}
.seg label{{display:flex;align-items:center;gap:7px;margin:0;padding:7px 13px;border-radius:999px;font-size:13.5px;color:var(--ink-soft);cursor:pointer}}
.seg input{{position:absolute;opacity:0;pointer-events:none}}
.seg b{{font-weight:600}}
.seg small{{font-size:11px;color:var(--ink-faint)}}
.seg label:has(input:checked){{background:var(--surface-soft);box-shadow:inset 0 0 0 1px var(--rule);color:var(--ink);font-weight:600}}
.seg label:has(input:focus-visible){{outline:2px solid var(--accent);outline-offset:2px}}
.hint{{margin:13px 0 0;font-size:12.5px;color:var(--ink-faint)}}
.hint b{{color:var(--ink-soft)}}
.chips-label{{font-size:12px;color:var(--ink-faint);margin:0 2px 8px 0}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chips .btn{{min-height:30px;border-color:var(--rule);color:var(--ink-soft);font-size:12.5px;background:var(--surface)}}
.chips .btn:hover:not(:disabled){{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-strong)}}

/* buttons — soft, rounded, human */
.btn{{font:600 14px/1 var(--font);color:var(--ink-soft);background:var(--surface);
  border:1px solid var(--rule-strong);border-radius:var(--r-sm);padding:0 18px;min-height:42px;
  cursor:pointer;transition:background .15s ease, border-color .15s ease, box-shadow .15s ease}}
.btn:hover:not(:disabled){{background:var(--surface-soft);border-color:var(--ink-faint);color:var(--ink)}}
.btn:disabled{{opacity:.55;cursor:wait}}
.btn:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.btn.primary{{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:var(--sh-sm)}}
.btn.primary:hover:not(:disabled){{background:var(--accent-strong);border-color:var(--accent-strong);color:#fff}}
.btn.danger{{border-color:var(--danger);color:var(--danger)}}
.btn.danger:hover:not(:disabled){{background:var(--danger-soft);color:var(--danger)}}
.btn.mini{{padding:0 13px;min-height:30px;font-size:12.5px;border-radius:999px;font-weight:500}}
.btn.ghost{{border-color:transparent;color:var(--accent-strong);box-shadow:none}}
.btn.ghost:hover:not(:disabled){{background:var(--accent-soft);border-color:transparent}}

/* mission — calm step sequence, friendly progress */
.mission{{display:flex;flex-direction:column}}
.mission-bar{{display:flex;align-items:center;gap:14px;margin:2px 0 0}}
.bar{{flex:1;height:9px;border-radius:999px;background:var(--surface-soft);overflow:hidden}}
.bar i{{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--accent),var(--accent-strong));transition:width .5s ease}}
.bar-label{{font-size:13px;color:var(--ink-soft);white-space:nowrap;font-variant-numeric:tabular-nums}}
.stg{{display:grid;grid-template-columns:32px 1fr;gap:2px 12px;padding:12px 10px;border-top:1px solid var(--rule)}}
.stg-no{{font-size:11.5px;color:var(--ink-faint);font-weight:500}}
.stg-icon{{grid-row:1 / span 2;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;background:var(--surface-soft);color:var(--ink-faint);align-self:start;margin-top:2px}}
.stg-title{{display:flex;align-items:center;gap:9px;flex-wrap:wrap;font-weight:600;font-size:15px;grid-column:2;min-width:0}}
.stg-title .zh{{font-weight:400;color:var(--ink-faint);font-size:12px}}
.stg-what{{margin:2px 0 0;font-size:13.5px;color:var(--ink-soft);grid-column:2}}
.stg-why{{margin:0;font-size:13.5px;color:var(--ink-faint);grid-column:2}}
.stg-note{{font-size:12.5px;color:var(--ink);margin-top:4px;grid-column:2}}
.stg-tech{{font-size:11.5px;color:var(--ink-faint);margin-top:2px;font-family:var(--mono);grid-column:2}}
@keyframes breathe{{50%{{opacity:.35}}}}
.stg.running{{background:var(--live-soft);border-radius:var(--r-sm);border-top-color:transparent;margin-top:6px}}
.stg.running .st-icon{{background:var(--live);color:#fff}}
.stg.running .stg-title .tick::before{{content:'● ';animation:breathe 1.6s ease-in-out infinite}}
.stg.done .st-icon{{background:var(--ok-soft);color:var(--ok)}}
.tick{{margin-left:auto;font-size:12px;font-weight:600}}
.stg-title .tick{{opacity:.9}}
.stg.running .tick{{color:var(--live)}}
.stg.done .tick{{color:var(--ok)}}
.tick em{{font-style:normal;font-weight:400;color:var(--ink-faint)}}

/* raw drawer — the only mono surface on the page */
details.rawtail{{margin-top:10px}}
details.rawtail summary{{cursor:pointer;padding:9px 14px;border:1px solid var(--rule);border-radius:999px;
  font:500 12.5px var(--font);color:var(--ink-soft);list-style:none;display:inline-flex;align-items:center;gap:7px}}
details.rawtail summary::before{{content:'▸ ';color:var(--accent)}}
details.rawtail[open] summary::before{{content:'▾ ';color:var(--accent)}}
#tail{{margin:10px 0 0;padding:14px 16px;height:260px;overflow:auto;border:1px solid var(--rule);
  border-radius:var(--r);background:#14170f;color:#dbe2c9;font-family:var(--mono);font-size:12px;line-height:1.55;white-space:pre-wrap}}

/* run archive — question-first calm cards */
.runs{{display:flex;flex-direction:column;gap:12px}}
.run-card{{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r-lg);box-shadow:var(--sh-sm);padding:16px 20px}}
.rc-head{{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}}
.rc-title{{font-weight:600;font-size:15.5px}}
.rc-q{{margin:9px 0 0;font-size:15px;color:var(--ink);border-left:3px solid var(--rule);padding-left:12px}}
.rc-res{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.rc-link{{display:inline-flex;align-items:center;gap:6px;padding:6px 13px;border:1px solid var(--rule);border-radius:999px;font-size:12.5px;color:var(--accent-strong);background:var(--surface);text-decoration:none}}
.rc-link:hover{{border-color:var(--accent);background:var(--accent-soft);text-decoration:none}}
.rc-meta{{margin-top:10px;font-size:12px;color:var(--ink-faint)}}
.resume-row{{margin-top:10px}}

/* knowledge library — product surface */
.lib-toolbar{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:6px 2px 16px}}
.lib-toolbar .qsearch{{flex:1;min-width:220px;padding:10px 14px;font:15px/1.4 var(--font);
  border:1px solid var(--rule-strong);border-radius:999px;background:var(--surface);color:var(--ink)}}
.lib-toolbar .qsearch:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}}
.fpill{{padding:6px 13px;border-radius:999px;border:1px solid var(--rule);background:var(--surface);
  font:500 13px var(--font);color:var(--ink-soft);cursor:pointer}}
.fpill:hover{{border-color:var(--accent);color:var(--accent-strong)}}
.fpill.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
.lib-meta{{font-size:12.5px;color:var(--ink-faint);padding:0 2px}}
.lib-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.kcard{{display:flex;flex-direction:column;gap:10px;background:var(--surface);border:1px solid var(--rule);
  border-radius:var(--r-lg);box-shadow:var(--sh-sm);padding:16px 18px}}
.kcard-head{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.kcard-head .badge{{margin-right:auto}}
.kfav{{border:0;background:transparent;cursor:pointer;font-size:18px;line-height:1;color:var(--ink-faint);
  padding:2px 4px;border-radius:var(--r-sm)}}
.kfav.on{{color:var(--warn)}}
.kfav:hover{{background:var(--surface-soft)}}
.kcard-title{{font-weight:600;font-size:15px;color:var(--ink);line-height:1.4}}
.kcard-title:hover{{color:var(--accent-strong);text-decoration:none}}
.kcard-q{{font-size:13px;color:var(--ink-soft);display:-webkit-box;-webkit-line-clamp:3;
  -webkit-box-orient:vertical;overflow:hidden}}
.kmeta{{font-size:12px;color:var(--ink-faint);display:flex;gap:6px;flex-wrap:wrap}}
.ktags{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.ktag{{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:999px;
  background:var(--accent-soft);color:var(--accent-strong);font-size:12px}}
.ktag button{{border:0;background:transparent;color:var(--accent-strong);cursor:pointer;padding:0;
  font-size:13px;line-height:1}}
.ktag-add{{flex:0 0 auto;border:1px dashed var(--rule-strong);border-radius:999px;background:transparent;
  color:var(--ink-faint);padding:3px 10px;font:12px var(--font);width:110px}}
.ktag-add:focus{{outline:none;border-style:solid;border-color:var(--accent);color:var(--ink)}}
.kactions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:2px}}
.kdel{{margin-left:auto}}
.lib-empty{{grid-column:1/-1;background:var(--surface);border:1px dashed var(--rule-strong);
  border-radius:var(--r-lg);padding:34px 20px;text-align:center;color:var(--ink-faint);font-size:14px}}

/* reader */
.reader-head{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px}}
.reader-head .rtitle{{font-weight:700;font-size:18px;min-width:0;flex:1}}
.reader-banner{{background:var(--accent-soft);border:1px solid var(--rule);border-radius:var(--r);
  padding:12px 16px;margin:2px 0 14px}}
.reader-banner .bq{{font-size:15px;color:var(--ink);margin-bottom:6px}}
.rtabs{{display:inline-flex;gap:2px;background:var(--surface-soft);border-radius:999px;padding:3px}}
.rtab{{border:0;background:transparent;padding:7px 16px;border-radius:999px;font:500 13px var(--font);
  color:var(--ink-soft);cursor:pointer}}
.rtab.on{{background:var(--surface);box-shadow:var(--sh-sm);color:var(--accent-strong);font-weight:600}}
.kviewer{{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r-lg);
  box-shadow:var(--sh);padding:8px}}
.kviewer iframe{{width:100%;height:78vh;border:0;border-radius:var(--r)}}
.kprose{{max-width:820px;margin:0 auto;padding:22px 26px 60px;font-size:15.5px;line-height:1.75;color:var(--ink)}}
.kprose h1{{font-size:26px;margin:1.2em 0 .5em;padding-bottom:.3em;border-bottom:1px solid var(--rule)}}
.kprose h2{{font-size:20px;margin:1.4em 0 .5em}}
.kprose h3{{font-size:17px;margin:1.2em 0 .4em}}
.kprose h1:first-child{{margin-top:0}}
.kprose p{{margin:.6em 0}}
.kprose a{{color:var(--accent-strong);text-decoration:underline}}
.kprose ul,.kprose ol{{padding-left:1.4em;margin:.6em 0}}
.kprose li{{margin:.2em 0}}
.kprose blockquote{{margin:.8em 0;padding:.2em 1em;border-left:3px solid var(--accent);
  background:var(--surface-soft);border-radius:0 var(--r-sm) var(--r-sm) 0;color:var(--ink-soft)}}
.kprose code{{background:var(--surface-soft);border:1px solid var(--rule);border-radius:6px;padding:.1em .35em}}
.kprose pre{{background:var(--surface-soft);border:1px solid var(--rule);border-radius:var(--r);
  padding:14px 16px;overflow:auto;margin:.8em 0}}
.kprose pre code{{background:none;border:0;padding:0}}
.kprose table{{margin:.8em 0}}
.kprose img{{max-width:100%;border-radius:var(--r)}}
.kprose hr{{border:0;border-top:1px solid var(--rule);margin:1.4em 0}}

/* status chips */
.chip{{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;padding:4px 11px;border-radius:999px}}
.chip::before{{content:'';width:7px;height:7px;border-radius:50%}}
.chip.ok{{background:var(--ok-soft);color:var(--ok)}}
.chip.ok::before{{background:var(--ok)}}
.chip.run{{background:var(--live-soft);color:var(--live)}}
.chip.run::before{{background:var(--live);animation:breathe 1.6s ease-in-out infinite}}
.chip.fail{{background:var(--danger-soft);color:var(--danger)}}
.chip.fail::before{{background:var(--danger)}}
.chip.cancel{{background:var(--surface-soft);color:var(--warn)}}
.chip.cancel::before{{background:var(--warn)}}
.chip.muted{{background:var(--surface-soft);color:var(--ink-faint)}}
.chip.muted::before{{background:var(--ink-faint)}}

/* badges (manuscript/dashboard tables) */
.badge{{display:inline-block;font-size:11.5px;font-weight:600;padding:3px 10px;border-radius:999px}}
.badge.ok{{background:var(--ok-soft);color:var(--ok)}}
.badge.fail{{background:var(--danger-soft);color:var(--danger)}}
.badge.run{{background:var(--live-soft);color:var(--live)}}
.badge.cancel{{background:var(--surface-soft);color:var(--warn)}}
.badge.muted{{background:var(--surface-soft);color:var(--ink-faint)}}

/* tables & utilities */
table{{border-collapse:collapse;width:100%;font-size:13.5px}}
td,th{{border:1px solid var(--rule);padding:8px 12px;text-align:left}}
th{{background:var(--surface-soft);font-weight:600}}
tbody tr:nth-child(even){{background:var(--surface-soft2)}}
ul{{margin:.4em 0}}li{{margin:.15em 0}}
.muted{{color:var(--ink-faint)}}.green{{color:var(--ok)}}.red{{color:var(--danger)}}.amber{{color:var(--warn)}}
.mono{{font-family:var(--mono);font-size:12px}}
.id{{color:var(--ink-faint);font-size:12px}}
.mission-empty, .empty{{color:var(--ink-faint);font-size:14px;padding:14px 4px}}

/* colophon */
.colophon{{margin-top:44px;padding:16px 0 4px;border-top:1px solid var(--rule);
  font-size:12px;line-height:1.7;color:var(--ink-faint)}}

@media (prefers-color-scheme: dark){{
  :root{{
    --paper:#16181a; --surface:#1d2023; --surface-soft:#24282c; --surface-soft2:#1a1d1f;
    --ink:#e8e6e1; --ink-soft:#b4b6b2; --ink-faint:#83868a;
    --rule:#33363a; --rule-strong:#4a4e52;
    --accent:#7fb6a6; --accent-strong:#a4d3c5; --accent-soft:#22302b;
    --ok:#8fbc9d; --ok-soft:#233026; --live:#d9a476; --live-soft:#3a2c1e;
    --danger:#d98981; --danger-soft:#3a2422; --warn:#d3b26a;
    --sh-sm:0 1px 2px rgba(0,0,0,.35); --sh:0 1px 3px rgba(0,0,0,.4),0 10px 28px rgba(0,0,0,.35);
  }}
  .btn.primary{{color:#101312}}
}}
@media (max-width:700px){{
  .topbar-row{{gap:8px}}
  .navpills{{order:3;flex-basis:100%;min-width:0}}
  .main{{padding:18px 0 6px}}
  .probe-row .btn{{width:100%}}
  .stg{{grid-template-columns:28px 1fr;gap:2px 10px}}
  .st-icon{{width:24px;height:24px;font-size:12px}}
  .rc-head, .sect-head{{align-items:flex-start}}
}}
@media (prefers-reduced-motion: reduce){{
  *{{transition:none!important;animation:none!important}}
  .stg.running .stg-title .tick::before, .chip.run::before{{animation:none}}
}}
</style></head><body>
<div class="topbar"><div class="frame topbar-row">
<a class="brand" href="/"><span class="brand-dot" aria-hidden="true"></span>research_foodie<span class="brand-tag">{ui_brand_tag}</span></a>
<nav class="navpills"><a class="pill {cur_workbench}" href="/">{ui_nav_workbench}</a><a class="pill {cur_lib}" href="/library">{ui_nav_lib}</a><a class="pill {cur_dash}" href="/dashboard">{ui_nav_dash}</a><a class="pill {cur_fb}" href="/feedback">{ui_nav_fb}</a></nav>
<span class="langseg"><a class="pill {cur_lang_zh}" href="/_lang/zh">中文</a><a class="pill {cur_lang_en}" href="/_lang/en">EN</a></span>
</div></div>
<div class="frame main">
"""

HTML_TAIL = ('<footer class="colophon">research_foodie · local-first survey pipeline · '
             'pandoc + xelatex (YaHei) · zero external network on the page · '
             'binds 127.0.0.1 · citations are the lifeline</footer>'
             '</div></body></html>')

UI = {
    "en": {
        "nav_workbench": "Workbench", "nav_lib": "Library", "nav_dash": "Numbers", "nav_ms": "Manuscripts", "nav_fb": "Feedback",
        "brand_tag": "local survey workbench",
        "trust_cite": "every citation traceable",
        "trust_double": "two-tier PDF delivery",
        "trust_local": "runs offline · no API key",
        "mast_meta": "research_foodie · local-first survey pipeline · citations are the lifeline",
        "mast_title": "Survey workbench",
        "lede": ("Ask a question and get a survey where every sentence is traceable. Each step is "
                 "narrated as it happens — what stage the research is at, how it is done, and why. "
                 "Every survey ships in two tiers: the dry-goods manuscript (default) and an "
                 "arXiv-style preprint."),
        "probe_head": "Start a survey", "probe_head_en": "ask a research question",
        "quick_tasks": "or launch a saved scenario:",
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
        "lib_title": "Knowledge Library",
        "lib_search_ph": "search question, title or tag…",
        "lib_scan": "re-scan",
        "lib_items": "items", "lib_empty": ("No knowledge items yet. Run a survey — its "
                                             "manuscript (markdown + PDF) lands here."),
        "lib_all": "All", "lib_fav": "Favorites", "lib_pass": "Passed",
        "lib_mock": "Mock", "lib_real": "Real",
        "kind_survey": "survey", "kind_mock": "mock", "kind_bench": "bench",
        "read": "Read", "read_title": "Reader", "read_tab_doc": "Markdown",
        "read_tab_pdf": "PDF", "read_open": "new tab", "read_download": "download",
        "read_back": "Back to library", "read_missing": "not found in the knowledge library.",
        "tag_ph": "add tag…", "del_confirm": "Delete this item and its files from disk? (run logs are kept)",
        "del_done": "deleted", "lib_offline": "offline render · zero network",
    },
    "zh": {
        "nav_workbench": "工作台", "nav_dash": "数据", "nav_ms": "手稿", "nav_fb": "反馈",
        "brand_tag": "本地科研综述工作台",
        "trust_cite": "引用逐条可溯源",
        "trust_double": "双档 PDF 交付",
        "trust_local": "本地运行 · 免密钥",
        "mast_meta": "research_foodie · 本地优先调研管线 · 引用即生命线",
        "mast_title": "调研工作台",
        "lede": ("输入一个问题，得到一份逐句可溯源的综述。每一步研究都在这里直播——做到哪个阶段、"
                 "怎么做、为什么这么做。每次调研都双档交付：干货稿（缺省）与 arXiv 出版化稿。"),
        "probe_head": "投题", "probe_head_en": "输入一个研究问题",
        "quick_tasks": "或直接运行预置场景：",
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
        "lib_title": "知识库",
        "lib_search_ph": "搜索问题、标题或标签…",
        "lib_scan": "重新扫描",
        "lib_items": "条", "lib_empty": "还没有知识条目——跑一次调研，产出（markdown + PDF）就会沉淀在这里。",
        "lib_all": "全部", "lib_fav": "收藏", "lib_pass": "已通过",
        "lib_mock": "Mock", "lib_real": "真实",
        "kind_survey": "调研", "kind_mock": "演示", "kind_bench": "基准",
        "read": "阅读", "read_title": "阅读器", "read_tab_doc": "正文",
        "read_tab_pdf": "PDF", "read_open": "新窗口", "read_download": "下载",
        "read_back": "返回知识库", "read_missing": "知识库中找不到这个条目。",
        "tag_ph": "添加标签…", "del_confirm": "从磁盘删除该条目及其文件？（运行日志保留）",
        "del_done": "已删除", "lib_offline": "离线渲染 · 零外部网络",
    },
}


def T(lang: str, key: str) -> str:
    return UI.get(lang, UI["en"]).get(key, key)


def lang_of(request: Request) -> str:
    return request.cookies.get("rf_lang", "en") if request.cookies.get("rf_lang") in ("en", "zh") else "en"


def page(title, body: str, cur: str = "wb", lang: str = "en") -> HTMLResponse:
    kw = dict(
        cur_workbench="cur" if cur == "wb" else "",
        cur_lib="cur" if cur == "lib" else "",
        cur_dash="cur" if cur == "dash" else "",
        cur_ms="cur" if cur == "ms" else "",
        cur_fb="cur" if cur == "fb" else "",
        cur_lang_zh="cur" if lang == "zh" else "",
        cur_lang_en="cur" if lang == "en" else "",
        html_lang="zh-CN" if lang == "zh" else "en",
        ui_nav_workbench=T(lang, "nav_workbench"),
        ui_nav_lib=T(lang, "nav_lib"),
        ui_nav_dash=T(lang, "nav_dash"),
        ui_nav_ms=T(lang, "nav_ms"),
        ui_nav_fb=T(lang, "nav_fb"),
        ui_brand_tag=T(lang, "brand_tag"),
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
        alt = meta["zh"] if lang == "en" else meta["label"]
        status = s["status"] if s["status"] in ("done", "running", "pending") else "pending"
        ic = {"done": "✓", "running": "●", "pending": "○"}[status]
        if status == "done":
            tick = (T(lang, "done") + f" · {s['dur_s']:.1f}{T(lang, 'seconds')}"
                    if s.get("dur_s") else T(lang, "done"))
        elif status == "running":
            tick = T(lang, "running")
            if meta.get("est"):
                tick += f" · {meta['est']}"
        else:
            tick = T(lang, "pending")
        tech = " · ".join(f"{k}={v}" for k, v in (s.get("tech") or {}).items())
        rows.append(
            f'<article class="stg {status}">'
            f'<span class="st-icon" aria-hidden="true">{ic}</span>'
            f'<div class="stg-title">{label}<span class="zh">{alt}</span>'
            f'<span class="stg-no">{i}/{len(stages)}</span>'
            f'<span class="tick">{tick}</span></div>'
            f'<p class="stg-what">{meta["what"]}</p>'
            f'<p class="stg-why">{meta["why"]}</p>'
            f'<div class="stg-note">{meta["how"]}</div>'
            + (f'<div class="stg-tech">{tech}</div>' if tech else "")
            + '</article>')
    summary_html = ""
    if summary:
        links = " ".join(
            f'<a href="/manuscripts/{Path(x).name}" class="rc-link">{label}</a>'
            for label, x in ((T(lang, "link_manuscript"), summary.get("manuscript")),
                             (T(lang, "link_pdf"), summary.get("pdf")),
                             (T(lang, "link_preprint"), summary.get("pdf_pub")))
            if x)
        verdict = T(lang, "l6_pass") if summary.get("gate_passed") else T(lang, "l6_fail")
        summary_html = (f'<div class="run-card" style="margin:12px 0">'
                        f'<div class="rc-head"><span class="rc-title">{verdict}</span>'
                        f'<span class="chip {"ok" if summary.get("gate_passed") else "fail"}">'
                        f'{T(lang, "judge")} {summary.get("judge_label")}</span></div>'
                        f'<div class="rc-res">{links}</div>'
                        f'<div class="rc-meta">{summary.get("claims", 0)} {T(lang, "claims")} · '
                        f'{summary.get("n_papers_cited", 0)} {T(lang, "papers")} · '
                        f'{summary.get("elapsed_s", 0)}{T(lang, "seconds")}</div></div>')
    bar = (f'<div class="mission-bar"><div class="bar"><i style="width:{pct}%"></i></div>'
           f'<span class="bar-label">{done}/{len(stages)} · {pct}%</span></div>'
           f'<p class="muted" style="font-size:12px;padding:2px 4px;margin:0">'
           f'{len(stages)} {T(lang, "stages")}</p>')
    return bar + summary_html + "".join(rows)


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
    """HTML card for one run (list page). Question first; numbers live elsewhere."""
    from tools.eval.run_ledger import ResumeLedger
    status_badge = {
        "done": 'ok', "running": 'run', "pending": 'muted',
        "failed": 'fail', "cancelled": 'cancel', "interrupted": 'cancel',
    }.get(run.status, 'muted')
    status_label = T(lang, run.status)
    survey = _survey_summary(run)
    is_survey = survey or any(ln.startswith("[survey-stage]") for ln in run.lines)
    links = []
    if survey:
        for key, attr in ((T(lang, "link_manuscript"), "manuscript"),
                          (T(lang, "link_pdf"), "pdf"),
                          (T(lang, "link_preprint"), "pdf_pub")):
            x = survey.get(attr)
            if x:
                links.append(f'<a class="rc-link" href="/manuscripts/{Path(x).name}">{key}</a>')
    if is_survey:
        links.append(f'<a class="rc-link" href="/runs/{run.id}/mission" target="_blank">'
                     f'{T(lang, "research_view")}</a>')
    links.append(f'<a class="rc-link" href="/runs/{run.id}/log" target="_blank">{T(lang, "link_log")}</a>')
    q_html = f'<p class="rc-q">{survey.get("question", "")}</p>' if survey else ""
    res_line = f'<div class="rc-res">{"".join(links)}</div>' if links else ""
    # ledger progress for bench_eval / variance_run (they persist per-row state)
    progress = ""
    for mod, argv in (("tools.eval.bench_eval", r"bench_eval"),
                      ("tools.eval.variance_run", r"variance_run")):
        search = f"-m {mod}"
        if any(search in str(c) for c in run.cmd):
            led = ResumeLedger._load(argv)
            if led:
                progress = f'<span class="chip ok">{len(led.get("done", {}))} done</span>'
            break
    resume = ""
    if run.status in ("failed", "cancelled", "interrupted"):
        resume = (f'<button class="btn mini" onclick="resumeRun(\'{run.id}\')">'
                  f'{T(lang, "link_resume")}</button>')
    meta = (f'<div class="rc-meta">{" ".join(run.cmd)} · {run.elapsed:.0f}s · rc={run.returncode} · '
            f'{len(run.lines)} lines</div>')
    foot = f'<div class="resume-row">{progress} {resume}</div>' if (progress or resume) else ""
    return (f'<div class="run-card"><div class="rc-head">'
            f'<span class="rc-title">{run.title}</span>'
            f'<span class="chip {status_badge}">{status_label}</span></div>'
            f'{q_html}{res_line}{foot}{meta}</div>')


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
<section class="hero">
  <h1>{T(lang, "mast_title")}</h1>
  <p class="lede">{T(lang, "lede")}</p>
  <div class="trust">
    <span>{T(lang, "trust_cite")}</span><span>{T(lang, "trust_double")}</span><span>{T(lang, "trust_local")}</span>
  </div>
</section>

<section class="sect">
  <div class="sect-head"><h2>{T(lang, "probe_head")} <span class="en">{T(lang, "probe_head_en")}</span></h2>
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
            <b>{T(lang, "mock_label")}</b><small>{T(lang, "mock_note")}</small></label>
          <label><input type="radio" name="mode" value="real">
            <b>{T(lang, "real_label")}</b><small>{T(lang, "real_note")}</small></label>
        </div>
        <button class="btn primary" id="runbtn" onclick="startQuestion()">{T(lang, "run_btn")}</button>
        <span class="muted" id="q-msg"></span>
      </div>
      <p class="hint">{T(lang, "resume_hint")}</p>
      <p class="chips-label">{T(lang, "quick_tasks")}</p>
      <div class="chips">{menu_html}</div>
    </form>
  </div>
</section>

<section class="sect">
  <div class="sect-head"><h2>{T(lang, "mission_head")} <span class="en">{T(lang, "mission_head_en")}</span></h2>
    <div class="side"><span id="active-msg" class="muted"></span>
    <button class="btn danger mini" onclick="cancelRun()">{T(lang, "cancel_btn")}</button></div></div>
  <div id="mission">{mission_init or f'<p class="mission-empty">{T(lang, "no_mission")}</p>'}</div>
  <details class="rawtail"><summary>{T(lang, "raw_head")} · <span class="muted">{T(lang, "raw_head_en")}</span></summary>
  <div id="tail"></div></details>
</section>

<section class="sect">
  <div class="sect-head"><h2>{T(lang, "runs_head")} <span class="en">{T(lang, "runs_head_en")}</span></h2></div>
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
const ST_ICON = {{done:'✓', running:'●', pending:'○'}};
function renderMission(){{
  const el = document.getElementById('mission');
  const ids = Object.keys(stagesMeta);
  const doneN = ids.filter(i => stagePlan[i] && stagePlan[i].status === 'done').length;
  const pct = ids.length ? Math.round(100 * doneN / ids.length) : 0;
  let rows = '';
  ids.forEach((id, k) => {{
    const m = stagesMeta[id]; const p = stagePlan[id] || {{status:'pending', tech:{{}}, dur_s:0}};
    const st = ['done','running','pending'].includes(p.status) ? p.status : 'pending';
    let tick = {{done: UI.done, running: UI.running, pending: UI.pending}}[st];
    if (st === 'done' && p.dur_s) tick += ' · ' + p.dur_s.toFixed(1) + UI.seconds;
    if (st === 'running'){{
      tick += ' · ';
      tick += p.stageStart ? Math.round((Date.now()-p.stageStart)/1000) : '…';
      tick += UI.seconds;
    }}
    const tech = Object.entries(p.tech||{{}}).map(([a,b])=>a+'='+b).join(' · ');
    rows += `<article class="stg ${{st}}">
      <span class="st-icon" aria-hidden="true">${{ST_ICON[st]}}</span>
      <div class="stg-title">${{stageLabel(m)}}<span class="zh">${{stageAlt(m)}}</span>
        <span class="stg-no">${{k+1}} / ${{ids.length}}</span>
        <span class="tick">${{tick}}</span></div>
      <p class="stg-what">${{m.what}}</p>
      <p class="stg-why">${{m.why}}</p>
      <div class="stg-note">${{m.how}}</div>${{tech ? '<div class="stg-tech">'+tech+'</div>' : ''}}
      </article>`;
  }});
  el.innerHTML =
    `<div class="mission-bar"><div class="bar"><i style="width:${{pct}}%"></i></div>
      <span class="bar-label">${{doneN}} / ${{ids.length}} · ${{pct}}%</span></div>
     <div class="muted" style="font-size:12px;padding:2px 4px">${{UI.stages}}
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


# --------------------------------------------------------------------------
# Knowledge library (Phase H)
# --------------------------------------------------------------------------

_KIND_LABEL = {"survey": "kind_survey", "mock-survey": "kind_mock", "bench": "kind_bench"}
_CHIP_CLASS = {"survey": "ok", "mock-survey": "muted", "bench": "run"}


def _lib_card(item: dict, lang: str) -> str:
    q = (item.get("question") or "").strip()
    title = q or item.get("title") or item["key"]
    kind = _KIND_LABEL.get(item["kind"], "kind_bench")
    fav = "★" if item.get("favorite") else "☆"
    favcls = "on" if item.get("favorite") else ""
    tags = "".join(
        f'<span class="ktag">{t}<button title="×" onclick="rmTag(\'{item["key"]}\',' +
        f"'{t}')>×</button></span>" for t in item.get("tags", "").split(",") if t.strip())
    meta = []
    if item.get("mode"):
        meta.append(f'<span class="chip {_CHIP_CLASS.get(item["kind"], "muted")}">{item["mode"]}</span>')
    if item.get("verdict"):
        vcls = "ok" if item["verdict"] == "pass" else "fail"
        meta.append(f'<span class="chip {vcls}">{T(lang,"l6_pass") if item["verdict"]=="pass" else T(lang,"l6_fail")}</span>')
    if item.get("judge"):
        meta.append(f'<span>{T(lang, "judge")}={item["judge"]}</span>')
    if item.get("claims"):
        meta.append(f'{item["claims"]} {T(lang, "claims")}')
    if item.get("papers"):
        meta.append(f'{item["papers"]} {T(lang, "papers")}')
    if item.get("elapsed_s"):
        meta.append(f'{item["elapsed_s"]:.0f}{T(lang, "seconds")}')
    meta_html = f'<div class="kmeta">{"".join(meta)}</div>' if meta else ""
    actions = [f'<a class="btn mini" href="/read/{item["key"]}">{T(lang, "read")}</a>']
    if item.get("path_md"):
        actions.append(f'<a class="btn mini" href="/manuscripts/{Path(item["path_md"]).name}">MD</a>')
    if item.get("path_pdf"):
        actions.append(f'<a class="btn mini" href="/manuscripts/{Path(item["path_pdf"]).name}">PDF</a>')
    actions.append(f'<button class="btn mini danger kdel" onclick="delItem(\'{item["key"]}\')">'
                   f'{T(lang, "del")}</button>')
    return (f'<article class="kcard" data-q="{_h(q + " " + title + " " + item["tags"])}" '
            f'data-mode="{item["mode"]}" data-verdict="{item["verdict"]}" '
            f'data-fav="{1 if item.get("favorite") else 0}">'
            f'<div class="kcard-head">'
            f'<span class="badge {_CHIP_CLASS.get(item["kind"], "muted")}">{T(lang, kind)}</span>'
            f'<button class="kfav {favcls}" onclick="favItem(\'{item["key"]}\')" '
            f'title="{T(lang, "fav_on") if item.get("favorite") else T(lang, "fav_off")}">{fav}</button>'
            f'</div>'
            f'<a class="kcard-title" href="/read/{item["key"]}">{_h(title)}</a>'
            f'{meta_html}'
            f'<div class="ktags">{tags}'
            f'<input class="ktag-add" placeholder="{T(lang, "tag_ph")}" '
            f'onkeydown="if(event.key===\'Enter\')addTag(\'{item["key"]}\',this)"></div>'
            f'<div class="kactions">{"".join(actions)}</div>'
            f'</article>')


def _h(s: str) -> str:
    import html as _html
    return _html.escape(s, quote=True)


@app.get("/library", response_class=HTMLResponse)
def library_page(request: Request):
    lang = lang_of(request)
    items = knowledge.sync()
    cards = "".join(_lib_card(i, lang) for i in items)
    if not cards:
        cards = f'<div class="lib-empty">{T(lang, "lib_empty")}</div>'
    body = f"""
<script>
const LANG = {json.dumps(lang)};
const UI = {json.dumps(UI[lang])};
function esc(s){{const d=document.createElement('div');d.textContent=s;return d.innerHTML;}}
function applyLib(){{
  const q = document.getElementById('lq').value.trim().toLowerCase();
  const f = document.getElementById('lfilter').value;
  let n = 0;
  document.querySelectorAll('.kcard').forEach(c => {{
    const okQ = !q || 0 <= (c.dataset.q || '').toLowerCase().indexOf(q);
    const okF = f === 'all'
      || (f === 'fav' && c.dataset.fav === '1')
      || (f === 'pass' && c.dataset.verdict === 'pass')
      || (f === 'mock' && c.dataset.mode === 'mock')
      || (f === 'real' && c.dataset.mode === 'real');
    c.style.display = (okQ && okF) ? '' : 'none';
    if (okQ && okF) n++;
  }});
  document.getElementById('lcount').textContent = n + ' ' + UI.lib_items;
}}
function setFilter(v){{
  document.getElementById('lfilter').value = v;
  document.querySelectorAll('.fpill').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  applyLib();
}}
async function favItem(key){{
  const r = await fetch('/lib/api/' + key + '/favorite', {{method:'POST'}});
  const d = await r.json(); if (!d.ok) {{alert(d.error); return;}}
  const card = [...document.querySelectorAll('.kcard')].find(c => c.querySelector('[href^="/read/' + key + '"]'));
  if (card){{ card.dataset.fav = d.item.favorite ? '1' : '0';
    const b = card.querySelector('.kfav'); b.classList.toggle('on', !!d.item.favorite);
    b.textContent = d.item.favorite ? '★' : '☆'; }}
}}
async function addTag(key, input){{
  const card = input.closest('.kcard'); let t = input.value.trim(); if (!t) return;
  const cur = [...card.querySelectorAll('.ktag')].map(x => x.firstChild.textContent);
  const r = await fetch('/lib/api/' + key + '/tags', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{tags: [...new Set([...cur, t])]}})}});
  const d = await r.json(); if (!d.ok) {{alert(d.error); return;}}
  location.reload();
}}
async function rmTag(key, tag){{
  const card = [...document.querySelectorAll('.kcard')].find(c => c.querySelector('[href^="/read/' + key + '"]'));
  const cur = [...card.querySelectorAll('.ktag')].map(x => x.firstChild.textContent).filter(x => x !== tag);
  const r = await fetch('/lib/api/' + key + '/tags', {{method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{tags: cur}})}});
  const d = await r.json(); if (!d.ok) {{alert(d.error); return;}}
  location.reload();
}}
async function delItem(key){{
  if (!confirm(UI.del_confirm)) return;
  const r = await fetch('/lib/api/' + key, {{method:'DELETE'}});
  const d = await r.json(); if (!d.ok) {{alert(d.error); return;}}
  document.querySelectorAll('.kcard').forEach(c => {{
    if (c.querySelector('[href^="/read/' + key + '"]')) c.remove();
  }});
  applyLib();
}}
</script>
<section class="sect">
  <h1>{T(lang, "lib_title")}</h1>
  <div class="lib-toolbar">
    <input id="lq" class="qsearch" type="search" placeholder="{T(lang, "lib_search_ph")}" oninput="applyLib()">
    <input type="hidden" id="lfilter" value="all">
    <div class="seg" style="border-radius:999px;padding:3px;gap:2px">
      <button class="fpill on" data-v="all" onclick="setFilter('all')">{T(lang, "lib_all")}</button>
      <button class="fpill" data-v="fav" onclick="setFilter('fav')">{T(lang, "lib_fav")}</button>
      <button class="fpill" data-v="pass" onclick="setFilter('pass')">{T(lang, "lib_pass")}</button>
      <button class="fpill" data-v="mock" onclick="setFilter('mock')">{T(lang, "lib_mock")}</button>
      <button class="fpill" data-v="real" onclick="setFilter('real')">{T(lang, "lib_real")}</button>
    </div>
    <button class="btn mini" onclick="location.reload()">{T(lang, "lib_scan")}</button>
    <span class="lib-meta" id="lcount"></span>
  </div>
  <div class="lib-grid" id="lgrid">{cards}</div>
  <p class="muted" style="font-size:12px">{T(lang, "lib_offline")}</p>
</section>
<script>applyLib();</script>
"""
    return page(T(lang, "lib_title"), body, cur="lib", lang=lang)


@app.post("/lib/api/sync", response_class=JSONResponse)
def lib_sync():
    items = knowledge.sync()
    return {"ok": True, "count": len(items)}


@app.post("/lib/api/{key}/favorite", response_class=JSONResponse)
def lib_favorite(key: str):
    item = knowledge.toggle_favorite(key)
    return {"ok": item is not None, "item": item, "error": None if item else "not found"}


@app.post("/lib/api/{key}/tags", response_class=JSONResponse)
def lib_tags(key: str, payload: dict):
    tags = payload.get("tags") if isinstance(payload.get("tags"), list) else []
    item = knowledge.set_tags(key, tags)
    return {"ok": item is not None, "item": item, "error": None if item else "not found"}


@app.delete("/lib/api/{key}", response_class=JSONResponse)
def lib_delete(key: str):
    return knowledge.delete_item(key)


@app.get("/read/{key}", response_class=HTMLResponse)
def reader_page(key: str, request: Request):
    """In-page reader for one knowledge artifact: rendered markdown + native PDF view."""
    lang = lang_of(request)
    item = knowledge.get(key)
    if not item:
        return page(f"{T(lang, 'read_title')} · {key}",
                    f'<h1>{_h(key)}</h1><p class="empty">{_h(key)} {T(lang, "read_missing")}</p>'
                    f'<a href="/library">{T(lang, "read_back")}</a>', cur="lib", lang=lang)
    md_html, has_md, has_pdf = "", False, False
    if item.get("path_md") and (REPO_ROOT / Path(item["path_md"])).is_file():
        raw = (REPO_ROOT / Path(item["path_md"])).read_text(encoding="utf-8", errors="replace")
        md_html = _md.render(raw)
        has_md = True
    pdf_url = ""
    if item.get("path_pdf") and (REPO_ROOT / Path(item["path_pdf"])).is_file():
        pdf_url = f'/manuscripts/{Path(item["path_pdf"]).name}'
        has_pdf = True
    if not has_md and not has_pdf:
        return page(f"{T(lang, 'read_title')} · {key}",
                    f'<h1>{_h(item["title"])}</h1><p class="empty">{T(lang, "read_missing")}</p>',
                    cur="lib", lang=lang)
    banner = ""
    if item.get("question"):
        v = (f'<span class="chip {"ok" if item["verdict"]=="pass" else "fail"}">'
             f'{T(lang,"l6_pass") if item["verdict"]=="pass" else T(lang,"l6_fail")}</span>')
        meta = [v]
        if item.get("mode"):
            meta.append(f'<span>{item["mode"]}</span>')
        if item.get("claims"):
            meta.append(f'{item["claims"]} {T(lang, "claims")}')
        if item.get("papers"):
            meta.append(f'{item["papers"]} {T(lang, "papers")}')
        if item.get("elapsed_s"):
            meta.append(f'{item["elapsed_s"]:.0f}{T(lang, "seconds")}')
        banner = (f'<div class="reader-banner"><p class="bq"><strong>'
                  f'{T(lang, "mission_question")}</strong> {_h(item["question"])}</p>'
                  f'<div class="kmeta">{"".join(meta)}</div></div>')
    doc_panel = (f'<div class="kviewer" id="pane-doc">{md_html}</div>' if has_md else
                 f'<div class="kviewer" id="pane-doc"><p class="empty">PDF only</p></div>')
    pdf_panel = (f'<div class="kviewer" id="pane-pdf" style="display:none">'
                 f'<iframe src="{pdf_url}" title="PDF"></iframe></div>' if has_pdf else
                 f'<div class="kviewer" id="pane-pdf" style="display:none"><p class="empty">—</p></div>')
    tabs = f"""
<div class="reader-head">
  <a class="btn ghost mini" href="/library">← {T(lang, "read_back")}</a>
  <span class="rtitle">{_h(item["title"])}</span>
  <div class="rtabs">
    <button class="rtab on" data-tab="doc" onclick="rdTab('doc')">{T(lang, "read_tab_doc")}</button>
    <button class="rtab" data-tab="pdf" onclick="rdTab('pdf')">{T(lang, "read_tab_pdf")}</button>
  </div>
  <div class="rtabs">
    <a class="btn mini ghost" href="/manuscripts/{Path(item["path_md"]).name if item.get("path_md") else ""}"
       target="_blank">{T(lang, "read_open")}</a>
    {f'<a class="btn mini ghost" href="/manuscripts/{Path(item["path_pdf"]).name}" download>{T(lang, "read_download")} PDF</a>' if has_pdf else ""}
  </div>
</div>
"""
    body = f"""
<section class="sect">
  {tabs}
  {banner}
  {doc_panel}
  {pdf_panel}
</section>
<script>
function rdTab(t){{
  document.querySelectorAll('.rtab').forEach(b => b.classList.toggle('on', b.dataset.tab === t));
  document.getElementById('pane-doc').style.display = (t === 'doc') ? '' : 'none';
  const pdf = document.getElementById('pane-pdf');
  if (pdf) pdf.style.display = (t === 'pdf') ? '' : 'none';
}}
</script>
"""
    return page(f"{T(lang, 'read_title')} · {item['title'][:60]}", body, cur="lib", lang=lang)


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