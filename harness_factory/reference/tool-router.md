# Tool Router · 器具路由 —— 任务 → 工具生态（MCP · Skills · API · 仪器）

> 工欲善其事，必先利其器。做任何一类任务之前，先查"这个任务族有哪些可用的器"：MCP 服务器、Agent Skills、数据 API、模型与仪器；按质量门评估；登记进 SSOT；之后持续更新、代谢（退役失效者）。
> Before executing a task family, survey its tool ecosystem (MCP servers, Agent Skills, data APIs, instruments), score candidates through a quality gate, register them in the SSOT, then keep them fresh — the tooling analogue of the outlet/evidence maps.

**Updated:** 2026-10-28 · Load via `harness skill tool-router`. Machine-readable truth: `data/harnesses.json` (class `skills-protocols`), `data/sources.json` (feeds + `outlets`), `data/watchlist.json` (discovery topics). Related: [`capability-router.md`](capability-router.md) (situation→capability), [`evidence-instruments.md`](evidence-instruments.md) (claim→instrument), [`outlet-map.md`](outlet-map.md) (field→information outlet).

---

## 中文速览

三张地图各管一段：**outlet-map** 管"去哪找资料"，**evidence-instruments** 管"用什么仪器出证据"，本表管**"用什么工具干活"**——某个任务族当前可发现、可评估、可登记的 MCP / Skill / API / 模型 / 平台清单与入口。流程固定四步：**发现**（官方注册表 API · 目录 · 技能市场 · watchlist 主题检索）→ **评估**（来源、维护、许可、协议符合度、安全面——M6.11"能看到≠被授权"，工具投毒须设防）→ **登记**（进 `sources.json`/`harnesses.json`，带 verified+access 日期）→ **代谢**（feed 拉更新、定期复测、停维者标 `defunct` 保留标记，如 Papers with Code 先例）。古籍整理一节是**完整 worked example**，其他任务族照此格式开新表。

---

## 1. The loop · 四步循环

| Step | Action | Where it lives |
|---|---|---|
| **Discover · 发现** | Query the discovery surfaces (§2): official registry JSON API, directories, skill marketplaces; LLM discovery via `watchlist.json` topics | `harness refresh --provider feed` (RSS/Atom feeds of registered repos) + `--provider llm` (topic queries) |
| **Evaluate · 评估** | Score against the intake gate (§5): provenance, maintenance, license, spec conformance, security posture | judgment recorded in `why` + `verified`/`access` fields |
| **Register · 登记** | Add to SSOT: feeds → `sources.json`; tools/servers/directories → `harnesses.json` (class `skills-protocols`) or `outlets`; data sources per task family → `outlets` | `harness catalog --write` regenerates views; guards in `tests/` |
| **Metabolize · 代谢** | Feeds pull changes; re-probe `access` dates each round; defunct entries flip `verified:false` + `defunct` tag but stay as markers | P35 (Papers with Code) precedent; `cycle audit` flags drift |

Rule unchanged from §6.1 of the meta-discipline: **an aggregator is a discovery door, not a citation** — resolve every tool claim to the producer (its repo/spec page) before trusting it.

## 2. Generic discovery surfaces · 通用发现面（probed 2026-10-27/28）

| Surface | Door | Machine-readable? | Status 2026-10-28 | Registered as |
|---|---|---|---|---|
| Official MCP Registry | https://registry.modelcontextprotocol.io/ | **yes — `GET /v0/servers` JSON** | L 200 · API 200 with server metadata | `sources: mcp-registry-repo` · `harnesses: mcp-registry` |
| MCP reference servers | https://github.com/modelcontextprotocol/servers | releases feed | `releases.atom` 200 (old examples split to `servers-archived`, 2026-03 archive notice) | `sources: mcp-servers-repo` · `harnesses: mcp-servers-reference` |
| MCP project blog | https://blog.modelcontextprotocol.io/ | RSS | `/index.xml` 200 (442 KB) | `sources: mcp-blog` |
| Smithery | https://smithery.ai/ + `registry.smithery.ai/servers` | **yes — JSON registry + hosted connect** | L 200 · API 200 | `harnesses: smithery` |
| Glama | https://glama.ai/mcp/servers | HTML; grading per server | L 200 | `harnesses: glama` |
| PulseMCP | https://www.pulsemcp.com/servers | HTML, daily-updated; self-reported "22,290+ servers" page title | L 200 · `/feed` 404 (no verifiable RSS) | `harnesses: pulsemcp` |
| MCP.so | https://mcp.so/ | HTML (`servers.json` now 404) | L 200 | `harnesses: mcp-so` |
| Agent Skills spec | https://agentskills.io/ + https://github.com/agentskills/agentskills | releases feed | both 200; open standard with spec+SDK, published 2025-12-18 (cross-checked secondary; spec repo is primary) | `sources: agentskills` (feed was null — now filled) |
| Anthropic skills repo | https://github.com/anthropics/skills | releases feed | `releases.atom` 200 | `sources: anthropic-skills-repo` · `harnesses: anthropics-skills-lib` |
| skills.sh (Vercel) | https://skills.sh/ + `npx skills` CLI (github.com/vercel-labs/skills) | releases feed | both 200 | `sources: vercel-skills` · `harnesses: skills-sh` |

