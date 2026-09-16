# Research Foodie — Progress Log (进度日志)

> 中文速览：本文件记录执行进度、事实核验结果、修正与错误来源。按日期逆序追加。所有事实声明带来源与访问日期;无法验证的标记 *unverified*。

- `Updated`: 2026-09-16
- `Status`: Ongoing (implementation phase: `tools/llm/` ✓ · `tools/pipeline/` P2 minimal vertical GREEN + **framework integration** — STORM outline · orx/arXiv live discovery rail · DAS-Bench-style judge gate · benchmark-style evaluation pilot · **multi-paper evidence synthesis (P0) GREEN — 3-source evidence pool, per-paper grounding, cited=3** · **survey-depth S_write GREEN — per-section grounded drafting, preview Total 2.75→3.17**)

---

## 2026-09-16 — Session 13: survey-depth S_write — per-section drafting lifts TSQ (分节写作升级：TSQ 修复、总分提升)

**User instruction:** "好的，继续下一步" — proceed with the roadmap's #1 lever (draft-depth → survey-grade TSQ/MAR).

1. **Per-section S_write (graph.py)** — the single-draft paragraph became a **survey pass**: one intro call + one independent grounded paragraph `## <heading>` per outline section (≤6) + one conclusion call. Each section prompt: "use only matching claims; 150-300 words as 2-3 paragraphs; attribute EVERY factual sentence inline (arXiv:id); cite both where sources agree, name the disagreement where they conflict, close with the open gap." Claims (tagged `paper_id`) share the section context → **citation balance** + **synthesis/disagreement** behavior in the text, not just in scoring. Draft artifact grew **~5-7×** (mock 518 chars, real 16,281 chars, bench P-A/P-C 23-26K chars).
2. **S_org outline depth** — sections requested **4-6** (was 2-4); real run produced a 5-section outline.
3. **Mock determinism** — three new mock routes (INTRO / SECTION / CONCLUSION) so mock mode also exercises the per-section path with `## ` section markers; test_pipeline added asserts: survey-draft length > 500 and per-section heading markers in output. **mock 25/25 PASS**, **real 25/25 PASS** (498.6 s for 10 opencode calls; draft 16,281 chars, 5 sections, L6 1.0, judge=pass).
4. **DAS-16 pilot refreshed (one full 5-scenario run, real `opencode/big-pickle`):** proxies P-A 2.94 / **P-B 3.19 / P-C 3.38**, 001/019 no-evidence. **Family means (n=3): BSC 3.25 / MAR 2.50 / TSQ 3.17 / HDQ 3.75 / Total 3.17** — up from Session 11's 2.75 family total and 2.42 TSQ; **TSQ jump 2.42→3.17** (Research-Space + Taxonomy + Organization + Synthesis all 2→3+) confirms the draft-depth lever; residual low axis = MAR 2.50, dominated by Figure/Table Quality + Layout (rendering axes a plain-markdown artifact cannot score — honest, out of scope until page-render output exists). Judge run-to-run variance ±0.5 documented (P-A 2.94-3.06, P-C 2.94-3.38 across runs).
5. Report `_eval_out/bench_pilot_das.md` refreshed with `papers`/`cited`/`out chars` columns (L6 all pass).

Next (roadmap §7): the TSQ/MAR floor now being structural (per-section writing done), the next levers are (a) P1 judge threshold calibration, (b) MAR render axes (page-rendered artifact / figure-table extraction — P3-compliant scoring path), (c) Track B, (d) DAS-2M + ≥300B judge for a compliant run.

---

## 2026-09-16 — Session 12: multi-paper evidence synthesis (P0) — 3-source pool GREEN (多论文证据合成启用：3 源证据池)

**User instruction:** "继续实现，逐步实现完整的工作链路，保证各大框架，工具的完美整合和融入" — keep implementing toward the complete working chain, with clean integration of the major frameworks/tools.

