# Domain · Model selection / fit-for-task evaluation · 模型选型·任务适配性评估域
> From requirement matrix to reproducible fit-for-task evaluation with provenance.
> 从需求矩阵到可复现的任务适配性评估，并保持全程溯源。
**Updated:** 2026-10-12

## What this domain is for
Select the right model for a concrete task by making the decision verifiable: define a Task Requirements Matrix, discover candidates, check evidence, run a minimal fit-for-task evaluation on your own samples, and pass a hard decision gate with full provenance.

## Pipeline layers
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Requirements matrix | M0,M7 | define acceptable criteria (quality/latency/cost/constraints/licenses/privacy) |
| L1 | Candidate discovery | M1,M4 | use registries/leaderboards to get top-N with rationale |
| L2 | Evidence provenance | M4 | check task-subset evidence (not just overall scores) |
| L3 | Fit-for-task eval | M2,M3 | run minimal eval on your own hold-out (lm-eval/simple-evals/lighteval) |
| L4 | Decision gate | M3,M7 | compare by weighted matrix; require hard gate pass |
| L5 | Record & reproducible | M2,M4,M7 | write PROVENANCE.md + ledger with scripts/metrics/model versions |

## Tools & sources
- Registries/leaderboards: HF Models/OpenRouter/LMArena/Artificial Analysis/PapersWithCode
- Evidence: Elicit/Consensus/OpenAlex
- Eval frameworks: LM Evaluation Harness, HELM, simple-evals, LightEval
