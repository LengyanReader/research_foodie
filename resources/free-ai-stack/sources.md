# Sources & Verification Ledger · 来源与核验账本
> Every claim in this catalog resolves to a source with an access date.
> 本目录中的每条主张都对应一个带访问日期的来源。
**Updated:** 2026-11-08 · **Access date:** 2026-11-08 (unless noted)

---

## 中文速览
这份账本记录本轮实际抓取的页面与 GitHub API 元数据。**✅ = 抓取成功并用于正文；🟡 = 抓取成功但有未核验部分；⚪ = 仅登记、未核验；404 = 页面不存在。** 免费层数字均为 **2026-11-08** 快照；不要把它当长期事实。

---

## Official provider pages · 官方页面
| Claim supported | Source | URL | Status |
|---|---|---|---|
| Gemini free tier, model availability, data use | Google AI Studio — Gemini Developer API pricing | https://ai.google.dev/gemini-api/docs/pricing | ✅ fetched |
| Groq free-plan RPM/RPD/TPM/TPD | Groq Docs — Rate Limits | https://console.groq.com/docs/rate-limits | ✅ fetched |
| Groq pricing page (not used) | Groq console pricing | https://console.groq.com/docs/pricing | 404 |
| OpenRouter free models, 50/1,000 requests/day, privacy tiers | OpenRouter — FAQ | https://openrouter.ai/docs/faq | ✅ fetched |
| Cohere trial key, 1,000 calls/month, per-endpoint limits | Cohere — API keys and rate limits | https://docs.cohere.com/docs/rate-limits | ✅ fetched |
| Cloudflare Workers AI 10,000 Neurons/day | Cloudflare — Workers AI pricing | https://developers.cloudflare.com/workers-ai/platform/pricing/ | ✅ fetched (page last updated 2026-10-20) |
| Hugging Face free users get no inference credits; PRO $2/month | Hugging Face — Inference Providers pricing | https://huggingface.co/docs/inference-providers/pricing | ✅ fetched |
| GitHub Models retired 2026-07-30 | GitHub Docs — GitHub Models | https://docs.github.com/en/github-models | ✅ fetched |
| Mistral Vibe Free plan; API free tier not verified | Mistral — Pricing | https://mistral.ai/pricing | 🟡 fetched (Vibe plan verified; API free tier not) |
| GitHub Copilot Free: 2,000 completions/month, AI credits, auto model | GitHub Docs — Plans for GitHub Copilot | https://docs.github.com/en/copilot/about-github-copilot/plans-for-github-copilot | ✅ fetched |
| Gemini Code Assist quotas | Google — Gemini Code Assist quotas | https://developers.google.com/gemini-code-assist/resources/quotas | ✅ fetched |
| Amazon Q Developer Free: 50 agentic requests/month | AWS — Amazon Q Developer pricing | https://aws.amazon.com/q/developer/pricing/ | ✅ fetched |
| Vercel Hobby free limits | Vercel — Pricing | https://vercel.com/pricing | ✅ fetched |
| Supabase Free limits | Supabase — Pricing | https://supabase.com/pricing | ✅ fetched |
| Tavily 1,000 free credits/month | Tavily — Credits & Pricing | https://docs.tavily.com/documentation/api-credits | ✅ fetched |
| Langfuse Hobby limits | Langfuse — Pricing | https://langfuse.com/pricing | ✅ fetched |
| Qdrant Cloud Free limits | Qdrant — Pricing | https://qdrant.tech/pricing/ | ✅ fetched |
| Cloudflare Pages Free limits | Cloudflare — Pages limits | https://developers.cloudflare.com/pages/platform/limits/ | ✅ fetched |

---

