# Self-modifying harnesses, digest-ingested · 自改造 harness 一轮：周报摄取实录

> What a weekly papers digest can and cannot justify: two clauses (M3.17, M5.13) landed from abstract-verified
> primary sources, and an explicit ledger of what stayed *unverified* — then (P38, 2026-10-28) the full-text reread
> that resolved the ledger: three verified, three corrected in kind, one ledger premise itself found wrong.
> 一份周论文精选能支撑什么、不能支撑什么：两条子句（M3.17、M5.13）落在摘要级一手核实上，其余主张明列「未验证」台账——随后（P38，2026-10-28）全文重读裁决台账：3 项验证、3 项纠正、1 项台账前提本身有误。
**Updated:** 2026-10-28 · Rounds P34 + P38 · Evidence level: **full-read** (R252–R259 + R260 affiliations via `arxiv.org/html`, 2026-10-28); the 2026-10-27 round was **abstract-verified** (0 full reads) — its history is kept below.

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

**Full texts were not reachable from this environment** (2026-10-27 state). Seven attempts across `arxiv.org/html/*` and `ar5iv`
all failed to parse (context-deadline / cancellation), and the Semantic Scholar API returned HTTP 429; abs
pages themselves succeeded only on spaced retries. So that round was graded, honestly, **abstract-verified** —
the same posture as the P12 precedent ("no reachable HTML full text and stays unverified"). A **full-text
reread trigger** was registered as roadmap item P34.R1: any upgrade of these items to *full-read* status
(checking method sections, ablations and the claims in §4 below) reopens the two landed clauses for revision.
Nothing in `core/` states a body-only number as fact; both clauses cite `[R###] (abstract-level)`.

**P38 (2026-10-28): the trigger fired and the reread is done.** `arxiv.org/abs` and `arxiv.org/html/<id>`
were probed reachable again (2026-10-28), and all of **R252–R259 were read as HTML full texts** (method,
results, tables; each fetch checked for the specific ledger claims below), plus **R260's affiliation block**
(HTML renders affiliations; abs pages do not). Evidence level is now **full-read** for the eight; the two
landed clauses' hedges are promoted (`core/04` M3.17, `core/06` M5.13), and the §4 ledger below carries each
item's resolution — three verified, three corrected in kind, one ledger premise found wrong, one attribution
confirmed true.

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

## 4. The ledger, resolved — P38 reread (2026-10-28)

Each claim below appeared in the digest's article body but **not** (as far as the 2026-10-27 abstract read
showed) in the corresponding abstract, and stayed *unverified* until the P34.R1 reread. All access dates for
the resolutions: **2026-10-28**, `arxiv.org/html/<id>` full text. Verdicts:

1. **HERMES "task pass rate 6.5% → 31%" (R255) — verified, metric corrected in kind.** The pair is real
   ("the composite score rises from 6.5% to 31.0% under medium effort", GPT-5.6 Sol, SWE Refactor Bench,
   §4.2) but the metric is a **composite score**, not the digest's "task pass rate". Side finding recorded:
   an *internal* tension — the abstract states a **26.2%** inference-cost cut on Terminal-Bench 4.0, while
   §4.3's discussion reports **37.4%** lower total inference cost ($2.13k vs $3.40k); different measurement
   bases or a drafting slip, but the library quotes the abstract figure as abstract-stated and flags the pair.
2. **VERA's "+5% accept / −20% reject" gate thresholds (R256) — verified, semantics corrected in kind.**
   The paper states **two distinct criteria for two update types** (§2.1): a *harness edit* must pass
   self-tests and improve the Overall development score **by at least 5 percentage points** (a required
   gain); a *model checkpoint* is accepted if its development-benchmark score **decreases by no more than
   20%** relative to the previously accepted checkpoint (a tolerated-regression bound). The digest's
   symmetric "+5% accept / −20% reject" fused an advance bound with a tolerance bound. Also confirmed at
   full-read: the LLM/Harness attribution reports, paired reruns on a frozen model so "only the edit can
   cause the difference", 9,000+ environments, the 10.3/13.0 and 71.6/80.7 headline results.
