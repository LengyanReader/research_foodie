# Feed-health round survey (P59) · 信息渠道健康巡检

**Updated:** 2026-11-02 · probes run 2026-11-02 from this host. Companion to `reference/tool-router.md` (tool surfaces) and `review/mcp-skills-landscape-2026-10.md` — this one audits the **intake doors of the update loop itself**: does every feed we claim to poll still answer, and does every watchlist topic have a source that can actually carry it?

> 中文速览：本轮由「全面更新升级与进化」指令触发——`full-update` 六阶段全绿跑完后，对它的产出做人工分诊：4 个 high 级"主题无源"、4 个"未跟踪来源"、23 个"停更来源"。逐一直连复探后：两个主题是真的没接线（P41/P35 登记主题时只写了 keywords，没有将任何 feed 实体挂上主题）；4 家源的 feed 门确实 404 了（The Batch 已改道找回，Anthropic 官方从无 RSS、改挂社区镜像并如实降级标注，Meta/AAIF 暂无门、改走 LLM-discovery）；"未跟踪"三件里有两件是审计逻辑的假阳性（主 URL 与 feed 域名不同），已修引擎；arXiv 周末空 feed 是正常公告节奏，加注防误报。主题覆盖率 67% → 91.7%，端到端 feed 拉取 2069 候选验证通过。

## 1. Method

One `harness full-update` tick (2026-11-02: intel 3395 items / probe-domains 5 clusters / trace-audit 1 proposal / evolve 27 audits / cycle audit 0·0 / scoreboard 1.0), then per-item triage: every audit claim was re-checked with a **direct fetch from this host** before anything was written to the SSOT — an audit row is a lead, not a fact (M0.3).

## 2. Topic wiring (the two high-severity findings, plus P41's two)

| watchlist topic | finding | fix (2026-11-02) |
|---|---|---|
| `scholarly-discovery` | registered P35 with keywords but **no entity carried it** → feed path could never attribute paper pulls to it | carried by the 4 RSS-pullable arXiv doors (`arxiv-cs-ai/cl/lg/ma`) + `neurips-blog`; non-RSS portals (HF Papers, S2, OpenAlex…) stay on the LLM-discovery path (roadmap P35.R1) |
| `mcp-skills-ecosystem` | registered P41, same defect | carried by 14 entities: `anthropic-mcp`, `mcp-servers-repo`, `mcp-registry-repo`, `mcp-blog`, `agentskills`, `anthropic-skills-repo`, `vercel-skills`, `aaif`, `anthropic`, `meta-fair`, `huggingface`, `openrouter`, `simon-willison`, `openai` |
| `classical-texts-dh` | registered P41, same defect | partial: `archive-blog` (preservation/corpus-availability news); the CBETA/ctext/CBDB doors are JSON/HTML portals with no feeds — full wiring waits for a real 古籍 task (P41.R1) |
| `ambition-and-agency` | registered earlier, still **no honest carrier** | **deferred, not force-wired** (roadmap P59.R1) — no tracked feed genuinely publishes goal-elevation/requirement-refinement content; faking coverage would be metrics theater |

\* Guard catch (P59 close): the `openai` carrier was listed here but not yet wired in the SSOT — the P59 guard test caught the 13-vs-14 gap and `openai` now carries the topic (it does publish MCP/agent-skills content via its platform news door).

Coverage after wiring: **67% → 91.7%** (11/12 loop topics), `evolve` metric line.

## 3. Dead and moved feed doors (probed 2026-11-02)

| entity | old door | verdict | action |
|---|---|---|---|
| `the-batch` | `deeplearning.ai/the-batch/feed/` | **404**; the Ghost CMS feed moved to `charonhub.deeplearning.ai/rss/` (**200**, 15 items, newest 2026-10-30) | repointed, note added |
| `anthropic` | `anthropic.com/news/rss.xml` | **404** — and Anthropic publishes **no official RSS** (third-party surveys and the Alan Turing Institute's [ai-rss-feeds](https://github.com/alan-turing-institute/ai-rss-feeds) project both state it; the institute's own anthropic-news mirror carries stale ordering) | repointed to the BestBlogs RSSHub mirror `rsshub.bestblogs.dev/anthropic/news` (200, 10 items, newest 2026-10-17); marked **discovery-grade mirror** — resolve claims to anthropic.com originals, freshness lags ~2 weeks |
| `meta-fair` | `ai.meta.com/blog/rss/` | **404**; `/blog/rss`, `/rss/`, `/blog/feed/` also 404; blog live at `/blog/` | `feed: null` + note; enters via LLM-discovery/manual |
| `aaif` | `aaif.io/news/rss.xml` | **404**; no `<link rel=alternate>` on the (200) homepage | `feed: null` + note; re-probe deferred (P59.R1) |
| `arxiv-cs-ai` | `export.arxiv.org/rss/cs.AI` | 200 but **0 items on 2026-11-02 (Sunday)** — arXiv announces no new listings on weekends | not a defect: why-text documents the weekend gap so the stale-source audit cannot mislead |
| `openai-swarm` | releases.atom 200, empty | repo **not archived but last push 2026-04-15** (GitHub API) | dormancy note; legacy-pattern record, expected quiet |

## 4. Engine fixes (false positives in the evolution audit)

- **untracked_source over-matched on host identity**: candidates arrive on the *feed* domain (`karpathy.github.io`, `latent.space`) while entities are tracked by canonical url (`karpathy.ai`, `www.latent.space/`). Two of the three "untracked" findings were already-tracked blogs. Fixed in `evolution.py`: the known set now unions **url + feed + api hosts**, and `www.` is stripped as a presentation variant. `blog.archive.org` was a genuine gap — registered as entity `archive-blog`.
- **stale_source at day granularity**: with only same-day intel, every feed shows "no new items". Left as-is (low severity, informational); the notes added this round (weekend gaps, dormancy, closed doors) are what make the row actionable.

## 5. New channels registered (intake gate passed, probed 2026-11-02)

| entity | door | freshness at probe | why |
|---|---|---|---|
| `neurips-blog` | `blog.neurips.cc/feed/` 200 | 10 items, newest 2026-10-25 | the conference-side channel the paper-discovery loop was missing (award/workshop commentary; NeurIPS 2026 runs in Dec) |
| `archive-blog` | `blog.archive.org/feed/` 200 | 10 items, newest 2026-10-21 | Internet Archive / Open Library news — corpus-availability and long-term-preservation claims behind digital-humanities and classical-texts work |

## 6. Deliberate non-actions (M0.4/M0.5)

- **No source retired on one tick's evidence.** 19 stale rows after fixes are cadence noise or documented gaps above; retirement is a metabolism decision for a round with a consumer, per `tool-router.md` §6.
- **No forced carrier for `ambition-and-agency`** — a topic earns sources, sources don't earn topics.
- **The `trace-audit` low-outcome proposal and the 5 vendor-keyword domain clusters** (openai/chatgpt/face/introducing/work — vendor-news noise, nearest-domain rule says they change no routing) are left as observations; nothing landed from them.
- **No new capability, clause, or catalog entry** — this round repairs the pipes, it does not grow the map.

## 7. See also

`reference/tool-router.md` · `review/mcp-skills-landscape-2026-10.md` · `review/scholarly-channels-2026-10.md` · `tasks/REFRESH.md` · cycles P35/P41/P59.
