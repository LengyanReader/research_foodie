# AI 工具栈扫描 · The outside-harness tool ecosystem (P68)

> 中文速览：本轮回答一个问题——**harness 模式之外，还有哪些"能直接加强大模型能力"的现成工具应当整合进本工厂的循环**。方法：先广泛检索（二手线索），再逐一回一手源（GitHub API 元数据 + 官方 README/规范页）核验许可与维护状态，访问日期统一 **2026-11-03**。结论按七个能力族整理：记忆层、可观测、代码沙箱、结构输出、评测/红队、网关/本地推理、护栏；另发现三条"代谢事实"（GraphRAG 进入维护模式、Mem0 榜单分属托管平台、LiteLLM/NeMo 许可为 NOASSERTION），均已如实入册。可持续机制：新观察主题 `ai-tool-stack` 已接进 watchlist（LLM 发现）+ sources.json（feed 拉取）→ 每次 `full-update` 的 intel→evolve→self-model 环自动扫描-评估-提案，人审后入册。

**Updated:** 2026-11-03 · Purpose: survey integrable AI-era tooling beyond harness *patterns* · Machine-readable registration: `data/sources.json` group `tools` (topic `ai-tool-stack`) · Router sheet: [`reference/tool-router.md`](../reference/tool-router.md) §4 family #2 · Loop: discover → evaluate → register → metabolize (tool-router §1).

---

## 1. Scope and method · 范围与方法

The library already encodes *patterns* (core M0–M8) and *harnesses* (vendor surfaces). What it did not systematically carry: **component tools** — memory layers, observability stacks, sandboxes, structured-output engines, eval/red-team runners, gateways, local inference — that an emitted harness can *use* to make an LLM strictly more capable. This scan covers seven such families.

Method (citations-lifeline): every row below was resolved to a **primary source** — the GitHub REST API (`api.github.com/repos/…`, machine metadata: license SPDX, `pushed_at`) and/or the official README/spec page — probed **2026-11-03**. Directory/blog claims were used only as discovery leads, never as facts. Anything not verified from this environment is marked *unverified*.

Already registered before this round (not re-surveyed): `dspy` (prompt optimization), `letta` (memory server), `guidance`, `qdrant`, `chroma`, `huggingface`, `exa`/`tavily`/`brave-search`/`searxng`/`serpapi` (search), the MCP discovery surfaces (`tool-router.md` §2).

## 2. The seven families · 七个能力族

| # | Family · 能力族 | What it adds to a harness · 补什么能力 | Anchor modules |
|---|---|---|---|
| F1 | Agent memory layers 记忆层 | persistent, retrievable, temporal user/agent state beyond the context window | M2 (context), M5 (provenance) |
| F2 | LLM observability 可观测 | traces/metrics/cost of every model+tool call; OTel-standard telemetry feeds the trace vocabulary | M4 (gates), M5, trace-vocab v2 |
| F3 | Code sandboxes 执行沙箱 | isolated run-as-backend for generated code — the `sandboxed-execution` capability made concrete | M6 (tools), M3 (least privilege) |
| F4 | Structured outputs 结构输出 | schema-valid JSON/regex/CFG-constrained generation; contracts between steps stop being prose | M3 (verifiable closure), M4 |
| F5 | Eval & red-team runners 评测/红队 | declarative prompt/agent tests with CI gates; attack-surface probing before deployment | M4 (verification), M8 |
| F6 | Gateways & local inference 网关/本地推理 | one API surface over 100+ providers with cost tracking; free local/remote-GPU serving (cost gate M3/M7) | M7 (cost), model-choice |
| F7 | Guardrails 护栏 | programmable dialog/tool-call rails: topical, safety, jailbreak rails as pre-gates | M3, M6.11 |

## 3. Verified inventory · 核验清单（as of 2026-11-03）

License/activity from GitHub API metadata; purpose from the project's own README.

