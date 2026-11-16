# Free Vibe Coding · 免费 vibe coding 资源
> Free coding agents, IDEs, CLIs, and open-source alternatives — with limits and safety notes.
> 免费编码 agent、IDE、CLI 与开源替代——含限额与安全说明。
**Updated:** 2026-11-08 · All numbers are **as of 2026-11-08**.

---

## 中文速览
零成本起步有三条路：**① 官方免费套餐**（GitHub Copilot Free、Gemini Code Assist、Amazon Q Developer Free、Mistral Vibe Free）；**② 开源 agent + 自带密钥**（Gemini CLI、Cline、Aider、OpenHands、Goose、Roo Code、OpenCode、Qwen Code）；**③ 本地模型**（Ollama + 开源权重，隐私最好，但要硬件）。**“免费”通常只免工具，不免模型调用**：BYOK 的开源 agent 仍要付 provider 费用；官方免费套餐有严格配额；免费层常会用你的数据改进产品。**不要用“无需 Key、无限免费前沿模型”的代理。**

---

## Verified free coding tools · 已核验免费编码工具
| Tool | Free offering | Limits (as of 2026-11-08) | Open source / license | Model source | Data / privacy | Caveat |
|---|---|---|---|---|---|---|
| **GitHub Copilot Free** ✅ | Free individual plan | **2,000 completions/month**; allowance of GitHub AI Credits; **auto model selection only**; limited agents | Proprietary | GitHub/Microsoft-hosted models | Per GitHub Copilot data policy | Limited features; no premium model choice |
| **Gemini Code Assist Standard** ✅ | Free tier | **2 requests/sec**; **6,000 code requests/day**; **960 chat requests/day**; agent mode + Gemini CLI **1,500 requests/day** (Standard) | Proprietary service | Google Gemini | Per Google Cloud terms | Quota shared across agent mode/Gemini CLI; GitHub app PR reviews ≥100/day (preview) |
| **Amazon Q Developer Free** ✅ | Free tier | **50 agentic requests/month**; **1,000 lines of code/month** for Java upgrades; IDE/CLI | Proprietary | AWS/Claude models | **Data collection opt-out available** | Very small agentic quota; Pro is $19/mo |
| **Mistral Vibe Free** ✅ | Free product plan | Limited messages and web searches; **limited coding sessions**; web/mobile | Proprietary | Mistral models | Per Mistral terms | Not an API free tier; verify Pro/Team limits |
| **Gemini CLI** ✅ | Open-source CLI + free quota via Google account | Quota shared with Gemini Code Assist agent mode: **1,500 requests/day** (Standard) | **Apache-2.0**; 108,774 stars; pushed 2026-11-08 | Google Gemini | Per Google account/Cloud terms | Quota and model availability can change |
| **Cline** ✅ | Open-source IDE agent | No bundled free model; **BYOK** | **Apache-2.0**; 71,455 stars; pushed 2026-11-07 | Any OpenAI-compatible provider | Depends on your provider; code leaves your machine | Human-in-the-loop; you pay model costs |
| **Ollama** ✅ | Open-source local runtime | No cloud quota; limited by your hardware | **MIT**; 186,320 stars; pushed 2026-11-08 | Open-weight models | **Local; no cloud** | Needs RAM/GPU; model quality varies |

---

## Open-source candidates · 开源自托管候选
These are listed in the factory catalog (`harness_factory/data/harnesses.json`) as verified tools, but their **license was not re-verified this round**. Check the repo license before redistribution or commercial use.

| Tool | What it is | Why it is here | Verify before use |
|---|---|---|---|
| **Aider** | Git-native pair programmer | Repository map; CLI; BYOK | License, provider costs |
| **OpenHands** | Open platform for software agents | Sandboxed runtime; Agent Skills | License, sandbox requirements |
| **Goose** | Block's extensible agent | MCP client; code/research/automation | License, model setup |
| **Roo Code** | VS Code-side agent | Modes and approvals | License, provider costs |
| **OpenCode** | Open-source terminal coding agent | Provider-agnostic; plugin/skill system | License, plugin trust |
| **Codex CLI** | OpenAI local coding agent | Agent-first workflow | License, OpenAI account/credits |
| **Qwen Code** | Qwen coding CLI | Open-source CLI alternative | License, Qwen account/quota |

**Official repos:** [Aider-AI/aider](https://github.com/Aider-AI/aider) · [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) · [block/goose](https://github.com/block/goose) · [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) · [sst/opencode](https://github.com/sst/opencode) · [openai/codex](https://github.com/openai/codex) · [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)

---

## Vibe-coding builders · 待核验的“一键建应用”平台
These are **candidates**, not verified free tiers. They change pricing frequently; fetch their official pricing page before use:
- **Lovable**, **Bolt.new**, **v0**, **Replit**, **Firebase Studio**, **Google AI Studio Build**.

Do not assume a "free plan" includes API access, private projects, or commercial use. Check:
1. Free credits/limits and expiry.
2. Whether the free tier trains on your data.
3. Whether generated code/assets are yours to use commercially.
4. Whether deploy/hosting is included or billed separately.

---

## Deploy it for free · 免费部署
A vibe-coded app is not done at "generate code"; it needs hosting, a database, and (if it uses RAG) search. Verified free prototypes:
- **Vercel Hobby** — full-stack hosting, $0, **personal/non-commercial**; 1M CDN requests/month, 100 GB fast data transfer, 1M function invocations.
- **Cloudflare Pages Free** — static hosting; 500 builds/month, 20,000 files, 100 custom domains/project.
- **Supabase Free** — Postgres + Auth + Storage; 500 MB DB, 50,000 MAU, 2 active projects, **paused after 1 week of inactivity**.
- **Tavily** — search API for RAG; 1,000 credits/month, no card.
- **Qdrant Cloud Free** — vector DB; 0.5 vCPU / 1 GB RAM / 4 GB disk.
- **Langfuse Hobby** — LLM observability; 50k units/month, 30 days data access.

Full details, limits, and unverified leads: [`free-app-infra.md`](free-app-infra.md).

**Prototype-only rule:** free hosting has no SLA, can pause, and may be non-commercial. Move to a paid tier or self-host before production.

## Selection guide · 选择建议
| Your situation | Recommended start | Why |
|---|---|---|
| Student / individual, light use | **GitHub Copilot Free** or **Gemini Code Assist** | No card; official quotas |
| AWS shop, Java upgrade | **Amazon Q Developer Free** | 50 agentic requests + 1,000 lines Java/month |
| Want one IDE agent + your own key | **Cline** (Apache-2.0) | Human-in-the-loop; provider-agnostic |
| Terminal-first, open source | **Gemini CLI** or **Aider** | CLI workflows; BYOK/free quota |
| Sensitive code, no cloud | **Ollama + open-weight model** | Local; no data leaves the machine |
| Non-sensitive prototype | **Gemini / Groq / OpenRouter free tier** | Fast start; watch limits |

---

## Safety rules for coding agents · 编码 agent 安全规则
- **Least privilege:** run agents in a sandbox/container, not on your main machine with your whole home directory mounted.
- **Review diffs:** never auto-commit or auto-push an agent's changes. Read the diff; run the tests.
- **No secrets in prompts:** API keys, `.env`, customer data, and private keys are not context.
- **Scoped keys:** use a provider key with a spend cap and the minimum scope; rotate it.
- **Pin versions:** install from official package managers; verify release provenance; avoid `curl | bash`.
- **Local-first for sensitive code:** a smaller local model is slower but keeps the code on-device.
- **Beware "free unlimited":** if a tool promises no key and no limit, assume credential pooling or ToS violation until proven otherwise.