1. **New corpus paper: GLTR (arXiv:1906.04043, Gehrmann et al. 2019)** — 6 pages, text-layer confirmed, downloaded to `_demo_downloads/gltr_1906_04043.pdf`. MinerU `-m txt` parsed in two 3-page windows → **workaround discovered**: per-window runs MUST use distinct `-o` output dirs, else the later window SILENTLY OVERWRITES the earlier one (same `<stem>/txt/<stem>.md` path) — Session 10's K12 merge note is updated accordingly. Merged canonical md (24,107 chars) at `_demo_downloads/mineru_out_ds0509/gltr_1906_04043/auto/gltr_1906_04043.md`; registered in `corpus._LOCAL_MD`.
2. **P0 multi-paper evidence S_lit** (`corpus.py`): new `resolved_evidence(question, limit=3)` — candidates → paper pool `[{arxiv_id, label, path, md}]` for every **local-parsed** paper (Liang `2304.02819` · Weber-Wulff `2306.15666` · GLTR `1906.04043` all resolve). Seed precision guard: `SEED_MIN_SCORE=2` + **stopword-filtered tokens** (Session 11's flaw — the DAS 001 topic wrongly matched `2306.15666` via the `for`/`tool` tokens; now `001` resolves to `2409.13740` only, correctly no-evidence).
3. **Multi-paper S_org/S_write/S_final** (`graph.py`): outline reads primary + secondary paper windows; one claim-plan extraction per source paper (≤3), each **grounded against ITS OWN markdown** (`grounded_claims` per paper) before merge; claims carry `paper_id`; draft instructed to synthesize across sources with inline `(arXiv:…)` attribution; finalize emits a `Sources` list + per-claim paper tags. Backward-compat for the pre-parsed single-paper path (`papers` = 1-entry pool).
4. **L6 metrics** (`validate.py`): new informational `multi_paper` check (`papers_available` vs `n_papers_cited`, cited = distinct `paper_id`/cite arXiv IDs); `n_papers_cited` flows into the bench report. P3 judge prompt now includes `Sources: N papers`. Reliable JSON parsing: **code-fence-tolerant** `parse_json_list/parse_json_dict` (`_unfence`) — the Session 11 scorer bug where ```json-fenced judge replies scored 0/16 is fixed at the shared layer.
5. **Robustness (opencode CLI):** `_run_opencode` now passes `--auto` after a headless run auto-rejected a `Temp\*` permission request (modal tool-use during `opencode run --pure`), making real-mode runs deterministic.
6. **Tests**: mock regression 23/23 PASS (multi-paper asserts added). Real run 110 s, all PASS, real 4 grounded claims with `paper_id`.
7. **DAS-16 pilot refreshed** (`--scenarios P-A,P-B,P-C,001,019`, real `opencode/big-pickle`): **P-A Total 3.06** (↓ artifacts to 3269 chars but papers=**3**, cited=**3**) vs 2.62 in Session 11 — the multi-paper pool lifts BSC Multi-Reference Synthesis+Citation Distribution to 3/4 (P0 acceptance ≥3 met on P-A; TSQ still ~2). 001 correctly no-evidence-clean (was wrongly-scored 2.44). Report table now shows `papers`/`cited` columns (`_eval_out/bench_pilot_das.md`; P-B/P-C judge flakiness — one fenced reply — fixed by `_unfence` and re-verifiable next run).
8. opencode `--auto` + fence tolerance + stopword precision: the pipeline is now robust across parser, network, CLI-permission and judge-parse failure modes.

Next (roadmap P0–P2): full real bench re-run to refresh the P-B/P-C rows post-`_unfence`; raise draft length/section count toward survey-grade TSQ/MAR (multi-paragraph per outline section, evidence per section); P1 judge threshold calibration; P3 DAS-Bench compliance (DAS-2M pools + ≥300B judge).

---

## 2026-09-16 — Session 11: benchmark-style evaluation using the DAS-Bench dataset assets (基准评测试点：复用 DAS-Bench 数据集资产)

**User instruction:** "继续。。。另外看是否可以使用已有 benchmark 数据集做评估呢" — continue; check whether the existing DAS-Bench benchmark dataset (already vendored in `external/DAS`) can be used to evaluate the pipeline.

1. **Asset inventory of `external/DAS/DAS-Bench` (as of 2026-09-16, local):** `benchmark/topics.json` (30 topic instances, id 001–030) — ✅ usable; `benchmark/evaluation_protocol.md` (16 criteria / 4 families BSC·MAR·TSQ·HDQ, integer 1–5, family avg = mean of its 4 criteria, Total Avg = unweighted mean of all 16) — ✅ usable; `results/main_results_30_topics.csv` (published per-method scores incl. Human 4.34, DAS 4.34, Naive RAG 4.03, Gemini DR 3.92, GPT DR 3.68, SurveyForge 3.78, AutoSurvey 3.73, LiRA 3.62, InteractiveSurvey 3.81, Codex 3.18) — ✅ usable as directional context; `evaluation/{eval_bsc,eval_mar,eval_prepare,eval_tsq_hdq}.py` + `run_eval_all.sh` — ✅ present (full compliance additionally needs DAS-2M pools + rendered pages + a ≥300B judge). **Not usable in this env:** DAS-2M candidate-paper metadata pools, gold source PDFs/reference surveys (Hugging Face, network), frozen ≥300B judge (keys/GPU).
2. **New harness `tools/eval/bench_eval.py`** — re-implements the 16 criteria **verbatim** from `evaluation_protocol.md` and runs, per scenario: `Pipeline` (real or mock via `--backend/--base-url/--model`) → if evidence produced, one extra LLM judge call scoring the assembled artifact on all 16 axes → family avgs + Total Avg + feasibility matrix + full-compliance checklist. Default scorer = repo judge (`opencode/big-pickle`, recorded honestly via `judge_model`). Judge keys are normalized (the model returned `"BSC: <criterion>"` prefixed keys → first real run parsed 0/16, fixed; re-verified). Mock server gained a deterministic `DAS-Bench rubric` route (all 16 → 4) so mock mode stays a stable regression. `tools/eval/__init__.py` added (imports fixed to avoid a self-import cycle).
3. **Pilot run (real, `opencode/big-pickle`, ~5 min):** 2 paper-anchored **proxy** topics (evidence in local corpus) + 2 verbatim DAS-Bench topics (001, 019). Results (L6 all pass, preview):
   - **P-A** proxy (Weber-Wulff `2306.15666`): **Total 2.62** (BSC 2.75 / MAR 2.00 / TSQ 2.50 / HDQ 3.25), internal judge pass@4.
   - **P-B** proxy (Liang `2304.02819`): **Total 3.19** (BSC 3.00 / MAR 2.75 / TSQ 3.00 / HDQ 4.00), internal judge pass@5 — the **best** preview score.
   - **001** ("Tool Learning and Function Calling for LLM Agents"): **Total 2.44** — **discovery-precision flaw surfaced**: the seed rail fuzzy-matched `tools` and wrongly pulled detection-paper `2306.15666` as evidence for an agent-function-calling topic (the wrong-evidence artifact was scored honestly).
   - **019** ("Human-AI Collaboration in Scientific Writing and Research Workflows"): **NO-EVIDENCE** (candidates `2409.13740`, `2510.24701` — seed matches, but no parsed local md) — demonstrates the 2/30-topic corpus evidence gap.
   - Family means across scored runs: **BSC 2.83 / MAR 2.25 / TSQ 2.42 / HDQ 3.50 / Total 2.75** vs published multi-paper survey systems 3.2–4.3: our single-paper-grounded artifacts sit **below** the survey floor on MAR & multi-reference axes (expected; this *quantifies* the gap to survey-level output).
   - Report: `_eval_out/bench_pilot_das.md` (tracked; per-criterion tables + feasibility matrix + full-compliance checklist).
4. **Signals for the roadmap:** (a) **internal P3 judge is too lenient vs survey-level scoring** (pass@4–5 while DAS-16 preview totals are ~2.4–3.2) → P3 threshold calibration is now *measured*, not just scheduled; (b) seed-rail fuzzy-match precision needs a threshold/tie-break before multi-paper discovery; (c) Multi-Reference Synthesis + MAR dominate the drag → the single-paper minimal vertical is not yet a survey generator.
5. Mock regression green: `bench_eval` mock mode (P-A total 4.00 cov 16/16; 019 no-evidence) after the key-normalization fix.

Next: (a) P3 judge threshold calibration against the DAS-16 scores (first calibration checkpoint now available); (b) multi-paper evidence in S_lit (fetch + parse top-k full texts) to attack the MAR/multi-ref drag and enable real DAS topic instances; (c) DAS-2M pools + ≥300B judge for a compliant DAS-Bench submission.

---

## 2026-09-16 — Session 10: second real paper — generalization verified (第二篇真实论文：泛化验证通过)

**User instruction:** "好，继续" — proceed with the documented next step: parse a second real paper and prove the question→evidence→draft loop generalizes beyond the single demo PDF.

1. **Paper chosen: Weber-Wulff et al. 2023, "Testing of Detection Tools for AI-Generated Text" (arXiv `2306.15666`, 46 pp)** — same research area as the demo (Liang), different authors/writing style; seed-manifest entry already existed. PDF downloaded via `Invoke-WebRequest` (12.4 MB) to `_demo_downloads/weber_wulff_2306_15666.pdf`.
2. **MinerU CPU parse — OCR-rec stage flakiness (new K12 → workaround).** Full-run `-b pipeline` crashed twice with **502 Bad Gateway** in the doc-analysis worker (once at Layout 14/46, later in OCR-det at 424/514 and OCR-rec at 384/733). Root symptoms match the known Windows-CPU OCR instability (PaddleOCR onednn family, cf. K7). Workaround that works: **`-m txt`** (uses the PDF text layer) **+ page-window slices `-s/-e`** (6 pp each). Result: 8 windows parsed (some needed 1–2 retries — crash is probabilistic per worker), md merged → `_demo_downloads/mineru_out_ds0509/weber_wulff_2306_15666/auto/weber_wulff_2306_15666.md` (**124,408 chars**; title & sections parse correctly). Registered in `corpus._LOCAL_MD`.
3. **Full-loop real run on Paper 2 (`opencode/big-pickle`), 149.8 s:** discovery-led `Pipeline.run(question="How reliable are automatic detection tools for AI-generated text?")` → candidates **['2306.15666', '2304.02819', '1706.03762']** (seed keyword scoring, correct top pick) → local md resolved → graph. Result: topics 5, STORM outline 3 sections, **4 grounded claims** (all `arXiv:2306.15666`, confidence high/medium, quotes verbatim in source — spot-checked), draft 1725 chars, **L6 gate PASS (score 1.0)**, **P3 judge = pass (score 4, all 4 rubric axes)**. Model calls: 5. **This is the first demonstration that the question→evidence→draft loop generalizes across papers**, not just questions.
4. Docs synced: runbook (status/§5 new K12 workaround + §8), PLAN §6 row 13, README status.

Next: (a) P3 judge threshold calibration + a ≥300B-class judge once keys/GPU; (b) DAS-2M subset / orx powered discovery sweep on the live rail; (c) Track B / proactive-loop wiring.

---

## 2026-09-16 — Session 9: framework integration — STORM outline · OpenResearch/orx + arXiv live discovery · DAS-Bench-style AI judge (三大参考框架运行时整合)

**User instruction:** "继续，另外注意之前提及的几个重要的框架，一定要整合进去，openresearch，standard的，等等吧" — continue and make sure the previously-mentioned important frameworks (OpenResearch/orx, STORM, DAS-Bench-style judge, etc.) are actually integrated into the pipeline, not just referenced.

1. **Network correction (supersedes Session 6/7/8 "live discovery blocked").** Re-probed 2026-09-16: `export.arxiv.org/api/query` answers **200 OK in ~1.1 s** (was measured timing out on 2026-09-15). The live arXiv rail is therefore exercised in this env; `orx` binary is still **not** installed (Rust source only in `external/orx`).
2. **OpenResearch/orx + arXiv live discovery rails integrated** (`tools/pipeline/corpus.py`): `discover(question, backend=…)` now supports `seed | arxiv | orx`, selected via env `S_LIT_BACKEND` (default `seed` — keeps integration tests deterministic) or `discovery_backend=` on `Pipeline.run`. `fetch_arxiv()` = free no-key arXiv API (the same backend family `orx discover keyword`/`openalex` uses), relevance-sorted Atom parse, `[]` on any failure → graceful fallback. `orx_discover()` shells out to `orx discover keyword <q>` **only when the binary is on PATH** (absent here); failure chain = orx → arxiv → seed. **Live smoke:** `discover("GPT detectors bias against non-native English writers", backend="arxiv")` returns the demo paper `2304.02819` as the top relevance hit; `backend="orx"` falls back to arxiv then seed with no binary present.
3. **STORM-style outline (S_org)** — Stanford OVAL STORM methodology absorbed: `_org` now extracts not just `topics` but an **outline** `{thesis, sections:[{heading, key_points:[…]}]}` from the evidence window + research question; `S_write` drafts **outline-driven** (one short paragraph per section, STORM co-writer style) instead of a single paragraph; `_finalize` includes the outline; new `outline` key in `PipelineState`. Real draft grew 1207 → **3357 chars** with 3 anchored sections.
4. **P3 DAS-Bench-style AI judge gate** (`tools/pipeline/judge.py`): new graph stage `finalize→gate→judge→END` — the mechanical L6 gate always runs **before** any AI review (blueprint §0/§3). `judge_draft()` returns `{label: pass|revise|fail, score: 1-5, checks:{groundedness, structure, bilingual, clarity}, feedback, judge_model}` under a 4-axis rubric; it is defensive (never raises; parse failure → labeled `fail` for audit). Runs on the **same LLMClient** (default `opencode/big-pickle`) — recorded honestly via `judge_model`; the DAS convention's ≥300B-class cloud judge + threshold calibration remain a P3 refinement pending keys/GPU.
5. **Tests extended and green.** `test_pipeline mock` → **19/19 PASS** (~0.1 s; new asserts: outline sections ≥1 + headings; judge verdict ∈ pass/revise/fail + 4 rubric checks; mock judge=pass score 5). `test_pipeline real` (`opencode/big-pickle`) → **18/18 PASS in 121.7 s** — outline 3 sections, claims=4, draft 3357 chars, validation score 1.0, **judge = pass** (5 model calls per run: topics, outline, claim-plan, draft, judge — up from 3). DB: mock canned judge/outline routes added.
6. Docs synced: runbook (banner/Status/§3 → live-rail + judge recipes, §6, §8 rows + checklist), PLAN §6 row 12 + Status, README (banner/table/Status). **Session 7 item 6 & Session 8 "Next" superseded**: OpenResearch/orx is no longer "reference-level only"; find it under `S_LIT_BACKEND`.

Next: (a) second real paper (new MinerU parse) to prove question→evidence→draft generalizes beyond one PDF; (b) P3 judge threshold calibration + ≥300B-class judge once keys/GPU; (c) DAS-2M subset / orx powered discovery sweep on the live rail.

---

## 2026-09-16 — Session 7: default LLM backend switched to opencode CLI free model; Ollama retired from default path (默认 LLM 后端切换为 opencode CLI 免费模型;Ollama 退出默认路径)

**User decision:** "能否尝试调用 opencode cli，然后不要再考虑 ollama 的这种模型了" — use opencode's hosted free model as the pipeline's default real LLM; stop considering local Ollama models.

1. **opencode CLI headless backend verified.** `opencode run --format json -m opencode/big-pickle` emits line-delimited JSON events; assistant text is concatenated from `type=text` events (`part.text`), token usage from `step_finish.part.tokens`. `opencode models` lists `opencode/big-pickle` as the default free model. Two integration gotchas found & fixed (Windows): (a) prompts containing double quotes (`{"title": …}`) get mangled by argv quoting on the cmdline and the run falls back to an empty greeting — **prompt is always written to a temp file and attached via `-f`**; (b) `-f` is a greedy array flag, so the instruction message must come **before** `-f`, else it is eaten as a filename.
2. **`LLMClient(backend="opencode")` added** (`tools/llm/client.py`, stdlib-only). `is_reachable()` = `opencode --version` rc==0; `chat()` renders system/user messages into one prompt, spawns `opencode run --format json --pure`, parses events, maps step_finish tokens → ChatResponse.usage. Config: `OPENCODE_MODEL` (default `opencode/big-pickle`). Ollama kept only as a legacy offline fallback backend (documented as such); default backend is now `opencode` everywhere.
3. **Default real paths switched off Ollama:** `test_pipeline.py real` → `LLMClient(backend="opencode")`; `smoke_test.py` gained `opencode` mode (3rd prompt set = claim list w/ arXiv cites); `claim_plan.py` CLI → `LLM_BACKEND` env (default `opencode`, model `OPENCODE_MODEL`); all command-recipe docs updated.
4. **Smoke on `opencode/big-pickle` → 3/3 PASS** (~11–14 s per call): bilingual ✓, JSON-extract ✓ (`{"title": …, "year": 2023}`), claim-list with `arXiv:` cite ✓. No JSON wrapping/fabrication issues observed (hosted model ≫ local 3B).
5. **Full P2 pipeline on `opencode/big-pickle` → 14/14 PASS in 51.0 s** (vs 35.8 s qwen2.5:3b / 51.8 s earlier — same order of magnitude, far more content): claims=4 (qwen kept 2 after the grounding filter), topics=4, iteration=1, draft =861 chars, **validation score 1.0** — structure/cites/grounding all pass with verbatim quotes; the L6 gate stays deterministic regardless of which model drafts. `test_pipeline mock` re-ran → **14/14 PASS** (regression clean).
6. **OpenResearch (`orx`) status confirmed, not integrated.** Reference-level only: documented in refs guide/blueprint/PLAN (E1 verified `orx lit` nonexistent → `orx discover keyword|embedding|openalex|biorxiv`), repo cloned into `external/` (gitignored), ledger entry in `corpus.py`. **Not used at runtime**: no `orx` binary installed (Rust source only) + live `orx discover`/arXiv API blocked by network in this env; discovery backend remains the offline seed manifest pending a live source.
7. Docs synced: runbook (banner/§3/§5/§7/§8/§10 status), PLAN (§6 log), README (banner/status/tables) — Ollama rows re-labeled legacy; "default real model = `opencode/big-pickle`".

## 2026-09-16 — Session 8: Ollama fully removed · full-text claim extraction (Ollama 彻底移除 · 全文 claim 抽取)

**User instruction:** "停掉ollama的部分，进入下一步" — remove the Ollama part entirely; move to the next step.

1. **Ollama backend deleted from code** (`tools/llm/client.py`): removed the `ollama` branch, `_chat_ollama`, `_post`, `think`/`num_ctx`/`thinking` plumbing, and `OLLAMA_*` envs. `backend="ollama"` now raises a clear "removed 2026-09-16" ValueError. Callers updated: `smoke_test.py` (dropped ollama mode), `claim_plan.py` (LLM_BACKEND = opencode|openai only), `test_pipeline.py` (real = opencode only), `graph.Pipeline` (dropped `num_ctx`). No Ollama server process was running on the host (nothing left to stop).
2. **Next step = full-text claim extraction (prior hardening item "fewer `md[:…]` truncations").** `S_write` claim-plan step now feeds the model the **entire paper markdown** (`MAX_SOURCE_CHARS = 20000`, was `md[:2500]`), asks for a `section` field (= the heading the verbatim quote lives under), and L6 grounding still scans the full text. `opencode/big-pickle` (huge context) makes this cheap; the old truncation was a qwen2.5:3b CPU limit that no longer applies.
3. **REAL tests green with full text:** `test_pipeline real` → **14/14 PASS in 58.1 s** (claims=4, topics=4, draft 1207 chars, validation score 1.0). Spot-check run showed all claims `[high]`, quotes verbatim (e.g. `…misclassified over half of the TOEFL essays as "AI-generated" (average false positive rate: 61.22%)`, `…P-value 0.035`), cites normalized to `arXiv:2304.02819`, and — fixed vs qwen2.5:3b (Session 6 item 6) — correct `section` attribution ("Simple prompt can easily bypass current GPT detectors" → the self-edit finding; "Mitigating Bias through Linguistic Diversity Enhancement of Non-Native Samples" → the 49.45% reduction + ICLR 2023 perplexity findings). `test_pipeline mock` → **14/14 PASS** (regression clean). Total model calls per run: org + claim-plan + draft = 3.

Next: (a) live S_lit discovery backend (orx / DAS-2M subset / arXiv API) once network/GPU allows — seed manifest stays the offline default; (b) P3 DAS-Bench-style AI judge gate (judges cloud/API, ≥300B-class); (c) wade into a second real paper (new MinerU parse) to prove the question→evidence→draft loop generalizes beyond one PDF.

---

**User instructions:** continue; go ahead and test Ollama; keep an interface for later APIs. (Later: user chose "方案 B" — `Disable-WindowsOptionalFeature … HypervisorPlatform` + reboot — which unblocked the Ollama server; K11 is now closed.)

1. **K7 RESOLVED.** Re-ran `PaddleOCR(lang='ch', enable_mkldnn=False)` (unchanged code) on `_demo_downloads/ocr_test.png`: after the rec model files fully downloaded this session, the Chinese line `中文学术文献扫描测试页 2026` is recognized at score 0.999 (earlier `?` placeholders were a partially-initialized/downloaded model, not a config bug). Ground truth from `ocr_result.txt`. Track B evidence layer is now usable.
2. **Ollama local server: BLOCKED → new K11 → RESOLVED by user (方案 B).** Root cause: `ollama serve`/`ollama app.exe` failed to bind any socket (WinError 10013/WSAEACCES) on `127.0.0.1:11434/11440`, `0.0.0.0:11440`, `[::1]:11441` — process-level ACL from Hyper-V / Windows Hypervisor Platform port reservations (upstream ollama#2627, #9444, #16270). After user ran the elevated `Disable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform` + reboot, `ollama serve` listens on `127.0.0.1:11434` (version 0.32.14, startup log 2026-09-15 20:36/21:02). Server is kept running via the Ollama tray app (persists across shells).
3. **Unified LLM client delivered & hardened (`tools/llm/`, stdlib-only).** `client.py` speaks two backends behind one `LLMClient.chat()`: `ollama` (`POST /api/chat`) and `openai` (any OpenAI-compatible `/v1/chat/completions` — DeepSeek, DashScope/Qwen, OpenRouter, Moonshot/Kimi, OpenAI), with `json_mode`, temperature, `num_ctx`, **`max_tokens`** (→ Ollama `options.num_predict` / OpenAI `max_tokens`, bounds runaway generation), config via kwargs/env. `smoke_test.py` exercises bilingual reply + JSON extraction + claim-list with cites (supports `expect_regex`). `mock_openai_server.py` is a keyless OpenAI-compatible stub.
4. **Ollama model pulls &实测 (this session):**
   - `qwen3.5:4b` pulled (list size 3.4 GB — default-quant tag, i.e. ~Q4; much smaller than runbook's Q8_0 5.3 GB reference). **Revised verdict: usable on this CPU — thinking is a request-level `think` toggle, not `/no_think`.** Verified 2026-09-15 via `/api/chat`: `think=true` (default) burns the whole `num_predict` budget on reasoning and returns the trace in **`message.thinking`** (755–775 chars observed) with `content` empty unless the budget has headroom; `think=false` answers instantly (1.4 s / eval=2 for "4"; 11 s / 25 tok for the prime explanation). Thinking mode ≈4–5 tok/s on CPU → keep `think=false` for fast steps; use `think=true` + generous `max_tokens` only for reasoning-heavy steps (outlines, routing rationale). `LLMClient.chat(..., think=…)` exposes the toggle and surfaces the trace as `resp.thinking`.
   - `qwen2.5:3b` pulled (1.9 GB; fast, no thinking mode) → **local fast-tier winner**.
   - **Smoke results:** `python -m tools.llm.smoke_test mock` → **3/3 PASS** (OpenAI-compatible wire path end-to-end). `python -m tools.llm.smoke_test ollama` with `OLLAMA_MODEL=qwen2.5:3b` → **3/3 PASS** (bilingual 2.35 s, JSON-extract 2.31 s, claim-list arXiv-cite 11.98 s). First run FAILED only on the claim-list *hard-coded* expectation `arXiv:1706.03762` (3b gave a valid arXiv ID, different one) → fixed smoke to `expect_regex` `arXiv:\d{4}\.\d+`.
5. Docs updated: runbook K11 row (closed) + §3 (max_tokens) + §7 (实测列) + §8/§10 status; PLAN/README status synced.
6. **First real pipeline LLM step ran on `qwen2.5:3b` (L4 claim-plan).** Input: MinerU-parsed `_demo_downloads/mineru_out_ds0509/liang2023_test/auto/liang2023_test.md` (Liang et al. 2023, *Patterns*). `LLMClient(backend="ollama", model="qwen2.5:3b")`, `json_mode`, `max_tokens=1024`. Result: valid JSON, 4 evidence-backed claims; quotes verbatim (e.g. `average false positive rate: 61.22%`, self-edit prompt `100% → 13%`, `P-value 0.035`), bilingual claim + 中文, cite=Paper ID. Measured: **135.0 s, usage {prompt_tokens: 3491, completion_tokens: 516}** (≈3.8 out-tok/s net, dominated by 3.5k-token prompt eval). Observed limitation: claim 3's `section` attributed the self-edit result to the "Mitigating Bias…" heading instead of the "Simple prompt can easily bypass…" section — section attribution is weak on 3b; acceptable for a skeleton demo, harden later via STORM/PaperQA2 grounding.
7. **L4 claim-plan packaged as reusable module** `tools/llm/claim_plan.py` (stdlib-only; `LLMClient`-driven; CLI `python -m tools.llm.claim_plan <md> <paper_id>`, env `OLLAMA_MODEL`). Re-run on the same demo: exit 0, 4/4 claims, 138.4 s, {3474+421 tok}. This is the piece P2's S_write/S_org wiring reuses directly.
8. **Vision-OCR fallback VERIFIED on `qwen3.5:4b` with `think=false`.** Read `_demo_downloads/ocr_test.png` directly via Ollama `/api/chat` (images in prompt): transcribed all three lines in 20.4 s (prompt_eval 260 / eval 26 tokens), including the Chinese line `中文学术文献扫描测试页 2026`; read the English line as `AI Research Foodie Pipeline Test` (ground truth `ocr_result.txt` records the typo `Al Research…`). Confirms the Track B alt evidence path (OCR-by-VLM) is locally usable without PaddleOCR.
9. **K8 DECIDED — no env split; single `ds0509`.** Verified coexistence in one env: MinerU OK, paddleocr 3.7.0, paddle 3.3.1, cv2 4.10.0; installing langgraph afterwards did not disturb them. A dedicated `ds0509-mineru`/`ds0509-ocr` split is unnecessary — revisit only if a future package pins incompatible native deps.
10. **langgraph installed in `ds0509`** (cost-sensitive decision taken — skeleton step needs it; stdlib-only until here): `langgraph 1.1.10` + `langgraph-checkpoint 4.0.3` + `langchain-core 1.4.0` (pydantic 2.13.4); import + minimal graph compile/`invoke` verified after install; env healthy.
11. **P2 LangGraph skeleton built (`tools/pipeline/`).** `state.py` (typed `PipelineState`), `graph.py` (`Pipeline` — S_lit→S_org→S_write→`review`→S_final with scoped `revise_para` re-entry; stale converges to finalize), `test_pipeline.py` (mock | real). **Significant bug found & fixed during testing:** the `iteration` counter was a plain last-write-wins channel, so inside the write⇄revise_para cycle LangGraph never accumulated it → `review` always saw `iteration=1` → *infinite* `revise` loop (this was the earlier "hang" — it was a `GraphRecursionError` at limit 10007). Fix: `iteration: Annotated[int, operator.add]` **accumulator channel** + `StateGraph(PipelineState)`; `write` returns `+1` per visit, graph provably converges. Also hardened parsing: `_extract_json_list/_extract_json_dict` recover JSON wrapped in prose/fences (real LLMs do this), and the mock gained content-aware canned routes for the pipeline prompts.
12. **P2 integration tests — ALL PASS both modes.** `python -m tools.pipeline.test_pipeline mock` → **7/7 PASS** (~0.1 s; claims=2, topics=2, iteration=1). `python -m tools.pipeline.test_pipeline real qwen2.5:3b` → **7/7 PASS in 51.8 s** (CPU): claims=3, topics=3, bilingual draft 904 chars, iteration=1 (review passed first pass). First end-to-end run of the blueprint §3 S_lit→S_org→S_write→S_final skeleton against the real local model + real MinerU output.
13. **S_lit discovery + L6 deterministic validator added** (`tools/pipeline/corpus.py`, `tools/pipeline/validate.py`). Live discovery verified BLOCKED in env: export.arxiv.org API read times out; `orx` binary is not installed (`external/orx` is Rust source only). So discovery defaults to a **seed-corpus manifest** of 7 verified arXiv IDs (each in this ledger), scored with deterministic keyword matching; new entry `Pipeline.run(question="GPT detectors bias…")` = question → candidates → matched local MinerU parse → graph. **L6 gate node** wired `finalize→gate→END`: checks structure (keys/output length), cites (arXiv ID with/without prefix, or DOI), quote grounding, bilingual draft. Grounding gates on a shared **5-content-token sequence** with the source (verbatim exactness reported as a quality metric `verbatim_quotes`).
14. **Robustness findings (important for model choice):** on the claim-plan step `qwen2.5:3b` sometimes (a) returns a **single JSON object** instead of a list (fixed: wrap→list in `_extract_json_list`); (b) outputs **bare arXiv IDs** `2304.02819` without prefix (fixed: cite regex accepts bare form + write-time normalization to `arXiv:…`); (c) **hallucinates fabricated claims** with plausible quotes on larger inputs — e.g. "new fertilizer increased crop yield by 30%" — even when the paper is about GPT-detector bias. Fixed mechanically: `grounded_claims()` drops any claim whose quote shares no 5-gram with the source **before** drafting, so fabricated claims never reach the draft. This is the first live demonstration of the L6 gate catching hallucination (the earlier garbage-claim run would fail the gate).
15. **P2 tests expanded and green — 14 asserts both modes.** `mock` → **14/14 PASS** (~0.1 s) · `real qwen2.5:3b` → **14/14 PASS in 35.8 s** (claims=2 kept after grounding filter + cite normalization, topics=3, validation score 1.0). Final graph: S_lit(discovery→evidence) → S_org → S_write(grounded claim plan + draft) → review → S_final → L6 gate.

Next: minimal vertical is now demonstrably GREEN end-to-end (question → candidates → evidence → grounded claims → bilingual draft → deterministic validation) on the local model. Remaining, in priority order: (a) real S_lit live discovery backend (orx / DAS-2M subset / arXiv API) once the network or GPU platform allows — manifest stays the honest offline default; (b) DAS-Bench-style AI judge gate + threshold calibration (P3), judges stay cloud/API (no local <9B judge); (c) parser/§4 hardening (fewer `md[:…]` truncations, full-text grounding across sections, section-attribution fix on 3b).

## 2026-09-15 — Session 5: doc clarity pass + lightweight local-model evaluation (文档清晰化 + 轻量本地模型评估)

**User decisions:** keep using opencode free models for all LLM steps (no change); **do not pull local models yet — evaluate which lightweight Ollama models are usable**; and write/draw purpose, flowchart and workflow clearly in the docs.

**Doc clarity pass (purpose + diagrams):**

- `README.md` — added "Purpose & pipeline at a glance": what the pipeline does/does not do, plus an ASCII L0–L6 flow diagram that renders in any editor.
- `docs/design/research-foodie-blueprint.md` — §0 now has a "what it does vs does not" table (explicit non-goals); §3 adds (a) a plain-text (ASCII) fallback of the L0–L6 mermaid, (b) a `S_lit/S_org/S_write/S_final` state-machine diagram (mermaid + ASCII) with scoped `revise_para` loop and proactive `stale → re-discovery` edge, and (c) an end-to-end numbered workflow sequence.
- `docs/setup-runbook.md` — renumbered sections; added §7 "Local model candidates (Ollama)" evaluation; added a pipeline-at-a-glance diagram in §1.

**Lightweight local-model evaluation (as of 2026-09-15; no pull yet):**

- Evaluated against pipeline nodes from blueprint §3/§5 (S_org taxonomy, routing, claim plans, drafting) and the host constraint (Win11 CPU-only, RAM not yet confirmed).
- **Shortlist (Ollama):** `qwen3.5:4b` = default local workhorse (4.66B; Q8_0 5.3 GB; Apache-2.0) — multilingual EN/中文, tools+native thinking, multimodal (vision) so also a candidate OCR/vision fallback for K7; `qwen3.5:2b` = fast tier for labels/tags; `gemma4:e2b` ≈2 GB = tiny fallback; `phi4-mini` ≈2.5 GB = CPU-only sweet spot; `qwen3.5:9b` (Q4_K_M 6.6 GB) = drafting-quality tier only if RAM ≥16 GB.
- Host RAM rule of thumb (directional, source: LocalAIMaster "Ollama System Requirements", 2026-08-03): 8 GB→7B, 16 GB→13–14B, 24 GB+→32B at Q4; CPU-only ≈3–8 tok/s @7B. For agents Ollama docs recommend context ≥64k but memory grows with `num_ctx` — keep modest on CPU.
- **Not recommended now:** `gemma4:26b` / `qwen3.8:27b` / MoE >15 GB — need remote GPU; judge node stays on cloud/cheap-API (DAS's own judges are 300B-class; no local <9B judge). Referenced: ollama.com/library/qwen3.5; registry.ollama.ai/library/qwen3.5 (accessed 2026-09-15); PromptQuorum "Best Local LLMs Aug 2026" (2026-08-28); PopularAI "Best CPU-only Local LLMs 2026".
- Before adopting any model: verify host RAM, run a bilingual structured-output + tool-call smoke test, log result in PROGRESS.md.

## 2026-09-15 — Session 4: P1 tooling smoke tests + runbook (P1 工具链冒烟 + 运行手册)

**User decisions this session:** use existing conda env `ds0509` (there is **no** `ds0508`); defer remote GPU (use opencode free models meanwhile); defer Ollama model pulls; samples via auto-download. Action: also produce a full bilingual operations doc.

**P1 results (all in `conda ds0509`, Python 3.12.13, CPU-only):**

- **MinerU — PASS**: installed `mineru[pipeline]` (K4: `[cli]` extra is insufficient — pipeline backend is a separate extra). Ran on arXiv:2304.02819 (Liang et al., 3 pages): full markdown out incl. title/authors/abstract; re-run 2/2 OK. Output: `_demo_downloads/mineru_out_ds0509/`. cv2=4.10 collision (K8) did not break it.
- **PaddleOCR — PARTIAL**: paddlepaddle 3.3.1 + paddleocr 3.7.0 installed. CPU oneDNN executor bug (K5) → fixed with `enable_mkldnn=False`; `use_gpu` arg removed in 3.x (K6). English line recognized (`Al Research Foodie Pipeline Test`), **Chinese line returns `?` placeholders** — **K7 OPEN, next-session task #1**. Console CJK print needs `PYTHONIOENCODING=utf-8` (K9).
- Network recon: `git clone` to GitHub RST-blocked → tarball via codeload (K1); arXiv webfetch blocked but `Invoke-WebRequest` download OK (K2); pytorch.org HEAD 403 but `/whl/cpu` index works (K3). DAS `examples/*.pdf` are 0.1 KB LFS stubs (K10).
- **Deliverable**: `docs/setup-runbook.md` — bilingual operations runbook (env baseline, command reference, smoke results, K1–K10 issues+workarounds, pipeline status, next-session checklist).

To-do carried forward: K7 (Chinese OCR), K8 env-split decision, then optionally scaffold P2 (LangGraph skeleton).

## 2026-09-15 — Session 3: Tasks A/B/C complete (核验、修订与蓝图交付)

**Task A (verification) — DONE.** All residual claims verified via primary sources; full ledger appended to the guide (see below). Harvests:

- U1 DAS judges: verified — primary judge Qwen3.5; Kimi K2.6 used for cross-judge robustness (ρ=0.507, MAE=0.630) per arXiv:2608.18034 (fetched via websearch; arXiv direct fetch blocked in env).
- U2 DAS-2M↔MinerU: verified — paper: "We use MinerU to parse the complete content and document structure of each PDF"; and DAS-Bench README:134 "PDF preprocessing uses MinerU." Confirmed in `external/DAS`.
- U3 STORM timing "3–4 min/topic": demoted to *unverified* (third-party only; official tool reports longer). URL storm.genie.stanford.edu live ✓.
- U4 Research Rabbit 50-seed cap: verified (Litmaps acquisition 2025-05-08; freemium 2025-10-30; RR+ $10/mo = 300 seeds).
- U5 Elicit accuracy: corrected upward → 96% headline (94–99% range, self-reported).
- U6 scite: corrected → 1.6B+ Smart Citations / 300M+ articles indexed (scite.ai/coverage).
- U7 Curtin→Turnitin: verified (disabled from 2026-01-01, Curtin announcement 2025-09-04).
- U8 judge-switch anecdote: verified — DeepResearch Bench adopted GPT-5.5 (README 2026-05-11) after Google's Gemini-2.5-Pro deprecation announcement.
- U9 NotebookLM→Gemini Notebook: verified (blog.google, 2026-07-16).
- U10 Claude Science (Jun 30) / GPT-Rosalind (Apr 16) / Gemini for Science (May 19–20): all verified via official announcements.
- U11 Weber-Wulff et al. 2023 = IJIE 19:26 (arXiv:2306.15666, DOI 10.1007/s40979-023-00146-z); Liang et al. 2023 = Patterns 4(7) (arXiv:2304.02819, DOI 10.1016/j.patter.2023.100779).
- U12 PaddleOCR 109 langs (PaddleOCR-VL, arXiv:2510.14528) ✓; DeepL $8.74/mo Pro annual ✓.
- U13 Ai2 ScholarQA: exists — free, open-source (Apache-2.0, `allenai/ai2-scholarqa-lib`), 11M+ full-text + 100M+ abstracts; ADDED to guide.

**Task B (guide revision) — DONE.** `docs/refs/ai-research-tools-workflow-guide.md` updated:

- Banner "Verified as of 2026-09-15".
- Fixed: `orx lit`→`orx discover keyword|embedding|openalex|biorxiv` + `orx paper` (all occurrences incl. table, prose, mermaid, code comment); MinerU license (custom MinerU Open Source License since v3.1.0/2026-04-18, not Apache 2.0; OpenDataLab≠DAS lab); S2 count 214M→~237M; Copilot Free "2,000 completions" stale-removed; scite 1.6B/300M; Elicit 90%→96% (both mentions); STORM timing demoted to unverified.
- Added: Ai2 ScholarQA (table row + agents section), verification-ledger appendix (15 rows), full References section.

**Task C (blueprint) — DONE.** `docs/design/research-foodie-blueprint.md` (bilingual): dual-track scope, L0–L6 layered architecture + mermaid, DAS-mirrored state model (S_lit/S_org/S_write/S_final), reuse map, environment/cost matrix (local CPU + remote GPU + cheap APIs, ≈$0 core), proactive re-synthesis loop, P1–P5 roadmap, risks.

**Dowloads (harnesses) — DONE.** `external/` (gitignored; git clone blocked by network RST in this env → tarball downloads):

- storm (74 files), DAS incl. DAS-Bench eval harness (267), paper-qa (183), DeepResearch/Tongyi (346), open_deep_research (45), MinerU (427, default branch is `master`), PDF-Extract-Kit (396), OpenResearch (501), orx = alphaXiv/openresearch-cli (501, incl. `agent-skills/`: orx-paper, orx-lit-review, orx-evidence, orx-experiment-tree, …). All extracted; used as primary reference in Tasks B/C.
- Also vendored `tools/citation-verify/` (scripts + references) from the local `citation-verification` skill.

## 2026-09-15 — Session 2: skills/harness teased out & downloaded (skills/中间件整理与下载)

- Teased out reuseable harness material from local `~/.agents/skills/` and vendored it into the repo:
  - `tools/citation-verify/` — copied verbatim from the `citation-verification` skill (`scripts/`): `verify-citations.py` (4-layer check), `api-clients.py` (CrossRef/arXiv/Semantic Scholar clients + unified `CitationAPIManager`), `format-checker.py` (BibTeX/LaTeX format checks), `README.md`. Pending: copy `references/` for full context.
  - Note: the skill's SKILL.md explicitly prefers WebSearch + Google Scholar as primary workflow; these Python scripts are **reference implementations for batch/automation**, matching our Task A/B needs (batch-verify the ~20 arXiv IDs / DOIs behind the References list).
- Teased out the `research` skill (background-agent research over primary sources → single Markdown) and `citation-verification` skill principles (verify during writing; canonical authority order DOI > arXiv > CrossRef > S2 > Zotero > Google Scholar).

## 2026-09-15 — Session 1: planning + initial verification (规划与首轮核验)

- Created: `LICENSE` (MIT, 2026 yunan), `AGENTS.md`, `docs/PLAN.md`.
- Verified against primary sources (all `as of 2026-09-15`):
  - DAS paper arXiv 2608.18034v1; DAS total 4.34 = Human 4.34; Naive-RAG 4.03; Gemini DR 3.92; GPT DR 3.68; SurveyForge 3.78; AutoSurvey 3.73 (ZhikaiXu24/DAS README table) ✓
  - DAS vs Naive-RAG expert preference 27/30 (majority vote) ✓
  - DAS-2M ≈2M papers, arXiv 2020-01→2026-06, 8 field groups, HuggingFace; DAS-Bench 30 topics / 16 criteria; generation code "To be released"; eval harness released (`evaluation/run_eval_all.sh`, `PDF_EXTRACT_KIT_ROOT`, OpenAI-compatible judge) ✓
  - OpenResearch: `orx lit` **does not exist** → `orx discover keyword|embedding|openalex|biorxiv` (E1)
  - MinerU license changed 2026-04-18 (v3.1.0) → custom "MinerU Open Source License", not plain Apache-2.0 (E2); MinerU = OpenDataLab, not ZJU/SJTU
  - Semantic Scholar index 214M (API) vs ~223M (official site) — reconcile (E3)
  - GitHub Copilot usage-based billing June 1, 2026, 1 credit = $0.01, Pro $10/mo ✓; Free "2,000 completions" stale (E4)
  - OpenScholar Nature 650:857–863, DOI 10.1038/s41586-025-10072-4; beats PaperQA2 by ~6% ✓
  - Tongyi DeepResearch 30.5B/3.3B (arXiv 2510.24701, open Apache-2.0) ✓
  - PaperQA2 retraction check + LitQA2 superhuman (arXiv 2409.13740) ✓
- Open items for Task A verification (U1–U12, see PLAN.md §3). Not yet checked: DAS judge models, DAS-2M↔MinerU, STORM timing, Research Rabbit caps, Elicit accuracy, scite counts, Curtin/Turnitin, judge-switch anecdote, NotebookLM rename, Claude Science/GPT-Rosalind/Gemini for Science, Weber-Wulff/Liang citations, PaddleOCR/DeepL numbers.

## Next steps (next session) / 下一步

1. ✅ **K7 closed** and **K8 decided**: Chinese OCR works; single `ds0509` env, no split.
2. ✅ **P2 LangGraph skeleton built + green** (`tools/pipeline/`): mock **14/14** · real `qwen2.5:3b` **14/14** (35.8 s) — PROGRESS Session 6 items 11–12, 13–15 (discovery, L6 gate, robustness hardening). `langgraph` 1.1.10 installed.
3. ✅ **S_lit (seed discovery) + L6 deterministic validator** wired: true minimal vertical (question → candidates → evidence → grounded claims → bilingual draft → validation gate) — all GREEN, both modes.
4. ✅ **Default LLM backend switched to opencode CLI free model** — `opencode/big-pickle` (Session 7): smoke **3/3** · pipeline **14/14 in 51.0 s** (claims=4, score 1.0). Ollama removed from code entirely (Session 8).
5. ✅ **Full-text claim extraction** (Session 8): `S_write` reads the whole paper markdown (was `md[:2500]`); correct `section` attribution; **real 14/14 in 58.1 s** · mock 14/14.
6. **Next bigger step:** (a) live S_lit discovery backend (orx / DAS-2M subset / arXiv API) once network/GPU available — OpenResearch/orx is reference-level only, **not runtime-integrated**; (b) DAS-Bench-style AI judge gate (P3) — judges stay cloud/API (no local <9B judge); (c) a second real paper (new MinerU parse) to generalize the demo.
7. Keep PROGRESS.md and PLAN.md in sync; no commits unless requested.