3. **CorpusMap "+6.4–11.7 points, −34–57% tokens" (R253) — verified, and the ledger's premise was wrong.**
   The magnitudes are stated **in the abstract itself** ("overall quality by 6.4 to 11.7 points", "34% to
   57% fewer input tokens on average") — the 2026-10-27 abstract read missed them, which is M3.17 in
   miniature: even a careful single read is a sample. The body confirms: Table 6 gives +6.45 to +11.74 vs
   raw-corpus agentic search (Holm-corrected p < 10⁻⁴), token ratios 0.43×–0.65× (geometric mean), over
   7 models × 3 benchmarks, beating the four alternative navigation layers (Document Page, Group Page,
   LLM Wiki, Corpus2Skill).
4. **Agent Plasticity's named models and the "$1,073 total cost" (R259) — models verified; cost figure
   corrected in kind.** The named models check out (Claude Fable 5, Claude Opus 5/4.8/4.6, Claude Sonnet 5,
   GPT-5.5, GPT-5.6 Sol/Luna, Gemini 3.1 Pro). But "$1,073 total cost" is a digest compression that changed
   the claim: the paper's only dollar figure is **Claude Opus 5.5's prior learning cost, $1,072.73** (per
   model, Appendix C) — there is no total-evaluation-cost figure. Plasticity is reported as score points
   per $1,000 of learning cost (e.g. GPT-5.6 Sol 298 vs Claude Fable 5 57).
5. **Institution attributions, incl. CMM → Sakana AI (R260) — verified true.** All six R260 authors are
   affiliated with **Sakana AI** (Regan additionally University of Tsukuba). P34's suspicion was an artifact
   of abs pages not showing affiliations; the digest's attribution stands.
6. **Sharpening Tax / MASS headline numbers (R258, R257) — §3's abstract-side quotes confirmed; body-side
   numbers now carried.** Sharpening Tax: Tax_S(128) > 0 in **36 of 42** combinations; the crossover budget
   k* falls from >128 (4B) to ≈3 (31B); bimodalization measured (pass-given-compute 87.6% → 30.0%,
   gemma-4-31B WebShop); PTGS shrinks the tax (e.g. GRPO Sokoban 0.081 → 0.025) while lifting both pass@1
   and pass@128; the work is **observational, not interventional** (§9). MASS: the 1.2–1.6× per-output-token
   range is confirmed, with honest smallness (AstaBench 0.053 → 0.067); the 1.4×-token efficiency control is
   **"not a matched-data control"** (Appendix D); the workflow search is pairwise with elite size one, not
   population evolution.

**Added by the reread — the R254 release pool is located (§6's open item).** Appendix E names the release
targets: rollouts at `huggingface.co/datasets/caiqizh/veriharness`, verification code at
`github.com/google-research/veriharness` (trajectories, delivered files, grader scores; no benchmark content
redistributed). The skill-evolution loop (§5) adds held-out gains for library evolution: +6.8 (APEX-Agents) /
+3.7 (SpreadsheetBench 2) from evolving the human-authored library. Retrieval of the actual dataset remains
its own task; the *commitment* is now first-party-verified.

## 5. Roadmap status after this round

- **P34.R1 → done (done_in P38, 2026-10-28)**: the full-text reread ran with the §4 ledger as its checklist;
  the two landed clauses' "abstract-level" hedges are promoted, not retracted — both mechanisms survived the
  full text, and M5.13(d) gains VERA's two-bound exemplar (advance bound for harness edits, tolerance bound
  for checkpoints).
- **D7 (agent-judge robustness)**: R254 is now a **full-read-grade** primary source on agentic verification
  (mechanisms §3.2/§3.3 verified verbatim; self-evolving verification skills §5) — D7's revisit trigger has
  *fired*. The robustness pass itself remains a round of its own (a golden-set audit, not a clause edit);
  D7 stays deferred with the reason upgraded from "no candidate source" to "trigger fired, round not yet queued".
- **D1 (trace-driven evolution)**: stage-C precedents R252/R256 now **full-read** — the precedent basis is
  solid; stage C itself still awaits the first real measured effect receipt (P37's completion definition).
- **No new capability, domain, or catalog entry** (M0.5 discipline): all systems are research artifacts; the
  reread verified *claims and release commitments*, not runnable implementations (the R254 dataset/code URLs
  are named and first-party, but the artifacts were not downloaded or executed this round).

## 6. Licenses and reach — capture hygiene

R256 is **CC BY-NC-SA 4.0** (non-commercial) — any future derivative of its materials inside this factory needs
the license checked *before* reuse, not after. R253 and R259 carry the **arXiv non-exclusive distribution**
license (no blanket CC grant). R261 is **CC0 1.0**. R260's notes show a NeurIPS 2026 workshop context (PALM).
R254's release pool is first-party-located as of the P38 reread (2026-10-28): rollouts at
`huggingface.co/datasets/caiqizh/veriharness`, verification code at `github.com/google-research/veriharness`
(§4, added item) — the most useful artifact of the set for this library's scored-task work
(`scored-task-set-2026-10.md`); retrieval and inspection of the actual data remains its own task.

---

## See also

`../core/04-verification-and-gates.md` (M3.17) · `../core/06-self-evolution.md` (M5.13) ·
`./harness-ablation-2026-10.md` (M5.12, the digest-hygiene precedent) ·
`./self-model-and-gap-seeking-2026-10.md` (M5.11, sampling-agreement aside) ·
`./references.md` §X (R252–R262) · `../sources/source-map.md` (M3.17 / M5.13 rows)
