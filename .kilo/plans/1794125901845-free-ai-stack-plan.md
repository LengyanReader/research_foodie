# Plan: `resources/free-ai-stack/` — Free LLM API / Coding Agent / Vibe Coding IDE Catalog

**Status:** implementation-ready (pending switch to implementation-capable agent)  
**Updated:** 2026-11-08  
**Scope:** New, standalone resource directory at repo root (parallel to `harness_factory/`). No changes to `harness_factory` SSOT, generated files, or tests.

## Goal & Deliverable
Create `resources/free-ai-stack/` containing a maintainable, source-cited catalog of **free-usable** resources across three categories (Kilo explicitly included): (1) Free LLM APIs / inference endpoints, (2) Coding agents, (3) Vibe coding IDEs / AI-native editors. Bilingual-friendly structure (EN primary, concise 中文速览 where helpful); identifiers/links in English.

## Decisions (confirmed)
- **Location:** `resources/free-ai-stack/` (repo root, parallel to `harness_factory/`).
- **Files:** `README.md` (index + inclusion standard + maintenance), `llm-apis.md`, `coding-agents.md`, `vibe-coding-ides.md`.
- **Inclusion tiers (A/B/C, uniform across categories):**
  - **A — $0 sustainable:** permanent free tier / ongoing free quota / free self-host path; currently obtainable; **primary source** (official site/pricing/docs) required.
  - **B — Trial/credits (widened):** signup credits, one-time credits, time-limited free trial currently obtainable; state one-time/expiry/trigger + post-trial billing path; primary source preferred, else `unverified`.
  - **C — Watch/unverified (appendix):** promos/rumors/insufficient source/status unknown; **not a usable recommendation**; list separately with `unverified` reason and `as of`.
- **Presentation:** Main lists show **A/B**; **C in a separate appendix** per file.
- **Provenance discipline (M4-aligned):** No fabricated claims/quotas. Every entry has source link(s) + `as of 2026-11-08`. Unverifiable → `unverified` (never presented as fact). Record limits (quota/rate, card/region/account, ToS/abuse risk).

## Entry Schema (tables)
Columns (adapt minimally per category): `Name` | `Tier (A/B/C)` | `What’s free` | `Limits / requirements (quota, rate, card, region, account)` | `Models/notes (APIs) or key capability (agents/IDEs)` | `Primary source` | `As of` | `Status (verified/unverified)`.

## Affected Boundaries
- **Creates (new):** `resources/free-ai-stack/README.md`, `resources/free-ai-stack/llm-apis.md`, `resources/free-ai-stack/coding-agents.md`, `resources/free-ai-stack/vibe-coding-ides.md`.
- **Reads (reference only):** `AGENTS.md` (conventions/provenance), `harness_factory/core/05-provenance-and-integrity.md`, `harness_factory/domains/deep-research/*` (method; not copied), existing tool landscape notes under `harness_factory/review/` if relevant.
- **Must not touch:** `harness_factory/src/**`, `harness_factory/data/*.json`, generated `CAPABILITIES.md`/`HARNESS-MAP.md`/`docs/index.html`, `harness_factory/tests/**`, `AGENTS.md` (test-pinned) — out of scope.

## Data Flow (research → catalog)
1. **Seed candidates** per category from authoritative aggregators/directories *as discovery only* (resolve each to producer/official page before citing) + known exemplars (include **Kilo** in IDEs/agent context with its free path tiered and sourced).
2. **Verify against primary sources** (official pricing/docs/product pages). Capture exact free offer, limits, and access date. Use `webfetch`/`websearch` (network allowed for content gathering during implementation).
3. **Normalize & tier** into A/B/C; deduplicate (same product across categories cross-linked, not duplicated as fact).
4. **Write markdown tables** + short per-category notes; add C appendix.
5. **Index** in `README.md` with scope, tier definitions, schema, maintenance procedure, and changelog stub.

## Risks & Mitigations
| Risk | Mitigation |
|---|---|
| Free tiers change fast / regional variance | `as of` date on every row; state region/account/card conditions; “verify before use” note. |
| Aggregator claims treated as fact | Aggregators = discovery only; cite producer primary source (M4). |
| Kilo/competitor details mis-stated | Source from official Kilo properties only; mark `unverified` if not confirmable. |
| “Free” ambiguity (self-host cost) | Tier A includes self-host path but note infra/API-key costs where applicable. |
| Legal/ToS constraints | Note “subject to provider ToS”; no guidance to evade limits. |

## Validation (Definition of Done)
- [ ] Directory and 4 files exist at `resources/free-ai-stack/`.
- [ ] `README.md` documents A/B/C tiers, schema, discovery≠citation rule, and maintenance.
- [ ] Each category has A/B main table + C appendix (empty appendix allowed but section present) and includes **Kilo** in the relevant file with a sourced, tiered entry.
- [ ] Every row has `Primary source` + `As of 2026-11-08` + `Status`; no unsourced quota numbers; unverifiable rows marked `unverified` and placed appropriately.
- [ ] No edits under `harness_factory/` SSOT/data/tests; no generated artifacts modified.
- [ ] Markdown renders cleanly (tables/headings); links are absolute and resolvable at authoring time.

## Rollout / Maintenance
- Treat as a living snapshot: re-verify `access/as of` on a cadence; move defunct/changed offers between tiers or to C (retire-in-place, don’t silently delete facts). Future updates can follow `harness_factory/reference/tool-router.md` discover→evaluate→register→metabolize pattern (optional).

## Open Questions
None (location and A/B/C tiering confirmed). Out of scope unless requested: automation/scripts, adding to `harness_factory/data/sources.json` as tracked entities, or CI checks for this directory.
