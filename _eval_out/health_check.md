# Health check / 健康检查 (WS-C E-2)

> Updated: 2026-09-20 · elapsed 5s · frozen subset = mock 34/34 + judge sanity ['P-A', 'P-B', 'P-C'] + pools re-scan + L6 gate coverage
> Judge: skipped (--quick)  ·  thresholds: 2σ FAIL / 1σ WARN (σ per proxy from baselines.json)
> Provenance (D-4): judge skipped (--quick)

- **[PASS]** `mock` — mock 34/34 (baseline 34/0)
- **[PASS]** `pools` — coverage 22/30 (full 14)
- **[PASS]** `arxiv_probe` — reachable
- **[PASS]** `gate_coverage` — 23/23 mutants killed (100%)
- **[SKIP]** `judge:P-A` — no current score (skipped (--quick))
- **[SKIP]** `judge:P-B` — no current score (skipped (--quick))
- **[SKIP]** `judge:P-C` — no current score (skipped (--quick))

## Baselines (frozen at freeze time)

| proxy | baseline mean | σ | n | 2σ |
|---|---|---|---|---|
| P-A | 3.88 | 0.53 | 2 | 1.06 |
| P-B | 3.31 | 0.0 | 2 | 0.00 |
| P-C | 3.53 | 0.13 | 2 | 0.26 |

- qa_panel: {'n': 31, 'correctness': 4.23, 'groundedness': 4.45, 'pass': '24/31'}
- pools: {'total': 30, 'covered': 22, 'full': 14, 'partial': 8, 'empty': 8}
- gate_coverage: {'mutants': 23, 'passed': 23, 'kill_rate': 1.0, 'results': {'interleave gap1 s0': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s1': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s2': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s3': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s4': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s5': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s6': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'interleave gap1 s7': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'synthetic negative 0': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'synthetic negative 1': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'synthetic negative 2': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'synthetic negative 3': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['grounding']}, 'structure no draft': {'expected_reject': True, 'got_reject': True, 'score': 1.0, 'fails': ['structure', 'bilingual']}, 'structure no taxonomy': {'expected_reject': True, 'got_reject': True, 'score': 1.0, 'fails': ['structure', 'bilingual']}, 'structure no claims': {'expected_reject': True, 'got_reject': True, 'score': 0.0, 'fails': ['structure', 'bilingual']}, 'bad cite 0': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['cites']}, 'bad cite 1': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['cites']}, 'bad cite 2': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['cites']}, 'bad cite 3': {'expected_reject': True, 'got_reject': True, 'score': 0.5, 'fails': ['cites']}, 'verbatim quote': {'expected_reject': False, 'got_reject': False, 'score': 1.0, 'fails': []}, 'one-word paraphrase': {'expected_reject': False, 'got_reject': False, 'score': 1.0, 'fails': []}, 'empty quote (informational)': {'expected_reject': False, 'got_reject': False, 'score': 1.0, 'fails': []}, 'latin-only draft (bilingual=warn only)': {'expected_reject': False, 'got_reject': False, 'score': 1.0, 'fails': ['bilingual']}}}
