# Research Foodie — Progress Log (进度日志)

> 中文速览：本文件记录执行进度、事实核验结果、修正与错误来源。按日期逆序追加。所有事实声明带来源与访问日期;无法验证的标记 *unverified*。

- `Updated`: 2026-09-22
- `Status`: Ongoing (implementation phase: `tools/llm/` ✓ · `tools/pipeline/` P2 minimal vertical GREEN + **framework integration** — STORM outline · orx/arXiv live discovery rail · DAS-Bench-style judge gate · benchmark-style evaluation pilot · **multi-paper evidence synthesis (P0) GREEN** · **survey-depth S_write GREEN** · **P1 judge threshold calibration GREEN** · **MAR render axes Part 1 GREEN** · **data hygiene (Session 16)** · **Track C evidence-grounded QA GREEN — QA panel n=31 correctness 4.23, extract/context 12/13 (Sessions 17–19)** · **30-topic evidence-pool battery GREEN — 22/30 pools, 10 judged Total 3.13 (Session 19)** · **judge variance measured — P-A 3.88±0.53 / P-B 3.31±0.00 / P-C 3.53±0.13 (Session 19)** · **comparison + next-plan docs (Session 20)** · **self-evolution design + usage/demo runbook + web-frontend analysis (Session 21)** · **parallel-workstream re-plan + model-routing Phase D (Session 21b)** · **web frontend implemented + web-scoped usage flow + arXiv paper outline (Session 21c)** · **F-3 static export (Session 21d)** · **E-1/E-2 health check + D-1/D-2 model profiles + durable run resume (Session 21e)** · **WS-C self-evolution mechanism E-3/E-4/E-5 + L-6 one-command self-check + Phase L retrieval/judge strengthening L-1/L-2/L-3 + D-3 judge matrix (Session 22)** · **scheduled capability×benchmark report `capability_report` + 3-option base model (free-opencode/openai-compat/judge-strong, qwen3.8-flash redirect) + paper draft v1 (Session 23)** · **key-free hardening — opencode 401 root-cause + Qoder-endpoint probe + client fail-fast + deterministic §4.6 ablations + daily-cadence scheduler + paper Mermaid figures (Session 24)** · **D-5 deterministic key-hygiene audit + cadence wiring, guards 33→39 (Session 25)** · **OpenResearch-style parallel *autoresearch* orchestrator integrated model-free (`tools/pipeline/autoresearch.py`), guards 39→47 (Session 26)** · **free-model blocker resolved — full health check GREEN on `opencode/big-pickle` (Session 26b)** · **first live testing on the free lane — proxy trio 3.65 + fresh variance P-A stable/P-C −1.7σ flagged (Session 27)** · **paper outline v2 (S22–27 folded in) + bidirectional outline↔draft map §12 + draft v2 per-section `(⇐ outline §X)` markers + web server live on 8787 (Session 28)**)

---

## 2026-09-22 — Session 27: live testing on the free-model base (基座已打通, 首次真实跑分)

**Why:** Session 26b confirmed the opencode free-model blocker was resolved (that verification was on 2026-09-22, see header below). User green-lit actual testing ("可以的，请继续"); this session ran the first **live** benchmark + variance measurements on the free lane end-to-end (org→write→L6 gate→judge), no keys.

1. **Live proxy trio (full pipeline, `bench_eval --scenarios P-A,P-B,P-C`)** — all 3 proxies ran the complete graph on `opencode/big-pickle`:
   - **P-A 4.31** (BSC 4.50 / MAR 3.50 / TSQ 4.25 / HDQ 5.00) · **P-B 3.25** (3.00 / 2.25 / 3.75 / 4.00) · **P-C 3.38** (4.00 / 3.00 / 2.75 / 3.75) — family Total **3.65** (BSC 3.83 / MAR 2.92 / TSQ 3.58 / HDQ 4.25), L6 gate **1.00 passed all**, DAS-16 coverage **16/16 all**, papers-cited 1-3. Elapsed ≈ **275-315 s/proxy** → full 36-scenario cadence ≈ 2.5-3 h on the free lane (viable as a background/overnight run). Report at `_eval_out/bench_live_freetest.md`.
   - vs frozen median-of-1 baseline: P-A +0.43 (0.8σ, PASS) · P-B −0.06 (0.6σ, PASS) · P-C −0.15 (**1.2σ WARN**).
2. **Fresh variance round (`variance_run --rounds 1 --median-rounds 2`)** — new records bucketed separately from the median-1 baseline by the resume ledger (median protocol is part of the fingerprint): **P-A 3.875** (0.0σ, −0.005) · **P-B 3.438** (+1.3σ) · **P-C 3.31** (**−1.7σ**).
   - Interpretation (honest): P-A rock-stable. P-B moved *up* (3.31→3.44 — fine). **P-C dropped −0.217 (1.7σ) with TSQ 2.75 / BSC 3.75** — but this is a *fresh full-pipeline* run, so the delta blends draft-wobble + judge noise, not judge-drift alone (judge-sanity on the cached manuscript was 0.2σ). E-3 rule: WARN accumulates evidence over ≥2-3 rounds before a debug ticket; one round is a flag, not a verdict.
3. **Provenance & guard state:** every artifact carries D-4 provenance (`judge_model: opencode/big-pickle`, temperature 0.0, profile `free-opencode`); resume ledger wrote each row crash-safely; health check stayed **GREEN (exit 0)** through the session.

Next (user to pick): **A.** full 36-scenario free-lane run (refreshes paper §4, ≈3 h background) · **B.** P-C drift watch — 2-3 more variance rounds to confirm/narrow the 1.7σ (also gives the L-3 sd<0.40 target) · **C.** Track C QA panel subset re-score · **D.** `autoresearch` with a model-lane attached (real drafted surveys per direction). Paper §4 is a *living document* — refresh with whatever we produce.

---

## 2026-09-22 — Session 28: paper outline v2 tuning + bidirectional outline↔draft map + web server live (论文大纲调优 + 大纲↔正文联动 + 前端启动)

**Why:** user answered Q1–Q4 and directed: (Q4) **论文必须"先调优大纲，再有论文内容的对应和联动"**；同时要求**打开前端自己看**。本会话按此顺序执行——大纲先行、映射其次、正文后同步；前端以可访问地址交付。

1. **Frontend live** — `uvicorn tools.web.app:app` 默认 8000 被系统保留端口区占用（`winerror 10013`，WinHTTP 排除区冲突），改起在 **`http://127.0.0.1:8787/`**（PID 25752，GET `/` 200，len 5512）。会话前已探明路由：`/` · `/dashboard` · `/manuscripts` GET 200；`/runs` POST-only（GET 405 预期）；`/runs/{id}/resume|log|status|events|DELETE`、`/feedback` 全在——免费基座打通后 live SSE / cancel / resume 都可真实端到端测。
2. **大纲 → v2（`docs/design/tool-paper-outline.md`）**——S22–27 成果全部折入：
   - 状态改为 `Outline v2`（`as of 2026-09-22`）、新增 §12 双向映射表、lineage 改为 v2。
   - §2 摘要六 beat 更新：health GREEN (exit 0)、**live trio Total 3.65**、P-C −1.7σ 单轮旗标、O* 并行编排。
   - §4 贡献 **C1–C5**（C4=运行韧性 run-memory/key-hygiene/401 fail-fast; C5=诚实评测含单轮方差旗标）；问题陈述补第 (d) 韧性墙（S24–25 教训）。
   - §6 系统设计补：**11→10 项**（新增 §6.5 run-memory resilience、§6.7 D-3 judge matrix、§6.10 D-4 provenance 独立项）；编排项记 `autoresearch` (S26) 与 E-1..E-5 全部标记 implemented（去掉 stale `[PLAN]`）。
   - §7 评测刷新：7.1 mock/real 34/34 + self_check 15s；7.3 加 live trio 3.65 与 fresh variance；7.4 health GREEN 实测；7.5 live ~275–315s/篇、usage 已回传；7.6 消融 a/b/c 已完成（标注实测数字）、d 待 ≥300B。
   - §8 局限 +1 条（第 6 条：free-base 单轮漂移 P-C −1.7σ 需 E-3 2–3 轮确认——正验证 median-of-N 必要性）；§9 结论 C1→C5；§11 roadmap 更新。
3. **大纲↔正文 双向映射（大纲 §12）**——逐节列 `outline 节点 → draft 节`，规则：**大纲是主干，正文是展开；正文每节顶格标 `(⇐ outline §X)`；改大纲先、改正文后、cadence 同步**。新增 `§6.10 D-4 provenance` 入档保持对齐。
4. **正文 → v2（`docs/paper/research-foodie-paper.md`）** 按调优后大纲联动：
   - 每节加 `(⇐ outline §X)` 标记（Abstract→§2、Intro→§4、Related→§5、System→§6.x 逐节、Eval→§7.x 逐节、Discussion→§8、Conclusion→§9、References→§10）。
   - §3 重排为 **3.1–3.10**：3.4 追加 `autoresearch` 并行 worker（O* 小节 `[TODO]`）、新 3.5 run-memory & resilience、3.6 L6 gate（23/23）、3.7 AI judge + D-3 judge_matrix、3.8 model access（三选项 + D-5 33→39）、3.9 provenance、3.10 self-evolution E-1..E-5。
   - Abstract 与 §4 收 live trio **3.65 / P-A 4.31 / P-B 3.25 / P-C 3.38** + health GREEN + P-C −1.7σ flag；Eval 重排 4.1–4.6 使数字节号与大纲 §7.x 一一对应（4.3 并 16 轴 + 30 题电池 + live；4.4 self-evol；4.5 cost；4.6 ablations a/b/c 实测）。
   - 内部交叉引用全量修正（§4.4/§4.5/§6.7/§13 等 stale 引用清零并复检）。

**Verification:** 双文件 `rg` 交叉引用无 stale §-ref（§13→§12、§4.5→§4.4、§7→§4 header 均修正）；前端 `GET /` 200；`git status` 仅两份文档改动。**下一步（用户已确认顺序先做完）：36-scenario/QA/autoresearch 任一 live 选项由用户定，跑完回填 §4 living doc。**

---

## 2026-09-22 — Session 29: interactive demo entry point + tool-survey in paper (可演示页面 · 论文补工具综述)

**Why:** user gave three directives: (1) **首个可演示页面**——表现"工具能做什么"，先 mock、但要明确标注真实/模拟；(2) **性能持续调优**；(3) **论文大纲与内容要涉及相关工具综述与本工具的比较**。本会话按三点交付。

