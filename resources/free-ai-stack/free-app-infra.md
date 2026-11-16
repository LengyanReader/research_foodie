# Free App Infrastructure · 免费应用基础设施
> Free hosting, database/auth, search, vector DB, and observability for a vibe-coded app.
> 用于 vibe coding 应用的免费托管、数据库/鉴权、搜索、向量库与可观测性。
**Updated:** 2026-11-08 · All numbers are **as of 2026-11-08**.

---

## 中文速览
“免费 vibe coding”不只需要模型，还需要**能部署、能存数据、能搜索、能观测**。本页只列**官方免费层**：**Vercel Hobby**（静态/全栈托管，非商用）、**Cloudflare Pages**（静态站点，500 次构建/月）、**Supabase Free**（Postgres + Auth + Storage，500 MB 库，闲置一周暂停）、**Tavily**（搜索 API，1,000 credits/月，免卡）、**Qdrant Cloud Free**（向量库，1 GB RAM/4 GB 磁盘）、**Langfuse Hobby**（LLM 可观测，50k units/月）。这些免费层都适合**原型**，不适合生产 SLA。`⚪` 是未核验线索，不要引用数字。

---

## Verified free infrastructure · 已核验免费基础设施
| Category | Service | Free tier | Key limits (2026-11-08) | Caveat |
|---|---|---|---|---|
| **Hosting (full-stack)** | **Vercel Hobby** ✅ | $0/mo | 1M CDN requests/mo; 100 GB fast data transfer; 1M function invocations; 4 active CPU hours; 360 GB-hrs memory; 200 CI CPU minutes; 10 GB deployment storage | **Personal, non-commercial use**; usage caps, no overage purchase |
| **Hosting (static)** | **Cloudflare Pages Free** ✅ | $0 | **500 builds/month**; 1 concurrent build; 20,000 files; 25 MiB/file; 100 custom domains/project; 100 projects/account; unlimited preview deployments | Static/Pages Functions; Workers quotas apply to Functions |
| **DB + Auth + Storage** | **Supabase Free** ✅ | $0 | **500 MB database**; 5 GB egress; 1 GB file storage; 50,000 MAU; 500,000 Edge Function invocations; 2 active projects | **Paused after 1 week of inactivity**; community support |
| **Search API (RAG)** | **Tavily** ✅ | **1,000 credits/month**, no card | Basic search 1 credit; advanced 2 credits; extract 5 URLs/credit (basic); research 4–250 credits | Credits reset monthly; not a web-scale crawler |
| **Vector DB** | **Qdrant Cloud Free** ✅ | Free forever | **0.5 vCPU / 1 GB RAM / 4 GB disk**; single node; free inference with selected models | No high availability; upgrade for production |
| **LLM observability** | **Langfuse Hobby** ✅ | Free, no card | **50k units/month**; 30 days data access; 2 users; all platform features with limits | Community support; longer retention is paid |

---

## How these fit together · 组合方式
A minimal free vibe-coded stack:
1. **Frontend:** Vercel Hobby (Next.js) or Cloudflare Pages (static).
2. **Database/Auth/Storage:** Supabase Free.
3. **Search/RAG:** Tavily free credits + Supabase pgvector or Qdrant Cloud Free.
4. **LLM:** Gemini / Groq / OpenRouter free tier for prototypes; Ollama locally for sensitive data.
5. **Observability:** Langfuse Hobby (traces, prompts, evals).
6. **Safety:** never put production secrets in a free-tier prototype; set spend caps; expect inactivity pauses.

**This stack is for prototypes.** Free tiers have no SLA, can pause, and may train on data. Move to paid tiers (or self-host) before production.

---

## Unverified leads · 未核验线索
These are well-known options, but their current free-tier limits were **not** fetched this round. Treat as `⚪`; verify at the official page before quoting numbers.

| Category | Leads | Official starting point |
|---|---|---|
| Hosting | Netlify Free, Render Free, Railway trial, Fly.io, GitHub Pages, Firebase Hosting | `netlify.com/pricing`, `render.com/pricing`, `railway.com/pricing`, `fly.io/pricing`, `pages.github.com`, `firebase.google.com/pricing` |
| DB/Auth/Storage | Neon Free, Turso Free, Upstash Redis Free, Firebase Spark, Cloudflare R2 free tier | `neon.com/pricing`, `turso.tech/pricing`, `upstash.com/pricing`, `firebase.google.com/pricing`, `developers.cloudflare.com/r2/pricing/` |
| Search | Brave Search API, Exa, Jina Reader, SerpAPI | `brave.com/search/api/`, `exa.ai/pricing`, `jina.ai/reader/`, `serpapi.com/pricing` |
| Vector DB | Pinecone Free, Chroma (local/open source), Milvus Lite, Weaviate Cloud | `pinecone.io/pricing`, `trychroma.com`, `milvus.io`, `weaviate.io/pricing` |
| Observability/Eval | Helicone, Arize Phoenix, promptfoo, OpenTelemetry | `helicone.ai/pricing`, `phoenix.arize.com`, `promptfoo.dev`, `opentelemetry.io` |
| CI/CD | GitHub Actions free minutes, GitLab Free, Vercel CI | `docs.github.com/billing`, `about.gitlab.com/pricing`, `vercel.com/pricing` |

---

## Safety notes for free infrastructure · 免费基础设施安全
- **Non-commercial clauses:** Vercel Hobby is personal/non-commercial; check the terms before using it for a client.
- **Inactivity pauses:** Supabase Free pauses after 1 week; do not use it for a cron-only app without a keep-alive.
- **Data retention:** Langfuse Hobby keeps 30 days; do not rely on it for audit logs.
- **No SLA:** free tiers are not production. Keep backups and a paid fallback.
- **Secrets:** use environment variables; never commit `.env`; rotate keys after a prototype.
- **Egress:** free egress is finite (Supabase 5 GB, Vercel 100 GB). Watch it.
- **Region:** free tiers may pin a region; check data residency before storing PII.