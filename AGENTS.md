# AGENTS.md — research_foodie workspace principles

> 工作区原则 · Workspace principles for AI coding assistants and contributors.

**Updated:** 2026-11-02

> **This file is test-pinned.** `harness_factory/tests/test_docs_integrity.py` (`CountDriftGuardTest`) and
> `tests/test_standing_reference.py` (`QuickStartFidelityTest`) parse `AGENTS.md` and fail if the domain count,
> the test count, the `Test gate` line (must name `PYTHONPATH=src`), or the standing-reference blockquote in
> section 7 loses a required unit. After editing this file, run the suite before claiming done.

## 1. 语言政策 / Language policy

- **中英双语 / English and Chinese are both primary.** Default docs are English with a `> 中文速览` block or a
  mirrored `## 中文` section for design docs; code, configs and identifiers stay English.
- Preserve existing Chinese text as-is; translations must be faithful, not jargon-stuffed.

## 2. 仓库地图 / Repository map

```
harness_factory/          项目主体 —— agent harness 模式库 + `harness` CLI（入口见根 README）
  SKILL.md                agent-native entry (cardinal rules + load-index + output contract) — authoritative
  GUIDE.md                full guide + 10 worked examples (bilingual)
  introduction.md         what it is · mental model · quickstart
  CAPABILITIES.md         GENERATED — `harness capabilities --write` (do not hand-edit)
  HARNESS-MAP.md          GENERATED — `harness map --write` (do not hand-edit)
  core/                   cross-domain invariants M0–M8 (`01-meta-principles.md` first)
  domains/                34 学科 + general 兜底 (10 faculties; includes `writing/`)
  review/                 surveys · harness catalog/index · references.md/bib
  sources/                source-map.md (pattern ← primary source)
  reference/              capability-router · requirement-refinement · capability-flow · derivation-rules
                          · evidence-instruments · methodology-map · outlet-map · cross-language
                          · capability-cycle · tool-router
  src/harness_factory/    tool source + data/*.json (SSOT) + templates/
  tests/                  stdlib unittest (no external deps)
  tasks/                  PLAN · PROGRESS · REFRESH · DISTRIBUTION · ASSESSMENT · BATTERY
  updates/                cycle output (proposals/intel/evolution/cases) — gitignored, never hand-authored truth
  _archive/               archived legacy material — gitignored, do not revive
AGENTS.md                  本文件 · workspace principles (test-pinned)
README.md / README.zh-CN.md  project entry (English / 中文)
.github/workflows/ci.yml    the real gate definition (tests → cycle audit → CLI smoke → init/check/gate e2e)
```

## 3. Setup and commands

- Python ≥ 3.10; core CLI and tests have **zero external dependencies** (pytest/ruff/mypy are optional extras).
- No install needed (L2 packaging is cancelled as a distribution channel). Run from `harness_factory/`:
  `PYTHONPATH=src python -m harness_factory <cmd>` — bash alias: `alias harness='PYTHONPATH=src python -m harness_factory'`.
  From the repo root use `PYTHONPATH=harness_factory/src …`.
- Main commands: `derive`, `init --out <dir>`, `check --dir`, `gate --dir`, `harvest`, `profile`, `learn`,
  `standard`, `catalog`, `cycle audit`, `evolve`, `full-update`, `scoreboard`, `brief`, `classify`, `battery`,
  `collect`, `trace-audit`, `doctor`, `plugins --validate`, `skill`, `capabilities`, `map`.
- Everything is offline except `refresh` / `intel` (RSS/YouTube) and the optional `HARNESS_LLM_*` classifier.
- Two roots: tool home in user space (`%LOCALAPPDATA%\harness-factory`, override `HARNESS_HOME`) vs each target
  project's emitted files. In path mode the home is optional.

## 4. Quality gates

- **Test gate:** `PYTHONPATH=src python -m unittest discover -s tests` from `harness_factory/`
  (当前 **434** 用例; the number is parsed from this line by `CountDriftGuardTest`, so update it when the suite changes).
- Single test: `PYTHONPATH=src python -m unittest tests.test_docs_integrity.CountDriftGuardTest -v`.
- Changing `src/harness_factory/data/*.json` (the SSOT) requires `harness catalog --write` to regenerate
  `CAPABILITIES.md` + `HARNESS-MAP.md`, then the full suite; the same drift guards will fail otherwise.
- CI (`.github/workflows/ci.yml`) runs the suite on ubuntu+windows / py3.10+3.12, then `cycle audit`, a CLI smoke,
  and an `init → check → gate → harvest → doctor → plugins --validate` e2e. Reproduce those steps for risky changes.
