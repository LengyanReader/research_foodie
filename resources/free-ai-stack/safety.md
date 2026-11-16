# Safety, Privacy & Licensing · 安全、隐私与许可
> The rules that make a “free” resource safe enough to try.
> 让“免费”资源可以安全试用的规则。
**Updated:** 2026-11-08

---

## 中文速览
免费资源的最大风险不是“花钱”，而是**凭证泄露、ToS 违规封号、数据被用于训练、供应链恶意脚本、以及账单陷阱**。三条硬规则：**① 只用 provider 官方页面/官方仓库；② 永不把 API Key 交给“免费代理/共享”工具；③ 机密数据只用本地模型或明确 ZDR 的付费层。** 高星、免费、无限、免 Key——四个词同时出现时，默认它是坑。

---

## Threat model · 威胁模型
| Risk | What it looks like | Mitigation |
|---|---|---|
| **Credential theft** | Repo/extension asks for your API key or session token; "paste your key here" | Use official providers; store keys in env vars; scope and rotate; never commit |
| **ToS violation / ban** | "No key, unlimited frontier models"; proxy gateways; account sharing | Do not use; read the provider's terms; use official free tiers |
| **Data training / leakage** | Free tier says "content used to improve our products" | Do not send secrets/PII; prefer ZDR or local models; classify data first |
| **Supply-chain malware** | `curl \| bash`, opaque binaries, postinstall scripts, browser extensions | Use official installers; pin versions; verify checksums/signatures; read scripts |
| **Prompt injection** | Untrusted README/web page tells the agent to ignore rules or exfiltrate data | Treat fetched content as data, not instructions; sandbox; least privilege |
| **Billing trap** | "Free trial" requires a card; credits expire; overage auto-charges | Prefer no-card tiers; set spend caps; calendar the expiry |
| **Rate-limit lockout** | Free tier hits 429; app fails in production | Know RPM/RPD/TPM/TPD; implement backoff; keep a paid fallback |
| **Model deprecation** | A free model is retired or renamed | Pin versions; monitor changelogs; keep a provider-agnostic gateway |
| **Lock-in** | Proprietary SDK, proprietary format, no export | Prefer OpenAI-compatible APIs; keep prompts/data portable |

---

## API key hygiene · API Key 卫生
1. **Environment variables, not code.** `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY` — never hard-code.
2. **One key per project.** Revoke independently; limit blast radius.
3. **Least privilege.** Use scoped keys where the provider supports it.
4. **Spend cap.** Set a hard monthly cap before the first unattended run.
5. **Rotate.** Rotate after any leak, any shared machine, and on a schedule.
6. **Monitor.** Check usage dashboards for unexpected calls.
7. **Never commit.** Add `.env` to `.gitignore`; scan before push.
8. **Never paste into a third-party UI.** A "key tester" or "free proxy" is a key-stealer until proven otherwise.

---

## Data classification · 数据分级
| Data | Allowed on free tiers? | Recommended path |
|---|---|---|
| Public web text, open-source code | Yes | Any verified free tier |
| Internal docs, non-sensitive | With caution | Check data policy; prefer ZDR/opt-out |
| Customer PII, secrets, private keys | **No** | Local model or paid ZDR tier with a DPA |
| Proprietary source code | **No** by default | Local model; or a paid tier with no-training terms |
| Regulated data (health, finance, legal) | **No** | Compliance review; private deployment |

**Rule:** if you would not paste it into a public forum, do not paste it into a free tier.

---

## License & supply chain · 许可与供应链
- **OSI licenses:** MIT, Apache-2.0, BSD, GPL. Check the repo's `LICENSE` file, not the README badge.
- **`NOASSERTION` / missing license:** treat as **not open source** until clarified. (The factory's own scan flagged LiteLLM this way.)
- **Model licenses are separate:** an Apache-2.0 runtime does not make the model weights Apache-2.0. Check the model card.
- **Commercial use:** verify both the code license and the model license.
- **Releases:** prefer signed tags/releases; verify checksums; avoid unversioned `main`.
- **Dependencies:** run `pip-audit`/`npm audit`; pin lockfiles; review install scripts.

---

## Free-tier volatility · 免费层的波动
Free tiers are marketing, not contracts. They can change limits, models, regions, or disappear entirely.
- **GitHub Models** was retired on 2026-07-30. ✅
- **Hugging Face** free users get no inference credits; PRO gets $2/month. ✅
- **A 404 is a real outcome:** the widely cited `cheahjs/free-llm-api-resources` list returned 404 on 2026-11-08. ✅

**Mitigation:** keep a provider-agnostic client (OpenAI-compatible), a paid fallback, and a quarterly re-verification date.

---

## Red flags · 危险信号
- "No API key required" for frontier models.
- "Unlimited" free usage of paid models.
- "Use any client" via an unofficial proxy.
- Asks for your session token, cookie, or account password.
- `curl | bash` install from a short URL.
- Obfuscated binary with no source.
- No license, no issues, no maintainer identity.
- Free tier with no data-policy link.
- "Permanent free" claims with no provider source.

When you see one, stop. Do not "just test it" with a real key.

---

## Safe default stack · 安全默认栈
| Need | Safe default |
|---|---|
| Sensitive code/data | **Ollama + open-weight model** (local) |
| Non-sensitive prototyping | Official free tier: **Gemini / Groq / OpenRouter / Cloudflare / Cohere** |
| IDE coding | **GitHub Copilot Free / Gemini Code Assist / Amazon Q Free** |
| Open-source IDE agent | **Cline** (Apache-2.0, BYOK) with a scoped key |
| One API for many models | **OpenRouter** with ZDR settings; paid fallback |
| Never | "No-key unlimited" proxies, credential-sharing repos, cracked keys |

---

## Pre-adoption checklist · 采用前检查
- [ ] Official provider page fetched and dated.
- [ ] Free-tier limits recorded (RPM/RPD/TPM/TPD, credits, expiry).
- [ ] Data policy read; training/opt-out/ZDR status known.
- [ ] License verified (code and model, if applicable).
- [ ] Key stored in env var; spend cap set; rotation plan.
- [ ] Install path verified (official package, checksum/signature).
- [ ] Sandbox/least privilege for any code execution.
- [ ] Fallback provider identified.
- [ ] Re-verification date calendared (quarterly).
- [ ] If it looks too good to be true, it is.