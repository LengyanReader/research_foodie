# GitHub Lists & Red Flags · GitHub 清单与风险信号
> How to use GitHub “free LLM API” lists without getting burned.
> 如何安全使用 GitHub 上的“免费 LLM API”清单。
**Updated:** 2026-11-08 · GitHub metadata fetched from the API on 2026-11-08.

---

## 中文速览
GitHub 搜索 “free llm api” 返回 **2,409** 个仓库。多数是**聚合清单**，少数是**代理/共享密钥**。聚合清单可以作为**发现入口**，但**不能当引用**：每一条都必须回到 provider 官方页面核验。**高星不等于安全**——本次就看到 65k 星的“无需 API Key、无限免费前沿模型”仓库，这类是典型的代理/凭证共享风险。**不要安装、不要登录、不要输入任何 key。**

> **Rule:** an aggregator is a discovery door, not a citation (`reference/tool-router.md` §1).

---

## Meta-lists · 可用的聚合清单
Use these to **discover candidates**, then verify each candidate at the provider.

| Repo | License | Stars | Last push | What it claims | Use it as | Caveat |
|---|---|---:|---|---|---|---|
| [`mnfst/awesome-free-llm-apis`](https://github.com/mnfst/awesome-free-llm-apis) | **CC0-1.0** ✅ | 12,593 | 2026-11-07 | "List of Permanent Free LLM API (API Keys)" | Discovery index | "Permanent" is not guaranteed; verify each provider |
| [`open-free-llm-api/awesome-freellm-apis`](https://github.com/open-free-llm-api/awesome-freellm-apis) | **MIT** ✅ | 5,371 | 2026-11-07 | "134+ free LLM APIs & AI API keys from 40+ providers"; one-click setup for Claude Code, Cursor, Codex | Discovery index | One-click setup scripts are a supply-chain surface; inspect before running |
| [`zebbern/no-cost-ai`](https://github.com/zebbern/no-cost-ai) | **MIT** ✅ | 2,403 | 2026-09-21 | "80+ free AI services for chat, image, video, voice & APIs (may sometimes include access to lead gen ai models for free)" | Discovery index | "Lead gen" access is marketing/trial access, not a stable free tier |
| `cheahjs/free-llm-api-resources` | — | — | — | Formerly a widely cited list | **Do not cite as current** | **404 on 2026-11-08** ✅ |

### What these lists are good for
- Finding provider names you did not know about.
- Comparing categories (chat, embeddings, image, audio, coding).
- Spotting new free-tier programs.

### What they are not good for
- Establishing current limits, prices, or data policies.
- Proving a resource is safe or authorized.
- Replacing the provider's own terms.

---

## Red flags found in the wild · 实际发现的风险样本
These are **not recommendations**. They illustrate the pattern to avoid.

| Repo | What it claims | Why it is unsafe · 为何危险 |
|---|---|---|
| [`Ebony-Vinyl/dsh-our-free-model`](https://github.com/Ebony-Vinyl/dsh-our-free-model) | "No login, no sign-up, no API key" for DeepSeek V4.1 Flash / Kimi K3, "completely free, no usage cap" | **65,834 stars** does not make it a provider. "No key + unlimited frontier models" implies credential pooling/proxy access, likely violates the model provider's terms, and can expose your prompts or install malicious code. ⛔ |
| [`jwadow/kiro-gateway`](https://github.com/jwadow/kiro-gateway) | "Proxy API gateway for Kiro IDE & CLI (Amazon Q Developer / AWS CodeWhisperer). Use free Claude models with any client." | A proxy that repackages another product's free quota. Account bans, key exposure, and ToS violations are the expected failure modes. ⛔ |

**Pattern to recognize:** "no key", "unlimited", "frontier models", "reverse proxy", "use any client", "bypass", "unlimited credits". These are not free tiers; they are ways to borrow someone else's access.

---

## Evaluation checklist · 评估清单
Before adding a GitHub candidate to your stack, answer all ten:

1. **Official page?** Does the provider have its own pricing/rate-limit page that confirms the free tier?
2. **License?** Is the repo OSI-licensed (MIT/Apache-2.0/etc.), or is the license missing/`NOASSERTION`?
3. **Maintenance?** When was the last push? Are issues answered? Is there a release process?
4. **Maintainer identity?** Is there a real org/domain, or an anonymous account?
5. **Install path?** Does it ask you to `curl | bash`, run an opaque binary, or install a browser extension?
6. **Network behavior?** Does it proxy your prompts through an undisclosed server?
7. **Key handling?** Does it ask for your API key or session token? Where does it store it?
8. **Terms?** Does the provider allow this use? Does the repo mention ToS?
9. **Data policy?** Does the free tier train on your data? Is there a ZDR/opt-out option?
10. **Exit?** Can you export your data and leave? Is there a paid fallback?

If any answer is unknown, mark the candidate `⚪` and do not put it in a production path.

---

## Why stars are a weak signal · 为什么 star 数不可靠
- Stars measure attention, not security or legality.
- A repo can be popular and still be a credential trap.
- Fork/star counts can be gamed.
- A high-star list can contain stale or unsafe entries; the list's license does not vet its links.

**Better signals:** official provider domain, OSI license, recent commits, signed releases, reproducible builds, issue-response quality, and an explicit data policy.

---

## How to contribute a candidate · 如何贡献候选
Add it to this file with:
- Repo URL, license, stars, last push (GitHub API date).
- The provider's official free-tier URL.
- A one-line `✅` / `🟡` / `⚪` / `⛔` verdict and the reason.
- An access date.

If you cannot verify it, leave it `⚪`. A missing entry is better than a wrong one.