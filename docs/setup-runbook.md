# Research Foodie — Setup & Operations Runbook (设置与运行手册)

> **中文速览**
> 本文档是本仓库的**操作性手册**（bilingual）：基于 2026-09-15 P1 阶段的真实实测，记录环境怎么搭、哪些工具已跑通、每条命令、踩过的坑与临时解法、遗留问题，以及下一步怎么走。目标是"任何会话翻到本文档即可无缝继续"。
> **一句话现状**：MinerU PDF→Markdown 跑通；**PaddleOCR 中文识别已解决（K7 关闭）**；**统一 LLM client 已建**（`tools/llm/`，**默认后端 = opencode CLI 免费模型 `opencode/big-pickle`**，另支持任何 OpenAI 兼容 API）；**Ollama 后端已于 2026-09-16 彻底移除**（用户决定"不要再考虑 Ollama"，K11 历史排障见台账）；**P2 最小纵切已打通**（`tools/pipeline/`：S_lit 可插拔发现 rail + LangGraph 完整链 + L6 确定性校验 + 写时反幻觉过滤 + 全文 claim 抽取）；**三大参考框架已运行时整合（Session 9）**：STORM-style 大纲（S_org outline→S_write 大纲驱动写作）、OpenResearch/orx + arXiv **实时发现 rail**（`S_LIT_BACKEND=seed|arxiv|orx`，2026-09-16 实测 arXiv API 已可达 1.1 s）、DAS-Bench-style **AI 评审门**（P3 preview，`validation.judge`）；测试 mock **19/19** + real `opencode/big-pickle` **18/18** @121.7 s（draft 3357 字、outline 3 节、score 1.0、judge=pass）；**已在第二篇真实论文（Weber-Wulff `2306.15666`）上验证泛化（Session 10）**；**DAS-Bench 16 轴基准评测试点已完成（Session 11）**：`tools/eval/bench_eval.py`，预览总分 P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence，报告 `_eval_out/bench_pilot_das.md`；远程 GPU / 付费 API 仍按用户决定延后。

- `Updated`: 2026-09-20 (added §3.0 End-to-end usage flow + §3.1 Usage & Demos; WS-B web dashboard in §3.0.5; WS-C health check / WS-D model profiles / run-memory resume in §3.0.5)
- `Status`: P1 tooling — done (parsing ✓, OCR ✓ K7 closed, GPU deferred; LLM client ✓ opencode 3/3 + mock 3/3; Ollama removed 2026-09-16); **P2 minimal vertical — done** (LangGraph S_lit→S_org→S_write→S_final → L6 gate → P3 judge live: `tools/pipeline/` mock 19/19 + real `opencode/big-pickle` 18/18 @121.7 s, full-text claims, correct section attribution, STORM outline, orx/arXiv live discovery rail verified, DAS-Bench-style judge=pass; write-time grounded-claim filter catches fabrication; seed rail remains the offline default); **benchmark-style evaluation pilot vs DAS-Bench 16-criterion assets — done (Session 11, see §3 `bench_eval` + `_eval_out/bench_pilot_das.md`)**
- `Language`: bilingual (English master + 中文速览 notes)
- `See also`: `docs/design/research-foodie-blueprint.md` (architecture) · `docs/refs/ai-research-tools-workflow-guide.md` (tool survey)

---

## 1. What this document is / 这是什么

The blueprint (`docs/design/...blueprint.md`) says *what* to build. Plan/progress (`docs/PLAN.md`, `docs/PROGRESS.md`) say *what is done and next*. This runbook records **how to operate the working environment** — verified commands, versions, artifacts, workarounds, and known issues — so the next session (human or agent) starts where this one stopped.

Pipeline at a glance (full workflow & diagrams: blueprint §3; purpose: README):

```text
Question / field watch → Discovery (L1) → Parse+index (L2) → Outline+routing (L3)
  → Claim-led drafting (L4) → LangGraph S_lit→S_org→S_write→S_final (L5)
  → Deterministic checks → DAS-Bench judge → HUMAN gates (L6) → Manuscript
  ↔ proactive loop re-flags stale sections
```

## 2. Environment baseline / 环境基线 (as of 2026-09-15)

| Item | Value | Verified |
|---|---|---|
| Host | Windows 11, local CPU-only (no CUDA) | ✓ |
| Shell | PowerShell 7 (`pwsh`) | ✓ |
| Python (system) | miniconda `base` 3.12.9 · also 3.13/3.11 via `py -0` | ✓ |
| uv | 0.12.7 | ✓ |
| git | 2.54.0.windows.1 | ✓ |
| Ollama | **superseded** — backend removed 2026-09-16; client may still be on PATH but is not part of the pipeline (see PROGRESS Session 8) | ✓ |
| winget | 1.29.290 | ✓ |
| **Working ML env** | conda `ds0509` (Python 3.12.13) at `C:\Users\data\miniconda3\envs\ds0509` | ✓ |
| torch / torchvision | in `ds0509` (CUDA unavailable) | ✓ |
| mineru | `mineru[pipeline]` installed in `ds0509` (CLI: `...\ds0509\Scripts\mineru.exe`) | ✓ |
| paddlepaddle | 3.3.1 (CPU) + paddleocr 3.7.0 + paddlex 3.7.2 in `ds0509` | ✓ |

> Note: there is **no conda env `ds0508`** on this host; user confirmed `ds0509` was intended.

## 3. One-command inventory / 关键路径速查

```powershell
$PY = 'C:\Users\data\miniconda3\envs\ds0509\python.exe'     # ds0509 = working ML env
$MINE = 'C:\Users\data\miniconda3\envs\ds0509\Scripts\mineru.exe'
```

- **PDF → Markdown (MinerU, CPU pipeline):**
  ```powershell
  & $MINE -p input.pdf -o output_dir -b pipeline --formula False --table False
  # optional page slice & language hint:
  & $MINE -p input.pdf -o output_dir -b pipeline -s 0 -e 5 -l ch
  ```
  Outputs in `output_dir/<name>/`: `<name>.md`, `*_content_list.json`, `*_middle.json`, `*_model.json`.
  - **K12 workaround (long PDFs):** the doc-analysis worker 502s intermittently on this CPU box. For text-layer PDFs run `-m txt` in **page windows ≤6 pp** (`-s/-e`) and merge the `txt/<name>.md` outputs (done for Weber-Wulff, see PROGRESS Session 10). **Each window MUST use a distinct `-o` dir** — MinerU writes to `<out>/<stem>/txt/<stem>.md`, so a second window with the same `-o` silently overwrites the first (Session 12, GLTR). Merge windows into `<stem>/auto/<stem>.md` and register in `corpus._LOCAL_MD`.
  - Accessing MinerU-merged corpus: `corpus.md_path_for(arxiv_id)` / `corpus.resolved_evidence(question)` (multi-paper evidence pool resolver, Session 12).
