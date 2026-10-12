# Domain · Knowledge Management · 知识管理域
> Wiring `core/` modules into a coverage-mapped, source-ledgered knowledge base.
> 把 `core/` 模块接线成「覆盖度地图 + 来源台账」的知识库。
**Updated:** 2026-10-12

---

## 中文速览
知识管理域回答：**我覆盖了什么、缺了什么、每个判断的依据在哪。** 它把 `core/` 组合成「覆盖度地图（coverage map）+ 来源台账（source ledger）+ 门禁」：用 **M0.5** 保证一个事实只有一处权威；用 **M4** 让每条判断可溯源；用 **M0.3/M3** 设「何时可发布」的门；用 **M7** 记录变更。产物是**结构化的、可被下游检索与审计**的知识，而不是一堆散落笔记。来源：`huayan_collection/harness/{coverage-map,sources,compliance,rules}.md`、`workflows/*`。

---

## What this domain is for · 用途
Maintain a knowledge base you can *trust at a glance*: every entry sourced, every gap visible, every change reviewable. Combines **coverage mapping** (what topics are covered / missing), **source ledgers** (provenance per claim), and **gates** (when content is fit to publish).

## Module combination · 模块组合
- **M0.5 (SSOT).** One canonical entry per fact/concept; everything else links to it. Duplicates become a *Consolidate* mutation (M5).
- **M4 (provenance).** Each entry carries source + access date; `verified`/`unverified`/`disputed` status; quote vs inference separated.
- **M3 (gates).** Publication gate: coverage threshold met, sources resolved, no open `unverified` on load-bearing claims.
- **M1 (context).** Retrieval returns the matching entry, not the whole base; index-first.
- **M7 (governance).** Changes are diffs; ledgers append-only; no silent overwrite.
- **M5 (evolution).** Recurring gaps (a topic always missing) become *Register/Promote* signals.

## Patterns · 模式
1. **Coverage map.** A single table: area → status (covered / partial / missing) → owner → next action. Drives what to fill.
2. **Source ledger.** Claim → source → access date → status. Append-only; corrections are new rows.
3. **Gap-driven intake.** Only acquire material where the coverage map shows a gap (avoids hoarding).
4. **Concept canonicalization.** One page per concept; aliases redirect. Prevents the same idea living in five notes.
5. **Publication gate.** A topic may be published only when its load-bearing claims are `verified` and its coverage is above threshold.

## Anti-patterns
- Duplicate concept pages drifting apart (M0.5).
- Un-sourced assertions in the base (M4).
- Publishing while gaps or `unverified` flags remain (M3).
- Retrieval dumping the whole base (M1).

## See also
`../core/05-provenance-and-integrity.md` (M4) · `../core/08-change-governance.md` (M7) · `../sources/source-map.md` (knowledge-management row) · `C:\DA_Practice\huayan_collection\harness\`.