Scale claims across directories diverge (Smithery reported anywhere from ~7k to 26k+; Glama ~24k to ~99k) — **treat all directory counts as directional**, cite the directory page itself, not the blog post repeating it.

## 3. Worked example · 古籍整理（task family #1）

A full instantiation of §1–§2 for one task family. Swap the rows; keep the columns.

| Asset | Kind | Door | Machine path | Status probed 2026-10-28 |
|---|---|---|---|---|
| CBETA 電子佛典 (XML-TEI, 2026.R2 released 2026-08) | corpus / open data | https://cbeta.org/ | downloads + GitHub releases; TEI P5 XML — good for 校勘 diffing | L 200 · online reader `cbetaonline.dila.edu.tw` cert-failed from this network (unverified here) |
| CBETA Buddhist Texts **MCP server** (tendayspace) | MCP server (community) | https://www.pulsemcp.com/servers/tendayspace-cbeta-buddhist-texts | directory page 200; **repo itself not yet verified — treat as untrusted read-only per M6.11 until source-audited** | listed (via PulseMCP, discovered 2026-10-28) |
| CBDB 中国历代人物传记资料库 | database + API | https://github.com/cbdb-project (org) | official Open Web API `api.cbdb.org` SSL-blocked from this probe (unverified here); org + code repos 200; community **Claude Code skill for CBDB API** listed on mcpmarket (page 200) | org verified · API unverified (this network) |
| ctext.org 中國哲学書电子化計畫 | corpus + API | https://ctext.org/tools/api | documented JSON-RPC API (also data-writer); plain-text for pre-modern masters | L 200 · API docs 200 |
| 中华古籍资源库 (National Library) | portal / digitized books | https://guji.nlc.cn/ | image viewer for 古籍善本; no public API — manual intake into tasks | L 200 |
| Wikisource 中文源 | corpus + API | https://zh.wikisource.org/ | MediaWiki API + dumps; machine-readable classical texts with provenance notes | L 200 |
| BDRC / BUDA 佛教数字档案馆 | archive + linked open data | https://www.bdrc.io/ | IIIF + API; 28M+ pages claimed on official site; SSL handshake failed from this probe | **unverified here** (network), listed by official URL |
| 书生·端砚 Intern InkStone (古籍大模型, Shanghai AI Lab) | AI platform for ancient texts | https://discovery.intern-ai.org.cn/ | API-key metered (墨点 quota) — cost-sensitive gate M3/M7 before unattended use | L 200 |
| SikuBERT / SiKuRoBERTa | pretrained models (古文 NLP) | https://github.com/hsc748NLP/SikuBERT-for-digital-humanities-and-classical-Chinese-information-processing | 四库全书-based BERT variants for 自动标点 / NER / segmentation; companion paper line incl. SikuGPT (arXiv:2304.07778) | repo L 200 · `commits/master.atom` 404 (branch naming) — no feed registered |
| 中研院词书门户（dict.sinica） · MARCO 文本实体知识库（SJTU） | lexica / entity search | https://dict.sinica.edu.tw/ · http://marco.ihp.sjtu.edu.cn/ | 具体产品与收录范围未能证实（本机 SSL 失败 / 502）| **unverified** — registered as leads, re-probe next round |