- **OCR (PaddleOCR 3.x, CPU):** (English OK / Chinese currently broken — see §5)
  ```python
  from paddleocr import PaddleOCR
  ocr = PaddleOCR(lang='ch', enable_mkldnn=False)   # enable_mkldnn=False REQUIRED (onednn bug, Win CPU)
  res = ocr.predict(input='img.png')                # -> res[0]['rec_texts']
  ```
- **Unified LLM client (any backend):**
  ```python
  # tools/llm/client.py — backends: opencode (default) | openai (OpenAI-compatible:
  # DeepSeek/DashScope/OpenRouter/Moonshot/Kimi). Ollama backend REMOVED 2026-09-16.
  from tools.llm.client import LLMClient, Message
  c = LLMClient(backend="opencode")                      # default: opencode/big-pickle (hosted free model)
  r = c.chat([Message(role="user", content="hello")], json_mode=True, max_tokens=512)
  # c = LLMClient(backend="openai", model="deepseek-chat")   # needs OPENAI_BASE_URL/OPENAI_API_KEY
  ```
  - The opencode backend spawns `opencode run --format json` (prompt passed via `-f` temp file to dodge Windows argv-quoting on `"…"` prompts; message text must precede `-f`, which is a greedy array flag). The call also passes `--auto` (Session 12): headless runs previously auto-rejected a `Temp\*` permission request from the model's tool use and returned no text. `--pure` keeps plugins out.
  - `max_tokens` → OpenAI-compatible `max_tokens`; always set it to bound runaway generation.
  - Smoke (no keys): `python -m tools.llm.smoke_test mock` (spins an ephemeral mock API server, PASS expected 3/3).
  - Smoke (default model): `python -m tools.llm.smoke_test opencode` (3/3 PASS verified 2026-09-16, `opencode/big-pickle`).
- **Pipeline (P2, discovery → evidence → draft → L6 gate → P3 judge):**
  ```powershell
  & $PY -m tools.pipeline.test_pipeline mock        # ephemeral mock API server, ~0.1 s, 19/19
  & $PY -m tools.pipeline.test_pipeline real        # opencode/big-pickle, ~2 min, 18/18
  ```
  - **Live S_lit discovery rails** (`tools/pipeline/corpus.py`): env `S_LIT_BACKEND=seed|arxiv|orx`, or `discovery_backend=` on `Pipeline.run`. `arxiv` = live arXiv API (free, no key — **verified reachable 2026-09-16, ~1 s**); `orx` = shell to `orx discover keyword <q>` when the binary is on PATH (not installed here), else falls back arxiv→seed. Seed scoring is always available and deterministic → tests stay stable.
  - `result["validation"]["judge"]` = P3 DAS-Bench-style rubric verdict `{label, score, checks, feedback, judge_model}`; the judge uses the same LLMClient (default `opencode/big-pickle`; DAS convention prefers a cloud ≥300B-class judge — `judge_model` records which model actually reviewed).
- **Benchmark-style evaluation (DAS-Bench 16-criterion preview, Session 11):**
  ```powershell
  & $PY -m tools.eval.bench_eval                 # real: ALL 5 scenarios in ONE call (see note)
  & $PY -m tools.eval.bench_eval --scenarios P-A,P-B,P-C,001,019  # explicit list
  # mock (deterministic regression): start tools.llm.mock_openai_server on :8201, then
  & $PY -m tools.eval.bench_eval --backend openai --base-url http://127.0.0.1:8201/v1 --model mock-api
  ```
  Re-implements the 16 criteria (BSC·MAR·TSQ·HDQ) verbatim from `external/DAS/DAS-Bench/benchmark/evaluation_protocol.md`; artifacts scored by our LLM judge (recorded via `judge_model`). Report: `_eval_out/bench_pilot_das.md`. **⚠ `--out` OVERWRITES the whole report per invocation — always run the complete scenario set in one call to keep a canonical report.** Sidecar cache `_eval_out/bench_cache/<id>.json` merges non-run scenarios as `cached (vintage run)` (Session 16).
- **Evidence-grounded QA (`qa` scenarios, Sessions 17–18):** `--scenarios QA-1,…` — corpus-anchored or Qasper-style questions. A `seed_id` routes the question to the **grounded extractive-answer node** (`tools/pipeline/answer.py`, skips the survey graph) — "answer the question, not the paper". Gold-token fact hits + `score_qa` correctness/groundedness judge; `QA pilot` table in the report (excluded from the DAS family means). Qasper dev v0.3: `qasper-dataset.s3.us-west-2.amazonaws.com/qasper-train-dev-v0.3.tgz` (paper keys are arXiv IDs). Use `$PY -X utf8 …` to avoid cp1252 decode noise in the opencode subprocess.
- **Render a manuscript to PDF (`tools/eval/render_manuscript.py`, Session 15 — MAR substrate):**
  ```powershell
  & $PY -m tools.eval.render_manuscript <artifact.md> <out.pdf>   # prints "OUT <pdf> PAGES <n>"
  ```
  pandoc + MiKTeX xelatex + Microsoft YaHei (CJK) — both already installed (no new deps); page count via pypdf. The bench pipeline renders each scored artifact automatically to `_eval_out/manuscripts/<id>_manuscript.pdf` with a `pdf pg` report column. A text-only LLM judge still cannot score the MAR *Layout* axis — that needs a ≥300B page-aware judge (blocked).
- **Download a test paper** (arXiv reachable from this host): `Invoke-WebRequest -Uri https://arxiv.org/pdf/<ID> -OutFile x.pdf`
- **L-6 one-command self-check / 一键自检 (Session 22)** — the offline safety net in a single call (unit + integration + evolution cadence, ~15 s, zero LLM):
  ```powershell
  ./self_check.ps1              # or: & $PY -X utf8 -m tools.eval.self_check
  ./self_check.ps1 -Full        # + live LLM judge cadence (~1.5 min)
  ./self_check.ps1 -WithReal    # also `test_pipeline real` (needs opencode CLI)
  ```
  Runs `tools.eval.test_evolution` (31 deterministic guard tests) → `test_pipeline mock` (34/34) → `evolution_sprint --quick`; exit code is the max (GREEN 0 / WARN 1 / FAIL 2) so it gates directly.
