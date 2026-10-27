# Self-modifying harnesses, digest-ingested · 自改造 harness 一轮：周报摄取实录

> What a weekly papers digest can and cannot justify: two clauses (M3.17, M5.13) landed from abstract-verified
> primary sources, and an explicit ledger of what stayed *unverified*.
> 一份周论文精选能支撑什么、不能支撑什么：两条子句（M3.17、M5.13）落在摘要级一手核实上，其余主张明列「未验证」台账。
**Updated:** 2026-10-27 · Round P34 · Evidence level: **abstract-verified** (0 full reads)

---

## 0. What came in, and through what door

The input was the DAIR.AI "Top AI Papers of the Week" X article (`x.com/dair_ai/status/2109270464962916674`,
published 2026-10-11, ten items with arXiv links). Per the no-laundering rule (AGENTS.md §3; the WeChat digest
precedent, `harness-ablation-2026-10.md` §1), **the digest is discovery only** — every claim was re-verified
against the arXiv abstract page, and the digest's own commentary is admitted to the library nowhere except as a
pointer (R262). The account itself is now tracked as media `dair-ai-x` in `data/sources.json` alongside its
newsletter form (`nlpnews`). Direct `x.com` fetch is blocked from this environment; the readable receipt is the
fxtwitter API mirror (`api.fxtwitter.com/dair_ai/status/2109270464962916674`, fetched 2026-10-27).

## 1. Method and grading — where this round sits on the evidence ladder

| # | Item (ref) | arXiv | Submitted | License | Verification |
|---|---|---|---|---|---|
| 1 | Harness Learning (R252) | 2609.35738v1 | 2026-09-28 | CC BY 4.0 | **Abstract read in full** |
| 2 | CorpusMap (R253) | 2609.37226v1 | 2026-09-29 | arXiv non-exclusive | **Abstract read in full** |
| 3 | VeriHarness (R254) | 2610.00972v1 | 2026-10-01 | CC BY 4.0 | **Abstract read in full** |
| 4 | HERMES / Dev-Primitives (R255) | 2610.07832v1 | 2026-10-06 | CC BY 4.0 | **Abstract read in full** |
| 5 | VERA (R256) | 2610.05923v1 | 2026-10-05 | **CC BY-NC-SA 4.0** | **Abstract read in full** |
| 6 | MASS (R257) | 2610.12176v1 | 2026-10-08 | CC BY 4.0 | **Abstract read in full** |
| 7 | Sharpening Tax (R258) | 2610.01509v1 | 2026-10-01 | CC BY 4.0 | **Abstract read in full** |
| 8 | Agent Plasticity (R259) | 2610.08902v1 | 2026-10-06 | arXiv non-exclusive | **Abstract read in full** |
| 9 | CMM (R260) | 2610.07907v1 | 2026-10-06 | CC BY 4.0 | **Abstract read in full** (out of scope) |
| 10 | MIMESIS (R261) | 2610.09484v2 | 2026-10-07/08 | CC0 1.0 | **Abstract read in full** (out of scope) |

**Full texts were not reachable from this environment.** Seven attempts across `arxiv.org/html/*` and `ar5iv`
all failed to parse (context-deadline / cancellation), and the Semantic Scholar API returned HTTP 429; abs
pages themselves succeeded only on spaced retries. So this round is graded, honestly, **abstract-verified** —
the same posture as the P12 precedent ("no reachable HTML full text and stays unverified"). A **full-text
reread trigger** is registered as roadmap item P34.R1: any upgrade of these items to *full-read* status
(checking method sections, ablations and the claims in §4 below) reopens the two landed clauses for revision.
Nothing in `core/` states a body-only number as fact; both clauses cite `[R###] (abstract-level)`.

## 2. What landed — two clauses, each discrimination-tested

**M3.17 · Agreement is not verification** (`core/04-verification-and-gates.md`). Basis: R254's first-party
abstract — repeated sampling yields rollouts with *complementary* correct claims; "disagreement often exposes
correct alternatives, while consensus can conceal errors"; a disagreement resolver checks competing claims
against **environmental evidence**, a consensus challenger searches for **omitted requirements**; evidence-backed
revision adds 6.2/6.4 points over a single rollout on two frontier models (five long-horizon workspace
benchmarks). Discrimination: `core/04` ended at M3.16; M3.14 (gates buy precision, not coverage) covers a *gate*
filtering candidates, M3.17 covers a *vote* electing among duplicates — complementary, not restating; M5.11's
passing aside "sampling agreement is a cheap router signal, not a verdict `[R207]`" is sharpened from a
budgeting remark into a gate obligation.

**M5.13 · A self-edit is attributed and gated before acceptance** (`core/06-self-evolution.md`). Basis: R256's
abstract names the mechanism exactly — "a verifier which gates model checkpoints and harness edits using
explicit development-set acceptance criteria… its updates target not only the cause but the outcome". R252
supplies the caution the clause encodes: "the benefits of training on revision sequences vary across settings"
— do not credit a round's edits with prior rounds' momentum. Discrimination: the existing Guardrails line
"No metric, no promotion" stays the principle; M5.13 is its *procedure* for self-edits (criteria before
application, cause-vs-symptom, axis attribution, rejection bound), and it is the acceptance-side twin of M5.12
(retention-side measurement), sharing M5.12's confounding grounding `[R234]` rather than re-deriving it.

