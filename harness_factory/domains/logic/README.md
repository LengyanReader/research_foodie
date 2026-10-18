# Domain · Logic · 逻辑域
> Wiring `core/` modules into a checkable derivation: fixed language, explicit rules, countermodels, and a meta-theory that stays separate from the claim.
> 把 `core/` 模块接线成「语言固定、规则显式、可反例检验」的推导流程，并让元理论与对象层结论保持分离。
**Updated:** 2026-10-18

---

## 中文速览
逻辑域的目标是**把「推导」变成一件可以逐步检查的事**：先把语言（符号、形成规则、合式公式）固定下来（M0/M7），再明确公理/假设与目标公式；推导（证明）或求值（模型）每一步都要有规则依据（M3）；始终反问「有没有反模型/反例」（M3/M4）；最后把**对象层结论**与**元理论断言**（可靠性、完全性、可判定性）分开陈述（M0/M4）。域特有风险：**语言与元语言混用**、**规则条件不满足**、**用元理论反推对象层结论**、**把「没找到反例」当作「无反例」**。

---

## What this domain is for · 用途
Produce an argument a skeptical reader can replay step by step in a *fixed* language: every formula well-formed, every rule application licensed, every claim about the system (soundness, completeness, decidability) stated at the meta level with its assumptions. Covers mathematical logic, philosophical logic, formal semantics and the theory side of computing.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Fix the language | M0, M7 | signature, formation rules, well-formed formulas |
| L1 | State axioms & target | M1, M4 | assumptions explicit; source for each axiom |
| L2 | Derive / evaluate | M3 | one licensed rule per step |
| L3 | Machine-check (gate) | M3, M6 | proof assistant / SAT-SMT / checker, not prose |
| L4 | Countermodel search | M3, M4 | model, valuation, counterexample; bounded search ≠ refutation |
| L5 | Meta-level write-up | M7, M4 | object-language result vs meta-theory claim |

## Module combination · 模块组合
- **M0** — a plausible derivation is not a proof; the gate is a checkable one.
- **M1** — load the exact definitions, rules and lemmas in scope, with their side conditions.
- **M2** — long proofs checkpoint at lemma boundaries; a stalled tactic run is a loop problem.
- **M3** — step-level verification plus machine checking; a countermodel kills a claim outright.
- **M4** — every cited theorem and every axiom carries its source and its hypotheses.
- **M6** — proof assistant / SMT / countermodel search are tools: pin versions and record the check.
- **M7** — "this is proven" is a governance claim; it is published only with the checked artifact.

## Instruments · 仪器
Concrete tools for L3–L4 (catalog ids; full map: `../reference/evidence-instruments.md#formal-claims`):
- **Proof assistant** — `lean4` (+ `mathlib`) · `rocq` · `isabelle` · `agda`; `dafny` when the claim is about *code*.
- **Automation backend** — `z3` · `cvc5` (SMT). A remaining placeholder (`sorry` / `Admitted` / `postulate`) voids the gate.
- **Behaviour over all executions** — `tla-plus` · `alloy`; report the explored bound, since "no counterexample in scope N" is the claim.
- **Gate evidence** — the compiled proof or checker output **plus** the toolchain version.

## Discipline-specific risks · 领域特有风险
- **Object language / meta-language confusion** (using "⊢" and "⊨" interchangeably).
- **Rule applied outside its side conditions** (discharging a hypothesis that is still live).
- **Meta-theory shortcut** (inferring a theorem of the object theory from soundness/completeness).
- **Bounded search sold as refutation** ("no countermodel in 5 minutes" ≠ "valid").
- **Unstated background theory** (choice, extensionality, classical vs intuitionistic logic).

## See also
`../mathematics/README.md` (formal proofs, Mathlib) · `../core/00-index.md` · `../sources/source-map.md` · `../review/disciplines-crosswalk-2026-10.md`.
