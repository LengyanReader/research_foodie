# Research Foodie — Setup & Operations Runbook (设置与运行手册)

> **中文速览**
> 本文档是本仓库的**操作性手册**（bilingual）：基于 2026-09-15 P1 阶段的真实实测，记录环境怎么搭、哪些工具已跑通、每条命令、踩过的坑与临时解法、遗留问题，以及下一步怎么走。目标是"任何会话翻到本文档即可无缝继续"。
> **一句话现状**：MinerU PDF→Markdown 跑通；**PaddleOCR 中文识别已解决（K7 关闭）**；**统一 LLM client 已建**（`tools/llm/`，**默认后端 = opencode CLI 免费模型 `opencode/big-pickle`**，另支持任何 OpenAI 兼容 API）；**Ollama 后端已于 2026-09-16 彻底移除**（用户决定"不要再考虑 Ollama"，K11 历史排障见台账）；**P2 最小纵切已打通**（`tools/pipeline/`：S_lit 可插拔发现 rail + LangGraph 完整链 + L6 确定性校验 + 写时反幻觉过滤 + 全文 claim 抽取）；**三大参考框架已运行时整合（Session 9）**：STORM-style 大纲（S_org outline→S_write 大纲驱动写作）、OpenResearch/orx + arXiv **实时发现 rail**（`S_LIT_BACKEND=seed|arxiv|orx`，2026-09-16 实测 arXiv API 已可达 1.1 s）、DAS-Bench-style **AI 评审门**（P3 preview，`validation.judge`）；测试 mock **19/19** + real `opencode/big-pickle` **18/18** @121.7 s（draft 3357 字、outline 3 节、score 1.0、judge=pass）；**已在第二篇真实论文（Weber-Wulff `2306.15666`）上验证泛化（Session 10）**；**DAS-Bench 16 轴基准评测试点已完成（Session 11）**：`tools/eval/bench_eval.py`，预览总分 P-A 2.62 / P-B 3.19 / 001 2.44 / 019 no-evidence，报告 `_eval_out/bench_pilot_das.md`；远程 GPU / 付费 API 仍按用户决定延后。

- `Updated`: 2026-09-16
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
| Ollama client | 0.32.14 installed, **server not running**, no models pulled (user decision: defer) | ✓ |
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
| P5 | Robustness, ablations, cost report | not started |

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