| Tool | Family | License (verified) | Activity (`pushed_at`) | Integration note · 整合要点 | Not for · 不为 |
|---|---|---|---|---|---|
| **Mem0** (mem0ai/mem0) | F1 | Apache-2.0 | active 2026 | drop-in memory layer; April-2026 algorithm: single-pass ADD-only extraction, entity linking, multi-signal retrieval, temporal ranking; paper arXiv:2504.19413 | the headline LoCoMo 92.5 / LongMemEval 94.4 scores are **platform (managed) numbers** — README states proprietary optimizations are not in the OSS SDK; treat as directional |
| **Graphiti** (getzep/graphiti) | F1 | Apache-2.0 | 2026-11-01 · 32,455 stars | temporal context graphs: facts carry validity windows, **every derived fact traces back to episodes (raw source data)** — structurally the same discipline as our M5 provenance rule; hybrid retrieval (semantic+BM25+graph) | it is a framework, not a service — Zep/Konig is the governed enterprise layer (README); paper "Zep: A Temporal Knowledge Graph Architecture" (arXiv) — id not re-verified here, *unverified* |
| **Langfuse** (langfuse/langfuse) | F2 | MIT (core; `ee/` folders excluded) | active 2026 | self-hostable LLM trace/eval platform; OTel-based ingestion is the interop door — same standard our `traces.jsonl` vocabulary could emit toward | traces are exposure, not audit — pairing with M4 gates stays ours (M6.11) |
| **OpenTelemetry GenAI semantic conventions** (open-telemetry/semantic-conventions-genai) | F2 | Apache-2.0 (OTel) | active 2026 | the **vendor-neutral contract**: spans/metrics/events for GenAI clients *and MCP*; YAML model + Weaver + Python compliance matrix — the right anchor to standardize harness telemetry without lock-in | conventions ≠ collection — needs a backend (Langfuse/Phoenix/etc.) |
| **E2B** (e2b-dev/E2B) | F3 | Apache-2.0 | 2026-11-02 · 14,676 stars | open-source SDK, cloud sandbox compute ("secure environment…for enterprise-grade agents", self-described) | **the isolation guarantee is a backend claim** (M6.11): OSS SDK does not prove the cloud boundary; hosted compute is metered → cost cap before unattended runs |
| **Instructor** (567-labs/instructor) | F4 | MIT | active 2026 | Pydantic-validated extraction with auto-retry/streaming across providers incl. `ollama/*` local; ~3M monthly downloads, 10k+ stars (README claims, directional) | schema-first extraction only — the README itself routes agent-runtime needs to PydanticAI |
| **Outlines** (dottxt-ai/outlines) | F4 | Apache-2.0 | 2026-09-21 · 15,999 stars | constrained generation to JSON schema/regex/CFG — guarantees structural validity *by construction*, the strongest F4 semantics (complements Instructor's retry-based validation) | company also sells enterprise libraries (README "license our enterprise-grade libraries") — OSS/core boundary to check before deep adoption; slower cadence since Sep |
| **promptfoo** (promptfoo/promptfoo) | F5 | MIT | 2026-11-03 · 26,758 stars | declarative prompt/agent/RAG tests + red-team scans, CLI + CI/CD — the closest existing instrument to our `gate` command; README: "Used by OpenAI and Anthropic" (self-claimed) | eval green ≠ capability proof — our paired-trial discipline (A-bare vs B-harness) stays the standard of evidence |
| **LiteLLM** (BerriAI/litellm) | F6 | **NOASSERTION per GitHub API** — verify terms before adoption | 2026-11-03 · 62,573 stars | AI gateway: 100+ providers behind OpenAI-format API, cost tracking, guardrails, load balancing — natural fit for the cost-sensitive default (open/free local, paid API only at quality-critical steps) | license flag above is a real intake-gate failure until resolved; proxy becomes a new trusted surface (key custody) |
| **vLLM** (vllm-project/vllm) | F6 | Apache-2.0 | 2026-11-03 · 96,165 stars | high-throughput local/remote-GPU serving engine — the F6 answer for "self-hosted model" in the M3/M7 cost gate | needs GPU or remote-GPU platform; not a harness component per se — a backend |
| **NeMo Guardrails** (NVIDIA-NeMo/Guardrails) | F7 | **NOASSERTION per GitHub API** — verify terms | 2026-11-03 · 7,418 stars | programmable rails (dialog, topic, safety, jailbreak) as pre-gates in front of the model/tool surface | same license caveat as LiteLLM;rails are advisory, not a sandbox |
| **Microsoft GraphRAG** (microsoft/graphrag) | F1/F-检索 | — | **maintenance mode** (README warning 2026-11-03: "largely in maintenance mode, won't be accepting new PRs") | methodology value stands: community-summarized graph retrieval for narrative private data; paper arXiv:2404.16130; indexing is LLM-expensive (README's own warning) | **do not adopt as a new dependency** — registered with `defunct-track` marker per P35 precedent; Graphiti (F1) is the active temporal-graph alternative |

Not yet primary-verified this round (leads only, queued for the standing scan): DeepEval, Ragas, PydanticAI, BAML, XGrammar, Modal, Daytona, Arize Phoenix, LangSmith. They enter the loop as `ai-tool-stack` discovery candidates rather than being half-cited here (M0.4).

## 4. Metabolism findings · 代谢发现（本轮的三个"事实翻转"）

1. **GraphRAG → maintenance mode.** The flagship structured-retrieval project self-declares it will not take new features (CVE/dep fixes only). Pattern stays valuable; dependency status flips. Registered as a tracked-with-caveat source, not a tool to adopt.
2. **Mem0 benchmark numbers are platform numbers.** The OSS repo's own README scopes LoCoMo/LongMemEval scores to the managed platform with proprietary optimizations. Citing them for the OSS SDK would be a category error — recorded as directional.
3. **Two popular gateways/rails carry `NOASSERTION` licenses** (LiteLLM, NeMo Guardrails — GitHub API, 2026-11-03). The intake gate (§ tool-router 5) fails until the terms are read; both are still *worth tracking* for their feed, hence `license-check` tags rather than exclusion.

## 5. The sustainable mechanism · 可持续机制

Wiring (all pre-existing engine, zero new surface — M0.4):

```
watchlist.json  +topic "ai-tool-stack" (queries+keywords)   → collect.discover (LLM discovery, every refresh)
sources.json    +13 tool entities with releases.atom feeds  → feed provider (deterministic pull, every refresh)
intel → probe-domains → trace-audit → evolve               → uncovered-topic / stale-source audits → add_source proposals (human-gated, M0.8)
→ cycle-audit → scoreboard → self-model                    → topic coverage re-measured each full-update
```

Each `harness full-update` therefore **auto-scans the tool ecosystem** against the `ai-tool-stack` queries, scores findings through the same relevance pipeline, and turns registry gaps into human-gated proposals; this document + `tool-router.md` §4 family #2 are the curated snapshot between runs. The guard (`tests/test_docs_integrity.py::P68ToolEcosystemTest`) pins topic↔carrier wiring so a later edit cannot silently unplug it — the exact failure P59 found.

Follow-ups recorded to roadmap (`tasks/PLAN.md` P68.R*):
- **P68.R1** — verify DeepEval / Ragas / PydanticAI / BAML / Modal / Daytona / Phoenix / LangSmith against primary sources; intake per §3 format.
- **P68.R2** — resolve LiteLLM & NeMo Guardrails license terms (intake gate box).
- **P68.R3** — pilot one F4 (structured-output) and one F2 (OTel-genai export) integration in a derived harness, judged by a paired trial (A-bare vs B-with-tool), registered via `battery.json` `trial_projects` metabolism (P67 machinery).

## 6. Sources · 来源（all accessed 2026-11-03）

- https://api.github.com/repos/{getzep/graphiti, dottxt-ai/outlines, e2b-dev/E2B, promptfoo/promptfoo, BerriAI/litellm, vllm-project/vllm, NVIDIA-NeMo/Guardrails} — license SPDX, `pushed_at`, stars (machine metadata)
- https://github.com/mem0ai/mem0 (README: Apache-2.0, April-2026 algorithm, benchmark scope note, arXiv:2504.19413 citation block)
- https://github.com/getzep/graphiti (README: temporal context graphs, episodes-as-provenance, Zep/Konig split)
- https://github.com/langfuse/langfuse (README: MIT-except-ee, self-host, ClickHouse; joined ClickHouse Jan 2026 per README notice)
- https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/README.md (scope: GenAI+MCP conventions)
- https://raw.githubusercontent.com/microsoft/graphrag/main/README.md (maintenance-mode warning; arXiv:2404.16130 link)
- https://github.com/567-labs/instructor (README: MIT, provider list, PydanticAI routing note)
- https://github.com/promptfoo/promptfoo (API description: testing + red teaming, CI integration)

## 中文 · 本节备忘

- 本表不是"工具推荐"，是**工厂的进料单**：每行都过了一手源核验（许可、活跃度、自述能力），未核验者只留线索不入表。
- 三条代谢事实（GraphRAG 维护模式、Mem0 榜单属托管平台、NOASSERTION 许可）与正面发现同等重要——它们防止未来的 agent 把过期事实当弹药。
- 机制零新代码：新主题进 watchlist 即被既有 discover 循环扫描；feed 进 sources 即被既有 refresh 拉取；缺口由既有 evolve 提案、self-model 度量。这就是"每次自动运行"的落点。
- 采用任何一件工具前，仍回 `tool-router.md` §5 质量门打勾；配对试验（A-裸模型 vs B-加工具）是唯一合格证据形式，试验必须经 `battery.json` 的 `trial_projects` 登记（P67 代谢机件）。
