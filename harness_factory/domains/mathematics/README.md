# Domain · Mathematics · 数学域
> Wiring `core/` modules into a proof-checked derivation with explicit assumptions.
> 把 `core/` 模块接线成「可逐步校验、假设显式」的数学论证流程。
**Updated:** 2026-10-18

---

## 中文速览
数学域的目标是**把结论降维成从假设到结论的可核验推理链**。以 L0–L5 编排 `core/`：L0 陈述定义与假设（M7）、L1 回顾已知结果（M1/M4）、L2 构造证明或计算（M3）、L3 逐步校验（M3）、L4 反例与边界情形（M3/M4）、L5 撰写（M7）。域特有风险：**隐藏假设**、**把猜想当定理**、**跳步**、**过早套用定理（条件不满足）**、**忽略退化/边界情形**。

---

## What this domain is for · 用途
Reach a result — a theorem, a proof, a computation — that a skeptical reader can verify step by step, with every assumption stated and every cited result's hypotheses checked before use.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Definitions & assumptions | M0, M7 | precise objects; plan-first |
| L1 | Recall known results | M1, M4 | cite with hypotheses verified |
| L2 | Construct proof / computation | M3 | each step justified |
| L3 | Check every step | M3 | no implicit leap (gate) |
| L4 | Counterexamples & edge cases | M3, M4 | degenerate cases, n=0/1 |
| L5 | Write up | M7, M4 | provenance for quoted theorems |

## Module combination · 模块组合
- **M0** — a confident derivation is not a correct one; verify each step.
- **M1** — load only the lemmas in scope, with their exact preconditions.
- **M2** — long proofs / large computations checkpoint at lemma boundaries.
- **M3** — the gate is step-level verification plus an edge-case sweep.
- **M4** — every quoted theorem carries its source and a precondition check.
- **M6** — when computation is used (CAS/numeric), pin versions and cross-check.
- **M7** — the write-up is reviewable; sharing a claim as proven is governed.

## Instruments · 仪器
Concrete tools for L2–L3 (catalog ids; full map: `../reference/evidence-instruments.md#certified-computation`):
- **Proof assistant** — `lean4` (+ `mathlib`) · `rocq` (+ `mathcomp`) · `isabelle` · `agda`; `metamath` for a minimal, step-checkable verifier.
- **Computer algebra** — `sagemath` · `singular` · `macaulay2` (commutative algebra / algebraic geometry) · `gap` (groups) · `pari-gp` (number theory) · `oscar` · `sympy`.
- **SAT / SMT for finite cases** — `cadical` (SAT) · `z3` · `cvc5` (SMT); an encoded instance settles the *instance*, not the general theorem.
- **Geometry & topology** — `cgal` · `gudhi` · `regina` · `snappy` · `polymake` (deepened in `../geometry-topology/README.md`).
- **Gate evidence** — a compiled proof with **no placeholder left**, or a computed value under **exact/certified arithmetic** that is **independently re-derived** (M3.12). An unchecked CAS/SAT output is a conjecture.

## Methodology · 方法论
- **Proof methodology** — state the language, axioms and the target; check the derivation; attempt a counterexample; keep object-level results separate from meta-theory claims.
- **Computation is not proof** — a CAS/SAT result is evidence for an *instance*; a general claim still needs a derivation (M3.12).
- Full map: `../reference/methodology-map.md` (M3.13).

## Discipline-specific risks · 领域特有风险
- **Hidden / unstated assumptions**.
- **Conjecture presented as theorem**.
- **Skipping steps** ("it follows that…").
- **Applying a theorem whose hypotheses are unmet**.
- **Ignoring degenerate/boundary cases**.

## See also
`../core/00-index.md` · `../sources/source-map.md` · `../review/harness-catalog.md`.
