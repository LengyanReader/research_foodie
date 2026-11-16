# Free LLM APIs · 免费大模型 API
> Official free tiers, verified limits, and corrections to stale GitHub lists.
> 官方免费层、已核验限额，以及对过期 GitHub 清单的纠错。
**Updated:** 2026-11-08 · All numbers are **as of 2026-11-08** and may change without notice.

---

## 中文速览
真正可用的官方免费层集中在少数几家：**Google Gemini（免费层会用你的内容改进产品）**、**Groq（快速开源模型，额度小）**、**OpenRouter（免费模型 50 次/天，买 10 美元额度后 1,000 次/天）**、**Cohere（试用 key，1,000 次/月）**、**Cloudflare Workers AI（每天 10,000 Neurons）**。**Hugging Face 免费用户没有推理额度**；**GitHub Models 已于 2026-07-30 退役**；**Mistral 的免费计划是 Vibe 产品，不是已核验的 API 免费层**。**不要使用“无需 API Key、无限免费前沿模型”的代理**。

---

## Verified free tiers · 已核验免费层
| Provider | Free offering | Limits (as of 2026-11-08) | API compatibility | Data use | Best for | Caveat |
|---|---|---|---|---|---|---|
| **Google Gemini API** (AI Studio) ✅ | Free tier: selected models, free input & output tokens | Free-tier limits vary by model; **Gemini 3.8 Flash: free**; **Gemini 4 Argon: not available** | Gemini API (not OpenAI-compatible by default) | Free tier: **content used to improve Google products**; paid tier: not used | Multimodal and long-context prototyping | Do **not** send confidential data on the free tier |
| **Groq** ✅ | Free plan: gpt-oss-120b/20b, qwen3.8-27b, prompt guard, whisper | Chat models: **30 RPM · 1K RPD · 8K TPM · 200K TPD**; prompt guard: 30 RPM/1.4K RPD/15K TPM/500K TPD; whisper: 20 RPM/2K RPD | OpenAI-compatible | Data policy not verified this round | Fast inference for open models | Model subset; limits are per organization |
| **OpenRouter** ✅ | `:free` model variants and `openrouter/free` router | **50 free requests/day total**; **1,000/day if ≥10 credits purchased** | OpenAI-compatible | Prompts/completions **not logged by default**; ZDR / Safety Retention / Retention & Training tiers; logging/training providers are not routed unless enabled | One key, many models; fallback | Low limits; not suitable for production |
| **Cohere** ✅ | Trial key (free) | **1,000 API calls/month**; chat **20 req/min**; embed 2,000 inputs/min; rerank 10 req/min | Cohere API | Data policy not verified this round | RAG, embeddings, rerank | Trial only; production needs a paid key |
| **Cloudflare Workers AI** ✅ | **10,000 Neurons/day** on Workers Free | $0.011 per 1K Neurons beyond; some models require paid | REST + Workers binding | Data policy not verified this round | Edge/serverless inference | Frontier models may need Workers Paid |

### Notes that matter · 关键说明
- **Google free tier is not private.** The pricing page explicitly lists "Content used to improve our products" for the Free tier; the Paid tier lists "Content not used to improve our products." Treat free Gemini as **public-data only**.
- **Groq's free plan is a model subset, not the whole catalog.** The rate-limit table lists the free-plan models; exact limits can change per organization.
- **OpenRouter's free models are rate-limited by credits.** If you have purchased at least 10 credits, the free-model limit becomes 1,000/day; otherwise 50/day.
- **Cohere's trial key is for evaluation.** 1,000 calls/month and 20 req/min chat is enough to test, not to serve users.
- **Cloudflare's free allocation is daily and shared.** All limits reset at 00:00 UTC.

---

## Multimodal free tiers · 多模态免费层
| Provider | Free modality | Limits (as of 2026-11-08) | Data use | Caveat |
|---|---|---|---|---|
| **Google Gemini** ✅ | Gemini 3.5 Transcribe / Live: **free of charge** on free tier | Free-tier model limits vary; content used to improve products | Free tier: trains on content | Real-time audio/transcription; not for confidential audio |
| **Groq** ✅ | Whisper large-v3 / turbo | Free plan: **20 RPM · 2K RPD** | Data policy not verified this round | Audio transcription only |
| **Cloudflare Workers AI** ✅ | Whisper, Flux image models | Within **10,000 Neurons/day** | Data policy not verified this round | Some models require paid |
| **Cohere** ✅ | Embed / Rerank | Trial: **2,000 inputs/min** embed; **10 req/min** rerank; 1,000 calls/month | Data policy not verified this round | Trial only |