- **WS-C self-evolution loop (E-3/E-4/E-5, `tools/eval/evolution*.py`, Session 22)** — scheduled measurement + regression detection + human-gated repair (never auto code/prompt change, never a commit):
  ```powershell
  & $PY -X utf8 -m tools.eval.evolution_sprint --quick   # zero-LLM cadence
  & $PY -X utf8 -m tools.eval.evolution_sprint           # + live judge sanity
  & $PY -X utf8 -m tools.eval.evolution_sprint --report-only
  & $PY -X utf8 -m tools.eval.test_evolution             # deterministic guards (temp-isolated)
  ```
  Writes ONLY ledgers under `_eval_out/`: `tickets.json` (E-3 debug board, one-open-per-component, auto-closed on PASS), `deps_ledger.json` (E-4 version pins + drift detection), `feedback/feedback.jsonl` (E-5 provenance + real-gold quota), `revisions.json` (numbered human-gated bumps), `evolution_sprint.md` (the one-screen review). Evolution triggers come only from external measurement; a repair is *eligible* only after N≥3 sustained cadences AND Δ≥2σ AND no mock/gold regression. Design + evidence: `docs/design/self-evolution-mechanism.md`.
- **D-3 cross-model judge matrix (`tools/eval/judge_matrix.py`, Session 22)** — score the frozen proxies through several judge vantages; a promotion delta must survive a *different* judge:
  ```powershell
  & $PY -X utf8 -m tools.eval.judge_matrix --judges free-opencode,judge-strong --rounds 3
  # deterministic offline: start mock_openai_server on :8201, then
  & $PY -X utf8 -m tools.eval.judge_matrix --judges mock-api,mock2 --backend openai --base-url http://127.0.0.1:8201/v1
  ```
  Report `_eval_out/judge_matrix.md` = topic×judge Totals + cross-judge spread + D-4 provenance. One free model → single-column matrix (states it cannot corroborate); add `judge-strong` (needs `OPENAI_API_KEY`) for a real second vantage.
- **L-4 citation-verification checklist (agent-side, no code path)** — before any manuscript is treated as final, run this checklist against the References (the `citation-verification` skill guidance; scripts in `tools/citation-verify/` stay reference-only):
  1. every `arXiv:<id>` resolves at `https://arxiv.org/abs/<id>` (the L6 gate already rejects malformed IDs);
  2. the cited paper's *title* matches the claim it supports (spot-check via the local MinerU parse or arXiv abstract);
  3. no reference appears in the sheet that no inline `(arXiv:…)` in the body uses, and vice-versa;
  4. a quote backing a claim is verbatim-grounded (already enforced by the L6 5-gram gate; `gate_coverage` mutation check proves the shield fires).
- **Scheduled capability & benchmark snapshot (`tools/eval/capability_report.py`, Session 23)** — one dated screen of every capability's current benchmark performance **plus the base-model/tool config that produced it** (reads cached `_eval_out/` artifacts; offline, ~0 s; `--live` runs a quick health+deps cycle first). It is refreshed automatically as **step 8 of every `evolution_sprint`**, and on demand:
  ```powershell
  & $PY -X utf8 -m tools.eval.capability_report            # -> _eval_out/capability_report.md
  & $PY -X utf8 -m tools.eval.capability_report --live     # re-measure (quick) first
  ```
  To run it **on a schedule / 定时** without hand-writing the recipe, use the shipped idempotent registrar (registers the **offline** `evolution_sprint --quick` — no LLM, no key — as a daily Windows task; `-At` sets the time, `-Unregister` removes it):
  ```powershell
  pwsh -File tools/web/schedule_task.ps1 -At 09:00        # register / re-register
  pwsh -File tools/web/schedule_task.ps1 -Unregister      # remove
  Get-ScheduledTask -TaskName research_foodie-daily-cadence | Get-ScheduledTaskInfo
  ```
  The *live* model-backed cadence is deliberately **not** scheduled — the free hosted judge is currently credit-blocked (opencode.ai returns HTTP 401 "No payment method"), so only the key-free offline loop runs unattended.
- **Deterministic §4.6 ablations, model-free (`tools/eval/ablations.py`, Session 24)** — offline, no LLM, no key: (a) grounding-gate ON/OFF draft-leakage on a fixed fixture, (b) cached 30-topic pool coverage, (c) median-of-N judge spread from `variance_runs.json`. Writes `_eval_out/ablations.md` (feeds paper §4.6):
  ```powershell
  & $PY -X utf8 -m tools.eval.ablations                    # -> _eval_out/ablations.md
  ```
- **D-5 key-hygiene audit, model-free (`tools/eval/key_hygiene.py`, Session 25)** — offline, no LLM, no key: walks the tracked source tree (skips `external/`, `_demo_downloads/`, `_eval_out/`, `.venv`, …) and reports hard-coded credential *literals* (sk-/AWS/GCP/Slack/GitHub/HF/PEM/bearer/`*_key=` long values). Scans secret **values**, never variable **names** (so `os.environ["OPENAI_API_KEY"]` is fine), **masks** every match, and exits non-zero on any finding (pre-commit-ready). Writes `_eval_out/key_hygiene.md`; refreshed automatically at cadence step 8:
  ```powershell
  & $PY -X utf8 -m tools.eval.key_hygiene                  # -> _eval_out/key_hygiene.md (expect: CLEAN, 0 findings)
  ```
- **OpenResearch-style parallel *autoresearch* (`tools/pipeline/autoresearch.py`, Session 26)** — offline, no LLM, no key: the unique `openresearch.sh` primitive (fan one query into K orthogonal research directions, pursue each in an **isolated worktree** in parallel, then **merge** with per-direction source divergence). It reuses `corpus.resolved_evidence` + the L6 grounding gate and does **not** require the `orx` binary:
  ```powershell
  & $PY -X utf8 -m tools.pipeline.autoresearch "how reliable are AI-text detection tools?" --directions 4   # -> _eval_out/autoresearch/<slug>/AUTORESEARCH.md (+ one wt-<id>/ per direction)
  ```
- **Base-model options (三种选项, env-only — pick with `LLM_PROFILE`; no keys ever committed):**
  | profile | draft / qa | judge | needs |
  |---|---|---|---|
  | `free-opencode` (default) | opencode hosted free | opencode hosted free | — |
  | `openai-compat` | OpenAI-compatible provider | same provider | `OPENAI_API_KEY` |
  | `judge-strong` | opencode hosted free | OpenAI-compatible (strong) | `OPENAI_API_KEY` |
  Redirect the hosted free model (e.g. to **Qwen 3.8 Flash**) with `OPENCODE_MODEL=opencode/qwen3.8-flash`; run the *whole* pipeline on a Qwen API via `LLM_PROFILE=openai-compat` + `OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1` + `OPENAI_MODEL=…`. The active config is stamped into every report (D-4) and into `capability_report.md` §1; guards in `tools/eval/test_capability.py`.