## 3. Where the other seven went — mapped, not merged

- **R252 Harness Learning** — the loop M5.13 governs, made trainable: a proposer RL-trained to revise a solver's
  harness from execution feedback, "harness revisions playing the role of weight updates". Recorded as a **stage-C
  precedent under roadmap D1** (trace-driven evolution) — not landed, because it is weight-level training of a
  proposer, outside this library's harness-level scope until the reread.
- **R253 CorpusMap** — entity pages as a cross-query navigation layer; strengthens the existing
  `entity-resolution` capability's *why* (evidence: entity anchors beat 4 alternative navigation layers over 7
  models × 3 benchmarks, fewer tokens on average — abstract-stated). No new clause: the library's KM modules
  already govern the invariant.
- **R255 HERMES** — repository components as agent-native interfaces (artifact + resident LLM), dependency-aware
  activation, bug diagnosis mapped to the component to revise; +12.4% over matched baseline harnesses, a
  Qwen3-8B configuration within 4.5% of a GPT-5.6 Sol one at −26.2% inference cost (abstract-stated). **Name
  collision alert:** this HERMES (arXiv:2610.07832) is *not* the catalogued `hermes-agent` (NousResearch) —
  same trap as P28's "hermit" finding; no catalog merge.
- **R257 MASS** — weight-level RSI (evolutionary workflow search alternating with SFT); per the training-methodology
  boundary (`training-methodology-coverage-2026-10.md`, P15), noted as an **entity**, not ingested into M5.
- **R258 Sharpening Tax** — post-training trades pass@1 gains for pass@K coverage loss; feeds
  `model-portfolio-discipline`'s *why* (choose base+light harness vs post-trained by test-time budget).
- **R259 Agent Plasticity** — experience→held-out-gain efficiency, endpoint vs acquisition divergence; consistent
  with M5.11/M5.12's measurement-first stance; registered for the reread, no clause (its findings are
  benchmark-level, not invariant-level, at abstract grade).
- **R260 CMM** — a recurrent *architecture* with dual matrix memories; deliberately **not included**: model
  internals are outside harness scope (boundary decision, logged in `cycles.json`).
- **R261 MIMESIS** — user-simulator training environments; agent-training substrate, same boundary as R257;
  *why*-refresh only if the reread finds a harness-level invariant.

## 4. What stayed unverified — the digest-body-only ledger

Each claim below appears in the digest's article body but **not** in the corresponding abstract. Per AGENTS.md §3
they are *unverified* and are excluded from every landed document; the reread (P34.R1) decides each one:

1. HERMES "task pass rate 6.5% → 31%" (R255) — the abstract reports +12.4% relative to matched baselines; the
   absolute pair is body-only.
2. VERA's "+5% accept / −20% reject" gate thresholds (R256) — the abstract names acceptance criteria but no thresholds.
3. CorpusMap "+6.4–11.7 points, −34–57% tokens" (R253) — the abstract states direction (better discovery, fewer
   tokens) without magnitudes.
4. Agent Plasticity's named models and the "$1,073 total cost" figure (R259) — absent from the abstract.
5. **All institution attributions** — including the digest crediting CMM to Sakana AI (R260's listed authors are
   affiliated elsewhere as far as the abs page shows; attribution **unverified**, flagged in the earlier assessment).
6. Sharpening Tax and MASS headline numbers beyond what §3 quotes — §3's figures are abstract-side; any
   additional body-side numbers were not carried.

## 5. Roadmap status after this round

- **D7 (agent-judge robustness)**: R254 is on-topic evidence **but at abstract grade**, and D7's revisit trigger
  demands a full-read-grade primary source → stays **deferred**, reason upgraded (no longer "no candidate source").
- **D1 (trace-driven evolution)**: stage-C precedents R252/R256 noted on the entry; still deferred pending reread.
- **P34.R1 (new, deferred)**: full-text rereads of R252–R259 with the §4 ledger as the checklist; the two landed
  clauses carry "abstract-level" hedges that this round may promote or must retract.
- **No new capability, domain, or catalog entry** (M0.5 discipline): all systems are research artifacts without a
  verified public runnable implementation reachable and checked this round (no code-page verification attempted
  beyond abs metadata); landing them would be self-report without an external check (M5.11).

## 6. Licenses and reach — capture hygiene

R256 is **CC BY-NC-SA 4.0** (non-commercial) — any future derivative of its materials inside this factory needs
the license checked *before* reuse, not after. R253 and R259 carry the **arXiv non-exclusive distribution**
license (no blanket CC grant). R261 is **CC0 1.0**. R260's notes show a NeurIPS 2026 workshop context (PALM).
R254's abstract promises release of a ~26,000-rollout pool (> $100k compute, abstract-stated) — the pool is the
most useful artifact of the set for this library's scored-task work (`scored-task-set-2026-10.md`); retrieval of
the actual data release belongs to P34.R1.

---

## See also

`../core/04-verification-and-gates.md` (M3.17) · `../core/06-self-evolution.md` (M5.13) ·
`./harness-ablation-2026-10.md` (M5.12, the digest-hygiene precedent) ·
`./self-model-and-gap-seeking-2026-10.md` (M5.11, sampling-agreement aside) ·
`./references.md` §X (R252–R262) · `../sources/source-map.md` (M3.17 / M5.13 rows)
