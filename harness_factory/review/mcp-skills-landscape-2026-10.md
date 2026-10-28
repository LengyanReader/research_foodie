# MCP 与 Agent Skills 生态扫描 · The Tool-Ecosystem Landscape, surveyed 2026-10-28

> P41 轮的扫描底稿：工具协议（MCP）、技能标准（Agent Skills）、发现渠道（注册表/目录/市场）与安全面（工具投毒）的一次广域检索记录，全部标注访问日期与一手来源。操作面见 `reference/tool-router.md`。
> Working notes behind round P41: one broad, dated sweep of the tool-protocol (MCP), skill-standard (Agent Skills), discovery-channel (registries / directories / marketplaces) and security surface. The operational sheet is `reference/tool-router.md`.

**Updated:** 2026-10-28 · Probes run from this machine on 2026-10-27/28; all statuses below are *as observed then*, not standing claims.

---

## 1. Protocol layer · 协议层（MCP）

| Fact | Source | As of |
|---|---|---|
| MCP is the standard protocol for exposing tools/resources/prompts to agents; the 2026-07-28 core revision brings stateless requests, MRTR mid-call human input, a Tasks extension for durable runs, list-cache hints, 12-month deprecation window | spec blog: https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; digested in this repo at P20 (R244) | 2026-10-23 read |
| **Official MCP Registry** live at https://registry.modelcontextprotocol.io/ (launched in preview 2025-09-08), "the official centralized metadata repository for publicly accessible MCP servers" | launch post: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/ ; about page: https://modelcontextprotocol.io/registry/about | probe 2026-10-28: L 200 |
| Registry exposes a **JSON discovery API**: `GET https://registry.modelcontextprotocol.io/v0/servers` returns server metadata (`{"servers":[{"server":{"$schema":…`) | probe from this machine | 2026-10-28: 200 |
| Reference server collection: https://github.com/modelcontextprotocol/servers — pre-2026 examples moved to an archive repo (archive notice 2026-03) | repo page + its README notes | probe 2026-10-28: L 200, `releases.atom` 200 |
| Spec repo & registry repo both have pullable GitHub Atom release feeds | `anthropic-mcp`, `mcp-servers-repo`, `mcp-registry-repo` feeds in `data/sources.json` | probe 2026-10-28 |

## 2. Skill layer · 技能层（Agent Skills）

| Fact | Source | As of |
|---|---|---|
| A skill = a folder with `SKILL.md` (name+description frontmatter) + optional scripts/resources; loaded by **progressive disclosure** — the contract our M6.10 encodes | https://agentskills.io/ (spec site) ; Anthropic research post https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills | 2026-10-28 (site probe 200 → /home) |
| Agent Skills introduced Oct 2025; **published as an open standard (spec + SDK) on 2025-12-18** | introduction per Anthropic post (2025-10-16); open-standard date carried by multiple independent secondary reports (strapi.io 2026-02-10; unite.ai 2025-12-19), consistent — spec repo `github.com/agentskills/agentskills` is the primary artifact | reports read 2026-10-28 |
| Spec repository live with releases feed | probe of https://github.com/agentskills/agentskills (`releases.atom`) | 2026-10-28: both 200 |
| Anthropic's own skills library (document skills docx/pdf/pptx/xlsx + examples) | https://github.com/anthropics/skills | probe 2026-10-28: L + `releases.atom` 200 |
| Cross-harness install path: **skills.sh directory + `npx skills` CLI** (vercel-labs/skills) — detects installed agents, installs a skill into any compatible harness | https://skills.sh/ ; https://github.com/vercel-labs/skills | probe 2026-10-28: both 200 |
| Adoption signals: Gemini CLI documents Agent Skills (`.gemini/skills/`); its docs page states Gemini CLI was replaced by Antigravity CLI on 2026-06-18 | https://geminicli.com/docs/cli/skills/ (official docs header) | read 2026-10-28; *unverified beyond the docs page* |

## 3. Discovery channels · 发现渠道

