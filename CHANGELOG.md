# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Fixed
- **Housekeeping - hand-maintained counts now guarded.** The workspace `AGENTS.md` claimed **27** domains and **242** tests
  while the SSOT carries **31** (30 disciplines + `general`, 10 faculties) and the suite ran **284**; its bare
  `python -m unittest discover -s tests` command also fails without `PYTHONPATH=src` (CI has always set it). Fixed: both
  README layout trees re-grouped to the real faculties and completed (statistics / geometry-topology / logic under formal
  sciences; digital-humanities / writing / reading under humanities; data-science / model-selection under engineering),
  the references range refreshed R1-R106 → R1-R251, and a new `CountDriftGuardTest` (5 guards) makes these counts fail CI
  instead of drifting: the AGENTS.md/README counts must equal the `domains.json` SSOT, the layout trees must name every
  domain, the test count must equal the discovered suite, and the gate command must name `PYTHONPATH=src`.
- **References backlog cleared.** `review/references.bib` gains the 12 missing entries (R237-R242, R246-R251; R243-R245
  were already present), so the machine-readable bib covers R1-R251 again.
- **Line endings.** The two legacy CRLF files (`domains/model-selection/README.md`, `tasks/REFRESH.md`) are normalized to LF.
- **Counts.** **284 → 289 tests** (+5 guards). `cycle audit`: 0 hard, 0 gaps.

### Added
- **Environment resilience & brief pipeline (P33).** `doctor` command hardened against restricted permissions
  and read-only sandbox environments (captures `OSError`/`PermissionError`, reports friendly status and hints
  for `$env:HARNESS_HOME`, avoids crashes on diagnostic calls, M0.4 compliant). Closed the brief-to-init pipeline
  via `harness init --from-brief <brief.md|brief.json>`, which reads refined goal/domain from the confirmed brief,
  derives the plan, and emits `.harness/BRIEF.md` directly into the generated harness. 5 new tests; **349 -> 354 tests**.
- **Task-brief round (P32) - `harness brief` renders a paste-ready execution draft.** The second capability-evaluation
  gap closed: one step from goal to an executable brief. `brief.py` renders the requirement-refinement fields the rules
  can compute (R0 restate · R2 hard/soft/assumed tiers · R3's three offerings with mechanical deltas — MVP / Elevated /
  Exploratory naming P31's intersections), the 8-axis feature vector with reasons, the module/capability plan, the
  domain workflow, first-phase actions (first workflow step + PLAN skeleton + declared evidence instrument +
  self-check), the gates, and an explicit R4/R5 confirm block — the brief is a **draft to confirm, never a licence to
  start** (WAIT rule, M0.4). CLI: `harness brief --task … [--out FILE] [--json]`. `tests/test_brief.py` 6 guards;
  scoreboard addition deliberately declined (same pipeline already pinned). **343 → 349 tests**; `cycle audit` 28 cycles, 0 hard, 0 gaps.
- **Intersection round (P31) - discipline overlaps declared, near domains named, unions united.** Disciplines overlap;
  single-domain routing silently dropped the other half. Three layers: (1) **32 domains declare `overlaps`** (adjacent
  domain → one-line discriminator note, e.g. digital-humanities↔history: encoding work vs historical interpretation;
  history gains the 修纂 signal so the tie is real); (2) **derive reports `secondary_domains`** when a
  declared-overlap neighbour scores ≥1 and is close or strong (≥2), at most two, each with its discriminator note;
  (3) a neighbour scoring ≥2 **contributes its domain-keyed capabilities to the plan union** (re-run of the existing
  matcher with the alternate domain — nothing invented, M0.4). The emitted AGENTS.md gains a "Secondary domains ·
  交叉域" stanza. Two self-introduced bugs caught by the guards: the secondary scorer skipped lowercasing (sentence-
  initial "Bayesian" escaped the word-initial match) and the scoring refactor changed tie-breaks to alphabetical
  (restored to stable registry order — the French battery case caught it). `tests/test_overlaps.py` 7 guards incl.
  the 8-sample routing battery. **336 → 343 tests**; `cycle audit` 27 cycles, 0 hard, 0 gaps.
- **One-instruction round (P30) - `harness full-update` chains the whole observe loop.** Saying 「全面更新 harness」 now
  triggers everything: `full_update.py` chains intel (networked, `--offline` skips) → probe-domains → trace-audit →
  evolve → cycle audit → scoreboard, each phase failure-isolated (a failing phase reports and the rest still run —
  never faked, M0.3), ending in one bilingual report `updates/FULL-UPDATE.md` with the human-gate line (M0.4/M0.8).
  Wired for the phrase: SKILL.md step 8 (the L0 six-phase procedure), a capability-router row for the situation, the
  README quickstart line, the workspace AGENTS.md standing-reference addendum, and refresh.ps1 now runs refresh +
  `full-update --offline`. No new clauses/capabilities/domains — it is composition of existing mechanisms (M0.5).
  **334 → 336 tests**; `cycle audit` 26 cycles, 0 hard, 0 gaps.