## 3.0 End-to-end usage flow / 端到端使用流程

> 中文速览：本节回答一个普通用户的问题——**"我想调研 XX 问题，该怎么用这个工具？"** 五步走：(1) 写下研究问题 → (2) 选证据来源轨道 → (3) 设置输出**干货**（密度/语言/页数档位）→ (4) 设置输出**符合规范**（DAS-16 判题规范、L6 确定性门、引用核验、PDF 渲染规范/F 验证）→ (5) 运行并迭代（CLI 或 web dashboard）。每步给"已实现 knob"（直接可用）与"规划 knob"（Phase X/D，标注不可用），不夸大。

### 3.0.1 Step 0 — 从一个"研究问题"开始（不是从工具开始）

The tool is *question-first*. Write the survey-style question in one line, exactly the form the benchmark uses:

```text
P-A  "How reliable are automatic detection tools for AI-generated text?"
001  "Tool Learning and Function Calling for LLM Agents"
QA-6 "What does the corpus say about …?"      (answered from the local 3-paper pool)
```

Then choose a **track** — which determines the graph:

| Your intent | Track | Entry point | Evidence source |
|---|---|---|---|
| 写一篇综述草稿 | survey | `tools.pipeline.test_pipeline real` | seed corpus / arXiv live (`S_LIT_BACKEND`) |
| 就语料回答一个具体问题 | grounded QA | `bench_eval --scenarios QA-*` | local `_LOCAL_MD` pool |
| 给批量话题打分（跑数） | benchmark battery | `bench_eval` / `pools_30` | scenario sets in `bench_eval.py:79-366` |

### 3.0.2 Step 1 — 选证据来源轨道（discovery rail）

```powershell
$env:S_LIT_BACKEND = 'seed'    # 只有本地语料（确定性、离线、测试可复现）
$env:S_LIT_BACKEND = 'arxiv'   # 实时 arXiv API（免费无 key，实测 ~1.1 s）— 20-09-16
$env:S_LIT_BACKEND = 'orx'     # auto-research 外壳（本机未装 → 自动回退 arxiv→seed）
# 每次运行都显式声明来源；seed 是离线默认，测试稳定靠它。
```

### 3.0.3 Step 2 — 设置"输出干货"（输出密度/形态档位）

干货 = 结果信息密度可配。当前可调的 knob（已实现）：

| 干货维度 | 已实现 knob | 说明 |
|---|---|---|
| 判题（输出质量门） | `validation.judge {label, score, checks, feedback}` | DAS-Bench 16 轴细化 |
| 长度/页数 | `render_manuscript x.md out.pdf` → `PAGES n` | pandoc + xelatex + YaHei |
| 语言 | LLM 自带双语能力（prompt/语料决定） | 无独立 flag，见规划 knob |
| 批量数量 | `bench_eval --scenarios …` · `pools_30 --limit N` · `--judge K` | 覆盖度/成本权衡 |

规划 knob（Phase X/D，**未实现**，做基线后再上）：`语言/篇幅/深度` 显式档位、密度打分、草稿 vs 判题模型分 lane（D-2/D-3）——目标把"草稿字数 3357、判题 1.0"这类产出固化成语料级指标。

### 3.0.4 Step 3 — 设置"输出符合某种规范"（spec/格式约束）

结果要**符合某套规范/标准的文档**时，把规范挂到门禁上：

| 你想符合的规范 | 工具内对应 | 状态 |
|---|---|---|
| 学术论文文风与引用 | STORM-style outline + full-text claims + `tools/citation-verify` | 已实现（引用核验见 TOOL-COMPARISON） |
| DAS-Bench 16 轴评审规范 | `validation.judge` + `bench_eval` 报告 | 已实现（pilot P-A 2.62 / P-B 3.19） |
| 确定性事实门（L6） | `tools/pipeline/validate.py`（写时反幻觉过滤） | 已实现 |
| 排版规范（CJK/边距/页数） | `render_manuscript`（YaHei、pandoc） | 已实现（MAR Layout 轴需 ≥300B page-aware 判题） |
| 自演化基线规范（不允许回归） | Phase X `health_check` + `gate_coverage` + `baselines.json` | 规划（WS-C） |
| 判题模型是 ≥300B 大模型 | `>>300B` conventions — DAS 默认 | 需 key/GPU（Phase D-3，`judge_model` 已记录实际判题模型） |

关键原则：**要符合的规范 = 判题时挂哪条 rubric**。目前因判题模型是 `opencode/big-pickle`（free 权重方向性），DAS-16 判分为 *directional*（见 AGENTS 质量门）。

### 3.0.5 Step 4 — 运行 + 看结果（CLI 或 web）

```powershell
# CLI：一条命令跑完 + 看报告
& $PY -m tools.eval.bench_eval                        # 报告 _eval_out/bench_pilot_das.md
# 调研一个问题（用户入口）：全程接地综述 → Markdown + PDF 手稿
& $PY -X utf8 -m tools.pipeline.run_survey --question "GPT detectors bias against non-native writers"
#    --mock  确定性离线 demo（~1 s，输出 _eval_out/mock_manuscripts/，明确标注 MOCK）
#    --fast  性能档：单遍写作（revisions 上限为 1）——演示/夜间批处理更快出稿
#    --backend arxiv  指定发现 rail
# 手稿/PDF 落在 _eval_out/manuscripts/<slug>.{md,pdf}；log 打印 per-node 计时，便于性能调优
# Web dashboard（WS-B，已实现）：触发/取消/SSE tail/dashboard/manuscripts/feedback
#   Runs 页顶部新增"Try it — answer a research question"输入框 + Mock/Real 切换（明确标注）
#   "Live research mission"看板：跑 survey 时按阶段叙述 what/how/why（业务语言+技术要点）
#   已完成 survey run 有只读研究视图：http://127.0.0.1:8000/runs/<id>/mission
& $PY -m uvicorn tools.web.app:app --host 127.0.0.1 --port 8000
# 打开 http://127.0.0.1:8000/
```

**健康自检（WS-C E-2，已实现）** — 方差感知阈值对照冻结基线，退出码 0 GREEN / 1 WARN / 2 FAIL：

```powershell
& $PY -X utf8 -m tools.eval.health_check --freeze     # E-1 基线冻结（零 LLM）→ _eval_out/baselines.json
& $PY -X utf8 -m tools.eval.health_check --quick      # 跳过 <10 min 判题 sanity，其余全跑
& $PY -X utf8 -m tools.eval.health_check              # 全量：mock + pools + arxiv_probe + gate_coverage + judge sanity
```

