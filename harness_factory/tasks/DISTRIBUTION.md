# DISTRIBUTION · 打包与工具形态评估

**Updated:** 2026-10-12 · **Status:** accepted & implemented · **Owner:** user + agent
**Related:** `tasks/PLAN.md` · `introduction.md` · `tasks/REFRESH.md`

> **Decision (locked 2026-10-12):** primary form = **installable package via `uv tool install`**;
> cross-project state = **user data dir**; channel = **git-only first**; names = pkg `harness-factory`,
> cmd **`harness`**. §5 checklist implemented (see §7).

> Question: **what form should `harness-factory` take** so it can be used across *many* tasks
> and projects — frequently **outside this repository** — with little friction?
> 问题：这个工具应做成什么形态，好在**不同任务、不同项目**（常常**不在本仓库目录下**）里低摩擦使用？

---

## 中文速览

**结论（推荐）。** 做成**可安装的 Python 包**，用 **`uv tool install`**（本机已装 uv 0.12.7）装成全局的隔离命令 `harness`，在**任意目录**可用；开发期用 `uv run` / 可编辑安装；再保留一个**零安装 zipapp（`.pyz`）** 作为离线兜底；**MCP server** 作为后续可选项（让 agent 直接调用）。

**但真正决定「能否跨项目」的不是打包方式，而是**：把工具的**知识库/状态**与**被生成的目标项目**解耦。现状 `harness init --out` 已经能写到任意目录 ✓，但 `refresh` 仍假定知识库在 `<root>/review` 并把产物写到 `<root>/updates`——把「工具自己的 KB」和「目标项目」混在了一起。需要引入**用户级数据目录 + 配置文件**。

**待你拍板的点**：包名与发布渠道（仅 git / 上 PyPI）、命名（`harness` 命令是否太通用）、是否要 SQLite 事件库、是否现在就做 MCP。

---

## 1. Requirements · 需求

From the user (2026-10-12), the tool must:

1. Work for **different tasks** and **different projects** (multiple, ongoing).
2. Be usable when the **current working directory is not** this repo.
3. Be distributable / installable with low friction, ideally one command.
4. Stay **cost-sensitive / local-first** (AGENTS.md): open-source, no mandatory paid API, runs on local Win11 CPU.

Non-requirements (for now): a GUI, a hosted service, multi-tenant auth.

---

## 2. The crux: two different "roots" · 关键：两种「根目录」

Most of the cross-project difficulty is a **conflation of two locations**:

| # | Location | What it is | Who writes it |
|---|---|---|---|
| **A** | **Tool / knowledge base** | the modules+domains+watchlist catalogs and the *tool's own* `review/` corpus that `refresh` updates | the tool, in **user space** |
| **B** | **Target project** | the directory a generated harness is emitted into | the user, via `--out` |

Today:
- `harness init --out DIR` — already correct: writes **B** anywhere on disk. ✅
- `harness refresh --root R` — reads corpus from `R/review/*` and writes `R/updates/*`. This is fine **when the tool is a checkout of this repo**, but wrong for a globally-installed tool used elsewhere: the KB must not live inside an arbitrary target project. ⚠️

**Therefore the packaging decision is necessary but not sufficient.** Any installable form must also:
- resolve catalogs from a **user data dir** (seeded from package data on first run),
- keep `refresh` writing to that **user data dir**, not to the CWD,
- keep `init` writing to `--out` (any project).

This is the single most important change for "not always in the current project directory".

---

## 3. Options evaluated · 形态选项

| # | Form | Install | Isolation | Any-dir | Offline | Deps | Update path | Agent-callable | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **A** | Source checkout + editable venv (`uv sync` / `pip install -e .`) | manual | venv | yes (activate) | yes | stdlib | `git pull` | indirect | **Dev only** |
| **B** | **Installable wheel, global via `uv tool install` / `pipx`** | one cmd | isolated | **yes (global `harness`)** | yes | stdlib | `uv tool upgrade` | indirect | **Recommended primary** |
| **C** | **zipapp `.pyz`** (stdlib `zipapp`) | copy 1 file | none | yes (`python harness.pyz`) | yes | stdlib | re-download | indirect | **Offline escape hatch** |
| **D** | PyInstaller single binary | per-OS build | none | yes | yes | bundled | re-download | indirect | Later, if no-Python users |
| **E** | Docker image | `docker pull` | container | via mount | if pulled | docker | `docker pull` | indirect | Overkill now |
| **F** | **MCP server** (stdio) exposing `derive/init/check/refresh` as tools | config line | process | yes | yes | stdlib/`mcp` | with B/C | **yes (native)** | **Recommended later** |
| **G** | Editor/agent plugin (VS Code, opencode) | marketplace | host | yes | host | host | host | yes | Only if demand |