- **Interdisciplinary & frontier round (P29) - the audit and the automated finder.** 12 interdisciplinary/frontier
  tasks classified empirically (2026-10-23), four verdicts: composition (most are work-type combinations already
  covered - M0.5), signal fixes (2 real misroutes: bioinformatics `pipeline` → devops, interpretability `circuit` →
  devops; biology +3 signals, earth-environment +3), one landed frontier domain **`ai-safety`** (safety properties →
  capability measurement → red-team records → claim-by-claim safety case → M3.16 disclosure self-audit → residual
  risk declared; 6-dim rubric; 33 → **34 disciplines**), and three deferrals with triggers (interpretability ·
  embodied · systems-science). The second ask got a mechanism: **`harness probe-domains`** clusters collected intel
  that lands on `general` into disjoint keyword proposals (nearest existing domain named = cheapest signal fix),
  written to `updates/DOMAIN-PROBES.md` only (M0.4/M0.8) — the factory can now *find* the unmentioned domains itself:
  refresh/intel pulls known topics, probe-domains finds unknown clusters, evolve audits catalog health, humans decide.
  `review/interdisciplinary-frontier-domains-2026-10.md`; `tests/test_domain_probe.py` 4 guards.
  **330 → 334 tests**; `cycle audit` 25 cycles, 0 hard, 0 gaps.