1. **可演示页面（真实入口，标注 MOCK/REAL）**：
   - 新 CLI 驱动 `tools/pipeline/run_survey.py`——接受自由文本 `--question`，跑 discovery→evidence→S_lit→S_org→S_write→L6→P3 judge 全流程；逐阶段 flush `[survey]` 进度（SSE 直播可见、非冻结）；产出 Markdown+PDF 手稿到 `_eval_out/manuscripts/`；结尾打 `[survey-result]` JSON 供前端渲染手稿/PDF 链接。
   - `--mock` 模式：确定性离线（复用 mock 服务器），~1 s，输出隔离到 `_eval_out/mock_manuscripts/`，首行即 `MODE: MOCK`，run-card 显式标 **MOCK demo**（`NOT a live result`）；`--real` 默认显式标 **REAL run**。虚线原则：demo 永不冒充真跑。
   - Web `/` 页顶部新增 **"Try it — answer a research question"**：文本输入 + **Mock(demo)/Real(live)** 单选（各自注明耗时与温度语义）；后端 `_run_card` 解析 `[survey-result]` 显示 question / L6 gate / judge / claims / papers / elapsed + manuscript+PDF 链接（`/manuscripts/*` 现同时服务托管 mock 与 real 两个目录）。
   - 实测：mock 端到端 **1.3s、L6 pass、judge pass 5.0、四检查全 OK**，web POST→done 后 run-card 正确呈现 MOCK demo 徽标与手稿/PDF 链接（md 200 / pdf 200）。
2. **性能（本次第一轮，持续迭代）**：
   - `_TimedPipeline`：包装每个图节点打印 per-node 壁钟（lit/org/write/review/finalize/gate/judge）——定位热点（真实 run 的 362s 中大头是哪些 LLM 调用），是后续每轮优化的第一手测量。
   - `--fast`：revisions 上限 1（跳过 revise_para 循环），供演示/夜间批处理快速出稿。
   - 真实单篇 362s 基线已记录（free lane）；下一轮按节点耗时施计（如 BM25 窗口长度、max_revisions 预算、判题视图 ≤40K 字符）。
3. **论文补工具综述 + 比较（对应请求 3）**：
   - 大纲 `docs/design/tool-paper-outline.md` §5 增 **§5.1 工具综述对照表 `tab:tools`**（所列列: system | grounding | eval/judge | budget posture | relation to ours，末行 **Ours** ≈$0 CPU-only 强制溯源生态位），并同步 §12 映射行。
   - 正文 `docs/paper/research-foodie-paper.md` §2 拆出 **§2.1 工具综述**（四桶: outline+retrieval 写手 / agentic deep research / retrieval+cite-verify QA / 评测与解析层）与 **§2.2 comparison table 含 "Research Foodie (ours)" 行**；status 与 lineage 记录本次增补。

**Verification:** `run_survey --mock` 退出码 0、手稿/PDF 均生成；app.py ast 解析 OK；web 全链路 POST→SSE→done→run-card（MOCK demo 徽标 + 链接）实测通过；大纲/正文双文件交叉引用已同步。**下一步(按顺序)：** (a) per-node 计时跑一次真实单篇确认热点；(b) 36-scenario/night 批处理用 `--fast` 折半时间；(c) 前端加 read-only 静态导出（F-3 已有 CLI，未接线到这次新入口）。

---

## 2026-09-22 — Session 31: editorial workbench redesign + 两档交付物（一套源·双渲染 · Q&A 干货稿 + arXiv 出版化稿）

**Why:** two user directives. (a) *"从用户体验角度，实现一个简明但看得出来是经过良好设计的页面"* — the dashboard was functional but visually generic; needs a deliberate, subject-grounded identity. (b) *"输出内容注意两个层次：1 良好整理的干货内容；2 在干货基础上满足出版/发表要求"* — deliverables must be two-tier. Chosen via option-pick: 干货 default = **问答驱动·证据卡片**；出版化 = **arXiv preprint 风格**；交付 = **一套源·双渲染**（不改生成引擎、同 `.md`、双 PDF）。

1. **前端重设计（`app.py`）——编辑部/手稿方向的视觉系统**，刻意避开 AI 生成模板痕迹（无奶油+赤陶、无酸绿黑底、无圆角卡片阴影、无 `→` 链接、无全大写 eyebrow）：
   - 质感：冷纸底 `#f4f5ef` + 墨色 `#20211c`；结构用**细规则线**而非阴影；衬线显示字（Georgia）承载标题与叙事，等宽用于技术脚注行。
   - 单一亮点：**阶段 01–09 序号作为页面脊柱**（管线分明是一条真实序列，序号有语义）。live mission 与 mission 页共用同一套 `.stg` 卡片。
   - 两级层级明确：**叙事层在上（what/how/why + 进度条），工程层藏进 `<details>` 技术日志**；nav 增加当前页高亮（`page(..., cur=)`）；键盘焦点可见、`prefers-reduced-motion` 尊重、<700px 响应。
   - 页面文案同时给中英（投题/研究进行时/历次运行）。
2. **两档交付物（`render_manuscript.py` + `run_survey.py`）**：
   - `render_to_pdf(..., style="plain"|"preprint")`：plain=阅读级干货稿（11pt/2cm/蓝链，原行为不变）；preprint=arXiv 风格（A4 2.6cm、10pt、**章节编号 `--number-sections`**、中性链色、居中 title/author/date 标题块）。`[survey]` 双档各打一行，`deliver` 阶段 `tech` 报 `pages` + `pages_preprint`。
   - `run_survey --render plain|preprint|both`（默认 both）；产出 `<slug>.pdf` + `<slug>.preprint.pdf`；`[survey-result]` 新增 `pdf_pub`/`pages`/`pages_pub` 字段（旧字段 `pdf` 语义不变——手工兼容已有 run-card/mission 解析）。
3. **干货缺省组织——问答驱动·证据卡片（`graph.py` `_finalize`）**：手稿正文 Abstract 后插入 `## Q&A Digest (问答速览)`——主问题 → 一句话答案（取 abstract 首句）→ 子问题（outline 视角含 key_points）→ 证据卡片计数（claims→Sources）。纯索引、零新增模型调用，生成引擎不动。
4. **web 暴露双档**：run-card 与 mission 摘要链接改为 `manuscript / pdf 干货稿 / preprint 出版化稿`；manuscripts 页自动收录新 PDF（同目录遍历）。

**Verification:** `run_survey --mock` 双档均 2 pages、`[survey-result]` 含 `pdf_pub`、md 含 Q&A Digest（Q/A/子问题/证据卡片 4 行齐全）✓；app.py AST OK、nav 四页 `cur` 高亮断言通过 ✓；web 实测：home=200 含 preprint 链接与 mission 初始快照、`/manuscripts/*.preprint.pdf`=200 application/pdf ✓。**诚实边界：** preprint 是**同一源码**的排版变体（满足 arXiv 外形/结构规范），**不是**重新生成内容；作者字段为管线署名占位（"Research Foodie (autonomous survey pipeline)"），投稿前人工替换。**下一步：** per-node 计时优化真实单篇；36-scenario 夜间 `--fast` 批处理（可直接产出双档 PDF）；静态导出（F-3）纳入 mission/preprint 视图。

---

## 2026-09-22 — Session 30: research-mission narration on the web (研究任务叙事层：what/how/why + 业务/技术双语言)

**Why:** user directive — *"现在前端展示了很多技术信息，但从应用场景（如何完成 research 工作）角度还缺乏系统的信息反馈/告知，让使用者明确知道你在做什么：现在研究做到什么阶段了、怎么做的、为什么这么做；既要有业务语言，也要有关键技术信息。"* 即：**把"研究任务视角"做成第一层叙事**，技术日志退为第二层。

1. **结构化阶段事件（`run_survey.py`）**——新增 `[survey-stage]` 机器可读事件（`{"id","status","dur_s","tech"}`）：
   - 每个图节点（lit/org/write/review/finalize/gate/judge）由 `_TimedPipeline` 包装后发 start/done；discovery/evidence/finalize/deliver 直接发；全 9 阶段：**discover · evidence → synthesize · outline · write · finalize · gate · judge · deliver**。
   - 这样 run log 同时携带两条信息流：人类可读 `[survey]`（工程细节）+ 机器可解析 `[survey-stage]`（叙事素材）。
2. **前端「研究任务」叙事层（`app.py`）**：
   - **`SURVEY_STAGES` 元数据**——每个阶段配 `label`(EN)/`zh`/`what`(业务：这一步对研究意味着什么)/`how`(怎么做的，含关键技术)/`why`(为什么这么设计)/`key`(技术要点一栏)。同一份元数据驱动 live 看板、mission 页、run-card。
   - **Live 研究任务看板**（`/` 页，位于 raw tail 之上）：SSE 解析 `[survey-stage]` → 进度条（X/9 · %）+ 每阶段一行 `✓/●/○ 业务标签(中文) → why → how → 技术key+实测值+耗时`；页面刷新后从最近 survey run 恢复快照，不丢失。
   - **只读研究视图页 `/runs/{id}/mission`**：单个已完成 run 的完整叙事——问题、L6/judge 结果摘要、9 阶段 what/how/why 全文、手稿/PDF 链接；run-card 加 `research view` 链接。
   - 层级关系明确：**业务语言（研究任务）在上层，技术日志（raw tail + `/log`）在下层**，两者都可达。
3. **诚实边界**：无证据 run（candidates=0）仍如实走"no parsed evidence"并标失败，mission 页照常显示已完成的 discover/evidence 与 0 证据结论——叙事层不掩盖失败。

**Verification:** `run_survey --mock` 阶段事件 17 行齐全；app.py ast 解析 OK、无 escape 警告；live 服务器实测：POST→SSE→done→（a）mission 页 9 阶段"what 计数=9"、问题/L6/manuscript 链接齐全；（b）主页面 Live research mission 看板渲染 + 恢复快照 + run-card research view 链接；（c）无证据场景诚实失败。尚未接线：F-3 静态导出（gh-pages）不含 mission 视图——保留到后续。**下一步：** per-node 计时定向优化（写阶段/判题各一次）、`--fast` 夜间批处理、mission 视图进静态导出。

---

**Why:** user asked to (a) check overall progress and (b) evaluate whether the **opencode free model (`opencode/big-pickle`) can now be the base model for testing** — i.e. is the live path unblocked? Session 24 had root-caused an HTTP 401 "No payment method" (CreditsError) on the opencode hosted "zen" gateway and left the model lane *deferred*; this session re-verified the live path.