**What a 古籍整理 harness derives from this table**: grounding=required (M4 provenance on every collation claim); M6 tool surface `read`+`external` (APIs) with the least-privilege rule — a community MCP server reads canonical data and **never** gets write/publish authority; M3 gates = back-conversion checks, TEI schema validation, collation diffs against two independent witnesses (e.g., CBETA XML vs. 大正藏 image via NLC portal); skills crystallize the recurring procedure (用户级写作/校订 skill 与本工作区三闸门实践即属此层).

## 4. Other task families · 开新表模板

Rows for coding/web-automation/data-analysis tooling should be added the same way — one table per family, each door probed with a date, each count directional. The capability layer already routes *when to use tools* (`capability-router`: `tool-use`, `sandboxed-execution`, `portable-skills`, `untrusted-content-discipline`); this file answers *which tools exist and are trustworthy right now*. Seed candidates per family come from watchlist topics (`mcp-skills-ecosystem`, `classical-texts-dh`) — discovery is wired into the update loop, not manual.

## 5. Intake quality gate · 入表质量门

Adopt a tool only after all boxes are checkable (M6 + M4 + M0.4):

- [ ] **Provenance** — official org/repo or named author; directory listing alone is *discovery*, not verification (resolve to producer).
- [ ] **Maintenance signal** — recent release/commit feed; note last-release date. Dormant ≠ dead, but dormant ≠ trusted.
- [ ] **License & data terms** — e.g., CBETA 的著署名可転載許可（attribution-based license）、目录站点的 ToS 对抓取的约束。
- [ ] **Spec conformance** — MCP version support (2026-07-28 core: stateless, MRTR, Tasks); Agent Skills format (frontmatter name+description, progressive disclosure).
- [ ] **Security posture** — tool poisoning exposure (descriptions can change after approval — pin versions; Invariant Labs advisory 2025-04-01; CSA *Agentic MCP Security Best Practices* v1); authorization must live **inside** the tool on concrete arguments (M6.11, R242); least privilege; no untrusted-read paired with secrets/outbound-send.
- [ ] **Cost surface** — metered APIs (InkStone 墨点, Smithery hosted) get a budget cap before unattended runs (cost-budget-caps).
- [ ] **Not-for** — every row records what the tool is *not* for (outlet-map discipline applied to tooling).

## 6. Metabolism · 新陈代谢

- Registered feeds pull diffs each refresh round; new releases/servers enter via LLM discovery on the watchlist topics.
- `access` dates are re-probed in scheduled rounds (P35 did this for paper portals; P41 for tool surfaces); failures flip `verified:false` with a note, entries are **retired in place**, not deleted (paperswithcode precedent).
- Directory count claims get refreshed with source + date or marked directional.
- Candidate not yet wireable (JSON APIs not pullable by `feed_provider`): tracked by roadmap **P35.R1** (JSON-API discovery provider) — registry endpoints (`/v0/servers`, `registry.smithery.ai`) are its named consumers.

---

## 中文 · 本节备忘

- 本表回答"**这个任务族现在有哪些可用、可信、已核实的工具**"；outlet-map 管资料，evidence-instruments 管证据仪器，capability-router 管纪律该不该启用工具。三表互引、不重复。
- 每行必须带探测日期与诚实状态：200 才写 verified；SSL/403/502 一律标 *unverified（本机网络）*，留作线索复测，不冒充事实。
- 社区 MCP 服务器（如 CBETA MCP）默认按**不可信只读**处理：源码审计前不授权写入、不外发（M4/M6.11）；工具描述可被作者事后改动，版本要锁定（工具投毒，Invariant Labs 2025-04）。
- 规模数字（目录收录数）一律"方向性"，引用目录自身页面而非转述博客。
- 新任务族照 §3 的列格式开表；种子来自 watchlist 的 `mcp-skills-ecosystem` / `classical-texts-dh` 检索主题，由 refresh 循环持续供给——梳理不是一次性动作，而是循环代谢。

## See also · 参见

- [`core/07-tools-and-skills.md`](../core/07-tools-and-skills.md) — M6.10 progressive skill loading · M6.11 exposure≠authorization, "sandbox" is a backend claim.
- [`reference/outlet-map.md`](outlet-map.md) §AI-paper portals — same wiring pattern, one round earlier (P35).
- [`review/mcp-skills-landscape-2026-10.md`](../review/mcp-skills-landscape-2026-10.md) — this round's landscape survey with full citations.