Official registry (machine door, §1) + four third-party directories, all probe-verified reachable 2026-10-28: **Smithery** (hosted connect + `registry.smithery.ai/servers` JSON API 200), **Glama** (per-server grading on license/quality/maintenance), **PulseMCP** (daily-updated; page title self-reports "22,290+ servers"; no verifiable RSS — `/feed` 404), **MCP.so** (client-compat views; former bulk `servers.json` 404). Secondary 2026 comparisons report wildly divergent counts for the same directories (Smithery ~7k–26k; Glama ~24k–99k; sources: truefoundry 2026-04-06, scalekit 2026-10-13, seosiri 2026-10-21) — **counts are directional; cite the directory page itself.** Skill-side doors: skills.sh, anthropics/skills, plus marketplaces (ClaudePluginHub, mcpmarket.com — the latter listing e.g. a community "CBDB API Claude Code Skill", page 200 on probe).

## 4. Security surface · 安全面

- **Tool poisoning** remains the protocol's signature threat: a server can change a tool description after user approval; mitigations = pin/lock versions, re-hash descriptions, audit before enabling (Invariant Labs advisory, 2025-04-01: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).
- CSA *Agentic MCP Security Best Practices v1* (https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/) prescribes separate authorization/resource servers, OAuth 2.1 + PKCE, and registry vetting — consistent with our **M6.11** clause: exposure is not authorization; a remote MCP server must authorize its own protected operations (R242).
- Repo consequence (already in `core/07-tools-and-skills.md`): community servers enter the tool-router as **untrusted read-only** until source-audited; never pair untrusted-read with secrets or outbound-send.

## 5. What this round changed · 本轮落点

- `sources.json`: +5 harness-group entities with verified feeds (`mcp-servers-repo`, `mcp-registry-repo`, `mcp-blog`, `anthropic-skills-repo`, `vercel-skills`); `agentskills` feed filled (was `null`); +9 digital-humanities outlets for the 古籍整理 worked example (ctext, CBETA, CBDB, BDRC, 中华古籍资源库, 维基文库, 书生·端砚, Sinica lexica, MARCO — with honest verified/access states).
- `harnesses.json`: class `skills-protocols` grows 4 → 12 entries (+2 kinds: `server-registry`, `server-collection`); 205 → 213 catalog entries.
- New operational sheet: **`reference/tool-router.md`** (discover → evaluate → register → metabolize; 古籍整理 as task family #1; intake quality gate; registered in SKILL.md + `harness skill tool-router` + capability-router).
- `watchlist.json`: discovery topics `mcp-skills-ecosystem`, `classical-texts-dh`.
- Deferred (roadmap): P35.R1 now has named consumers (`/v0/servers`, `registry.smithery.ai`) for the JSON-API discovery provider; P41.R1 — source-audit the community CBETA MCP server (repo not yet located/verified) and re-probe SSL-blocked doors (api.cbdb.org, bdrc.io, dict.sinica.edu.tw, cbetaonline) from a cleaner network.

## 中文 · 结论一段

MCP 与 Agent Skills 在 2026 年已从"协议/格式"长成有**官方注册表、第三方目录、跨 harness 安装 CLI 与安全咨询**的完整生态；本仓库原有的模式层（M6.10/M6.11）与单一协议条目不足以回答"这个任务有什么器可用"。P41 补上的是**操作层**：一张可代谢的器具路由表（发现→评估→登记→代谢四步），一个完整任务族样例（古籍整理：CBETA/CBDB/ctext/国家图书馆/维基文库/端砚/SikuBERT 等九个入口，逐个带 2026-10-28 探测状态），两个新的检索主题与五条带 feed 的注册渠道。数字保持方向性判断，未证实的渠道一律 unverified 留待复测——引用即生命线，没有松动。

## See also

- [`reference/tool-router.md`](../reference/tool-router.md) — the operational sheet this survey feeds.
- [`review/scholarly-channels-2026-10.md`](scholarly-channels-2026-10.md) — P35's analogous survey for paper-discovery portals.
- [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) — M6.10 / M6.11 clauses.
