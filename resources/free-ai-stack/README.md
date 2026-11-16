# Free AI Stack · 免费 AI 栈
> A curated, safety-first snapshot of free LLM APIs, free coding tools, and open-source resources.
> 免费大模型 API、免费编码工具与开源资源的安全优先快照。
**Updated:** 2026-11-08 · **Scope:** global, official sources only · **Status:** v1.1 snapshot

---

## 中文速览
这份目录回答三个问题：**哪些免费 LLM API 真的可用？哪些 vibe coding 工具可以零成本起步？哪些“免费”资源其实是代理/共享密钥的坑？** 结论：**官方免费层确实存在**（Gemini、Groq、OpenRouter、Cohere、Cloudflare、Tavily、Supabase、Vercel、Qdrant、Langfuse），但**都有配额、数据使用或模型限制**；**GitHub 上的“无限免费前沿模型、无需 API Key”几乎都不是官方免费层**，而是代理/共享凭证，存在 ToS、封号、密钥泄露与恶意脚本风险。**本地开源栈（Ollama / vLLM）是隐私与长期成本最稳的路线**，代价是硬件与运维。所有数字均为 **as of 2026-11-08**，免费层随时会变。

> **Verification legend · 核验图例**
> - ✅ **Verified** — provider's own page or GitHub API fetched on 2026-11-08.
> - 🟡 **Free with caveat** — official free tier, but training/limits/region/model restrictions apply.
> - ⚪ **Listed / unverified** — a lead; do not treat as current fact.
> - ⛔ **Avoid** — proxy, credential-sharing, or ToS-violating pattern.

---

## Quick picks · 快速选择
| Need · 需求 | Start with · 先用 | Why · 理由 | Caveat · 注意 |
|---|---|---|---|
| Fast free API for open models | **Groq** ✅ | OpenAI-compatible; free plan includes gpt-oss-120b/20b and qwen3.8-27b | 30 RPM, 1K RPD, 8K TPM, 200K TPD; model subset |
| One key, many models | **OpenRouter `:free`** ✅ | 50 free requests/day; 1,000/day after ≥10 credits | low limits; not for production |
| Multimodal / Gemini experiments | **Google AI Studio** ✅ | free tokens on selected models; Gemini 3.8 Flash free | free tier trains on content; Gemini 4 Argon not free |
| RAG / embeddings / rerank | **Cohere trial** ✅ | 1,000 API calls/month; strong embed/rerank | trial key only; 20 req/min chat |
| Edge / serverless inference | **Cloudflare Workers AI** ✅ | 10,000 Neurons/day free | some frontier models require paid |
| Free IDE coding | **GitHub Copilot Free** ✅ | 2,000 completions/month; limited AI credits | auto model selection only; limited agents |
| Free CLI + 1,500 req/day | **Gemini CLI / Gemini Code Assist** ✅ | open-source CLI + free quota | quota shared with Code Assist agent mode |
| Free AWS coding agent | **Amazon Q Developer Free** ✅ | 50 agentic requests/month; IDE/CLI | limited; 1,000 lines Java upgrade/month |
| Private / local | **Ollama + open-weight model** ✅ | no cloud, no key, MIT | hardware and electricity |
| Open-source IDE agent | **Cline** ✅ | Apache-2.0; BYOK; human-in-the-loop | you pay the model provider |
| Open-source CLI agents | **Gemini CLI, Aider, OpenHands, Goose** ✅/⚪ | open source; provider-agnostic | verify license and model cost |
| Deploy a prototype | **Vercel Hobby / Cloudflare Pages** ✅ | free hosting | Vercel Hobby is non-commercial; Pages is static-first |
| DB / auth / storage | **Supabase Free** ✅ | Postgres + Auth + Storage | 500 MB DB; paused after 1 week inactivity |
| Search for RAG | **Tavily** ✅ | 1,000 credits/month, no card | credits reset monthly |
| Vector DB | **Qdrant Cloud Free** ✅ | 1 GB RAM / 4 GB disk | single node; no HA |
| LLM observability | **Langfuse Hobby** ✅ | 50k units/month | 30 days data access |

---