**模型路由（WS-D D-1/D-2，已实现）** — judge lane 可走已注册的强模型（其余 lane 保持免费 opencode）：

```powershell
$env:LLM_PROFILE='judge-strong'; $env:OPENAI_BASE_URL='https://api.deepseek.com/v1'
$env:OPENAI_MODEL='deepseek-chat'; $env:OPENAI_API_KEY='sk-…'   # key 只进环境变量，永不入库
& $PY -X utf8 -m tools.eval.bench_eval --profile judge-strong    # 或 health_check / variance_run
```

**断线续跑（run memory，已实现）** — 长跑在中间断线/死机后，重开同一命令即可从已完成的 topic 继续，不重付：

```powershell
& $PY -X utf8 -m tools.eval.bench_eval                # 默认 resume：跳过 ledgers 中已 done 的 id
& $PY -X utf8 -m tools.eval.bench_eval --no-resume    # 强制全部重跑
& $PY -X utf8 -m tools.eval.variance_run --rounds 2   # variance/topic 级续跑（逐 topic crash-safe 落盘）
```

进度记在 `_eval_out/ledgers/<command>.json`（指纹 = profile + id 集合；换模型/换 id 不会误续跑）。Web dashboard 里中断的 run 会标 `interrupted` 并可直接 Resume。

**只读静态导出（F-3，已实现）** — 活版 dashboard 只能本地跑（SSE/cancel 需后端）；
部署 GitHub Pages 的形态是只读快照：

```powershell
# 生成 gh-pages/（3 页 + manuscripts/*.pdf 副本，纯 stdlib，无需 uvicorn/fastapi）
& $PY -X utf8 -m tools.web.export_static --out gh-pages
```

GitHub Pages **只托管静态文件**（不支持任何服务端代码），发布源设
`branch: main / folder: /gh-pages` 即可随 commit 自动重发布；每次重新导出后 commit 该目录。
`.nojekyll` 已包含，避免 Jekyll 处理。

### 3.0.6 Step 5 — 反馈 & 迭代（自演化入口）

- `POST /feedback`（web）或直接追加 `_eval_out/feedback/feedback.jsonl` → 这是 Phase X E-5 的语料入口。
- 迭代规则（Phase X 设计，见 `docs/design/self-evolution-mechanism.md`）：小改动跑 `health_check`（方差感知阈值，2σ=±0.5 FAIL）；结构改动跑 `gate_coverage`（≥20 变异全杀）；晋升征求 N≥3 轮、Δ≥2σ、mock/gold 无回归 + 换判题人复证（R 期）。

---

## 3.1 Usage & demo walkthroughs / 用法与演示

> 中文速览：本小节把"怎么用"钉死成两份东西——(1) **工具速查表**（每条工具：用途 / 验证过的命令 / 版本引脚 / 对应已知问题）；(2) **四条端到端 demo**（PDF→接地综述→渲染、接地 QA、30 话题判题库电池、人工 L6 判题检查）。每条给出可复制的命令与预期产物。规划对应 `docs/PLAN.md` §8：L-5（工具使用入档）· Phase X（自演化基线）· Phase F（web 前端）· Phase D（**模型接入与路由**——demo 里的 `opencode` 是零 key 默认 lane，注册任一 OpenAI 兼容 API key 后可由 profile 路由到更强判题模型，见 `docs/PLAN.md` §8 Phase D）。
> **All commands below already ran green in Sessions 9–20** (with the recorded caveats). `$PY`, `$MINE`, `$UTF8` as in §3.

### 3.1.1 Per-tool usage cheat-sheet / 逐工具速查

> **模型后端（Phase D）**：demo 全部用零 key 的默认 profile（`opencode`，`OPENCODE_MODEL`=opencode/big-pickle）。注册任一主流 API key 后，可用 **judge 强模型 lane** —— 设 `OPENAI_BASE_URL`/`OPENAI_MODEL`/`OPENAI_API_KEY`，跑 `health_check`/`bench_eval`/`variance_run` 时把 judge 路由到它（D-1/D-3）。key 只走环境变量，永不入库。

| Tool | Purpose / 用途 | Verified command (copy-paste) | Ver. pin (E-4 ledger) | Known issue |
|---|---|---|---|---|
| `mineru.exe` | PDF → Markdown (CPU) | `& $MINE -p in.pdf -o out -b pipeline --formula False --table False` | `mineru[pipeline]` in `ds0509` | K12 → use `-m txt` + page windows ≤6pp, **distinct `-o` per window** |
| MinerU window **merge** | long PDFs, text layer | merge `txt/*.md` → `<stem>/auto/<stem>.md`; register via `corpus.md_path_for(arxiv_id)` | — | K12 (silent overwrite if same `-o`) |
| arXiv API **live rail** | realtime topic discovery | `S_LIT_BACKEND=arxiv` on `Pipeline.run` | backends `seed\|arxiv\|orx` | reachable ~1.1 s (verified 2026-09-16); free; no key |
| `orx` CLI | auto-research shell (uninstalled here) | `S_LIT_BACKEND=orx` — falls back arxiv→seed when binary absent | not installed | Phase R item |
| `tools.pipeline.test_pipeline` | full S_lit→…→judge smoke | `& $PY -m tools.pipeline.test_pipeline mock` (~0.1 s) / `real` (~2–4 min) | — | real run is live-LLM; rate OK |
| `tools.eval.bench_eval` | DAS-16 crit. benchmark | `& $PY $UTF8 -m tools.eval.bench_eval --scenarios P-A,P-B,P-C,001,019` | — | **`--out` overwrites whole report → always run complete set in ONE call** (cache merges vintages) |
| `tools.eval.pools_30` | 30-topic judge battery | `& $PY $UTF8 -m tools.eval.pools_30` | — | seed rail only; external pools Phase R |
| `tools.eval.variance_run` | judge-noise measurement | `& $PY $UTF8 -m tools.eval.variance_run` | — | judge P-A σ≈0.53 → median-of-3 (L-3) |
| `tools.eval.add_paper` | one-command corpus adder | `& $PY $UTF8 -m tools.eval.add_paper <arxiv_id>` | — | verified on `1703.10344` (12 pp) |
| `tools.eval.render_manuscript` | draft → PDF | `& $PY -m tools.eval.render_manuscript x.md out.pdf` | pandoc + MiKTeX xelatex + YaHei | MAR Layout axis needs page-aware judge |
| `tools.llm.client` | unified LLM gateway | `LLMClient(backend="opencode")` default | opencode CLI, `opencode/big-pickle` | prompt-must-precede `-f`; `--auto` `--pure`; `-X utf8` on Win |
| `tools.llm.smoke_test` | client sanity | `python -m tools.llm.smoke_test mock` / `opencode` | 3/3 PASS | no keys needed |