### Embeddings · 嵌入
- **Cohere trial** is the clearest verified free embedding path (2,000 inputs/min; 1,000 calls/month).
- **Cloudflare Workers AI** includes BGE embeddings inside the 10k Neurons/day budget.
- **Gemini embeddings:** verify current free-tier eligibility on the pricing page before quoting.
- **Hugging Face:** free users get **no** Inference Providers credits; self-host embeddings for zero marginal cost.

## Corrections to common lists · 对常见清单的纠错
| Claim you will see | Reality (verified 2026-11-08) | Implication |
|---|---|---|
| "GitHub Models gives free GPT/Claude/Gemini API access" | **Retired 2026-07-30**; playground, catalog, inference API, BYOK unavailable | Remove it from any current list |
| "Hugging Face Inference API is free" | Free users get **no** monthly credits; PRO gets **$2/month**; pay-as-you-go requires credits | Not a free API for free users |
| "Mistral has a free API tier" | The **Vibe Free** product plan is verified; the API free tier was **not** verified this round | Treat as `⚪`, not a fact |
| "GitHub Models replacement is free" | GitHub points to **Azure AI Foundry**; its free/credit terms were not verified this round | Verify before citing |
| "No API key, unlimited frontier models" | Not a provider free tier; likely proxy/credential-sharing | ⛔ Avoid; see [`github-lists.md`](github-lists.md) |

---

## Open-weight self-hosting · 开源自托管
Self-hosting is the safest route for sensitive data; the "free" is software freedom, not compute.

| Tool | License | Activity (GitHub, 2026-11-08) | Use | Note |
|---|---|---|---|---|
| **Ollama** | **MIT** ✅ | 186,320 stars; pushed 2026-11-08 | Local model runner; OpenAI-compatible server | Easiest local start; needs RAM/GPU |
| **vLLM** | **Apache-2.0** ✅ | Factory scan 2026-11-03 (96,165 stars then) | High-throughput serving | Needs GPU; production-grade |
| **llama.cpp** | ⚪ verify at repo | Listed in the factory catalog | CPU/GPU inference; GGUF | Lightweight; check license/version |

**Official pages:** [ollama/ollama](https://github.com/ollama/ollama) · [vllm-project/vllm](https://github.com/vllm-project/vllm) · [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

## Open-weight models & datasets · 开源权重与数据集
| Source | What is free | What is not | Caveat |
|---|---|---|---|
| **Hugging Face Hub** | Model/dataset downloads; community Spaces | Inference Providers credits for free users | Check the **model card license**; runtime license ≠ model license |
| **ModelScope** (China) | Model/dataset downloads; hosted inference | Free inference quota not verified | Region/real-name/data-residency rules |
| **Ollama library** | Model downloads via `ollama pull` | Compute/electricity | Curated models; verify the upstream license |
| **Kaggle** | Datasets, notebooks, community | GPU/TPU quota not verified | Competition rules may restrict use |

**Model-license warning:** open weights are not universally “free for any use”. Licenses vary (Apache-2.0, MIT, Llama community license, custom terms). Always open the model card and read the license before commercial use. The runtime (Ollama/vLLM/llama.cpp) and the weights are **two separate licenses**.

For regional providers and China-specific access rules, see [`regional.md`](regional.md).

---

## Gateways · 网关
| Gateway | Status | Why | Caveat |
|---|---|---|---|
| **OpenRouter** | ✅ verified | OpenAI-compatible; free models; privacy tiers | 50/1,000 free requests/day |
| **LiteLLM** | ⚪ hold | OpenAI-compatible gateway over 100+ providers | GitHub API reports **NOASSERTION**; verify license/terms before adoption (factory scan, P68) |

---

## Candidates to verify next · 待核验候选
These are leads, **not** verified facts. Do not quote numbers until the provider's own page is fetched:
- **NVIDIA NIM**, **Together AI**, **Fireworks AI**, **Cerebras**, **SambaNova**, **Mistral API**, **Azure AI Foundry**.
- Free trial credits that require a card, expire, or convert to paid usage.
- Regional free tiers (e.g., provider-specific student or startup programs).

**Why not list them now?** A stale free-tier number is worse than a missing one: it causes failed builds, unexpected bills, and bad decisions. `⚪` is honest.

---

## Selection guide · 选择建议
1. **Prototyping with public data:** Gemini free tier (multimodal) or Groq (fast open models).
2. **One API for many models:** OpenRouter `:free`; move to paid credits only when limits block you.
3. **RAG / embeddings:** Cohere trial; self-host embeddings if data is sensitive.
4. **Edge/serverless:** Cloudflare Workers AI; watch the daily Neuron budget.
5. **Sensitive code/data:** Ollama + an open-weight model on your own machine; no cloud key.
6. **Production:** none of the free tiers above. Budget for a paid tier and a fallback provider.

**Rule:** free tiers are for **evaluation and prototypes**. A production system needs an SLA, a spend cap, a data-processing agreement, and a fallback.