**Why B is the primary.** `uv` is already installed (0.12.7), so `uv tool install <path-or-git>` gives a **global, isolated, single `harness` command** with no dependency on any project's venv — exactly "usable in any directory". The package is already PEP 621 + src-layout with `[project.scripts]`, so it is wheel-ready today. `pip` alone would work too (`pip install --user`), but uv is present and cleaner.

**Why C is worth keeping.** A `harness.pyz` produced by `python -m zipapp src` (with `data/` and `templates/` bundled as package data) runs on any machine with Python and **no install at all** — good for air-gapped boxes and for "just try it". Templates/catalogs are already loaded relative to `__file__`, so they survive packaging.

**Why F is the natural second front.** The whole point is agent harnesses; exposing the compiler as **MCP tools** lets an agent call `harness init` mid-task. It is a thin wrapper over the existing API and should come *after* B lands.

**Not doing now:** Docker (E) and a native binary (D) add maintenance for little gain while the audience runs Python locally.

---

## 4. Recommended target architecture · 目标架构

```
                    user data dir  (A: tool KB + state)          target project(s)  (B)
   ┌───────────────────────────────────────────────┐      ┌──────────────────────────────┐
   │ %LOCALAPPDATA%\harness-factory\   (Windows)    │      │ <project>/.harness/…          │
   │ ~/.local/share/harness-factory/    (Linux)     │      │ <project>/AGENTS.md           │
   │   config.toml        modules.json domains.json │      │ <project>/tasks/…             │
   │   catalog/  watchlist.json                     │      │                               │
   │   corpus/   review/*            ← refresh writes here  └──────────────────────────────┘
   │   updates/  REPORT · queue · JOURNAL · proposals        ▲
   └───────────────────────────────────────────────┘        │  harness init --out <project>
                    ▲                                       │
                    │ seed from bundled package data        │
   install (B):  uv tool install  →  global `harness`  ───────┘
```

**Config resolution order** (first wins):

```
CLI flags  >  ENV (HARNESS_HOME / HARNESS_DATA_DIR / HARNESS_LLM_*)  >  ./harness.toml  >  user config.toml  >  packaged defaults
```

**New/changed CLI surface (proposal):**

```bash
harness init --task "…" [-o DIR]           # B: default DIR = ./<slug> or CWD; unchanged behavior
harness derive/explain/check …             # unchanged
harness refresh [--data-dir DIR] [--corpus DIR] [--verify] [--dry-run]
                                           # A: writes to user data dir by default, NOT CWD
harness doctor                             # NEW: show resolved data dir, config, versions, LLM status
harness self-update                        # NEW: upgrade the tool KB (seed/merge packaged defaults)
```

Only `refresh` changes semantics materially (from `<root>/review` → user data dir). `init`/`derive`/`check` remain project-agnostic already.

---

## 5. Concrete changes to make it so · 落地改动清单

1. **Config + paths module** (`config.py`): resolve `HARNESS_HOME`; platform default (`%LOCALAPPDATA%` / XDG); load `config.toml`; expose `data_dir()`, `corpus_dir()`, `updates_dir()`. Replace the current single `HARNESS_DATA_DIR` env in `registry.py`.
2. **First-run seeding**: if the user data dir is empty, copy packaged `data/*.json` + a `corpus/` skeleton from package data.
3. **Split `refresh` roots**: `--data-dir` (KB, default user dir) vs. existing corpus concept; stop defaulting corpus to `Path.cwd()/review`.
4. **`harness doctor`**: print resolved paths + `llm.available()` + version; makes "where did it put things?" obvious.
5. **`harness self-update`**: re-seed/merge packaged catalogs without clobbering user edits (3-way or "keep user, add new keys"), journaled.
6. **Packaging polish**: classifiers, `readme`, `[project.urls]`; confirm `package-data` ships `data/*.json` + `templates/*` in the wheel; add `python -m zipapp` build script.
7. **MCP server** (later): `harness-mcp` exposing `derive`, `init`, `check`, `refresh` as tools.

None of this blocks current usage (checkout + `PYTHONPATH=src`), it just makes global/other-project use first-class.

---

## 6. Decision record · 待决策

**Recommendation:** adopt **B (uv tool) as primary**, keep **A (editable) for dev**, ship **C (zipapp) as offline fallback**, schedule **F (MCP) next**.

Open questions for the user:

| # | Question | Options | Default suggestion |
|---|---|---|---|
| Q1 | Distribution channel | git-only / PyPI public / PyPI private index | **git-only first**, PyPI later |
| Q2 | Package & command name | `harness-factory` / other; command `harness` vs `hf` vs `harness-factory` | package `harness-factory`, command **`harness`** (short; note it is generic) |
| Q3 | Cross-project state | user data dir (recommended) / per-project `.harness/` / both | **user data dir for KB**, per-project for emitted files |
| Q4 | Event store | flat JSONL (now) / SQLite ledger | **JSONL now**, revisit at P3 |
| Q5 | MCP now or later | now / after B | **after B** |

Pick answers to Q1–Q5 and I will implement the §5 checklist (starting with `config.py` + `doctor` + `refresh` re-rooting), keeping everything reversible.

---

## 7. Implementation (done 2026-10-12) · 已落地

Decisions taken (user): **B primary (uv tool)**, **user data dir for KB**, **git-only first**, **pkg `harness-factory` / cmd `harness`**, implement now.

Delivered:

- `src/harness_factory/config.py` — resolves the tool home: `HARNESS_HOME` → platform default (`%LOCALAPPDATA%\harness-factory` / XDG) ; optional `config.toml`; `catalog_dir()`, `corpus_dir()`, `updates_dir()`, `seed_catalog()`, `ensure_home()`, `resolve_corpus_root()`.
- `registry.py` — catalog lookup order is now `HARNESS_DATA_DIR` → user catalog (if seeded) → bundled data.
- `refresh.py` — corpus resolved via `config.resolve_corpus_root()`: a checkout's `review/` if present, else the home `corpus/`. `refresh` CLI **defaults to the user home**, not the CWD; `--root`/`--data-dir` override.
- CLI additions — **`harness doctor`** (resolved paths, config, seed status, LLM status) and **`harness self-update`** (re-seed the tool catalog from packaged defaults; `--force` to overwrite; non-destructive by default, journaled).
- `init --out` now defaults to `./<task-slug>` (still project-agnostic).
- `refresh.ps1` no longer forces the repo root (defaults to home; pass `-Root .` for a checkout).
- `.gitignore`: `harness_factory/_archive/` and `harness_factory/updates/` excluded from version control.
- Tests: +7 (`test_config.py`); suite now **35** passing.

Still open (deferred): publish to PyPI, zipapp build script, MCP server (§3 options C/F), SQLite event store (Q4).

Landed path semantics:

```
tool home  (A, user space)  : %LOCALAPPDATA%\harness-factory\   catalog/ · corpus/ · updates/
target project (B, any dir) : <out>/  AGENTS.md · tasks/ · .harness/   (via harness init)
```

---

## 8. Re-evaluation (2026-10-12): packaging **cancelled** as a channel · 打包方向取消

**User feedback:** the package route "确实感觉用起来不太方便" — installing a global command and keeping a
user-space KB is ceremony that does not match how the tool is actually wanted: point a vibe-coding
assistant at the repo path + the task goal, and let it configure the harness.

**Decision (locked 2026-10-12):** **cancel packaging as a distribution channel.**
- ❌ PyPI publishing, `uv tool install` / `pipx`, and `zipapp`/binary/MCP packaging are **dropped from the roadmap**.
- ✅ Primary consumption is **agent-native (L0) + CLI-from-path (L1)**:
  - **L0:** `SKILL.md` + `core/` + `data/*.json` read directly by the assistant; `harness skill` prints the load-index.
  - **L1:** run without installing: `PYTHONPATH=<repo>/src python -m harness_factory <cmd>` (or `./refresh.ps1`).

**What is kept (no cost, still useful):**
- `pyproject.toml` stays only as a **dev/CI convenience** (editable install, `uv run`, `[project.scripts]`); it is
  **not** a publish target and needs no versioning/channel policy.
- `config.py` / `HARNESS_HOME` / `doctor` / `self-update` remain **optional**: path mode is primary, the user-space
  KB is a convenience for running many refreshes outside the repo. Nothing is deleted (reversible, M0.9).

**Rationale.** The asset is the knowledge + rules, not the executable. Agent-native consumption removes install
friction, works for any assistant (Claude Code / opencode / Cursor / …), and lets the assistant reason beyond the
fixed rule table — while L1 keeps a deterministic, reproducible path when one is needed. The trade-off
(non-determinism at L0) is mitigated by the provenance contract (`.harness/PROVENANCE.md`) and the `check` gate.

**Supersedes:** §3 (options B/C/F) and §5.6 packaging-polish as *distribution* goals; those items are retained only
as optional dev tooling.