1. **Live probe (new evidence):** `LLMClient(backend='opencode', model='opencode/big-pickle')` single-turn → **REPLY ok in 9.0s, 3386 prompt / 13 completion tokens, no key** — the previously credit-blocked account path now resolves. (The hosted account is provisioned again; session 24's ✓ error-class parser remains as fail-fast, harmless.)
2. **Full health check re-run (fresh real judge scores, ~88s):**
   - mock 34/34 ✓ · pools 22/30 (full 14) ✓ · arxiv_probe reachable ✓ · gate_coverage **23/23 (100%)** ✓
   - **judge sanity (live re-score of cached P-A/P-B/P-C on the free model):** P-A 3.62 (Δ=0.26, 0.5σ) **PASS** · P-B 3.31 (Δ=0.00, 0.0σ) **PASS** · P-C 3.50 (Δ=0.03, 0.2σ) **PASS** → **exit 0 GREEN** (previous WARNs P-B 1.3σ / P-C 1.7σ that reflected the flaky/blocked backend are gone).
3. **Assessment vs plan:** every E-1/E-2 baseline-delta now within judge noise; the previously-deferred items that only needed a *reachable model* — live unnested L-3/L-1 acceptance on real QA/proxies, §4.6(d) judge-swap, D-3 variance-compression on the free judge, F-2 live SSE cadence, per-run cost table — are **unblocked for testing** with the free model as base. Resource-gated R-* (≥300B judge / GPU / keys) remain out of scope; D-3 compression-vs-strong-judge stays Phase R.

Next: per user — decide what to test first with the free-model base (live bench vs QA re-run vs L-1/L-2 numeric acceptance vs D-3 matrix on two vantages). Merged report header carries D-4 provenance.

---

**Why:** user directive — *"只要能把 openresearch 最核心和独一无二的功能纳入，用什么方法实现，你来决定就行"* (incorporate OpenResearch's most core/unique capability; I choose the method). OpenResearch (`openresearch.sh` / alphaXiv) is not a better literature search (we already mirror arXiv/STORM/DAS) — its **unique** primitive is *autoresearch*: one research direction is **fanned out into several independent threads, each pursued in an isolated worktree, in parallel, then merged** ("give each research direction its own agent … in isolated worktrees"). That **orchestration is model-independent**, so unlike the rest of the deferred list it is implementable and runnable *now, key-free*.

1. **`tools/pipeline/autoresearch.py` (new — deterministic, model-free, stdlib+threading).** Layered on top of the existing single-survey graph, not a rewrite. `plan_directions(q,k)` fans the query into K orthogonal lenses (mechanism / evidence / limitations / comparison / impact); each runs in an isolated on-disk **`Worktree`** (`wt-<id>/`, the filesystem analogue of a git worktree — a direction writes only there) dispatched via `ThreadPoolExecutor`; per direction it resolves evidence with the real `corpus.resolved_evidence`, surfaces **extractive** (verbatim) claims and keeps only those the **L6 `grounded_claims` gate** retains; `merge` unions the per-direction pools and reports the true autoresearch signal — **which sources each direction uniquely surfaced vs agreed on**. The OpenResearch `orx` **binary is not a dependency** (uninstalled + its hosted model is credit-gated, Session 24); what is imported is its *method*, faithfully and offline. A future model lane attaches at `run_direction` without touching the orchestration.
2. **Runs now, offline:** `… -m tools.pipeline.autoresearch "how reliable are AI-text detection tools?" --directions 4` → **4 isolated worktrees, 2-source union, 15 grounded claims, 0 gate drops**, with real divergence (only the `limits` direction surfaced `2304.02819` alongside the shared `2306.15666`). Merged report at `_eval_out/autoresearch/<slug>/AUTORESEARCH.md`.
3. **Guards** (`test_capability.py`) — new `_test_autoresearch()`: plan determinism + distinct ids, **one isolated worktree per direction**, every worktree populated independently, merge ⊇ each direction's sources, report written, grounding tallies (and >0 claims on a resolvable query). Deterministic guards: **39 → 47**.

**Verification (this session):** `autoresearch` rc=0 end-to-end offline ✓ · `test_capability` **47/47 ALL PASS** ✓ · `self_check` **GREEN (exit 0)** (the config+capability step now exercises autoresearch each cycle) ✓ · py_compile rc=0.

**Honest boundary:** this integrates OpenResearch's *control pattern*, not the `orx` runtime. The per-direction drafting/judging can later upgrade from extractive-evidence to full model synthesis once a reachable model exists; `R-4` (`orx` binary enablement + `S_LIT_BACKEND=orx` live discovery) and the compute-marketplace remain out of scope / model-gated.

---

## 2026-09-20 — Session 25: D-5 deterministic key-hygiene audit (无模型可实现的收尾)

**Why:** user directive — *"既然你不愿意 hack 你自己，就先把其他的任务能实现的都实现了吧，完成后请记录工作进度"* (drop the self-hack line; implement everything else that is achievable, then record progress). With every live/model-gated item deferred, the one **open, model-free plan item still without an implementation** was **D-5 (Cost & key hygiene)**, whose acceptance is "*`rg` finds zero key/literal in repo*" — previously only a convention, not an enforced guard.

1. **`tools/eval/key_hygiene.py` (new — deterministic, stdlib-only, no network, no LLM).** Walks the tracked source tree (skipping vendored/generated dirs — `external/`, `_demo_downloads/`, `_eval_out/`, `.venv`, `.git`, `__pycache__` …) and reports high-signal secret *literals*: OpenAI/Anthropic `sk-…`, AWS access-key ids, GCP/Slack/GitHub/HuggingFace tokens, PEM private-key blocks, `bearer …`, and long literals assigned to `*api_key` / `*token` / `*secret` names. It scans **secret values, not variable names** (so `os.environ["OPENAI_API_KEY"]` is never flagged), **masks every match** so running it cannot itself leak, and offers a `key-hygiene-allow` line escape hatch. `--out` writes `_eval_out/key_hygiene.md`; **exit code is non-zero on any finding** → usable as a pre-commit hook.
2. **Cadence wiring** (`evolution_sprint` step 8) — the audit now refreshes alongside `capability_report`/`ablations` each sprint (informational; does not change the benchmark verdict) and prints `[sprint] key_hygiene CLEAN -> …`.
3. **Guards** (`test_capability.py`) — new `_test_key_hygiene()` asserts (a) the real repo is **CLEAN (60 source files, 0 findings)**, (b) it **walks a real tree** so it can't pass vacuously, (c) a **planted, runtime-built secret IS detected** and **masked**, (d) an **env-var-name reference is NOT flagged**. Deterministic guards: **33 → 39**.

**Verification (this session):** `key_hygiene` rc=0 — 60 files, **0 findings** ✓ · `test_capability` **39/39 ALL PASS** ✓ · `self_check` **GREEN (exit 0)** incl. the new guard in the 4-step cycle ✓ · py_compile rc=0 for all touched modules; the `.ps1` registrar still parses.

**Honest boundary:** D-5's other half — *per-run **token/cost** reporting* — is still **model-gated**: the `LLMClient` already captures `usage` from `step_finish`/OpenAI responses, but a real cost table needs a reachable backend (the free hosted judge is 401 credit-blocked; see Session 24). This session landed the fully key-free half (the credential-hygiene invariant); all remaining open items (`D-3` compression measure, `§4.6(d)` judge-swap, `R-*`, `F-2` live-run SSE, cost report) are gated on a reachable model / API key and stay deferred per "跟输入 api key 相关的内容留在后边".

---

## 2026-09-20 — Session 24: key-free hardening — model-blocker root-cause + deterministic ablations + scheduler (无 key 前提下的实现 + 确定性消融 + 定时任务)

**Why:** user directives — (1) **"先不考虑 api key 作为输入"** (operate key-free for now), (2) **"把和模型调用之外的内容都实现…跟输入 api key 相关的内容留在后边"** (implement everything except model calls; defer the API-key work) and record progress + plan, and (3) explore a CLI **redirect to Qoder's Qwen Flash** as a possible "hack".

1. **Free-model blocker root-caused (external, not code).** The live path failed because the `opencode` CLI on this host authenticates against opencode.ai's hosted **"zen" gateway**, which returns **HTTP 401 "No payment method" (CreditsError)** for the machine's account — hence `big-pickle` hangs (stuck retrying) and `qwen3.8-flash` returns rc=1. **Qoder-hack probe:** the `qoder` CLI is only the VSCode-style IDE launcher (`qoder 1.31.1`; diff/goto/window — no model subcommand); the two Qoder listeners are **not** a model API — `127.0.0.1:56510` is a private **WebSocket** control channel (`400` + `Sec-Websocket-Version: 13`) and `:9420` is the **Chromium remote-debugging** target; no `.qoder` config exposes a model base-URL/token. **Verdict:** Qoder's in-IDE Qwen is not published as a callable/key-free endpoint, so a clean CLI redirect would require driving the IDE's undocumented internal protocol (fragile, ToS-grey) — deliberately not done. Active base model stays the key-free `opencode/big-pickle`; all *model-call* work is deferred.
2. **Client fail-fast** (`tools/llm/client.py`) — new `OpencodeError(retryable=…)` + `_first_opencode_error()` parse opencode `{"type":"error"}` billing/401 events into a clear actionable message and stop retrying non-retryable account errors (no more ~600 s hang on a credit-blocked account). +3 deterministic guards.
3. **Deterministic §4.6 ablations** (`tools/eval/ablations.py`, new — model-free, offline, stdlib) — (a) grounding gate ON/OFF on a fixed fixture: draft-leakage **8 → 0**, 5/5 grounded retained, **0 false drops**; (b) cached 30-topic pool coverage **14 full · 8 partial · 8 empty (73%)**; (c) median-of-N per-topic spread from `variance_runs.json` (P-A 0.75 / P-B 0.00 / P-C 0.19, mean ≈ 0.31). Writes `_eval_out/ablations.md`. Paper §4.6 (a/b/c) filled with these *real* re-run numbers; live judge-swap (d) deferred.
4. **Daily-cadence scheduler** (`tools/web/schedule_task.ps1`, new) — idempotent Windows Task Scheduler registration of the **offline** cadence (`evolution_sprint --quick`, no LLM/no key) with `-At`/`-Unregister`; delivered but **not auto-run** so the host is not mutated unprompted.
5. **Paper figures** — `fig:architecture` (L0–L6 over the LangGraph state machine, gate→draft feedback, judge on top) + `fig:loop` (self-evolution cycle encoding both design rules + the real-gold quota) added as **Mermaid** (commit `a7188cc`).
6. **Tests** — `test_capability` grew 22 → **33 deterministic guards** (ablation invariants + client 401-parse) → **ALL PASS**.

**Verification (this session):** `ablations` rc=0 (leakage ON=0 · false_drops=0) ✓ · `test_capability` 33/33 ✓ · `client.py` py_compile rc=0 ✓ · `self_check` GREEN incl. the new guards ✓.

**Honest boundary:** the paper §4 *live-judge* figures (fresh L-3 sd, judge-swap) remain the frozen Session 19–22 baseline — NOT re-measured — because the free model is credit-blocked. Everything added here is model-free/deterministic and genuinely re-run. Deferred pending a reachable model/key: live cadence acceptance, §4.6(d) judge-swap, and any Qwen redirect.

---

## 2026-09-20 — Session 23: scheduled capability report + 3-option base model + paper draft v1 (定时能力快照 + 基座模型三选项 + 论文初稿)

**Why:** user asked to (a) "尽可能把实现都完成" + make features/tests thorough, (b) base model → **redirect Qwen 3.8 Flash** here but **keep API-key + opencode as selectable options** ("为 api key 和 opencode 留出接口位置，作为多种选项"), (c) **定时** output each capability's performance on the relevant tools + benchmark and keep the current tool **configuration/performance updated in the docs**, and (d) start writing the **paper** (optimize the design outline), keeping everything dynamically evolving.

1. **Base-model layer** (`tools/llm/profiles.py`) — added a third selectable option `openai-compat` (all three lanes → any OpenAI-compatible provider via `OPENAI_*`, e.g. Qwen through DashScope) alongside the existing `free-opencode` and `judge-strong`; surfaced a `MODEL_OPTIONS` tuple; documented the `OPENCODE_MODEL=opencode/qwen3.8-flash` redirect. Keys stay env-only (AGENTS.md). **Finding:** the standalone `opencode` CLI returns rc=1 for `opencode/qwen3.8-flash` — the Qwen 3.8 the user sees is provisioned in **Qoder/this IDE**, not the opencode CLI account — so the reliable "whole pipeline on Qwen" path is `openai-compat` + a DashScope key, with the CLI redirect available if the account provisions it.
2. **Scheduled capability snapshot** (`tools/eval/capability_report.py`, new) — one dated screen joining every capability's benchmark numbers (`baselines.json`/`variance_runs.json`) with the **active config** (profile lanes, `MODEL_OPTIONS`, 9-pin tool ledger, thresholds) and self-evolution state (open tickets, gold-quota, last-cadence verdicts). Reads cached artifacts (offline ~0 s), `--live` refreshes via a quick health+deps cycle. **Wired in as step 8 of every `evolution_sprint`**, so each cadence keeps it current; runbook §3 documents a `Register-ScheduledTask` (daily) recipe for the *定时* requirement. This is the "把工具配置的表现及时更新到相关文档" mechanism — it also proves the qwen redirect flows through to the reported config.
3. **Tests** — `tools/eval/test_capability.py` (22 deterministic, zero-network, temp-isolated guards: the 3 profile options + qwen redirect + loud failures + report assembly incl. the pass-fraction and missing-artifact cases + per-topic variance) → **ALL PASS**; wired into `self_check.py` as unit step 1b.
4. **Paper** — drafted **v1** at `docs/paper/research-foodie-paper.md` (English master + 中文速览) from the outline: abstract, intro+contributions, related work, full system design (incl. §3.7 model options + §3.9 self-evolution), evaluation §4 populated with the *real* measured numbers, honest limitations, IEEE refs (with `unverified` flags). Marked a **living document**: §4 is regenerated/verified by `capability_report`; outline `Status`/`Living doc` lines updated.
5. **Docs sync + L-5** — CAPABILITY-STATUS (中文速览 + §2.7 rows + reproduce + where-to-look), PLAN §8 (D-1 3rd option + E-6 partly-implemented), runbook §3 (capability_report + scheduling recipe + 3-option model table) updated; the stale Ollama inventory row flagged **superseded** (L-5 sweep — no runnable Ollama commands remain in the docs).

**Verification (this session):** profiles → 3 options resolve + loud-fail ✓ · `capability_report` renders offline + reflects a `qwen3.8-flash` redirect ✓ · `evolution_sprint --quick` GREEN and refreshes the snapshot (step 8) ✓ · `test_capability` 22/22 ✓.

**Honest boundary:** no *fresh* live judge numbers were captured this session (opencode subprocess was slow/flaky under sandbox); §4 still reflects the frozen Session 19–22 baseline, now surfaced + config-stamped by `capability_report`. The live cadence (real L-3 sd, L-1/L-2 acceptance) remains pending a working judge run.

---

## 2026-09-20 — Session 22: self-evolution mechanism (E-3/E-4/E-5) + L-6 self-check + Phase L/D implemented (自我演化机制落地 + 一键自检 + Phase L/D 实现)

**Why:** user asked to (a) implement every locally-feasible PLAN §8 item with sufficient tests, then (b) *重点规划和实现自我演化进化的机制* — plan and implement the self-evolution mechanism. Per `docs/design/self-evolution-mechanism.md` (Session 21 evidence), "self-evolution" here is a **scheduled-measurement + regression-detection + human-gated-repair** loop, never autonomous code/weight change.

1. **WS-C Phase X loop — the mechanism itself (E-3/E-4/E-5), `tools/eval/evolution.py` + `evolution_sprint.py`** —
   - **E-3 evolution cadence** `evolution_sprint.py` wraps `health_check.run_cycle` → **E-4** `verify_deps` → `tickets_from_verdicts` → `feedback_stats` → `promotion_check` → `log_cadence` → one-screen `_eval_out/evolution_sprint.md`. Debug-ticket board (`tickets.json`) is one-open-per-component, FAIL/WARN open + feed evidence, PASS auto-closes, SKIP leaves untouched (absent measurement ≠ fixed). The loop writes **only** ledger JSONs — no code/prompt edits, no commits (AGENTS.md).
   - **E-4 dependency/version ledger** (`deps_ledger.json`): 9 pins (python · langgraph · mineru · opencode CLI · default model · pandoc · xelatex · paddleocr · arxiv API), classifying `missing_required`(→FAIL) / `missing_optional`(→WARN) / `changed`(→WARN drift, never silent). **Live-verified this host**: python 3.12.13 · langgraph 1.1.10 · mineru 3.4.5 · opencode 1.18.31 · pandoc 3.8.2.1 · xelatex MiKTeX 24.4 · paddleocr 3.7.0 · arxiv reachable. Fixed `_cli_version` to resolve Windows `.cmd`/`.ps1` npm shims via a shell fallback (opencode was falsely MISSING).
   - **E-5 feedback corpus + promotion rule** (`feedback/*.jsonl`, `revisions.json`): every row provenance-tagged + `gold_anchored` + `artifact_sha`; **anti-model-collapse real-gold quota** (≥50% gold over ≥10 rows, Seddik et al. 2404.05090); **promotion gate** `promotion_check` = N≥3 sustained cadences ∧ Δ≥2σ ∧ no mock/gold regression → *eligible* (a human bumps the numbered revision; `bump_revision` keeps a revertable v1→v2 chain). Two design rules enforced: triggers come only from external measurement; every signal passes a variance-aware threshold.
2. **L-6 one-command self-check** — `tools/eval/self_check.py` + repo-root `self_check.ps1`: unit → mock integration → cadence, exit = max(GREEN/WARN/FAIL). **Verified offline GREEN in ~13 s.**
3. **Phase L retrieval/judge strengthening** — **L-1** `tools/pipeline/rerank.py` (Okapi-BM25 window selection, stdlib-only) wired into `graph._write` with per-paper `source_windows` provenance; the grounding gate still checks the FULL md so the shield is never weakened; no-harm fallbacks (full/raw). **L-2** `graph._org` reader-perspective rail (STORM-inspired, prompt-only, parse-fail→[]). **L-3** `bench_eval.median_bench` per-criterion median over `--median-rounds` + `variance_run` wiring; single-call population kept separate so the health σ baseline stays valid.
4. **WS-D** — **D-3** `tools/eval/judge_matrix.py` (frozen-proxy × judge-vantage matrix, cross-judge spread/agreement, D-4 provenance, optional L-3 median; mock-verified 2 vantages); **D-4** provenance banners (`model`+`judge_model`+`temperature`+profile) added to `bench_eval`/`health_check`/`evolution_sprint`/`judge_matrix` reports. **L-4** agent-side citation-verification checklist wired into `docs/setup-runbook.md` §3 (no code change, as scoped).
5. **Tests (this session's evidence)** — `tools/eval/test_evolution.py` (31 deterministic, temp-isolated, zero-network assertions: ticket dedupe/auto-close, promotion verdicts, gold-quota floor, revision chain, cadence streak, dep classification, L-3 median math, L-1 re-rank fallbacks) → **ALL PASS**; `test_pipeline.py` mock gained L-1/L-2 asserts → **34/34 ALL PASS**; `self_check.ps1` → **GREEN**. Refactored `health_check.main` into an importable `run_cycle()` so the sprint can wrap it.

**Honest boundary:** the zero-LLM loop and all guards are verified; the *numeric* acceptance of L-1/L-2 on real P-A..C/QA and L-3 sd<0.40 need a real judge cadence, and D-3/R-1 variance compression needs a registered ≥300B key (Phase R). No commits made (user has not asked).

---

## 2026-09-20 — Session 21e: E-1/E-2 health check GREEN · D-1/D-2 model profiles · durable run resume (run memory)

**Why:** user asked to (1) continue implementing PLAN §8 (E-2 health check was next in queue), (2) cover **model routing** (WS-D — "which model runs which lane"), and (3) add **run memory**: "跑到一半断线了/死机了 → 重开后应该可以继续" — long LLM runs must survive a crash/disconnect and *continue* from the last completed row instead of re-paying from scratch.

1. **WS-C E-2 `tools/eval/health_check.py` GREEN** — frozen-subset health checks with variance-aware thresholds (2σ FAIL / ≥1σ WARN, per-proxy σ from `_eval_out/baselines.json`):
   - `mock` regression (hard gate: subprocess `test_pipeline mock`, parsed `==== ALL PASS ====` / `==== N FAILED ====`) · `pools` re-scan (`pools_30.json`, coverage −10% vs baseline → WARN) · `arxiv_probe` (arXiv API reachability) · **`gate_coverage` (E-2b)**: L6 `validate()` mutation corpus — token-level gap-1 filler interleave + synthetic negatives + structure-breaks (no draft / no taxonomy / no claims) + bad-cite set + keep-controls (verbatim / one-word paraphrase / empty cite / latin-only draft) → **23/23 mutants killed, kill rate 1.0** (line: ≥20 mutants, 100% kill).
   - **Mutation-test debugging caught two real L6 leak paths**: (a) *word-level* gap-1 interleave still leaked on markup-heavy sentences — `<sup>1,2,3,+</sup>` inside a single raw word expands to 3 tokens after `_toks`, so a shared 5-gram (`zou sup 1 2 3`) survived; fixed by interleaving at **token level** (`_toks` first). (b) structure-break mutants "silently re-seeded" dropped keys because the runner rebuilt drafts/taxonomy after overriding — fixed by passing the **full result dict** that genuinely omits those keys.
   - `judge sanity`: re-scores the already-rendered P-A/P-B/P-C manuscripts via `score_survey` (<10 min, measures judge/backend drift without a full pipeline re-run). Threshold logic uses a **σ floor of 0.10** when recorded sd=0.00 (P-B has two identical rounds) so zero-variance proxies are still compared.
   - CLI: `--freeze` (zero-LLM baseline → `baselines.json`, E-1), `--quick` (skip judge), default full cycle. Exit code **0 GREEN / 1 WARN / 2 FAIL**.
   - **Measured (first full cycle, 2026-09-20):** elapsed 73s, mock 34/34, pools 22/30, arXiv reachable, gate 23/23, judge P-A 0.4σ PASS · P-B 1.3σ WARN · P-C 1.7σ WARN → **exit 1 (WARN)**. The WARNs are the honest output the design wants ("run more variance rounds before trusting the delta"), not false alarms.
2. **WS-D D-1 `tools/llm/profiles.py`** — named, immutable per-lane profiles `{draft, qa, judge} → {backend, model, base_url}`:
   - `free-opencode` (default): all lanes → opencode hosted free model (`opencode/big-pickle`).
   - `judge-strong` (user-configured): `draft|qa` stay opencode (free lane), `judge` → `OPENAI_BASE_URL`/`OPENAI_MODEL`/`OPENAI_API_KEY` (any OpenAI-compatible provider).
   - **Loud failure verified**: unknown `LLM_PROFILE`, bogus backend, or missing `OPENAI_API_KEY` → `ProfileError` with the valid choices; no silent fallback. `clients_for()` → `(draft_client, judge_client)`; `profile_header()` dumps per-lane models (D-1 accept).
3. **WS-D D-2 per-role routing wired** — `bench_eval.py`, `variance_run.py`, `health_check.py` now build two LLMClients from the profile; `Pipeline(client, judge_client=...)` routes the P3 judge through the judge lane (`judge.py` already had the `client=` param + `judge_model` provenance). CLI `--profile` + legacy `--backend/--model` overrides coexist. **Accept: mock regression still 34/34 ALL PASS with routing active; `score_survey` records the judge lane's model.**
4. **Run memory (user req #4 — the headline feature)**:
   - `tools/eval/run_ledger.py`: durable per-driver `ResumeLedger` at `_eval_out/ledgers/<command>.json`, atomically written on **every** mutation. **fingerprint = profile name + exact id-set** — a rerun with different models/ids deliberately does NOT resume (provenance).
   - `bench_eval` wiring: each row persisted via an `on_row` callback *as it completes*; on restart `pending()` filters out done ids → `RESUME: k/n already done — continuing with n−k remaining`; a fully-done ledger regenerates the report with **zero LLM calls** (verified end-to-end: seeded P-A ledger → `main` reported `1/1 already done`, wrote report, no judge call).
   - `variance_run` wiring: per-topic `OUT` write (crash-safe) + round-skip resume (verified seed 1 round → only round 2 re-runs).
   - `tools/web/run_manager.py`: manifest mirrored to `_eval_out/web_runs/runs.json` on every transition → a server restart **re-hydrates** history; any run that was `pending`/`running` when the server died is shown as **`interrupted`** (log replay keeps the tail useful); `POST /runs/{id}/resume` re-issues the exact CLI command and the driver ledger continues. New `GET /runs/{id}/log` page + run cards show ledger progress. **Fixed a latent bug: `_run_card` was referenced but never defined → the Runs page would have raised `NameError`.**

Next: WS-D D-3/D-4 (strong-judge lane → cross-model judge variance matrix; provenance report footers) · **multi-spec support (user req #3: default = world-universal academic spec, then DAS-16/densitometric)** · L-1 re-rank · paper outline full draft (after `tools/citation-verify`). Parked R-items unchanged (`CAPABILITY-STATUS.md §3`).

---

## 2026-09-20 — Session 21d: F-3 read-only static export (WS-B) — `tools/web/export_static.py`, GH Pages deployable

**Why:** user confirmed GH Pages is the deployment target but (verified) Pages serves **static files only** — no server-side runtime. So the live FastAPI dashboard (SSE/cancel) stays local; the deployable artifact is a read-only static mirror of `_eval_out/`.

1. **`tools/web/export_static.py` implemented (stdlib-only, no uvicorn/fastapi import)** — `REPO_ROOT = Path(__file__).resolve().parent.parents[1]`; regenerates `gh-pages/`: `index.html` + `dashboard.html` + `manuscripts.html` (same inline-CSS/no-external-JS style as app.py) + `manuscripts/*.pdf` copies + `.nojekyll`. Renders variance mean±sd (from `variance_runs.json`), pools coverage (`pools_30.json`), bench report head (`bench_pilot_das.md`), manuscripts file list.
2. **Path hierarchy bug caught + fixed**: first attempt resolved repo-root one level too high (`parents[1]` on the file → `tools/` instead of repo root) — export silently found 0 pdfs; verified with a debug import (`EVAL_OUT` printed wrong, `dir exists: False`), fixed to `parent.parents[1]` (matches run_manager.py convention), re-ran → **44 pdfs exported**.
3. **Verified end-to-end**: `python -m tools.web.export_static --out gh-pages` → 3 pages + 44 pdfs; `python -m http.server 8788 --directory gh-pages` served `index.html`/`dashboard.html`/`manuscripts.html`/`P-A_manuscript.pdf` all **200** (P-A 3.88±0.53 row renders, pools table present). P-A/B/C variance rows and pool counts match Session 19 numbers.
4. **Docs wired**: runbook §3.0.5 gains "只读静态导出 (F-3)" + deploy instructions (GH Pages `branch: main / folder: /gh-pages`, `.nojekyll` note); PLAN.md F-3 marked **implemented**; AGENTS.md commit policy refreshed ("日常交付可自动 commit，绝不自动 push"). `gh-pages/` committed to main as the Pages publish source (Pages rebuilds on push).

Next: WS-C E-2 `tools/eval/health_check.py` (variance-aware 2σ thresholds, feeds baselines.json) and/or WS-D D-1 profile registry; L-1 re-rank; paper outline full draft (after `tools/citation-verify` on flagged refs). Parked R-items unchanged (`CAPABILITY-STATUS.md §3`).

---

## 2026-09-20 — Session 21c: web frontend implemented (WS-B), end-to-end usage flow (runbook §3.0), arXiv paper outline

**Why:** the user asked (1) to clarify the *end-to-end usage flow* — from "a user wants to research X" through "how to ask for dense/informative output" to "how to make output conform to a spec/format doc" — and (2) to implement the **frontend first** so there is a tangible, testable UI to iterate on; (3) afterwards, to outline a tool paper per current AI-industry practices for a later arXiv submission.

1. **WS-B `tools/web/` implemented (Phase F-1 + F-2, FastAPI)** — `app.py` + `run_manager.py` + `static/` (inline-CSS/Jinja-lite templates, zero external JS → no network dep, K1/K2-safe):
   - `GET /` runs page: 7 one-click buttons mirroring the exact CLI commands (`bench_eval` proxies / DAS rows / QA subset · `variance_run` · `pools_30` · `test_pipeline mock|real`); **SSE live tail** (`/runs/{id}/events`, JSON line+status events, keep-alive) + **cancel** (`DELETE`, Windows `taskkill /T /F` tree-kill — no orphaned python; measured: cancel on real pipe → `cancelled` rc=1, 0 new python pids survive).
   - `GET /dashboard` read-only view over measured artifacts: `variance_runs.json` (mean±sd table), `pools_30.json` coverage, manuscripts list, raw `bench_pilot_das.md` head.
   - `GET /manuscripts` + `/manuscripts/{name}.pdf` (FileResponse); `GET/POST /feedback` append JSONL → phase-X E-5 corpus entry.
   - **Smoke tests run green**: all 4 pages 200 via TestClient; a full `test_pipeline mock` run streamed 38 SSE lines → `done rc=0`; cancel path cleaned the process tree. Env `ds0509` already had fastapi/uvicorn/jinja2/httpx (no new deps).
2. **runbook §3.0 "End-to-end usage flow / 端到端使用流程" added** (before §3.1) — answers the user's question-first framing:
   - Step 0 question-first track selection (survey / grounded QA / battery) → Step 1 discovery rail (`S_LIT_BACKEND=seed|arxiv|orx`) → Step 2 **"set dense/informative output"** (judge rubric, batch size `--limit`/`--judge`, render pages; language/depth knobs = Phase X/D roadmap, marked not-yet-available) → Step 3 **"output conforms to a spec"** (map desired spec → which gate enforces it: academic-style+reuse → STORM outline/citation-verify; DAS-16 → judge; deterministic fact → L6; typography/CJK → render_manuscript; non-regression → Phase X baselines; ≥300B judge → Phase D-3 lane) → Step 4 run via CLI or web → Step 5 feedback + Phase X iteration rules (variance-aware 2σ thresholds, N≥3 / Δ≥2σ promotion).
3. **`docs/design/tool-paper-outline.md` written (bilingual, arXiv-style systems paper)** — draft Title/Abstract (planned ~180–250 words, all 6 beats), Keywords, and full outlines for Intro (problem: GPT-4o hallucinated ~78–90% citations per OpenScholar Nature 650:857, DOI 10.1038/s41586-025-10072-4), Related Work (STORM 2402.14207 / orx / PaperQA2 2409.13740 / DAS 2608.18034 / Tongyi 2510.24701 / OpenScholar), System Design (L0–L6 + two routing modes + guardrail design + Phase X/D), Evaluation (Sessions 11–19 measured numbers with `as of` dates), Discussion (honest limitation list), Conclusion, and an **IEEE-style numbered reference list** with `tools/citation-verify` re-check flagged for the unverified arXiv IDs (DAS 2608.18034, Huang 2310.01798, Tyen 2311.08516, MinerU 2410.17381, PaddleOCR 2510.14528). Expansion roadmap at the bottom (`[PLAN]` markers for pending ablations/cost table/figures).
4. **Docs map updated**: AGENTS.md design map + self-evolution list entry (tool-paper-outline.md); README.md + README.zh-CN.md roadmap item 8 → paper outline. Runbook header Updated note extended (§3.0 + web).

Next: WS-C E-2 `tools/eval/health_check.py` and/or WS-D D-1 profile registry when green-lit; paper outline can be expanded into a full draft (run `tools/citation-verify` on the flagged refs first). Parked R-items unchanged (`CAPABILITY-STATUS.md §3`).

---

---

## 2026-09-20 — Session 21b: parallel workstream re-plan + model access/routing design

**Why:** the user asked to (1) locate the usage/demo docs, (2) systematically re-organize the plan so frontend+backend+self-evolution are **parallel and each evaluated**, and (3) design how the frontend gets its model — i.e. whether to rely on opencode registration and/or mainstream model API keys.

1. **Plan §8 reorganized into five parallel workstreams + evaluation gates (not phases):** WS-A core pipeline (Phase L) · WS-B web frontend/backend shell (Phase F) · WS-C self-evolution (Phase X) · **WS-D model access & routing (Phase D, new)** · WS-R resource-gated (Phase R). Each row carries a *blocking dep*, *can-start* date, and an *evaluation gate*; B/C/D can start immediately and in parallel with A — rule: **no B/D commit may regress C's baselines; no C "improvement" claim valid without a D cross-model check**; WS-C logs under its own PROGRESS heading so sessions interleave.
2. **WS-D model routing design (frontend model source):** both lanes are supported by the existing `tools/llm/client.py` — (a) **opencode registration** = zero-key free hosted model via `opencode run` (default, verified 3/3), (b) **mainstream API keys** = any OpenAI-compatible provider already wired in the `openai` backend (DeepSeek / DashScope·Qwen / Moonshot·Kimi / OpenRouter / OpenAI), via `OPENAI_BASE_URL`+`OPENAI_MODEL`+`OPENAI_API_KEY` (client.py:22-27). New: **per-role profiles** (`tools/llm/profiles.py`, D-1) put `draft|qa` on the cheap lane and `judge` on a strong-model lane (D-2/D-3) — the **judge lane currently runs on the same free model as drafting** (judge.py:71) and is a measured noise contributor (P-A ±0.53); a registered ≥300B judge lane is the cheapest model-side credibility lever and unblocks R-1/E-7. Keys stay env-only, never in repo/web bundle; profile name + model + temperature recorded in report footers (D-4/D-5, provenance).
3. **Cross-check vs measured evidence:** weak judge model is real (internal cross-judge Qwen-vs-Kimi agreement ?=0.507, MAE=0.630 — PROGRESS); free-model drafting is fine (draft quality not the bottleneck). So D-3 (strong judge lane) + L-3 (median-of-3) target P-A sd < 0.40.

Next: WS-B `tools/web/app.py` scaffold (F-1) and/or WS-D profile registry (D-1) can start now; WS-C `tools/eval/health_check.py` (E-2) is parallel-ready; L-1 re-rank awaits a green-light. All parked R items unchanged (`CAPABILITY-STATUS.md §3`).

---

## 2026-09-20 — Session 21: self-evolution mechanism design, tool-usage & demo docs, web-frontend analysis

**Why:** the user (after Session 20) asked to fold two more things into the plan — (1) put tool usage/demo content into the docs, (2) design a self-evolution mechanism (periodic evolution/update/debug) — then asked to research, argue and evaluate the self-evolution approach thoroughly. Web-verified 2026-09-20, blended with the measured numbers from Sessions 11–19.

1. **`docs/design/self-evolution-mechanism.md` written (bilingual, 10 sections)** — one source for the design rules + evidence + failure modes behind PLAN §8 Phase X. Core findings:
   - **Intrinsic self-correction is unreliable/harmful for reasoning**: LLMs keep their first GSM8K answer 74.7% and mostly change correct→wrong (Huang et al. 2310.01798); GPT-4 locates logical errors only 52.87% (Tyen et al. 2311.08516) → **evolution triggers must come from external measurement**, never "the model noticing it's wrong".
   - **Canonical 4-phase cycle** to adopt (experience acquisition → refinement → updating → evaluation, Tao et al. 2404.14387): our Phase X maps E-1/frozen subset → E-5/feedback corpus → E-3/tickets → E-2/health check.
   - **Prompt-level, metric-gated evolution is the right mechanism class** (DSPy 2310.03714 · MIPRO 2406.11695 · **GEPA 2507.19457: beats GRPO up to ~20pp using 35× fewer rollouts** · TextGrad 2406.07496) — but E-5 starts **manual** (mini-GEPA), automated only in Phase R with a strong reflection LM.
   - **Anti-collapse guardrail**: feedback must stay anchored to real primary gold (Seddik 2404.05090: mixing real data within a bound avoids collapse) → provenance tag + real-ground-truth floor per cadence.
   - **Mutation testing hardens the deterministic gate** (E-2b `gate_coverage`, zero-LLM) — the highest-value/lowest-cost "evolutionary" act.
   - Feasibility×value matrix + honest boundary (scheduled measurement + human-gated repair; **no** auto-commit / weight updates / unattended prompt evolution).
2. **PLAN §8 Phase X refined** per the research — added: `E-2b` gate-coverage mutation check (≥20 mutants, 100% kill-rate, σ-aware thresholds), E-5 provenance floor + promotion rule (N≥3, Δ≥2σ, no mock/gold regression, adjudicator-swap survival in R), E-7 GEPA/DSPy automated option (R-phase); hard design rules (a) external triggers only, (b) variance-aware thresholds (P-A σ 0.53 → its own 2σ).
3. **PLAN §8 L-5 delivered: `docs/setup-runbook.md` §3.1 "Usage & demo walkthroughs / 用法与演示"** — per-tool cheat-sheet (purpose · verified command · version pin · known issue K#) + Demo A (PDF → grounded draft → manuscript PDF), Demo B (evidence-grounded QA), Demo C (30-topic battery + variance → E-1 baselines), Demo D (manual L6 judge inspection). Requirement: fresh agent reproduces every stage from the runbook alone; `rg` stale-command sweep zero-hit.
4. **PLAN §8 Phase F added: local web frontend (FastAPI, ≈$0)** — **decision: FastAPI, not Flask, not static-only**:
   - *Static no-backend*: renders `_eval_out/` read-only only → can't trigger runs / stream progress / cancel → insufficient (kept as F-3 fallback).
   - *Flask (WSGI/sync)*: real bench runs take 2–8 min; sync worker blocks other requests; live progress+cancel needs hand-rolled threads/queues ≥ FastAPI's native async complexity, without Pydantic/OpenAPI → **not chosen**.
   - *FastAPI (ASGI/uvicorn)*: native async → SSE progress + concurrent triggers + cooperative cancel; Pydantic v2 models map `_eval_out` + pipeline state; auto OpenAPI/Swagger. Local single-user has no perf pressure, but async+types+docs come at zero extra cost → **chosen**. Frontend = Jinja2 + htmx (vendor-local CDN copy, K1/K2 network flakiness), **zero Node toolchain**.
   - *Gradio/Streamlit*: fast demo start but weak typing + boilerplate control → one-off comparison only, not the landing choice.
   - Directions (RPS 3–7×, star counts ~78-82k vs ~68k) are directional/secondary (tech-insider 2026-04-02 · ByteIota 2025-12 · dev.to 2025-02-05); decision rests on sync-vs-async + type/validation facts.
   - F-1 scaffold (`tools/web/app.py`, bind `127.0.0.1`, routes for dashboard/runs/SSE/cancel/manuscripts/feedback) · F-2 live SSE stage map + cancel · F-3 read-only fallback · F-4 wiring into Phase X cadence (E-2/E-3/E-4/E-5 visible on one local URL). Acceptance = uvicorn serves dashboard, real run cancellable, no orphaned processes.
5. Docs map/README cross-links pending in AGENTS/README (self-evolution-mechanism entry) — included in the Session 21 commit.

Next: commit+push Session 21 docs; then Phase L-1 (relevance re-rank) and/or F-1 scaffold when the user green-lights; parked P3/R-phase blocked items (≥300B judge / GPU / keys) remain in `CAPABILITY-STATUS.md §3`.

---

## 2026-09-20 — Session 20: tool comparison, reusable-asset survey, next-implementation plan

**Why:** the user asked for (1) a positioning/comparison doc of our tools per pipeline stage vs each stage's line-research tools, (2) a written next-implementation plan, (3) a survey of downloadable/referenceable/integratable skills–harnesses–methods–prompts (explicitly "Stanford 的工具"). Web-verified 2026-09-20.

1. **`docs/TOOL-COMPARISON.md` written** — L1→L6 stage-by-stage compare (ours vs STORM / orx-OpenResearch / PaperQA2 / DAS / DAS-Bench / MinerU / arXiv): 我们用 5-gram 接地门 + 本地零成本胜；真实缺口 = L1 无元数据湖（DAS-2M）、L3 无多视角/逆向路由（STORM/DAS）、L4 无检索重排（PaperQA2 RCS）、L6 判题自实现（官方工具包已出）。含**可复用资产清单**（附 2026-09-20 核验来源与 Feas×Val 决策）。
2. **`docs/PLAN.md` §8 added** — 后续实现规划两阶段：**Phase L（本地 ≈$0）** L-1 S_write 检索重排（BM25-style 复刻 PaperQA2 RCS）→ L-2 S_org 多视角分解（STORM 思想 prompt-only）→ L-3 判题 median-of-3（压 P-A 0.53 的 judge 噪声）→ L-4 引用校验接线（本地 skill）；**Phase R（资源门控）** R-1 官方 DAS-Eval 工具包运行（2026-08-20 发布，现已可套用）· R-2 DAS-2M 元数据湖 rail（2026-08-08 发布）· R-3 knowledge-storm 模块级替换（1.1.1，Co-STORM/VectorRM）· R-4 orx 启用（Windows beta + `install-skills`）· R-5 paper-qa 后端（可选加重）· R-6 220 篇样例综述做判题校准语料（2026-08-14 发布）。每项带可度量验收。
3. **被调研资产关键确认（2026-09-20 一手核证）**：
   - Stanford OVAL **knowledge-storm v1.1.1**（MIT, pip）：含 Co-STORM、litellm 集成、**VectorRM 支持用户文档 grounding**——但接入需 OpenAI 兼容端点（我们只有 opencode CLI，非 litellm 兼容）→ Phase R。
   - OpenResearch 已进化为 **autoresearch 平台**：`orx up` 仪表盘、`orx install-skills` 可把 agent-skills 装进 Claude Code/Codex/OpenCode/Cursor、Windows beta、`orx paper`=alphaXiv 全文检索（无需登录）。
   - **DAS-Bench + DAS-Eval 评测工具包 2026-08-20 发布**（HF+GitHub，含评测代码）；**DAS-2M 2026-08-08、220 篇 DAS 样例综述 2026-08-14 发布**；**DAS 方法代码仍 ⏳ 未发布** → 状态机/路由按论文复现路径未被推翻。
   - opencode Agent Skills 机制确认：SKILL.md 放 `.opencode/skills/` / `~/.config/opencode/skills/`，兼读 `.claude/skills/` 与 `.agents/skills/`。
4. Docs map updated（AGENTS.md / README.md / README.zh-CN.md 加入 TOOL-COMPARISON 条目；README 路线图加第 4 项并指向 `PLAN.md §8`）。

Next: Phase L-1 (relevance re-rank in `_write`) when the user green-lights; parked: P3 original blocked items (≥300B judge/GPU/keys) remain listed in `CAPABILITY-STATUS.md §3`.

---

## 2026-09-19 — Session 19b: 30-topic evidence-pool battery + judge variance (local, no keys)

**Why:** the user asked to push through the remaining local work and get a measured capability statement. Two gaps: (1) the pipeline had only ever been judged on 3 proxy topics + 2 no-evidence DAS rows — is it *generic*? (2) The local judge is a non-deterministic free model — how noisy is a Total?

1. **30-topic evidence-pool battery (`tools/eval/pools_30.py`)**: for each DAS-Bench topic → live arXiv discovery → download + windowed MinerU parse of top candidates → incremental manifest `_eval_out/pools_30.json`.
   - **Result: 30/30 topics processed; 22 have ≥1 locally parsed source paper (12 full 3-paper pools); 8 empty** (network/relevance caps — a measured coverage property, not silent).
   - Real bugs hit & fixed: arXiv API `.../2503.16581v1` version suffix broke `_ID_RE`'s trailing `\b`; MinerU subprocess had **no timeout** (30-min hang on one PDF); judge step had no breakpoint resume.
   - **End-to-end judged sample n=10 → Total 3.13** (BSC 3.08 · MAR 2.67 · TSQ 3.05 · HDQ 3.73; report `_eval_out/pools_30_report.md`). HDQ 3.73 confirms synthesis is where the pipeline shines; MAR 2.67 is dragged by 1-paper pools + text-only artifact.

2. **Judge variance (`tools/eval/variance_run.py`)**: P-A/P-B/P-C × 2 fresh rounds → **P-A 3.88±0.53 · P-B 3.31±0.00 · P-C 3.53±0.13**. P-A's ±0.53 is honest judge noise on the strongest topic.

3. **Robustness hardening**: LLMClient now retries empty opencode sessions up to 3× (flat, backoff); QA scorer recovers truncated judge JSON (max_tokens 400→1000 + regex fallback); judge is per-topic cached.

4. **PubMedQA yes/no mode (`answer_question(mode="yesno")`)**: final-decision convergence instruction added; PQ-1..14 real runs → 8/14 correct, correctness 3.57. Yes/no *conclusion* is a model boundary, not a prompt gap.

5. **QA panel regenerated full → n=31**: correctness 4.23 · groundedness 4.45 · 24/31; extract/context path (Qasper+SciQ+news+seed-route) **12/13**. New corpus paper `1703.10344` (news suggestions, 12 pp, one-command add via `add_paper.py`).

Next: capabilities document `docs/CAPABILITY-STATUS.md`; remaining blocked items are the API-key/GPU/Chinese-corpus ones listed in §3 of that doc.

---

## 2026-09-17 — Session 19: QA panel expansion — Qasper +3 papers, SciQ provided-context MCQs

**Why:** Session 18 proved the extractive-answer node on 2 Qasper QAs; widen the QA benchmark to a statistically meaningful panel and add a provided-context (MCQ) source — all local, no API keys.

1. **Qasper +3 external papers** (each 9–11 pp, MinerU `-m txt` windowed, all merged + registered in `_LOCAL_MD`): `1910.09982` (NLP4IF-2019 propaganda techniques), `1910.06036` (to-the-point QG metrics), `1908.06267` (MPAD document embeddings datasets). Parse flake hit once again on `1910.06036` pages 0-5 (3 failed tries) → **sub-windowed 0-3 + 4-5** (4-5 took 4 tries) — the known probabilistic worker instability; the window-splitting workaround holds.
2. **SciQ (AllenAI) provided-context mode — new `ctx` routing**: question + the dataset's `support` sentence = the whole source (no download, no paper). `check_answer(..., require_cite=False)` skips the arXiv-cite gate for context sources; answer node unchanged. 5 validation-set MCQs (frameshift/nucleotide, wetland, blood vessels, volcanic-ash clays, density).
3. **Real results** (all extract/context paths ~15–20 s/answer):
   - **QA-8 propaganda → c 5 · g 5 · gold 3/3** · **QA-9 QG metrics → c 5 · g 5 · gold 3/3** · **QA-10 MPAD datasets → c 5 · g 5 · gold 3/3**
   - **SQ-1..5 → all c 5 · gold 1/1** (groundedness 3–5 — short context limits the judge's citation check, correct answers still exact)
   - **QA pilot panel n=15: correctness mean 4.73 · groundedness 4.40** · 14/15 correct-and-grounded (only QA-3 taxonomy at c 3); **extractive/context paths 10/10 perfect**.
4. **Reading**: (a) the answer node is now reliable for extractive + provided-context factoids across four benchmark sources (Qasper, SciQ, PubMedQA, news-suggestion); (b) the remaining imperfect cells are *synthesis/taxonomy* (multi-paper S_write) and *yes/no-style biomedical judgment* (2/5 PubMedQA misses — model over-answers instead of concluding yes/no/maybe; the short one-paragraph abstracts cap available evidence); (c) judge `groundedness` on one-sentence contexts is conservative (3-4) — fine as a conservative floor.

5. **Efficiency tooling (same session):** new one-command corpus adder `tools/eval/add_paper.py` codifies the download → page-count → windowed `-m txt` parse (≤6 pp/window, distinct `-o` dirs) → sub-split recovery on flake → merge step (12-pp paper added in one call, both windows clean). Plus a QA-scorer fix: `parse_json_dict` can't recover a judge reply truncated by `max_tokens=400`; bumped to 1000 and added a regex fallback in `score_qa` (QA-12 was scored 0/0 by a truncated judge parse → recovery shows 5/5, gold 1/1).

6. **Extended panel (real runs, all extract/context):** PubMedQA `pqa_labeled` 5 QAs (PQ-1..5, yes/no/maybe with abstract context, gold tokens directional): PQ-2/3/4→c 4, PQ-1/5→c 2 (miss). News-suggestion paper `1703.10344` (12 pp, added via `add_paper.py`) → QA-11/QA-12 precision anchors → 5/5 each, gold 1/1.
   **QA pilot panel n=22: correctness mean 4.41 · groundedness 4.41 · 19/22 correct** — extract/context paths (Qasper + SciQ + news-suggestion) **13/13 perfect**; weaknesses concentrated in PubMedQA yes/no judgment (3/5).

Next (local-first): PubMedQA panel widening (better prompts for yes/no grounding), 30-DAS-topic evidence pools (CPU), variance re-runs.

---

## 2026-09-17 — Session 18: Qasper end-to-end on external-author gold questions (answer-not-survey node)

**Why:** Session 17 left QA-3 as a survey-path failure; the plan called for proving the pipeline against *external-author* gold QA (Qasper) — question + source paper, answers written by the benchmark's annotators.

1. **Qasper data obtained locally**: repo `allenai/qasper` is script-only (new `datasets` rejects scripts), so pulled `qasper-train-dev-v0.3.tgz` (10.8 MB) straight from `qasper-dataset.s3.us-west-2.amazonaws.com`; dev v0.3 = 281 papers; **paper keys ARE arXiv ids** (`1908.10084`, `1611.03599`, …). Selected two clean extractive QAs: SBERT "What metrics are used for the STS tasks?" (gold: Pearson/Spearman) and UTCNN "What is the size of the Chinese data?" (gold: 2,496 authors / 505,137 likers on the FBFans dataset).
2. **Two new corpus papers parsed locally** (`-m txt`, 11 pp each in two 6-page windows, all four MinerU windows first-try — no 502 tonight): `1908.10084` (SBERT) + `1611.03599` (UTCNN) registered in `_LOCAL_MD`.
3. **Bug #1 — seed routing**: `resolved_evidence` only honored an arXiv id when the whole question was a bare id; embedding ids in QA text fell through to discovery → `candidates=[]`, NO-EVIDENCE. Fix: **any arXiv id in the question resolves directly through the manifest** (Qasper/BenchQA contract). Mock + real verified (`paper_id` resolves).
4. **Bug #2 — survey ≠ answer**: with evidence routed, both Qasper QAs were judged **c=2 and c=1, gold 0/2** — the survey manuscript recites the paper ("…answers *about* the paper") even though gold facts (pearson×4, 2,496×1) are verbatim in the parsed corpus. Decisive learnable-loop fix: **new `tools/pipeline/answer.py` — grounded extractive-answer node**: question + target-paper md (40K) → one tight LLM call → terse answer with inline `(arXiv:…)` cites + verbatim evidence line; deterministic `check_answer` L6 gate (non-empty + cite present). `run_scenarios` routes `qa` scenarios that carry a `seed_id` to this node (survey graph stays for corpus-anchored synthesis QAs).
5. **Results after the fix** (each ~16 s, single LLM call):
   - QA-6 SBERT metrics → **c 5 · g 5 · gold 2/2** (was c=2/0/2)
   - QA-7 UTCNN data size → **c 5 · g 5 · gold 2/2** (was c=1/0/2)
   - QA-3 (taxonomy, re-routed to extractive) → **c 1→3, g 2→3, gold 1/2** — better but still not perfect: *taxonomy/relation synthesis* genuinely needs multi-paper synthesis, not extraction — a documented boundary, not a bug.
   - **QA pilot totals (n=7): correctness mean 4.43 · groundedness mean 4.57 · 6/7 correct-and-grounded**; extractive path 3/3 gold-hits perfect.
6. **Env nugg**: `UnicodeDecodeError: 'charmap' codec` in the opencode subprocess reader thread (0x81 byte, cp1252) — non-fatal (recovered, run completed), but note: console/redirect defaults are cp1252 on this box; use `python -X utf8` for UTF-8 pipelines. Panel B localization note.
7. **Real-suite variance witness (P1 strict matrix)**: `test_pipeline real` hit **33/34** on one run — P3 judge returned `verdict=fail` on the rubric checks for the *same* demo input; immediate re-run **34/34**. Confirms the strict deterministic thresholds are sensitive to local-model nondeterminism on check boundaries (expected; documented; thresholds deliberately NOT loosened — the fail-side is the safe side).

Next (all local-first): widen the QA panel (e.g. PubMedQA/SciQ MCQs via the same `seed_id` + scorer), 30-DAS-topic evidence pools (CPU time), run-to-run variance re-runs.

---

## 2026-09-17 — Session 17: Track C part 1 — evidence-grounded QA pilot (`qa` scenario family + QA scorer)

**Why:** the user asked whether we can absorb more external datasets/benchmarks (auto-research troves); we verified GAIA (ICLR 2024 · HF · 466 Qs · 3 levels) and Qasper (ACL 2022 · ~5k QAs over ACL full texts) are HF-reachable, then chose the cheapest local-first entry: **corpus-anchored QA** (questions answerable from our 3 already-parsed papers — zero downloads).

1. `tools/eval/bench_eval.py`: new `QA_SCENARIOS` (5 questions, each with `gold_tokens` for a deterministic fact-hit flag), `score_qa()` (correctness 1-5 + groundedness 1-5, JSON rubric prompt), qa routing in `run_scenarios` (row gets `row["qa"]` instead of DAS `bench`), console/report blocks (QA detail sections + `QA pilot` mean table); family-means table now only aggregates `das`/`proxy` rows (qa excluded). Mock route added to `mock_openai_server.py`. Mock sanity: 2 qa + 1 proxy + cache merge ✓ (34/34 test suite unaffected — qa is opt-in via `--scenarios QA-x`).
2. **Real pilot (5 Qs ≈ 25.5 min total; P-A re-run in same invocation restored its cache from the earlier mock pollution)**:
   - QA-1 GLTR visualization → c 4 · g 4 · gold 2/3 · **correct**
   - QA-2 Liang non-native bias → c 5 · g 5 · gold 2/2 · **correct** (61.22% FPR / 91 TOEFL essays reproduced)
   - QA-3 Weber-Wulff method families → c 1 · g 2 · gold 0/2 · **miss** — judge: "never answers the question; recites bibliographic-identity/evidence-boundary commentary; also misidentifies the paper's nature". Genuine failure mode: **question asks for a taxonomy mapping; the single-paper survey artifact answers 'about the paper' instead**.
   - QA-4 Liang Turing-test protocol → c 5 · g 5 · gold 1/2 · **correct**
   - QA-5 GLTR token statistics → c 4 · g 5 · gold 2/3 · **correct**
   - **QA pilot mean: correctness 3.80 · groundedness 4.20 (4/5 questions answered correctly and grounded).**
3. **Canonical DAS numbers updated**: P-A fresh re-run **3.94** (vs 3.62 last session — judge run-to-run variance ±0.3 again, documented) → family means **BSC 3.67 / MAR 3.33 / TSQ 3.42 / HDQ 4.25 / Total 3.67** (n=3).
4. **Batting average verdict**: the QA harness works end-to-end locally (~8 min/answer, gold-token fact check is cheap and meaningful: 4/5 aligned with the judge); QA-3 is a learnable case — taxonomy/relations questions need the multi-paper synthesis + an explicit "answer the question, not the paper" instruction, or fine-grained grounded extraction over the full text rather than the survey summary.

Next (local-first, no API keys): widen the QA panel (PubMedQA/SciQ MCQs via the same `seed_id` + scorer), 30-DAS-topic evidence pools (CPU time), run-to-run variance re-runs.

---

## 2026-09-16 — Session 16: data hygiene — bench sidecar cache + P-A/P-C dedup (评测缓存 + 代理问题去重)

**Why:** (a) bench `--out` overwrites the whole report per invocation — we hit the trap twice; (b) P-A and P-C were near-duplicates of the same question, double-counting the same bias/bench angle.

1. **Sidecar cache (`tools/eval/bench_eval.py`)** — per-scenario JSON cache under `_eval_out/bench_cache/`; when `--scenarios` is a subset, non-run scenarios load from cache (flagged `cached (vintage run)` in the report). Canonical report is now rebuildable at low cost; `--save`/merge logic unit-probed.
2. **P-A/P-C dedup** — P-C is now a *distinct* multi-paper synthesis question (methods taxonomy: statistical detection / watermarking / classifiers / human judgment — where the 3-source pool actually disagrees and the gaps are), not a re-run of P-A.
3. **Canonical numbers (this round)**: P-A **3.62** · P-B **3.06** · **P-C 4.00** (vintage cached run) — **family means BSC 3.42 / MAR 3.42 / TSQ 3.42 / HDQ 4.00 / Total 3.56** (best so far; MAR tied at 3.42 thanks to the manuscript fix). 001/019 no-evidence hold. Judge run-to-run variance ±0.4 still documented.
4. **Open choice (surfaced to user)**: next unblocked workstream — Track B (PaddleOCR Chinese evidence layer, needs a Chinese corpus choice) vs Track C (external benchmarks: GAIA verified reachable at HF · 466 Qs · 3 levels · level-1 sampleable; Qasper = QA-over-papers for evidence-grounded QA; PubMedQA/SciQ MCQ quick smokes). User approved plan → **Track C Qasper-style, starting with corpus-anchored QA pilot (5 Qs, zero new downloads), expanding to Qasper if HF reachable.**

Next: Track C pilot (Session 17+).

---

## 2026-09-16 — Session 15: MAR render axes (part 1) — manuscript output + PDF rendering (手稿化产物 + 本地 PDF 渲染)

**Why:** DAS-16 MAR family (Citation/Reference presentation, Figure/Table quality, Layout, Component completeness) was the residual low axis — the plain draft had no abstract/table/references, and figures were impossible, so MAR sat ~1–2. Delivery: complete-manuscript artifact + a real rendered PDF.

1. **Manuscript `_finalize` (graph.py)** — final output is now `# <question>` → `## Abstract` (intro's first ¶) → `## Intro` (the per-section draft body) → `## Evidence Table` (claims[:12], `| # | Claim | arXiv source | confidence |`) → `## References` (unique arXiv ids, abs links) → audit annex (`## Sources/Outline/Claims`, stripped by the bench so the annotator judges the manuscript proper).
2. **`tools/eval/render_manuscript.py` (new)** — pandoc + MiKTeX xelatex + Microsoft YaHei (CJK) markdown→PDF, pypdf page count; best-effort (pages=0 → skipped). Hitch-free, CJK smoke verified.
3. **bench_eval upgrades** — artifact = manuscript (annex stripped) + **judge context raised 12K→40K chars** (`_MAX_ARTIFACT_CHARS`) — **the bug fix: the Evidence Table and References sat past the old truncation so the judge never saw them** (this also explains the transient score dip in the intermediate run); per-scenario PDF render with `pdf pg` report column + `rendered manuscript (MAR)` note.
4. **Verification** — mock 34/34 · real 34/34 (243.6 s); PDFs render (P-A 8 pp / P-B 5 pp / P-C 7 pp). **MAR fix validated on P-A solo: Figure/Table 1→3, MAR 1.75→2.50.**
5. **Canonical combined run (single 5-scenario invocation; NOTE: `--out` overwrites, so always run all scenarios in one call)**: P-A 3.25 · P-B 2.75 · P-C 3.12 (all L6 1.0 · cov 16/16 · pdf 8/5/7 pp); 001/019 no-evidence hold. **Family means (n=3): BSC 2.92 / MAR 2.67 / TSQ 2.83 / HDQ 3.75 / Total 3.04.** Run-to-run judge variance ±0.4 documented (P-A 2.12–3.25 today).
6. **Honest residual — MAR "Layout and Formatting" axis**: a text-only LLM judge cannot score page layout; the rendered PDFs are now the substrate, so a ≥300B frozen page-aware judge (P3) is the remaining gap, not the pipeline.

Next (roadmap §7): P3 the judge + rendered-page MAR (needs keys/GPU/network); Track B (PaddleOCR Chinese evidence) wiring; P-A/P-C near-duplicate question dedup.

---

## 2026-09-16 — Session 14: P1 judge threshold calibration — strict matrix v1 (评审门槛收紧)

**Roadmap §7 P1 acceptance met:** documented pass/revise threshold matrix + regression.

1. **Rubric 1-5 anchors** — `judge.py` now defines what each score means (5 = publishable without reservation, 4 = strong/major-edits-free, 3 = usable-needs-revision, 2 = weak, 1 = unusable) and explicitly: "a typical strong survey is 4, not 5 — reserve 5 for the rare exceptionally tight draft." Direct answer to the leniency seen at pass@4–5.
2. **Strict deterministic threshold matrix v1** — `_pick_label` is now the *only* authority on the label (model's own label is ignored unless it's one of pass/revise/fail): **pass** = score≥4 ∧ **all four** checks true (clarity now mandatory); **fail** = groundedness False (factual integrity — DAS "Reference Faithfulness" family) OR score<2; else **revise**. Documented parity map: internal score 5 ≈ DAS-16 family Total ~3.2 (n=1 real run), score 3 ≈ ~2.4 (Session 11 preview range) — calibrated directionally, re-baseline flagged for a ≥300B frozen judge.
3. **Regression** — `test_pipeline._assert_label_matrix` unit-tests all 7 matrix cells deterministically (zero LLM) in both modes; mock judge (score 5, all checks) still passes.
4. **Verification** — **mock 33/33 PASS**, **real 33/33 PASS (276.3 s)**; the real-run judge verdict is still `pass` under the strict matrix — the tightened gate rejects only genuinely weak artifacts, and the current survey-draft clears the bar.

Next (roadmap §7): MAR render axes (page-rendered artifact / figure-table extraction — plain markdown cannot score Figure/Table quality), then DAS-Bench full compliance (DAS-2M + ≥300B judge), then Track B.

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
6. ✅ **WS-C self-evolution mechanism implemented (Session 22)** — E-3 cadence (`evolution_sprint.py`) + E-4 dep ledger + E-5 feedback/promotion (all zero-LLM, human-gated, ledger-only) + L-6 `self_check.ps1`; Phase L (L-1 BM25 re-rank · L-2 perspectives · L-3 median) + D-3 judge matrix + D-4 provenance. Guards `test_evolution.py` ALL PASS · mock 34/34 · self-check GREEN.
7. **Next plan (forward)** —
   - **A. First *live* cadence + acceptance numbers:** run `evolution_sprint` (not `--quick`) + `bench_eval --median-rounds 3` + `variance_run --rounds 2 --median-rounds 3` to (i) re-measure L-3 judge sd (target <0.40 on P-A), (ii) judge L-1/L-2 acceptance on real P-A..C + a mid-paper QA topic, (iii) let the E-4 ledger promote `baselines.json` only on a confirmed sustained shift. Then flip the loop's own ledgers (`tickets`/`revisions`) with the human green-light if a repair is *eligible*.
   - **B. Close the L-5 stale-command sweep** — `rg` the runbook's verified-command list vs old Ollama/env references; remove/flag `superseded`.
   - **C. WS-B (Phase F) web wiring of the new CLI surface** — expose `self_check.ps1` / `evolution_sprint` / `judge_matrix` as read-only dashboard actions over `_eval_out/*.json` (F-1..F-4 stable CLI + `_eval_out` I/O contract).
   - **D. Phase R (gated on a ≥300B OpenAI-compatible key):** D-3 strong-judge lane compression + official DAS-Eval (R-1) + GEPA/DSPy auto prompt evolution + adjudicator swap (E-7) feeding the promotion gate a *different* vantage.
8. Keep PROGRESS.md and PLAN.md in sync; **no commits unless requested** (none made this session).
