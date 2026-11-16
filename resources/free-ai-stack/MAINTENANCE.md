# Maintenance & Update Loop · 维护与更新循环
> How to keep this catalog correct as free tiers change.
> 免费层变化时，如何保持本目录正确。
**Updated:** 2026-11-08 · **Next full review:** 2027-02-08

---

## 中文速览
免费层是**营销手段，不是合同**：额度、模型、条款、数据政策随时会变。维护分三档：**每月轻检**（链接是否 404、red flag 是否新增）、**每季度全检**（重新抓官方页面、更新数字与访问日期）、**采用前专项核验**（生产决策前重新抓该 provider 的 pricing/terms/data policy）。**任何数字都必须带访问日期；抓不到就标 `⚪` 或 `404`，不要凭记忆补。** 失效条目不删除，标 `dead`/`⛔` 保留为“代谢标记”。

---

## Cadence · 节奏
| Cadence | Scope | Output |
|---|---|---|
| **Monthly light check** | HTTP status of every `sources.md` URL; GitHub lists' last push; new red flags | Update `sources.md` status; add a changelog line if anything changed |
| **Quarterly full review** | Re-fetch every official page; update limits/numbers/access dates; re-check all `⚪` leads | New snapshot date at the top of every file; changelog entry |
| **Before production adoption** | The specific provider's pricing, terms, data policy, SLA, region | A decision note; no production use on a free tier without a paid fallback |
| **On a dead link** | Mark `404`/`dead`; keep the entry as a marker; find a replacement | Changelog entry; do not silently delete |

---

## Procedure · 更新流程
1. **Pick the file(s)** to update from the coverage map in `README.md`.
2. **Fetch the official page** (provider pricing/rate-limit/terms). Use the URL in `sources.md`.
3. **Update the number and the access date.** If the page is unavailable, mark `⚪`/`404`; do not reconstruct.
4. **Re-check the safety gates:** data training, key handling, license, ToS, region, real-name, billing.
5. **Update the status:** `✅` verified, `🟡` partial, `⚪` lead, `⛔` avoid, `dead` retired.
6. **Update `sources.md`** with the new URL/status/access date.
7. **Add a `CHANGELOG.md` entry** (date, changed files, what changed, evidence).
8. **Run a scoped doc check** (links, fences, placeholders). Do not run the repo-wide doc scan in this sandbox; it hangs (pre-existing environment limitation).
9. **Commit** only when the user asks; **never push** without explicit approval.

---

## Entry template · 条目模板
```md
| Provider | Free offering | Limits (as of YYYY-MM-DD) | API | Data use | Best for | Caveat |
|---|---|---|---|---|---|---|
| **Name** ✅ | Free tier: … | RPM/RPD/TPM/TPD or credits | OpenAI-compatible / native | Trains? ZDR? opt-out? | … | … |
```

**Required fields:** official URL, access date, verification status, free-tier limits, data policy, caveat.
**Forbidden:** “unlimited”, “permanent”, “no key” unless the provider's own page says so.

---

## Status board · 状态板
| Document | Last verified | Next review | Coverage |
|---|---|---|---|
| `README.md` | 2026-11-08 | 2027-02-08 | Quick picks, legend, coverage map |
| `llm-apis.md` | 2026-11-08 | 2027-02-08 | Free LLM APIs + multimodal + self-host |
| `vibe-coding.md` | 2026-11-08 | 2027-02-08 | Free coding agents/IDEs + open source |
| `free-app-infra.md` | 2026-11-08 | 2027-02-08 | Hosting/DB/auth/search/vector/observability |
| `regional.md` | 2026-11-08 | 2027-02-08 | China/Asia/EU/global leads |
| `github-lists.md` | 2026-11-08 | 2027-02-08 | Meta-lists + red flags |
| `safety.md` | 2026-11-08 | 2027-02-08 | Threat model + checklist |
| `sources.md` | 2026-11-08 | 2027-02-08 | Source ledger |

---

## Next verification queue · 下一批核验队列
Priority order for the next update:
1. **China/Asia free quotas** — DeepSeek, Alibaba Model Studio (Qwen), Zhipu, Moonshot, SiliconFlow, ModelScope. Record real-name, region, cross-border data, and whether the free tier trains on data.
2. **Vibe-coding builders** — Lovable, Bolt.new, v0, Replit, Firebase Studio, Google AI Studio Build. Record free credits, expiry, commercial-use terms, and data policy.
3. **Open-source agent licenses** — Aider, OpenHands, Goose, Roo Code, OpenCode, Qwen Code. Fetch the `LICENSE` file and model-card terms.
4. **Free infra leads** — Neon, Turso, Upstash, Pinecone, Brave Search API, Exa, Jina, Helicone, Arize Phoenix, GitHub Actions minutes.
5. **Production comparison** — paid-tier SLA, data-processing agreement, spend cap, and fallback provider for the recommended stack.

## Automation options · 自动化选项
The factory already has a discovery/registration loop; this catalog can plug into it later:
- Add a `free-ai-stack` topic to `harness_factory/data/watchlist.json` (proposal; not done in this snapshot).
- Register verified providers/tools in `harness_factory/data/sources.json` / `data/harnesses.json` with `verified` + `access` fields.
- Re-run `harness refresh` / `harness intel`; keep proposals in `updates/` per workspace rules.
- A future `verify.py` could fetch every URL in `sources.md` and report HTTP status + last-modified; network access is environment-dependent.

**Do not** auto-apply an update to the catalog without a human review; free-tier changes are high-stakes for cost and data policy.

---

## Change log · 变更日志
See [`CHANGELOG.md`](CHANGELOG.md). Every update should answer:
- What changed?
- Which source proves it?
- What is now `dead`/`⛔`?
- What is the new next-review date?