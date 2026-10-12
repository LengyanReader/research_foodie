# REFRESH · 自我更新 / Self-update

**Updated:** 2026-10-12 · **Status:** active · **Module:** M5 (self-evolution)
**Owner:** user (human gate) + agent

> The knowledge base must not freeze. `harness refresh` periodically pulls the
> latest and most leading work, expands coverage in all directions, and surfaces
> what is **hot** and what is a **gap** — as *proposals only*, never as edits.
> 知识库不能冻结。`harness refresh` 定期抓取最新、最前沿的工作，全方位扩充边界，
> 标出**热点**与**缺口**——但只产出**提案**，绝不直接改写正文。

---

## 中文速览

**循环（M5）。** `信号 → 审计 → 变异提案 → 日志`，**人工把关**（M0.8）。

**它做什么。** 按 `data/watchlist.json` 的主题与前沿探针，从（a）本地 `updates/inbox.jsonl` 与（b）可选 LLM 检索，收集候选；对候选做**溯源审计**（无 url/外部 id 直接剔除，M4）、**去重**（对照 `review/` 语料中已有的 arXiv/DOI/URL）、**相关度排序**；再统计**热点主题**与**覆盖缺口**。

**它绝不做什么（M0.4）。** 不改 `review/`、`modules.json`、`domains.json`；不编造标题/编号/链接；不自动合并。所有产物落在 `updates/`，逐条可复核、可回滚（M0.9）。

**产出。**
```
updates/
  queue.jsonl       本轮采纳的候选（pending，等待人工确认）
  REPORT.md         双语人读报告（热点 / 缺口 / 采纳 / 剔除及原因）
  JOURNAL.md        append-only 运行日志（每次刷新一行）
  proposals/*.md    人工确认后生成的合并提案存根
```

---

## The loop · 循环

```
watchlist ──▶ collect ──▶ audit ──▶ rank ──▶ report+queue ──▶ (human) ──▶ proposals
   topics      file/llm    drop      score    updates/*         gate       merge by hand
                           untraceable
```

1. **Signal** — topics + frontier probes in `data/watchlist.json`; local `inbox.jsonl`; optional LLM discovery.
2. **Audit** — drop anything without a url or stable external id (`unverified` is dropped, not downgraded — M0.1/M4); dedupe in-run and against the existing corpus.
3. **Mutation-proposal** — write ranked accepted candidates to `updates/queue.jsonl` and a bilingual `updates/REPORT.md`; append one line to `updates/JOURNAL.md`.
4. **Journal / human gate** — a human runs `harness refresh-apply --accept <id|url|index>`; only then are merge stubs written to `updates/proposals/`. The catalogs are touched **by hand**, in a separate commit.

## Ways to feed it · 如何投喂候选

- **File inbox (offline, deterministic).** Put candidate JSON lines in `updates/inbox.jsonl`:
  ```json
  {"title": "...", "url": "https://...", "external_id": "2601.00001", "kind": "paper", "topics": ["agent-memory"], "published": "2026-01-05", "summary": "..."}
  ```
- **LLM discovery (opt-in).** Configure `HARNESS_LLM_BASE_URL` / `HARNESS_LLM_API_KEY` / `HARNESS_LLM_MODEL`; `--provider llm` asks the model for recent primary sources. Output is untrusted and always audited.

## Commands · 命令

```bash
# collect + score, write nothing
harness refresh --root . --dry-run

# one real cycle (writes updates/)
harness refresh --root . --provider auto --verify

# human gate: accept queued items (by index, external id, or url)
harness refresh-apply --root . --accept 0 2601.12345 https://arxiv.org/abs/2601.54321
```

## Scheduling · 定期执行

Pick one; keep cadence aligned with `watchlist.json` `"cadence": "weekly"`.

**Windows Task Scheduler** (weekly):
```powershell
$action  = New-ScheduledTaskAction -Execute "pwsh" `
    -Argument "-NoProfile -File `"$PWD\refresh.ps1`" -Root `"$PWD`""
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
Register-ScheduledTask -TaskName "harness-refresh" -Action $action -Trigger $trigger
```

**cron** (weekly, Mondays 09:00):
```
0 9 * * 1  cd /path/to/harness_factory && PYTHONPATH=src python -m harness_factory refresh --root .
```

**GitHub Actions** (`.github/workflows/refresh.yml`):
```yaml
on:
  schedule: [{ cron: "0 9 * * 1" }]
  workflow_dispatch: {}
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m harness_factory refresh --root . --provider file
        env: { PYTHONPATH: src }
      - run: git diff --quiet || echo "review updates/REPORT.md"
```

> Scheduling runs the **observe** half only. Merging into the catalogs stays a
> human, reviewed step (M0.8). Never let a cron job push content changes.
> 定时任务只跑「观察」半步；写入正文永远由人工复核（M0.8）。

## What "hot" and "gap" mean · 热点与缺口的定义

- **Hot topic** — a topic JSON-tagged by many *accepted* candidates this cycle (frequency), biased by recency in `audit()` scoring.
- **Coverage gap** — a declared watchlist topic with **zero** accepted candidates this cycle. Gaps drive the next cycle's probes and are the cue to extend `domains.json` / `watchlist.json` (boundary expansion).
- **Frontier probes** — deliberately adjacent queries (sandboxing, computer-use, world models, …) so the boundary keeps widening rather than confirming itself.

## Guardrails · 护栏

- **Provenance gate (M4):** no url/id → dropped, not "probably fine".
- **Observe-only (M0.4):** the loop writes reports and proposals; it never authors catalog content.
- **Human gate (M0.8):** `refresh-apply` only writes stubs; the human edits the catalogs.
- **Reversible (M0.9):** everything lands in `updates/`; delete the folder to undo a cycle. `JOURNAL.md` is append-only.

## Intel + self-evolution (P1.7) - ?????? + ??

Two more observe-only loops sit alongside `refresh`, both human-gated and reversible:

- **`harness intel`** - pulls the RSS/Atom feeds in `data/sources.json` (labs, vendor harnesses, venues, people, self-media), scores relevance, and writes `updates/INTEL.md` + `updates/intel.jsonl`. Briefs are verbatim excerpts unless an LLM is configured (`llm.summarize`). YouTube `@handle` pages are resolved to channel feeds.
- **`harness evolve`** - the structural loop: **snapshot -> audit -> mutation-proposal -> journal**. Audits topic coverage, empty source groups, and stale entities; writes `updates/EVOLUTION.md` + `updates/evolution.jsonl`, and appends a metric snapshot to `updates/metrics.jsonl` (cadence/drift is observable - M0.5/M0.10).
- **`harness evolve-apply --accept <id|target>`** - human gate; writes `updates/accepted.json` only, never the catalogs (M0.8/M0.9).

`refresh --provider all --intel` runs file + tracked feeds + (LLM if configured) in one pass.
