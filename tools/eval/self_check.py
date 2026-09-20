"""L-6 one-command self-check — the whole offline safety net in one call.

Bundles the deterministic layers that must stay green before any human trusts
a change (PLAN §8 Phase L / WS-C E-2). Zero LLM cost by default, ~15 s:

    1. tools.eval.test_evolution     self-evolution loop guards (unit, zero-LLM)
    1b. tools.eval.test_capability    base-model config layer + capability report
    2. tools.pipeline.test_pipeline mock   pipeline integration (in-proc mock)
    3. tools.eval.evolution_sprint --quick  health + dep drift + ticket board

`--full` swaps step 3 for a live cadence (adds the ~1.5 min LLM judge sanity);
`--with-real` appends the `test_pipeline real` run (needs the opencode CLI).

Exit code is the max across steps (0 GREEN · 1 WARN · 2 FAIL), so it drops
straight into a CI/`self_check.ps1` gate. Writes nothing outside the ledgers
`evolution_sprint` already owns.

Usage:
  python -m tools.eval.self_check            # offline (default)
  python -m tools.eval.self_check --full     # + live judge cadence
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_LEVELS = {"GREEN": 0, "WARN": 1, "FAIL": 2}


def _run(label: str, argv: list, timeout: int, hard: bool) -> int:
    """Run one step; echo a compact status. Returns a 0/1/2 health level.
    `hard` steps (unit + integration) are pass/fail → FAIL on any non-zero rc;
    soft steps (the cadence) forward their own 0/1/2 exit code verbatim."""
    t0 = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, "-X", "utf8"] + argv, cwd=REPO_ROOT,
            capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"  [FAIL] {label:<26} timeout >{timeout}s")
        return 2
    dt = time.time() - t0
    rc = proc.returncode
    if rc == 0:
        print(f"  [GREEN] {label:<26} {dt:5.1f}s")
        return 0
    # surface the failing tail so one command is enough to start triage
    tail = "\n".join(((proc.stdout or "") + "\n" + (proc.stderr or ""))
                     .strip().splitlines()[-12:])
    print(f"  [{'FAIL' if hard else ('WARN' if rc == 1 else 'FAIL')}] "
          f"{label:<26} {dt:5.1f}s  (rc={rc})")
    for line in tail.splitlines():
        print(f"        | {line}")
    if hard:
        return 2
    return rc if rc in (1, 2) else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="L-6 one-command self-check")
    ap.add_argument("--full", action="store_true",
                    help="run the live cadence (LLM judge sanity) instead of --quick")
    ap.add_argument("--with-real", action="store_true",
                    help="also run `test_pipeline real` (needs opencode CLI)")
    a = ap.parse_args(argv)

    print("== research_foodie self-check / 自检 (L-6) ==", flush=True)
    worst = 0

    worst = max(worst, _run("unit: self-evolution", ["-m", "tools.eval.test_evolution"],
                            120, hard=True))
    worst = max(worst, _run("unit: config + capability", ["-m", "tools.eval.test_capability"],
                            120, hard=True))
    worst = max(worst, _run("integration: mock pipeline",
                            ["-m", "tools.pipeline.test_pipeline", "mock"], 180, hard=True))

    sprint = ["-m", "tools.eval.evolution_sprint"] + ([] if a.full else ["--quick"])
    worst = max(worst, _run("cadence: evolution_sprint", sprint,
                            600 if a.full else 240, hard=False))

    if a.with_real:
        worst = max(worst, _run("integration: real pipeline",
                                ["-m", "tools.pipeline.test_pipeline", "real"],
                                600, hard=False))

    print(f"\nself-check -> {('GREEN', 'WARN', 'FAIL')[worst]} (exit {worst})", flush=True)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
