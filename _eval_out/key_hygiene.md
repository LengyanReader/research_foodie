# D-5 Key Hygiene Audit

_Generated 2026-09-20 by `tools.eval.key_hygiene` (deterministic, model-free)._

- Source files scanned: **60**
- Hard-coded credential findings: **0**
- Verdict: **CLEAN — no committed secrets**

Keys live only in environment variables (AGENTS.md secret policy); this
audit scans for secret *values*, never variable *names*, and masks any
match so running it cannot itself leak. Vendored/generated trees are skipped.