## Coverage map · 覆盖地图
| Area | Covered | Document |
|---|---|---|
| Free LLM APIs | Verified major providers, multimodal free tiers, corrections | [`llm-apis.md`](llm-apis.md) |
| Vibe coding | Free plans, open-source agents, builders to verify | [`vibe-coding.md`](vibe-coding.md) |
| Free app infrastructure | Hosting, DB/auth, search, vector DB, observability | [`free-app-infra.md`](free-app-infra.md) |
| Regional / global | China/Asia, EU, global leads | [`regional.md`](regional.md) |
| GitHub lists | Meta-lists, red flags, evaluation checklist | [`github-lists.md`](github-lists.md) |
| Safety | Threat model, key hygiene, data/licensing | [`safety.md`](safety.md) |
| Maintenance | Cadence, procedure, status board | [`MAINTENANCE.md`](MAINTENANCE.md) |
| Sources | Every URL + access date + status | [`sources.md`](sources.md) |

**Intentional exclusions · 有意排除:** paid-only tiers, cracked/shared keys, reverse-engineered proxies, “no-key unlimited” services, dead services (kept only as red-flag examples), and non-AI freebies.

**Audit verdict (2026-11-08) · 覆盖审计结论:** v1 covered free LLM APIs, coding tools, GitHub lists, and safety. v1.1 closes the three gaps found: **free app infrastructure**, **regional/global coverage**, and a **maintenance process**. Remaining gaps are explicit: China free quotas, vibe-builder pricing, open-source agent licenses, and paid-tier SLAs. See [`MAINTENANCE.md`](MAINTENANCE.md).

## What changed · 事实翻转（important)
- **GitHub Models is retired.** As of **2026-07-30**, the playground, model catalog, inference API, and BYOK are gone. Any list that still recommends GitHub Models as a free LLM API is stale. ✅
- **Hugging Face is not a free inference API for free users.** Free users receive **no** monthly Inference Providers credits; PRO gets **$2/month**. ✅
- **The widely cited `cheahjs/free-llm-api-resources` repository returned 404 on 2026-11-08.** Do not cite it as current. ✅
- **"No API key, unlimited frontier models" is not a free tier.** It is a proxy/credential-sharing pattern. Two high-star examples found in GitHub search are flagged in [`github-lists.md`](github-lists.md). ⛔
- **Mistral's free plan is a product plan (Vibe), not a verified free API tier.** The API free tier was not verified this round. 🟡
- **v1.1 audit added the missing layers:** free app infrastructure (hosting/DB/auth/search/vector/observability), regional/China leads, and a maintenance cadence. See [`CHANGELOG.md`](CHANGELOG.md) and [`MAINTENANCE.md`](MAINTENANCE.md).

---

## How this snapshot was built · 方法
Followed the factory's own `deep-research` L0–L9 loop and `tool-router` four-step loop:
1. **Discover** — GitHub API search, official provider pricing/rate-limit pages, the factory's `review/ai-tool-stack-scan-2026-11.md`.
2. **Evaluate** — license, activity, free-tier limits, data policy, ToS, security posture (`untrusted-content-discipline`).
3. **Verify** — every number resolved to the provider's own page; GitHub metadata from the API; access date recorded in [`sources.md`](sources.md).
4. **Register** — this snapshot is the registry; production adoption still requires a paired trial (A-bare vs B-with-resource) before promotion.

**Rule:** an aggregator is a **discovery door**, not a citation (`reference/tool-router.md` §1). A GitHub list can point you at a provider; only the provider's page can establish the free tier.

---

## Safety first · 先读安全
Read [`safety.md`](safety.md) before using any key. The short version:
- Never paste API keys into a repo, a browser extension, or a "free unlimited" proxy.
- Use environment variables; scope and rotate keys; monitor spend.
- Free tiers often train on your data. Do not send secrets, PII, or proprietary code.
- Prefer official installers and pinned versions; never `curl | bash` an unknown script.
- Stars are not safety. A 65k-star repo can still be a credential trap.

---

## Maintenance · 维护
This is a snapshot, not a monitored service. See [`MAINTENANCE.md`](MAINTENANCE.md) for the cadence, procedure, and status board; every change goes into [`CHANGELOG.md`](CHANGELOG.md). To refresh it:
1. Re-run the official pages in [`sources.md`](sources.md) and update the numbers/access dates.
2. Re-check GitHub lists for last push, license, and red-flag patterns.
3. Propose a `free-ai-stack` watchlist topic for the factory's `refresh`/`intel` loop (not yet registered).
4. Before adopting a tool in an emitted harness, run a paired trial and register the receipt (factory rule).