### 3.1.2 Demo A — PDF → grounded draft → manuscript (端到端拉通)

```powershell
$PY = 'C:\Users\data\miniconda3\envs\ds0509\python.exe'
$UTF8 = '-X', 'utf8'
& $PY -m tools.pipeline.test_pipeline mock      # ① deterministic gate: expect 19/19
& $PY $UTF8 -m tools.pipeline.test_pipeline real  # ② real LLM: expect verdict PASS, judge=pass (~2–4 min)
& $PY -m tools.eval.render_manuscript docs/design/resources/_demo_draft.md _eval_out/manuscripts/demo.pdf  # ③ PDF
```
- ② produces a LangGraph `result` with `outline` (3 sections, STORM-style) + `validation.judge {label, score, checks, feedback}`; a grounded-claim filter runs at write time (fabrications rejected, then JSON-normalized).
- ③ prints `OUT … PAGES n`. Bench scoring auto-renders every artifact to `_eval_out/manuscripts/<id>_manuscript.pdf`.
- **Demo topic**: "How reliable are automatic detection tools for AI-generated text?" (Liang `2304.02819` + Weber-Wulff `2306.15666` + GLTR corpped, Sessions 10/12).

### 3.1.3 Demo B — Evidence-grounded QA (`qa` scenarios)

```powershell
& $PY $UTF8 -m tools.eval.bench_eval --scenarios QA-6,QA-7,SQ-1,PQ-1,Qasper-1 2>&1 | Select-Object -Last 40
```
- `seed_id` routes to the **grounded extractive-answer node** (`tools/pipeline/answer.py`) — answers the question, not the survey. Gold-token fact hits + `score_qa` judge columns; QA rows are **excluded** from the DAS-family mean (separate `QA pilot` table).
- Requires Qasper dev v0.3 (`qasper-train-dev-v0.3.tgz`, S3) for QA/Qasper rows; corpus-anchored rows (QA-6/7) need only the local `_LOCAL_MD`.

### 3.1.4 Demo C — 30-topic judge battery + variance (measurement & baselines)

```powershell
& $PY $UTF8 -m tools.eval.pools_30        # → _eval_out/pools_30.json + pools_30_report.md (22/30 topic pools; 10 judged → Total 3.13)
& $PY $UTF8 -m tools.eval.variance_run    # → _eval_out/variance_runs.json (P-A 3.88±0.53, P-B 3.31±0.00, P-C 3.53±0.13)
```
- Feeds E-1 `_eval_out/baselines.json` (PLAN §8 Phase X) — the自演化 baseline freeze. Re-run after any prompt/judge change; a ±0.5-scale delta on P-A is *within its own judge noise* until L-3 median-of-3 lands.

### 3.1.5 Demo D — manual L6 gate inspection (human-in-the-loop)

```powershell
# trigger + inspect the DAS-Bench-style rubric verdict on one topic:
& $PY $UTF8 -m tools.eval.bench_eval --scenarios P-A --out _eval_out/bench_demo.md
Get-Content _eval_out/bench_demo.md | Select-String -Pattern "checks|feedback" -Context 0,6
```
- The rubric (`validation.judge.checks`) is keyed to the 16 DAS-Bench criteria (BSC·MAR·TSQ·HDQ) re-implemented verbatim from `external/DAS/DAS-Bench/benchmark/evaluation_protocol.md`.

---

## 4. P1 smoke-test results / 冒烟实测结果

### 4.1 MinerU — PASS ✓
- Input: `_demo_downloads/liang2023_test.pdf` = arXiv:2304.02819 (Liang et al., "GPT detectors are biased…"), 1.9 MB, 3 pages tested.
- Command: `mineru -p liang2023_test.pdf -o mineru_out_ds0509 -b pipeline -s 0 -e 2 --formula False --table False`
- Result: 3/3 pages; re-run 2/2 pages. Output `liang2023_test.md` (15.7 KB): title/authors/affiliations/abstract all preserved, markdown-clean, no placeholder text.
- Model cache: downloaded on first run (auto, from default source).

### 4.2 PaddleOCR — PARTIAL ⚠
- Input: `_demo_downloads/ocr_test.png` (900×260, English + 中文 lines, rendered with `msyh.ttc`).
- English line: recognized ✓ (minor `I→l` misread, clip cut leading `l` on line 3).
- Chinese line: detection found the line but **recognition returned placeholder `?`** — see §5 known issue.
- Console note for Windows: set `$env:PYTHONIOENCODING='utf-8'` before printing CJK results.

### 4.3 Downloads / artifacts in `_demo_downloads/` (gitignored)
`liang2023_test.pdf`, `mineru_out_ds0509/`, `mineru_out2/`, `ocr_test.png`, `ocr_result.txt`.

## 5. Known issues & workarounds / 已知问题与临时解法