- **Integration round (P28) - registry cross-link audit, two real catalog gaps, scan proposal.** The 15
  tracked-entities-without-same-id question resolved definitively: the cross-link is one-directional and fully
  consistent (71/71 `tracked` values resolve across groups); the reverse direction had 5 unreferenced entities —
  3 recorded exemptions with reasons, and **2 real gaps closed**: `mistral-agents` (Mistral's agents API — the
  catalog's smolagents is Hugging Face's, not Mistral's) and `hermit-cashapp` (Cash App's hermetic toolchain — the
  catalog's `hermit` is the Oxford reasoner, a different project). Catalog 203 → **205**; `RegistryBidirectionalTest`
  (2 guards) pins the bidirectional consistency. The ecosystem scan (AGENTS.md standard · ACP · LangMem · AgentOps ·
  skills registries · computer-use · D7/D8) is proposed in `updates/` (observe half, P20 method). **328 → 330 tests**;
  `cycle audit` 24 cycles, 0 hard, 0 gaps.
- **Breadth round (P27) - basic disciplines and schools of thought.** The user's directive (梳理基础学科与重要思想/学术流派).
  Three slices, criteria-first: (1) **3 domains landed** — `history` (source criticism, periodization declared, silences
  weighed), `philosophy` (argument reconstruction, position declaration, counterexample honesty), `political-science`
  (concept definition, method declaration, case-selection honesty) — each with workflow, bilingual signals, README and
  a weighted rubric; entry-doc counts 30 → **33 disciplines** (guard-enforced). (2) **methodology-map "Schools of
  thought" table, 16 rows** — hermeneutics (Gadamer) · phenomenology (Husserl) · analytic (Frege/Wittgenstein) ·
  pragmatism (Peirce/James) · critical theory (Horkheimer/Adorno) · structuralism (Saussure/Foucault) · positivism
  (Popper/Kuhn) · grounded theory (Glaser & Strauss) · ethnography (Malinowski/Geertz) · classical sociology
  (Durkheim/Weber) · economics schools (Smith/Marshall/Keynes) · behavioral (Kahneman & Tversky) · behaviorism→cognitive
  (Watson/Miller) · psychodynamic (Freud) · math foundations (Hilbert/Russell/Brouwer) · Chinese classical exegesis
  (朱熹/顾炎武/戴震: 训诂先于义理) — each with bibliographic canonical source, its demands, and who enforces it.
  (3) **7 outlets** (digital-humanities + cognitive-science) with real reachability results (2 verified, 5 honestly
  flagged; Europeana merged, not duplicated); `topic_ids` registry extended. Deferred with triggers: astronomy /
  materials / neuroscience / anthropology / geography. `review/basic-disciplines-schools-2026-10.md`.
  **326 → 328 tests**; `cycle audit` 23 cycles, 0 hard, 0 gaps.
- **Depth round (P26) - M6/M7/M8 gain anchorable clauses.** The clause distribution was asymmetric (M3/M4 carry 15
  numbered clauses, M6/M7/M8 zero or one), so `cycle audit` had nothing to audit on three modules. Four clauses landed,
  each numbering an existing prose rule and anchored in an already-verified source (zero new references): **M6.10**
  skills as versioned reusable methods, index-first progressive disclosure (Agent Skills open standard, tracked,
  verified 2026-10-15) · **M6.11** exposure is not authorization; a sandbox claim names its backend (R241/R242) ·
  **M7.10** every governing change is a reviewable attributable diff with a rollback path (Conventional Commits spec +
  R90) · **M8.11** handoff passes through artifacts, not memory (R93). Each with a checklist line, a source-map row and
  a content-presence guard (`P26ClauseAnchorTest`). **322 → 326 tests**; `cycle audit` 22 cycles, **39 clauses anchored**, 0 hard, 0 gaps.
- **Trace-audit round (P25 · D1 stage B) - the rules auditor turns recorded traces into proposals.** The missing half of
  the automation puzzle: `data/trace-rules.json` (five rules: gate-miss-repeat · capability-unused-repeat ·
  re-derive-repeat · correction-focus · low-outcome — the P24 effect axis feeding back) + `trace_audit.py` group traces
  by pattern and emit M5.3-vocabulary proposals to `updates/traces-proposals.jsonl` + `TRACE-EVOLUTION.md` only —
  never touching `data|core|domains|templates` (M0.4/M0.8). `low-outcome` counts only numeric scores at or below the
  threshold; grade strings stay human territory. CLI: `harness trace-audit` (offline). D1's revisit trigger now points
  at stage C (measured promotion). No clauses or capabilities; `tests/test_trace_audit.py` 7 guards.
  **315 → 322 tests**; `cycle audit` 21 cycles, 0 hard, 0 gaps.
- **Scoring round (P23) - a minimal scored task set for the factory's own harness.** Closes P16.9's revisit trigger
  and gives `component-ablation` (M5.12) a holdout, and D1 stage C its dependency. `data/scoreboard.json` +
  `scoreboard.py`: 5 canonical tasks (lit-review / unit-tests / kg-dh / deep-research / model-choice) scored on five
  deterministic axes (routing · capability coverage · module coverage · structural check · clean emission); all
  allowed/must values were taken from an actual classify+derive run on 2026-10-23 (M0.4), and the 1.0 baseline per
  task is pinned by `tests/test_scoreboard.py`, so a score move is a deliberate edit, never a silent drift. CLI:
  `harness scoreboard [--task ID] [--json]` (offline). Non-goals: not a task-quality benchmark, not a per-domain
  rubric (that is `harness standard`), no automatic promotion. **302 → 305 tests**; `cycle audit` 19 cycles, 0 hard, 0 gaps.
- **Trace round (P22 · D1a) - trace schema + collection for trace-driven self-evolution.** Stage A of the accepted D1
  design doc (`updates/2026-10-23-trace-driven-evolution-design.md`), before any auditor or promotion: new `trace.py`
  implements the schema (v1 JSONL, six-event vocabulary, required fields, append-only, legacy lines read back as
  `signal`); a failed `gate` run appends a `gate_miss` line to the tool home (passed runs record nothing — traces are
  facts, M0.4); `harvest --event/--detail` writes structured events; new CLI `harness collect --project DIR` pulls a
  project's local traces (offline, human-run); the emitted AGENTS.md template carries the optional trace contract.
  Stages B (rules auditor) / C (measured promotion, waits on the scored task set) / D (LLM-assisted) stay deferred.
  No clauses or capabilities; `tests/test_trace.py` 13 guards. **289 → 302 tests**; `cycle audit` 18 cycles, 0 hard, 0 gaps.
- **Docs round (P21) - dogfooding M4.15 on the entry docs.** The queue's dogfood candidate, opened on the project
  evaluation's readability flag. Method: per-section reader tasks + the four-defect search + SSOT cross-check over
  README.md / introduction.md / GUIDE.md / SKILL.md. 10 findings, 10 fixed: 5 caught by M4.15 (incl. the bare-`harness`
  quickstarts — an unstated precondition now that L2 packaging is cancelled, so a new user's first command failed; the
  M0.4 first-use gloss; introduction's 5-vs-30 domains self-contradiction; SKILL.md's Python 3.11+ floor corrected to
  3.10+ per pyproject/CI) and 5 outside it (cross-doc drift: stale counts and dates, the missing `outlets` group in the
  sources enumeration, introduction §10's duplicated roadmap compressed to a pointer). No new clause or capability:
  `cross-doc-consistency` cannot discriminate (revisit trigger recorded in `review/dogfood-m415-2026-10.md`); M4.17
  operability stays unexercised. Registered as P21 (0 capabilities / 0 domains / 0 clauses / 0 references); tests
  unchanged at **289**; `cycle audit` 17 cycles, 0 hard, 0 gaps.
- **Scan round (P20) - harness disclosure · MCP 2026-07-28 · two fired revisit triggers.** A round first proposed by a
  whole-web scan (`review/harness-landscape-scan-2026-10.md`) and applied as P20 after user approval (renumbered: P18/P19
  were already registered 2026-10-20). All three shrink conditions were checked against the primary texts and none fired.
  - **Disclosure - clause M3.16 (`core/04`)** (`review/harness-disclosure-2026-10.md`, §W R243-R251). A comparison that ranks
    agents across models or harnesses is incomplete unless both arms carry the seven-layer **ETCSOVG** card (Execution ·
    Tools · Context · Scheduling · Observation · Verification · Governance) and a variance statement; admissible protocols
    are **locked-harness** (vary the model) or **factorial** (η²_p paired with ω²/bootstrap and ranking-reversal counts).
    Full read of arXiv:2605.23950: HV̄/MV̄ ≈ 7.80× on one controlled 3×3 grid, 6/9 ranking reversals - the authors
    disclaim generality, so the figures are carried as directional. No new capability: the clause keys on the *claim
    type*, not a feature vector, and mirrors `component-ablation` (M5.12) - ablation removes parts *within* a harness,
    disclosure names the configuration *across* comparisons.
  - **AST10 cue closed (data-only).** OWASP AST10 v1.0 (R245, README read in full) targets the skills-execution layer -
    update drift, missing scans, supply chain at 1,184-malicious-skills scale - and is judged **not** a duplicate of the
    ingested ASI01-10 (R86). The `levers.json` security note and `portable-skills` / `untrusted-content-discipline` now
    cite it; the obligations themselves stay with M8.4/M3.11.
  - **MCP 2026-07-28 core revision digested.** Four mappings land in `review/workflow-patterns-2026-10.md` §9 with an
    explicit "no invariants changed": MRTR `input_required` = the human gate as a protocol-recorded state (M8); the
    Tasks extension = native convergence for `durable-execution` (M2); list cache hints = a `context-budget-policy` row;
    the 12-month deprecation window = an M7 exemplar. The `mcp` catalog entry is remapped M1,M6 → M1,M6,M2,M8.
  - **Numbers refreshed, all *listed*-marked.** METR 1.1 (~1.1 h, ~105-day doubling as of 2026-09, R249) refreshes the
    long-horizon-autonomy argument; Claude Code Agent Teams (R250) and A2A under the Linux Foundation (R251) stay
    pointer lines. Context-editing/memory is answered as reference parameters on `context-budget-policy` -
    `platform.claude.com` remains region-blocked, so the mechanism line rests on R237 alone.
  - **Counts.** R242 → **R251** (3 full reads, 6 *listed*) · 34 → **35** clauses · 38 capabilities and 196 catalog entries
    unchanged. **284 tests** (279 + 5 P20 guards). `cycle audit`: 16 cycles, 0 hard, 0 gaps. Deferred with triggers:
    agent-judge robustness (D7), A2A / peer-session re-audit after full texts (D8).
- **Model round (P19) - the models are the variable; what the Big Three disclosures changed for harnesses.** Primary
  vendor posts read (`review/model-families-2026-10.md`, §V R239-R242); with `openai.com` and `platform.claude.com/docs`
  blocked, OpenAI stays a documentation line - its model names are recorded only as named in the other two vendors'
  comparison tables, never as product facts.
  - Five converged mechanisms, three of which break defaults: effort tiers are priced goods (a cross-tier comparison is a
    settings comparison); the served model may differ from the requested one (silent re-routing, alias drift); history may
    be non-rewritable (preserved thinking); the workspace/sandbox is a product-level contract (manifest ≠ live workspace ≠
    snapshot); exposed ≠ authorized (toggles govern visibility; authorization lives inside the tool).
  - **Clauses.** **M1.11** (`core/02`) non-rewritable history compresses append-only - summaries write state, the original
    stays reachable. **M2.13** (`core/03`) effort is a budget row recorded with the model id, cache pricing in the same
    account. **M4.17** (`core/05`) the served model is part of provenance - requested id, served id and version, tier,
    substitution with reason; an evaluation whose model changed silently is not a measurement. M6 deepens without a new
    clause (two checklists, two anti-patterns: *exposure-as-authorization*, *"sandbox" as an adjective*).
  - **One capability added.** `model-portfolio-discipline` (fires only on `domain=model-selection`): requirements matrix →
    per-stage composition → measure on your own held-out set at the declared tier → hard gate with id/version/tier logged;
    ties go to the cheaper tier, tier changes reopen the evaluation. The router had to be fixed too - explicit selection
    cues must override neighbouring defaults (the P18 rule) or the capability was unreachable.
  - **Counts.** 37 → **38** capabilities · 31 → **34** clauses · R238 → **R242** · **279 tests** (+8). 32-family routing
    baseline still 32/32. Six non-additions recorded with revisit triggers (vendor citation APIs, computer-use detail,
    fast mode, CCL case, provider routing, 1M-context guidance).
- **Routing-completeness audit (P18) - can any task locate its capabilities?** No clauses, no capabilities: the round
  audits the compiler itself (`review/routing-coverage-2026-10.md`), splitting the claim into three testable ones -
  **totals** (does any task fall to the floor?), **discrimination** (do different tasks get different sets?),
  **correctness** (is the classification right?) - over 32 hand-written task families (16 zh / 16 en, two empty prompts
  included), per-value flips across eight axes, constructive satisfiability for all 37 capabilities, and a bidirectional
  router check.
  - Totals hold (32/32 produce a plan; every capability satisfiable and named by the router). Discrimination mostly - two
    real holes (`artifact=plan`, `domain=arts-design` with `grounding=off`) recorded with revisit triggers instead of
    forced fills. Correctness **failed first**: 9/32 misrouted for three reproducible root causes - substring false hits
    (`ci` ∈ "exercises", `eval` ∈ "retrieval", which inflated RAG tasks' capability counts), missing signals for common
    families, and the `artifact`/`grounding` axes never reading text.
  - **Fixes** (no module-rule changes): signals move to **word-initial** matching; 84 high-precision signals added across
    six domains, three wrong keys dropped; **explicit cues beat domain defaults** (artifact nouns → the axis;
    cite/provenance asks → `grounding=required`; only an explicit "no external knowledge" downgrades - a fake off is worse
    than a fake preferred). Post-fix: 32/32 land in allowed sets; the RAG set drops 18 → 15 (it was never
    high-verifiability). A latent DSL mismatch (`_cond_matches` early-return vs its printed AND) was fixed alongside.
  - **Counts.** **271 tests** (263 + 8 guards, data-driven, naming no specific capability) · capabilities/clauses/refs
    unchanged (37 · 31 · R238) · `cycle audit` 0 hard, 0 gaps.
- **Domain-criteria round (P17) - four cases read in full, two criteria overturned, a working set that can exit.**
  Closed P14.4 by scoring four domain harnesses against criteria **written before reading** (schema-before-extraction ·
  entity identity · evidence-bounded output with coverage reporting), plus meta-criterion C4: a criterion that scores the
  same value on every case is not discriminating. Four of six pre-registered predictions were overturned, all in one
  direction: full texts look better than abstracts, and binary criteria had been flattering them. C3a scored 1 on all
  four cases → rewritten as a three-rung ladder (prompt request → resolvable per-sentence keys → mechanism-enforced
  against the active evidence set): the bit-count was wrong, not the criterion.
  - **Clauses.** **M3.15** (`core/04`) attribute losses stage by stage - one end-to-end number cannot say whether to fix
    retrieval or generation; the first stage's denominator holds all samples and any scoring convention that inflates a
    stage must be declared. **M4.16** (`core/05`) a pointer is an assertion of a support relation - dangling / stale /
    unsupported each check differently; resolution runs against the **active** set; pointers land on the original text, not
    its summary; "accurate but miscited" is reported apart from "inaccurate". **M1.10** (`core/02`) the working set is
    rented, not owned - re-check at phase boundaries, evict with `{reason, reload_when}` receipts, always-on baselines are
    never evicted, and eviction without the index still in context is forgetting, not release; enforced by a
    `.harness/working-set.json` gate in `harness check`.
  - **Sources.** §T **R237** (Anthropic context-editing / memory post - vendor-reported numbers marked as such; the
    `docs.claude.com` pair is region-blocked, so no claim rests on it) and §U **R238** (PaperQA2, read in full). The
    candidate pool was resolved to primary arXiv ids before reading (GraphRAG 2404.16130v2 · LongHarness 2610.13075v1 ·
    PaperQA2 2409.13740v2); the two HTR papers were deliberately excluded rather than "re-writing their exam for them".
  - **A trigger gap fixed on the way.** `evidence-bounded-generation` never fired for *research + document artifact +
    grounding-required* (the PaperQA2 shape); `grounding: required` was added - deliberately not `preferred`.
  - **Counts.** 28 → **31** clauses · R236 → **R238** · capabilities unchanged at 37 · **263 tests** (242 + 21). No new
    capability for working-set eviction: its `when` is strictly contained in `context-budget-policy`, so M1.10 deepens it
    instead (the P16 precedent).
- **Expression round (P16) - form before words · translation as expression · a module that earns its place.** One round,
  five slices, and the first where the two headline papers were read **in full** rather than at abstract level.
  - **Expression design - clause M4.15 (`core/05`) + capability `expression-design`**
    (`review/expression-design-2026-10.md`, §R R219-R233). The content unit and the reader's task select the form:
    four reader needs > four documents (tutorial / how-to / reference / explanation), and a section must serve one.
    "What needs explanation" becomes a search (undefined term at first use, unstated precondition, unexplained jump, rule
    with no worked example). The modality ladder runs prose > list > table > diagram > chart > notation > animation >
    sound, climbed only as far as the relation requires, preferring the rung whose **source of truth is reviewable** -
    so for video the script is the artefact of record. A form change may change what the reader can check but **never
    what is claimed** (M4.10), hence the text spine (caption with claim, data, unit, caveat + alt text). Instruments
    `mermaid` (+ kind `diagramming`) and `vega-lite` (+ kind `visualization-grammar`).
  - **Translation as expression.** The 1898 preface that states 信·達·雅 (R233) was read as a **primary text**, not from
    a secondary account: 「不斤斤於字比句次，而意義則不倍本文」 carries the licence and its limit in one sentence, and
    一名之立，旬月踟躕 makes a coined term a logged decision. Modern evidence makes the trade-off measurable: fluency and
    faithfulness are **negatively correlated** over 130,486 paragraphs in 16 source languages (R229), sentence alignment
    is unrealistic for literary text (R230), and quality is reported as MQM error categories (R224) rather than "fluent".
  - **Context-adaptive polish - M4.14 deepened, no new capability.** Audience, register and channel are declared
    **before** writing and re-checked per section (`review/language-polish-2026-10.md` §3.1); an undeclared audience
    silently becomes "whoever is writing", which is the register failure the gate exists to catch.
  - **Ablation - clause M5.12 (`core/06`) + capability `component-ablation`** (`review/harness-ablation-2026-10.md`,
    §S R234-R236). Retention is not causal contribution and neither is deployed utility (R234); the procedure that
    separates them ablates one coupled functional unit at a time against the **per-task median over ablations**, reports
    performance and cost as two axes with paired tests, protects the set at alpha = 0.05, and evaluates the ladder on a
    held-out set as a Pareto frontier. Recorded against the obvious reading: removing a unit can **raise** cost, one
    harness in the study is a counter-example to "harnesses are redundant", and an all-pruned baseline that still scores
    is a statement about **task coverage**.
  - **Sources graded, and a second-hand piece demoted.** The WeChat article is an accurate explainer of the same SHaRP
    paper and is still **not a source**: it dropped the 24-of-27 cliff to 14.44%, the PaperQA2 counter-example, and the
    reading of the all-pruned baseline. It is a retrieval pointer only; §1 of the ablation doc records the omissions.
  - **Counts.** 35 > **37** capabilities · 26 > **28** clauses · 68 > **70** instruments (25 > 27 kinds) · R218 > **R236**
    (no new outlets). **242 tests** (237 + 5 guards). `cycle audit`: 0 hard, 0 gaps. Five non-additions recorded with
    revisit triggers (`modality` axis, genre templates, automated pruner, redundancy ratio, `harness-pruning` domain).
- **Depth round (P15) - KG canon · training boundary · scholarly channels · language polish · self-model.** Five
  surveys, two new invariants and the first round to *state what the library does not cover*.
  - **Knowledge graphs (`review/knowledge-graph-patterns-2026-10.md`, §N R155-R170).** A layered stack (data model >
    schema > vocabulary > constraints > query > provenance > reasoning) with the failure mode named - *layer confusion* -
    the classic method narrowed to **competency questions first** (Ontology Development 101; METHONTOLOGY/NeOn/OntoClean
    named but not re-read), and "knowledge feature" split into four different things: embeddings *rank*, GNNs *learn
    structure*, reasoners *decide*, OBDA *maps*. Frontier (generative construction, GraphRAG, agentic maintenance) did not
    repeal **identity** or **evidence**. Instruments `hermit`, `elk` (entailment can be refuted, not asserted).
  - **Training (`review/training-methodology-coverage-2026-10.md`, §O R171-R191).** Every family graded *in axis /
    adjacent / out of scope* against a stated criterion. Verdict: the stack is surveyed, the library covers the
    **boundary**. A `training-*` capability is refused because the feature vector cannot distinguish "train" from "use",
    so it would be a predicate the engine silently ignores (M5.10); recorded with a revisit trigger.
  - **Channels (`review/scholarly-channels-2026-10.md`, +20 outlets).** ~95 channels with observed statuses,
    first-party-vs-aggregator marks and seven no-laundering rules; OpenAIRE, DataCite, ROR, BASE, Connected Papers,
    ResearchRabbit, OpenReview, PubPeer, SciELO, Redalyc, HAL, CiNii, J-STAGE, CNKI, Wanfang, EThOS, PMLR, SpringerLink,
    Cambridge Core, PLOS. No duplicate ids: Semantic Scholar/Crossref/CORE/scite live in `tools`, OpenAlex in `projects`,
    AI/ML venue indices in `venues` - surfaced in prose, not re-registered.
  - **Language polish - clause M4.14 (`core/05`) + capability `prose-polish`** (`review/language-polish-2026-10.md`, §P
    R192-R200). A gate separate from truth: a machine may **reject** (declared house style, term consistency, punctuation
    per GB/T 15834-2011) and only a reader may **approve**; a readability score is a drift alarm, never a pass mark.
    Chinese failure modes named (欧化句式/翻译腔, 四字格堆砌, 的的不休, 全半角混用, 繁简不等价). Instruments `vale`,
    `languagetool`, `textstat` (+ kinds `prose-linter`, `readability-metric`).
  - **Self-model - clause M5.11 (`core/06`) + capability `gap-seeking`** (`review/self-model-and-gap-seeking-2026-10.md`,
    §Q R201-R218). Self-report is testimony; an external check is evidence. Three artefacts: an evidence-backed
    self-model, a two-halved gap register, and one **disconfirming** check per round. Exploration is bounded (holdout,
    budget, stop condition) and novelty is not value.
  - **Counts.** 33 > **35** capabilities · 24 > **26** clauses · 63 > **68** instruments (23 > 25 kinds) · 75 > **95**
    outlets · R154 > **R218**. **237 tests** (233 + 4 guards). `cycle audit`: 0 hard, 0 gaps.
- **Knowledge engineering & digital humanities (P14)** - the ask was a *class*: how to build, maintain,
  manage and evolve a knowledge base / graph / ontology, and what digital-humanities work adds. Grounded in
  a **full primary-source read** (关书朋 · 何宇佳 · 张英聘, 《文献与数据学报》 **8(3): 56–72**, Sep 2026, open
  publisher PDF; the printed DOI does **not** resolve and is recorded as printed-only) crosswalked against
  **normative first-party standards** (RDF 1.1, OWL 2, SKOS, SHACL, PROV-O, CIDOC-CRM, IIIF, DCMI Terms,
  Getty TGN, EAD3, TEI P5 → **§M, R136–R154**). The 11-mechanism crosswalk found **9 covered / 1 partial /
  2 real gaps**, so the round landed **4 clauses** — **M3.14** (a gate trades *precision*, not coverage:
  report recall beside precision — the case moves relation precision 88.79% → 97.67% while recall moves only
  83.05% → 83.42%), **M4.11** (ontology as a contract: types, relation directions and identity rules declared
  *before* extraction; an untypeable candidate is a defect to record), **M4.12** (one canonical identity per
  entity: aliases recorded, authorities reused, undecidable merges escalated to a human — never averaged),
  **M4.13** (bound the answer by the evidence: every named assertion carries a pointer, and "the sources are
  silent" is a complete answer) — **4 capabilities** (`ontology-as-contract`, `entity-resolution`,
  `evidence-bounded-generation`, `schema-evolution`) with router + provenance rows and guard tests, the
  **`digital-humanities` domain** (31st; faculty `humanities`, artifact `dataset`) with its weighted rubric,
  **13 `instruments` under 6 new kinds** (ontology toolkits, graph stores, KG construction, entity
  resolution, gazetteers, HTR), and **7 outlets** for standards/authorities. **Deliberate non-additions
  recorded:** no KG-retrieval capability, no `knowledge-engineering` domain, and **no `encoding-standard`
  instrument kind** — TEI/CIDOC/Dublin Core/EAD3/IIIF are norms, so they stay references. Crosswalk +
  verdicts: `review/knowledge-and-dh-crosswalk-2026-10.md`; domain: `domains/digital-humanities/README.md`.
- **P12 closeout — two negative results kept honest** — the 22 `verified: false` outlets were re-checked with
  a browser UA: **3 answered** (NOAA, APA PsycNet, CourtListener) and were flipped, while **19 remain
  host-blocked** and stay `verified: false` with their reason (the re-check is done; the flags are the
  result). The roundup's 17 uncited figures were cleared against the papers' own HTML: **16 confirmed
  verbatim**, **2 readings corrected in kind** (the 4.1×–39× range is the *TQ-cost gain* column, and
  41.1→53.3 is the **avg@5** metric), and **1 stays `unverified`** because `2610.20563` has no reachable
  HTML full text. A bounded 8-week backfill (Pass A) mapped 90 papers → 68 (75.6%); the archive carries no
  top-pick labels, so **Pass B is not worth its cost yet**.
- **Agent-harness frontier sourcing pass (group §L)** — the Oct 12–18 *Top AI Papers of the Week*
  roundup was entered through **primary records, not summaries**: nine arXiv preprints (R127–R135 in
  `review/references.md` §L + `references.bib`) recorded at **abstract level only** — one batched arXiv
  `id_list` query, id · title · authors · date agree in every case, zero phantom entries — with the
  roundup's own numbers and institutional attributions left **`[unverified]`** instead of carried across.
  Seven `sources/source-map.md` rows map them to **existing** capabilities (no new capability, no new
  clause); one item (LoGRA, `arXiv:2610.06647v2`) is recorded as **considered and declined** rather than
  listed. Same pass: the tracked entity `nlpnews` was repointed off a host this environment blocks
  (`*.substack.com` → the publication's own domain, whose paginated archive API also answers), the outlet
  map gained a retrieval-route rule plus an explicit **non-entry** for aggregator digests, and
  `harness refresh --provider feed` now ingests the feed end-to-end (20/20 accepted, **no new code** —
  the weekly loop rides the existing `refresh` callback). `references.bib`'s stale header count
  (`R1–R79` → `R1–R135`) was corrected in passing.
- **First round driven by the mechanism itself (P12, partial)** — the audit's 12 soft gaps were consumed,
  not restated: router rows for `portable-skills` and `reproducible-experiments` (capabilities that
  existed but were unreachable from the entry table), and `tests/test_capabilities.py::TriggerCoverageTest`
  (10 guards, each pinning a capability's declared trigger *and* the quiet vector it must not fire on).
  `harness cycle audit` now reports **0 hard problems and 0 gaps**.
- **M4.10 worked example** — `reference/cross-language.md` §7 carries a real EN↔ZH pair (the
  standing-reference block) through unit segmentation, a **rejected** first-pass drift hypothesis
  (widening the unit dissolved it), and two **real** defects: units 4 (declare the capability + file) and
  8 (M0.4 · M0.1/M0.2 · irreversible acts) were missing from the compressed Chinese renderings, and
  「只提案、不编造任务内容」 fused two units into a claim the English master does not make. Fixed in
  `AGENTS.md` §6, `GUIDE.md` and `introduction.md`; the master is untouched.
- **Quick-start fidelity gate** — the first sweep fixed "the guides" but missed the **READMEs**, the two
  copies users actually paste; a user pasting the block back exposed it. Both READMEs now carry units 4,
  5 and 8 and name `harness check --dir <output>`. New guard
  `tests/test_standing_reference.py::QuickStartFidelityTest` (5 cases) pins every copy, so this cannot
  silently regress; §7 records the miss and the rule it yields (enumerate renderings from the reader's
  entry points, not the writer's edits).
- **Path parameter in every paste block** — the block assumed the factory sits at `./harness_factory`, but
  the repo is cloned wherever the reader wants it. All eight renderings (`README` ×2, both README
  templates, `AGENTS.md`, `GUIDE.md`, `introduction.md`, `SKILL.md`) now mark the location as a parameter
  to fill — `<HF>` = the real path of the cloned `harness_factory/` directory, e.g.
  `~/src/research_foodie/harness_factory` — and give the no-install check form
  (`PYTHONPATH=<HF>/src python -m harness_factory check --dir <output>`); `check` is no longer named bare.
  The master keeps its own wording (「把 `./harness_factory` 换成真实路径」) and now cross-references `<HF>`,
  so the two conventions are one. `QuickStartFidelityTest` rejects the unmarked `./harness_factory` form.
- **Capability rounds as a mechanism (M5.10)** - new SSOT `data/cycles.json`: 9 recorded rounds
  (`baseline` -> `P13`, git-verified `added` ids), the **definition-of-done as data** (7 axes with
  hard/soft severity) and **11 roadmap items**, each carrying a `reason`, a `revisit_when` trigger and a
  `source`. `cycle.py` + CLI `harness cycle [list|show|audit|roadmap|dod]`: `audit` separates **hard
  problems** (phantom ids, clauses not anchored in their own module, `when` predicates the engine cannot
  evaluate, deferrals without a reason or trigger) from the **soft gap surface** (missing router rows,
  guards, provenance) - the gap list is the next round's worklist. New clause **M5.10** in `core/06`
  (a round is recorded, audited and closed; a deferral is a decision, not an omission); procedure
  `reference/capability-cycle.md`; guard `tests/test_cycle.py` (16 cases).
- **Clause anchoring repair** - `M2.10`, `M2.11`, `M3.10` and `M8.10` were cited across review/router docs
  but never anchored in `core/` (and `M2.11` was mislabelled inside `core/09`); all four are now anchored
  in their own module, and `sources/source-map.md` gained rows for M2.10/M2.11, M3.10-M3.13, M5.10 and
  M8.10.
- **Usage in the README** — the five usage rules (router · evidence instruments · methodology · outlets ·
  cross-language) now live in the root READMEs' *How to use this factory* section, beside the
  one-instruction standing reference and its revocation, so "how to use" is findable without the CLI.
  Guarded: each README must name all five reference docs + the revoke phrase.
- **Cross-language fidelity (M4.10)** — new invariant in `core/05`: when a claim moves into another
  language, align by **meaning unit** (意群 / sense group / *translation unit*), **corroborate** by
  back-translation / a target-language reader / a second-language source, preserve stance·scope·modality·
  entity identity, and **gloss — never silently substitute**. New procedure `reference/cross-language.md`
  (alignment · corroboration · term handling · bilingual deliverables · non-entries); sources R120–R126
  (ISO 17100, ISO 5060, XLIFF 2.2, Halliday & Hasan, Vinay & Darbelnet, Nida & Taber, MQM). No
  `cross-language` capability (no language axis in the feature vector → would not discriminate).
- **Per-field information outlets** — new `outlets` group in `data/sources.json` (**68** curated
  entries: portals · journals · preprint servers · databases/registries · repositories · media) keyed by
  field via 17 new field `topic_ids`, each with `outlet_kind` + `why` + `not_for` + `verified` + `access`;
  new `reference/outlet-map.md` (field → outlet → why / NOT-for). Live view: `harness sources --group
  outlets`; 18 field domains link it. Verification honest: 46 URLs reachable (HEAD/GET 2026-10-19), 22
  blocked (403/405) recorded `verified: false` + note (*listed, not confirmed*).
- **Guards** — `tests/test_docs_integrity.py::LoadIndexWiringTest` (index paths resolve; entry docs link
  the new reference) and `tests/test_sources.py::OutletDataTest` (outlet shape + every field covered).
- **Harness compiler CLI** (`harness`): `derive` / `init` / `explain` / `check` — derive a task's
  feature vector (M0–M8 rules; optional LLM) and emit a runnable harness scaffold.
- **Self-update loop** (M5): `refresh` / `refresh-apply` — collect → audit → rank → proposal → journal,
  with a hard human gate; output under `updates/`.
- **Cross-project packaging**: user-space tool home (`HARNESS_HOME`, platform default), `doctor`,
  `self-update`; installable via `uv tool install`.
- **Intel tracking**: `data/sources.json` (59 entities: labs, vendor harnesses, venues, people,
  self-media) with RSS/Atom + YouTube feed collection → `updates/INTEL.md` / `intel.jsonl`.
- **Self-evolution**: `evolve` / `evolve-apply` — snapshot → audit → mutation-proposal → journal plus
  metrics (`updates/EVOLUTION.md`, `evolution.jsonl`, `metrics.jsonl`); discovery→registry proposals.
- **Run watermark**: effective `since` persisted to `updates/state.json` so cycles only surface new items.
- **Generated overviews**: `CAPABILITIES.md` (per capability) and **`HARNESS-MAP.md`** — the whole
  factory on one page (modules · capabilities · domains · catalog classes · CLI · how to sync), rendered
  from the CLI parser + skill index + `data/*.json` by `harness map --write`; both drift-guarded.
- **Workflow capabilities**: `loop-discipline` + `graph-orchestration` (22 → 24) — the agent-loop
  contract (termination · step budget · per-step ground truth · stall detection) and a declared
  topology (typed state · nodes/edges · fan-out/fan-in · per-node checkpoints); module clauses
  M2.10/M2.11 + M8.10; sources R93–R97.
- **Discipline coverage**: 3 new domains — `logic` (new `formal-sciences` faculty), `linguistics`,
  `cognitive-science` — each with a rubric, plus 3 cross-cutting capabilities `formal-verification`,
  `dimensional-analysis`, `empirical-measurement` sharing one new clause **M3.10** (match the instrument
  to the claim: machine-checked derivation / units & error / effect size & reliability); sources R98–R106.
- **Evidence instruments**: a new catalog class **`instruments`** (13 kinds, **27 entries**, catalog 133 → 160)
  for the tools those capabilities name — proof assistants (Lean 4/mathlib/Rocq/Isabelle/Agda/Dafny), solvers
  and checkers (Z3/cvc5/TLA+/Alloy), units & uncertainty (Pint/uncertainties), chemistry & biology
  (RDKit/Biopython/RCSB PDB/UniProt), language (Universal Dependencies/INCEpTION/ELAN), empirical work
  (PsychoPy/jsPsych/OSF/statsmodels/lme4/Stan) and pipelines (Snakemake/Nextflow) — plus
  **`reference/evidence-instruments.md`** (claim type → instrument → catalogued tool → gate evidence, with
  deliberate non-entries) and an **Evidence instrument** stanza in the emitted `AGENTS.md` so every generated
  harness states what would settle its claim; sources R107–R110.
- **Mathematics, statistics & methodology systems (P10)**: 2 new domains — `statistics` and
  `geometry-topology` (faculty `formal-sciences`) — with rubrics; 2 new capabilities
  `statistical-inference` (frame · convergence · interval) and `certified-computation`
  (exact/certified + independent re-derivation), grounded in the new clauses **M3.11**/**M3.12**;
  **23 new `instruments`** rows (catalog 160 → 183; kinds 46 → 50 — computer-algebra-system, sat-solver,
  geometry-topology-toolkit, causal-inference-toolkit) covering SageMath/Singular/Macaulay2/GAP/PARI-GP/OSCAR/SymPy,
  CaDiCaL, mathcomp/Metamath, CGAL/GUDHI/Regina/SnapPy/polymake, R/PyMC/NumPyro/ArviZ/brms/R-INLA/emcee and
  DoWhy; the **methodology layer** — `reference/methodology-map.md` (field → methodology system → what the
  harness must enforce) plus clause **M3.13** (declare the method and its assumptions; *no* `methodology-fit`
  capability, by design); and the scope roadmap `review/integration-map-2026-10.md`; sources R111–R119.
- **Pattern library**: `core/` (M0–M8), `domains/` (research/knowledge-management/data-science/devops),
  `review/` (survey, catalog, playbooks, references), `sources/` (provenance map).
- CI (GitHub Actions), `CHANGELOG.md`, `.gitattributes`.

### Changed
- **A closed roadmap item records `done_in`, not a revisit trigger** — a `done` entry is no longer a
  deferral, so `cycle.audit()` now requires `reason` + `revisit_when` only while the item is open and
  `done_in` once it ships; `harness cycle roadmap` renders `done in …`.

### Fixed
- **Pointer coverage (P11.1)** — `.harness/pointer.json` hard-coded only **4** entry docs, so an emitted
  harness could not reach `derivation-rules`, `evidence-instruments`, `methodology-map`, `cross-language`
  or `outlet-map` by pointer alone. `pointer.ENTRY_DOCS` is now **derived from the skill index**
  (the `overview` + `reference` groups; 4 → 12 docs) so it can never drift from `harness skill`, and
  `pointer.verify` checks them all (plus the emitted `AGENTS.md` pointer block states the full set).
- **Doc link integrity** — new guard: every relative markdown link in a shipped doc must resolve
  (an audit found 0 broken before the guard was added).

[Unreleased]: https://github.com/LengyanReader/research_foodie/commits/main