- **引用即生命线 / Citations are the lifeline.** Every factual claim traces to a primary source (arXiv ID / DOI /
  official repo / docs page) with an access date; otherwise mark it *unverified*. Dates explicit: `as of <date>`.
  Pricing and leaderboard numbers are directional and sourced.
- Generated docs, emitted harness files, and `AGENTS.md` all carry structural guards (balanced code fences, no
  unfilled `{{ }}`, resolvable relative links, no raw assistant/tool markup). Don't paste tool-call traces into docs.

## 5. Conventions

- File names lowercase, `-` separated; ATX headings, language-tagged fences, tables for comparisons; docs carry
  `Updated: <date>`.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`docs(guide): …`).
- **Auto-commit allowed for daily doc/code delivery; never push** unless the user explicitly asks.
- Prefer editing existing files; no new docs unless they serve a plan, tracking, or a deliverable.
- **Proposals only.** `refresh`, `evolve`, `trace-audit`, `full-update` write proposals under `updates/`.
  Never edit `data|core|domains|templates` directly to "close" a finding — accept through the human gate.
- **Generalization rule.** A pattern earns a place only if it survives removal of its originating project; concrete
  details are labelled *Exemplar*, never the definition.
- Plan-first: multi-step work goes into `harness_factory/tasks/PLAN.md`, results/corrections into
  `harness_factory/tasks/PROGRESS.md`.

## 6. Session-end discipline (easy to miss)

- Record the session's structured facts instead of remembering them:
  `PYTHONPATH=harness_factory/src python -m harness_factory harvest --dir <project> --event human_correction --detail '{…}'`
  and `--event task_outcome --detail '{"judge":"human","score":<n>,"rubric":"<domain>"}'` (the human judges; the
  machine only records — M0.4). Then `collect --project <project>` and `trace-audit` (proposal-only).
- User standing directives: primary sources first; explore beyond the stated scope for research tasks; survey
  available MCP servers/skills/APIs first per `reference/tool-router.md`; cost-sensitive (free/local first).
- "全面更新 harness" / "full update" ⇒ `harness full-update` (intel → probe-domains → trace-audit → evolve →
  cycle audit → scoreboard), all output as proposals in `updates/FULL-UPDATE.md`.

## 7. 给 agent 的指令词：先配置，再提任务 / Directive for an agent: configure first, then task

**Step 1 · 常驻引用（贴一次，整段对话有效；写进项目规则文件可跨对话与子体）。** 权威版本见 `harness_factory/SKILL.md`
§"PASTE THIS EXACT INSTRUCTION"（含"停止使用"的撤销方式）；一句话版：

> 「**常驻引用（直到我说「停止使用 harness_factory」撤销）**：把本仓库当 harness 能力参考。**先替换路径参数**：
> `<HF>` = 本仓库克隆后 `harness_factory/` 目录的真实路径（如 `~/src/research_foodie/harness_factory`）。先读 `<HF>/SKILL.md`，按
> `<HF>/reference/capability-router.md` 路由、只加载命中行点名的文件；需求模糊/偏小时先跑
> `<HF>/reference/requirement-refinement.md`（R0–R5，等我确认）。**每次实质回答前先查有无适用能力；用了就声明用了
> 哪个能力、哪个文件。** 推导 harness 时产出 `AGENTS.md` + `tasks/*` + `.harness/*`（含 `.harness/capabilities.local.md`），
> 最后跑 `harness check --dir <产物目录>`（未安装时用 `PYTHONPATH=<HF>/src python -m harness_factory check --dir <产物目录>`）；
> 本地能力留在任务里，通用模式**只以提案**回流 `updates/`（不直接改
> `data|core|domains|templates`）。**不编造任务内容（M0.4）；真实与可溯源优先于速度（M0.1/M0.2）；不可逆动作须我明确同意。**
> **除非我说「停止使用 harness_factory」，一直沿用。**」

**Step 2 · 任务（同一轮接着写，或下一轮再发均可）。** 直接写目标，或直接附上文件/目录/链接，例如：
「为现有 Python 项目补全类型注解与单元测试，保证可验证闭环。」

Deriving a harness emits only `AGENTS.md`, `tasks/PLAN.md`, `tasks/PROGRESS.md`, `.harness/*` (incl.
`capabilities.local.md`, `manifest.json`, `PROVENANCE.md`); verify with `harness check --dir <out>` (or
`PYTHONPATH=<HF>/src …`). L0 = agent reads the docs; L1 = the CLI.