## GitHub API metadata · GitHub API 元数据
| Repo | License | Stars | Last push | Status | Used in |
|---|---|---:|---|---|---|
| `ollama/ollama` | MIT | 186,320 | 2026-11-08 | ✅ | `vibe-coding.md`, `llm-apis.md` |
| `cline/cline` | Apache-2.0 | 71,455 | 2026-11-07 | ✅ | `vibe-coding.md` |
| `google-gemini/gemini-cli` | Apache-2.0 | 108,774 | 2026-11-08 | ✅ | `vibe-coding.md` |
| `mnfst/awesome-free-llm-apis` | CC0-1.0 | 12,593 | 2026-11-07 | ✅ | `github-lists.md` |
| `open-free-llm-api/awesome-freellm-apis` | MIT | 5,371 | 2026-11-07 | ✅ | `github-lists.md` |
| `zebbern/no-cost-ai` | MIT | 2,403 | 2026-09-21 | ✅ | `github-lists.md` |
| `Ebony-Vinyl/dsh-our-free-model` | MIT | 65,834 | 2026-11-08 | ✅ metadata; ⛔ safety verdict | `github-lists.md` |
| `jwadow/kiro-gateway` | — | — | — | ✅ description; ⛔ safety verdict | `github-lists.md` |
| `cheahjs/free-llm-api-resources` | — | — | — | **404** | `github-lists.md` |

**API endpoints:** `https://api.github.com/repos/<owner>/<repo>` (metadata) · `https://api.github.com/search/repositories?q=free+llm+api&sort=stars&order=desc&per_page=10` (search, 2,409 results).

---

## Factory sources · 本仓库方法来源
| Use | File | Why it matters |
|---|---|---|
| Deep-research L0–L9 + quality bar | `harness_factory/domains/deep-research/README.md` | Scope → plan → parallel search → screen → extract → synthesize → verify → iterate |
| Tool discovery loop + aggregator rule | `harness_factory/reference/tool-router.md` §1 | Discover → evaluate → register → metabolize; aggregator ≠ citation |
| Discovery portals / outlets | `harness_factory/reference/outlet-map.md` | Where to look, not what to claim |
| Verified AI tool licenses | `harness_factory/review/ai-tool-stack-scan-2026-11.md` | vLLM Apache-2.0; LiteLLM NOASSERTION |
| Capability routing | `harness_factory/reference/capability-router.md` | `traceable-sources`, `untrusted-content-discipline`, `tool-use` |

---

## Unverified leads · 未核验线索
Marked `⚪` in the catalog; do not quote numbers until fetched:
- **LLM APIs:** NVIDIA NIM, Together AI, Fireworks AI, Cerebras, SambaNova, Mistral API, Azure AI Foundry, AWS Bedrock, Google Vertex AI, AI21, Aleph Alpha.
- **China/Asia providers:** DeepSeek, Alibaba Cloud Model Studio (Qwen), Zhipu (GLM), Moonshot (Kimi), Baidu Qianfan, Tencent Hunyuan, iFlytek Spark, MiniMax, SiliconFlow, ModelScope. All `⚪`; free quotas/real-name/data-residency not verified.
- **Free app infra:** Netlify, Render, Railway, Fly.io, GitHub Pages, Firebase, Neon, Turso, Upstash, Pinecone, Chroma, Milvus, Weaviate, Brave Search API, Exa, Jina, SerpAPI, Helicone, Arize Phoenix, promptfoo.
- **Coding tools:** Aider, OpenHands, Goose, Roo Code, OpenCode, Codex CLI, Qwen Code (tool existence is in the factory catalog; licenses not re-verified this round).
- **Vibe-coding builders:** Lovable, Bolt.new, v0, Replit, Firebase Studio, Google AI Studio Build.
- **Model/weights licenses:** every open-weight model (Llama, Qwen, DeepSeek, Mistral, Gemma, etc.) — check the model card separately from the runtime license.

---

## Re-verification schedule · 复验计划
| Date | Action |
|---|---|
| 2026-11-08 | v1 snapshot (this file) |
| 2027-02-08 | Re-fetch provider pages; update limits; re-check GitHub lists/red flags |
| Before any production use | Re-fetch the specific provider's pricing + terms + data policy; run a paired trial |

**Honesty rule:** if a page cannot be fetched, mark it `⚪`/`404`; do not reconstruct the number from memory or a secondary list.