| # | Issue | Status | Workaround / next step |
|---|---|---|---|
| K1 | `git clone github.com/...` fails with `Recv failure: Connection was reset` (smart-HTTP blocked) | Solved | Download tarballs: `Invoke-WebRequest https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/<br> -OutFile x.tgz` then `tar -xzf …` |
| K2 | Direct `/arxiv.org` fetch blocked in webfetch but **HTTP download works** | Info | Use `Invoke-WebRequest` for arXiv PDFs (verified OK) |
| K3 | `pytorch.org` `HEAD` → 403; wheel downloads via `--index-url https://download.pytorch.org/whl/cpu` work | Info | Use the `/whl/cpu` index for CPU wheels |
| K4 | `mineru[cli]` alone is NOT enough for local pipeline → `ModuleNotFoundError: transformers` then `shapely` (pipeline backend = separate extra) | Solved | Install `mineru[pipeline]` (pulls shapely/transformers/onnxruntime/PyYAML/…) |
| K5 | PaddleOCR 3.x CPU oneDNN executor bug: `NotImplementedError: ConvertPirAttribute2RuntimeAttribute … onednn_instruction.cc` | Solved | `PaddleOCR(lang='ch', enable_mkldnn=False)` |
| K6 | PaddleOCR 3.x: `ValueError: Unknown argument: use_gpu` | Solved | Argument removed in 3.x; use default device or `enable_mkldnn` to control CPU path |
| K7 | **Chinese recognition returns `?` placeholders** (English OK) | **Resolved** (2026-09-16) | Re-run after rec-model files fully downloaded: `PaddleOCR(lang='ch', enable_mkldnn=False)` recognizes `中文学术文献扫描测试页 2026` at score 0.999 — earlier `?`s were a partially-initialized model, not a config bug (PROGRESS Session 9/10) |
| K8 | opencv cross-conflict: paddleocr pinned `opencv-contrib-python==4.10.0.84`; `cv2` reports 4.10.0 (mineru wanted ≥4.11). MinerU still parsed fine | Monitored | If MinerU breaks later, isolate MinerU (dedicated env) from Paddle env |
| K9 | Windows console cp1252 can't print CJK → `UnicodeEncodeError` | Solved | `$env:PYTHONIOENCODING='utf-8'` (or write results to UTF-8 file) |
| K10 | LFS stub files (DAS `examples/*.pdf` = 0.10 KB pointers) unusable as samples | Info | Download real PDFs from arXiv instead; or `git lfs pull` in a real clone |
| K11 | **Ollama server cannot bind any socket** — `listen tcp 127.0.0.1:11434: bind: An attempt was made to access a socket in a way forbidden by its access permissions` (WinError 10013/WSAEACCES); reproduced on `127.0.0.1:11440`, `0.0.0.0:11440`, `[::1]:11441`. Ollama client 0.32.14 installed, server cannot start | **Closed 2026-09-15** (user "方案 B") | Upstream: GitHub ollama#2627, #9444 (Windows port ACL / Hyper-V & Windows Hypervisor Platform reservations), #16270 (Windows Firewall Control blocks the hidden `ollama.exe` server spawned by `ollama app.exe`). Fix applied: elevated `Disable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform` + reboot → server now listens on `127.0.0.1:11434` (kept alive by the Ollama tray app). Alt. fixes that still apply: global firewall rule for the Ollama binaries, or elevated `ollama serve`. During the block: `python -m tools.llm.smoke_test mock` + opencode free models for LLM steps |
| K12 | **MinerU CPU parse 502 Bad Gateway** — the local doc-analysis worker intermittently crashes (observed at Layout 14/46, OCR-det 424/514, OCR-rec 384/733; `-m txt` also reaches OCR-rec). Same Windows-CPU OCR instability family as K7 | Workaround ✓ (2026-09-16) | `-m txt` (use PDF text layer) **+ page-window slices** `-s X -e Y` (≤6 pp) with retry; merge the per-window `txt/*.md`. **Each window needs a distinct `-o`** (later window overwrites same-path output — GLTR Session 12). Worked for Weber-Wulff 46 pp (8 windows) and GLTR 6 pp (2 windows) |

## 6. Deferred by user decision / 已延后事项

- **Remote GPU / `orx up --remote`**: no GPU platform connected yet; opencode free models cover the LLM steps now. GPU-half of P1 → revisit later.
- **Local Ollama models**: **removed from the pipeline on 2026-09-16** (user decision "停掉ollama的部分"). `qwen2.5:3b` / `qwen3.5:4b` were pulled and tested in Session 6 (records in PROGRESS); the `ollama` backend was deleted from `tools/llm/client.py` and all callers. Default real LLM = opencode CLI free model (`opencode/big-pickle`).
- **Paid/cheap API keys** (DeepSeek/Qwen/Kimi, scite, etc.): not configured. A DAS-Bench-style judge gate now runs on the opencode free model (P3 preview — `validation.judge`), but the DAS convention's ≥300B-class cloud judge + threshold calibration still need keys (or a remote GPU tier).

## 7. Local model candidates (Ollama) / 轻量本地模型评估 (as of 2026-09-15; **superseded — Ollama backend removed 2026-09-16**) — historical evaluation kept for reference only; the pipeline now uses the opencode CLI free model.

Evaluated for the blueprint's small-model nodes (taxonomy plans, routing, claim plans, per-node drafting) on this Win11 CPU-only host. **No model pulled yet** (user decision: evaluate first). Verify host RAM (`systeminfo | Select-String "Total Physical Memory"`) before pulling >4B. As of 2026-09-15 (Session 6): pulling + inference deferred until **K11** (Ollama server cannot bind) is fixed by an admin action.

| Candidate | Size / quant | Disk | RAM incl. model | Fit in pipeline | Source & 实测 (2026-09-15) |
|---|---|---|---|---|---|
| `qwen2.5:3b` **← CPU fast tier (verified)** | 3.09B; ~Q4 | 1.9 GB (pulled) | ~4 GB | **Workhorse for CPU LLM steps**: no thinking mode, clean JSON; smoke ollama 3/3 PASS — bilingual 2.35 s, JSON-extract 2.31 s, claim-list arXiv-cite 11.98 s | ollama.com/library/qwen2.5 (2026-09-15) |
| `qwen3.5:4b` **← default-tier (think toggle verified)** | 4.66B; `latest`=~Q4 (3.4 GB pulled; Q8_0 = 5.3 GB); Apache-2.0 | 3.4 GB | ~6–8 GB | Routing / outlines / claims; EN+中文; tools+thinking; **multimodal (vision) → OCR fallback for K7**. ⚠ **Measured on CPU (2026-09-15): thinking is request-level `think` flag** — `think=true` (default) fills the whole budget with reasoning and puts the trace in `message.thinking` (≈4–5 tok/s; `content` empty unless `max_tokens` has headroom); `think=false` answers instantly (1.4 s for "4"; 11 s / 25 tok prime check) → default **`think=false`, opt in for reasoning-heavy steps** | ollama.com/library/qwen3.5 (2026-09-15) |
| `qwen3.5:2b` | ~2B; Q4 ~1.6 GB | ~1.6 GB | ~3 GB | Fast tier: tagging, label/refactor tasks; CPU ~30+ tok/s (not pulled yet) | same |
| `phi4-mini` | 3.8B; ~2.5 GB | ~2.5 GB | ~4 GB | Best CPU-only sweet spot; clean structured output; 30–50 tok/s on CPU (not pulled yet) | PromptQuorum 2026-08-28; PopularAI 2026 |
| `gemma4:e2b` | 2.3B eff; ~2 GB | ~2 GB | ~3 GB | Tiny fallback; 128k ctx; good instruction-following (not pulled yet) | ollama.com/library `gemma4` (2026-08) |
| `qwen3.5:9b` | 9.65B; `latest`=Q4_K_M 6.6 GB; Apache-2.0 | 6.6 GB | ~10–12 GB (need ≥16 GB RAM) | Local drafting-quality tier; EN+中文; tools+vision (not pulled yet) | registry.ollama.ai/library/qwen3.5 (2026-09-15) |
| ❌ not now: `qwen3.8:27b` / `gemma4:26b` | 15–24 GB | — | ≥24 GB | Reasoning tier → needs remote GPU, revisit later | PromptQuorum 2026-08-28 |

