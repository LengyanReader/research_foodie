# Ablations (deterministic, model-free)

_Regenerate: `python -m tools.eval.ablations` — no LLM call, no API key._

## (a) L6 grounding gate — ON vs OFF

Fixed fixture: 8 un-grounded candidates (contiguity-broken + fabricated), 5 grounded controls.

| configuration | un-grounded claims reaching draft | grounded claims kept | false drops |
|---|---|---|---|
| gate **OFF** | 8 | 5 | 0 |
| gate **ON**  | 0 | 5 | 0 |

The deterministic gate removes **8** hallucination candidates (leakage 8 → 0) while keeping all 5 grounded claims (**0** false drops).

## (b) Evidence-pool coverage (30 topics, cached)

| topics | full (≥3 papers) | partial (1-2) | empty (0) | covered |
|---|---|---|---|---|
| 30 | 14 | 8 | 8 | 73% |

## (c) Median-of-N robustness (cached repeat judge runs)

| topic | rounds | min | median | mean | max | spread | last-vs-median |
|---|---|---|---|---|---|---|---|
| P-A | 2 | 3.50 | 3.88 | 3.88 | 4.25 | 0.75 | 0.38 |
| P-B | 2 | 3.31 | 3.31 | 3.31 | 3.31 | 0.00 | 0.00 |
| P-C | 2 | 3.44 | 3.53 | 3.53 | 3.62 | 0.19 | 0.09 |

Mean single-round spread ≈ **0.31** Total points; reporting the median of N dampens this judge noise (E-5 promotion additionally requires Δ ≥ 2σ over N ≥ 3 rounds before any change).