Notes:
- RAM rule of thumb (directional): 8 GB→7B, 16 GB→13–14B, 24 GB+→32B at Q4; CPU-only ≈3–8 tok/s on a 7B (LocalAIMaster, 2026-08-03).
- Context: Ollama agents recommend ≥64k ctx, but memory grows with `num_ctx` — use modest values (8k–32k) on CPU for this pipeline's chunks.
- **Judge node stays on cloud / cheap API** (DAS's own judges are 300B-class); no local <9B model is a judge.
- Adoption gate before pull: run a bilingual structured-output + tool-call smoke test, log result in PROGRESS.md.

## 8. Pipeline status & next steps / 流水线状态与下一步

| Phase | Blueprint exit criterion | Status |
|---|---|---|
| P1 | PDF→Markdown ✓ · OCR page ✓ (K7 solved 2026-09-15) · GPU reachable ➖ (deferred) · LLM ✓ (K11 closed 2026-09-15; Ollama backend removed 2026-09-16 — now opencode free model) | **done** — parsing ✓, OCR ✓, LLM ✓; packaged as `tools/llm/` |
| P2 | LangGraph S_lit→S_org→S_write→S_final + L6 validation gate; seed-corpus discovery; write-time grounded-claim filter | **done — minimal vertical GREEN, frameworks integrated, generalizes** (`tools/pipeline/`, `corpus.py`, `validate.py`, `judge.py`); mock 19/19 + real **`opencode/big-pickle` 18/18 (121.7 s, STORM outline 3 sections, full-text claims, draft 3357 chars, score 1.0, judge=pass)**; **2nd real paper (Weber-Wulff `2306.15666`) full loop PASS (149.8 s, 4 claims, score 1.0, judge=pass)**; **live discovery rail (arxiv) verified 2026-09-16** (seed remains offline default; orx CLI wired, binary absent) |
| P3 | DAS-Bench judge gate + threshold calibration (220 examples ≈4.3x) + `tools/citation-verify` | **preview — DAS-Bench-style judge gate LIVE** on opencode free model (`validation.judge=pass`, mock 19/19 · real 18/18); **DAS-Bench 16-criterion benchmark pilot done (Session 11): `tools/eval/bench_eval.py`, preview totals P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence → internal judge too lenient vs survey-level scoring (calibration now measurable)**; ≥300B-class judge + calibration deferred (keys / GPU) |
| P4 | Track B (PaddleOCR pipeline) + proactive loop | partial — OCR engine ✓ (Track B evidence layer now usable) |
| P5 | Robustness, ablations, cost report | **partial (Session 24)** — deterministic model-free ablations (`tools/eval/ablations.py` → `ablations.md`: gate leakage 8→0 · 0 false drops · pool coverage 73% · median-of-N spread ≈0.31); live judge-swap + formal cost report gated on a reachable model |

**Next-session checklist (`ds0509`):**
1. ✅ P1 + P2 built: `tools/llm/` (client, mock, claim-plan) + `tools/pipeline/` (state, corpus, validate, graph, test). Seed-corpus S_lit + L6 deterministic gate wired. See PROGRESS Session 6–8.
2. ✅ **Ollama fully removed (Session 8, 2026-09-16)** — backend deleted from `client.py`, all callers/documents updated; full-text claim extraction landed (real **14/14 in 58.1 s**, claims=4 with correct `section` attribution, score 1.0).
3. ✅ **Framework integration (Session 9, 2026-09-16)**: STORM-style outline (S_org `outline` → outline-driven S_write); OpenResearch/orx + arXiv **live discovery rails** (`S_LIT_BACKEND=seed|arxiv|orx`; arXiv verified reachable ~1 s; orx CLI adapter wired, binary absent); **P3 DAS-Bench-style AI judge gate** (`judge.py`, graph `finalize→gate→judge→END`, `validation.judge`). **mock 19/19 · real `opencode/big-pickle` 18/18 @121.7 s** (outline 3 sections, draft 3357 chars, judge=pass).
4. ✅ **Second real paper — generalization proven (Session 10, 2026-09-16)**: Weber-Wulff `2306.15666` (46 pp) MinerU-parsed via `-m txt` + page windows (K12 workaround), merged md 124,408 chars; full loop on `opencode/big-pickle` **PASS in 149.8 s** (4 grounded claims, outline 3 sections, draft 1725 chars, L6 score 1.0, judge=pass). Corpus now spans 2 papers (`_LOCAL_MD`).
5. ✅ **Benchmark-style evaluation vs DAS-Bench assets (Session 11, 2026-09-16)**: `tools/eval/bench_eval.py` re-implements the 16 DAS criteria verbatim; real pilot preview totals **P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence** → report `_eval_out/bench_pilot_das.md` (+ feasibility matrix: topics.json / rubric / published-results / eval-harness are local; DAS-2M pools, gold surveys, ≥300B judge are not). Signals: internal P3 judge too lenient vs survey-level scoring; seed-rail precision issue surfaced on DAS topic 001.
6. **Next bigger step:** (a) multi-paper evidence in S_lit (fetch + parse top-k full texts) to attack the MAR/multi-reference drag and enable real DAS topic instances; (b) P3 judge threshold calibration against the DAS-16 preview scores; (c) DAS-2M pools + ≥300B judge for a compliant DAS-Bench submission; (d) Track B / proactive-loop wiring.
7. If user approves API keys: set `OPENAI_BASE_URL`/`OPENAI_MODEL`/`OPENAI_API_KEY` and re-run smoke; the client speaks OpenAI-compatible dial (or keep `opencode/big-pickle` free for everything).

## 9. Repo hygiene notes / 卫生与约定

- `external/`, `tools/.venv/`, `tools/.venv-ocr/`, `_demo_downloads/` are gitignored. `tools/.venv` (the abandoned ad-hoc venv) may be deleted; `ds0509` is the live env.
- Commits: Conventional Commits, only on explicit request. Docs updated: `docs/PLAN.md`, `docs/PROGRESS.md` per session.
- All factual claims carry source + access date (per `AGENTS.md`).

## 10. References / 参考
- MinerU CLI: `mineru --help` (backends `pipeline|vlm-engine|hybrid-*`; effort `medium|high`).
- PaddleOCR 3.x: paddleocr.ai; model cache at `C:\Users\data\.paddlex\official_models\`.
- Bilingual conventions & quality gates: `AGENTS.md`; architecture: `docs/design/research-foodie-blueprint.md`.