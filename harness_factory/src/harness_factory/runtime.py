"""Runtime hooks for an emitted harness (P3).

An emitted harness is not just files on disk; it is a small runtime. This module
gives the *factory* two hooks that operate on an emitted harness **in place**:

- :func:`gate_report` — a deterministic **gate runner**. It runs the structural
  self-check, then *executes the emitted* ``.harness/check.py`` as its own hook
  (proving the artifact is runnable), and finally reports the module-specific
  content gates (M2/M4/M6/M8) as advisory reminders. A harness "passes" when the
  hard, mechanical gates pass; the advisory gates tell a human what evidence is
  still missing (M0.3: every criterion starts ``false``).
- :func:`harvest` / :func:`record_signals` — **signal harvest**. It reads
  observable signals from the emitted harness (domain, modules, gate outcomes,
  progress/ledger counts) plus any agent-appended ``.harness/signals.jsonl``, and
  appends ONE observation line to ``<kb>/updates/signals.jsonl``.

Both hooks are **observe-only**: they never modify the target project and never
touch the factory catalogs. Harvest output is a proposal input for the M5
self-evolution loop, not an automatic change (M0.4/M0.8).
"""

from __future__ import annotations

import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .check import check_harness

MANIFEST_REL = ".harness/manifest.json"
CUSTOM_SIGNALS_REL = ".harness/signals.jsonl"
SIGNALS_REL = "updates/signals.jsonl"

# Enabled module -> tuple of (declared artifact, human label) that the harness must carry.
_MODULE_ARTIFACTS: dict[str, tuple[tuple[str, str], ...]] = {
    "M2": ((".harness/ledger.md", "ledger"),),
    "M4": ((".harness/PROVENANCE.md", "provenance"),),
    "M6": ((".harness/skills/README.md", "skills-index"),),
    "M8": ((".harness/decisions.md", "decisions-log"),),
}


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _load_manifest(root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    manifest = root / MANIFEST_REL
    if not manifest.exists():
        return None, [f"missing {MANIFEST_REL}"]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, [f"manifest is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, ["manifest is not a JSON object"]
    return data, []


def _enabled_modules(manifest: dict[str, Any] | None) -> set[str]:
    if not manifest:
        return set()
    modules = manifest.get("modules", [])
    return {m.get("module_id") for m in modules if isinstance(m, dict) and m.get("enabled")}


def _nonempty_lines(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return 0
    return sum(1 for line in text.splitlines() if line.strip())


def _count_marker(path: Path, marker: str) -> int:
    if not path.exists():
        return 0
    try:
        return path.read_text(encoding="utf-8").count(marker)
    except OSError:
        return 0


def _run_emitted_check(root: Path) -> tuple[bool, str]:
    """Execute the emitted ``.harness/check.py`` as its own runtime hook."""
    script = root / ".harness/check.py"
    if not script.exists():
        return False, "no .harness/check.py emitted"
    try:
        proc = subprocess.run(
            [sys.executable, str(script), str(root)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover - env dependent
        return False, f"could not run check.py: {exc}"
    lines = (proc.stdout or "").strip().splitlines() + (proc.stderr or "").strip().splitlines()
    detail = lines[-1] if lines else f"exit={proc.returncode}"
    return proc.returncode == 0, detail


def gate_report(root: str | Path) -> dict[str, Any]:
    """Run the runtime gates over an emitted harness.

    Returns ``{"root", "passed", "gates": [{"id", "kind", "status", "detail"}]}``.
    ``passed`` is true iff every ``hard`` gate passes; ``advisory`` gates never
    change the exit code but record what evidence is still outstanding.
    """
    root = Path(root)
    gates: list[dict[str, str]] = []
    manifest, manifest_problems = _load_manifest(root)
    structural = check_harness(root)

    gates.append(
        {
            "id": "manifest-valid",
            "kind": "hard",
            "status": "pass" if manifest is not None else "fail",
            "detail": "manifest parsed" if manifest is not None else "; ".join(manifest_problems),
        }
    )

    file_problems = [p for p in structural if p.startswith("missing file")]
    gates.append(
        {
            "id": "files-present",
            "kind": "hard",
            "status": "pass" if not file_problems else "fail",
            "detail": "all declared files present" if not file_problems else "; ".join(file_problems),
        }
    )

    placeholder_problems = [p for p in structural if p.startswith("unrendered placeholder")]
    gates.append(
        {
            "id": "no-placeholders",
            "kind": "hard",
            "status": "pass" if not placeholder_problems else "fail",
            "detail": (
                "no template placeholders"
                if not placeholder_problems
                else "; ".join(placeholder_problems)
            ),
        }
    )

    if manifest is not None:
        ok, detail = _run_emitted_check(root)
    else:
        ok, detail = False, "no manifest to gate"
    gates.append(
        {
            "id": "check-py-runs",
            "kind": "hard",
            "status": "pass" if ok else "fail",
            "detail": detail,
        }
    )

    enabled = _enabled_modules(manifest)
    for module_id, artifacts in _MODULE_ARTIFACTS.items():
        if module_id not in enabled:
            continue
        for rel, label in artifacts:
            lines = _nonempty_lines(root / rel)
            gates.append(
                {
                    "id": rel,
                    "kind": "advisory",
                    "status": "ok" if lines > 0 else "warn",
                    "detail": f"{label}: {lines} non-empty line(s)",
                }
            )
    if "M6" in enabled:
        matches = sorted((root / ".harness" / "skills").glob("*/SKILL.md"))
        gates.append(
            {
                "id": ".harness/skills/*/SKILL.md",
                "kind": "advisory",
                "status": "ok" if matches else "warn",
                "detail": f"portable-skill (Agent Skills format): {len(matches)} SKILL.md file(s)",
            }
        )

    hard = [g for g in gates if g["kind"] == "hard"]
    passed = all(g["status"] == "pass" for g in hard)
    return {"root": str(root), "passed": passed, "gates": gates}


def render_gate_report(report: dict[str, Any]) -> str:
    verdict = "PASS" if report["passed"] else "FAIL"
    lines = [f"gate report @ {report['root']}  ->  {verdict}"]
    for gate in report["gates"]:
        lines.append(f"  [{gate['kind']:<8}] {gate['id']:<24} {gate['status']:<4} {gate['detail']}")
    return "\n".join(lines)


def _read_custom_signals(root: Path) -> list[Any]:
    path = root / CUSTOM_SIGNALS_REL
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out: list[Any] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"raw": line})
    return out


def harvest(root: str | Path) -> dict[str, Any]:
    """Collect observable signals from an emitted harness (pure; no writes)."""
    root = Path(root)
    manifest, _ = _load_manifest(root)
    report = gate_report(root)
    hard = [g for g in report["gates"] if g["kind"] == "hard"]
    advisory = [g for g in report["gates"] if g["kind"] == "advisory"]
    features = (manifest or {}).get("features", {}) if manifest else {}

    return {
        "ts": _now(),
        "source": "harvest",
        "project": str(root),
        "domain": features.get("domain"),
        "modules": sorted(_enabled_modules(manifest)),
        "capabilities": (manifest or {}).get("capabilities", []) if manifest else [],
        "gates": {
            "passed": report["passed"],
            "hard_passed": sum(1 for g in hard if g["status"] == "pass"),
            "hard_total": len(hard),
            "advisory_warnings": sum(1 for g in advisory if g["status"] == "warn"),
        },
        "signals": {
            "progress_lines": _nonempty_lines(root / "tasks/PROGRESS.md"),
            "plan_open_items": _count_marker(root / "tasks/PLAN.md", "- [ ]"),
            "ledger_lines": _nonempty_lines(root / ".harness/ledger.md"),
            "decision_lines": _nonempty_lines(root / ".harness/decisions.md"),
        },
        "custom_signals": _read_custom_signals(root),
    }


def record_signals(kb_root: str | Path, bundle: dict[str, Any]) -> Path:
    """Append one observation line to ``<kb>/updates/signals.jsonl``."""
    path = Path(kb_root) / SIGNALS_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(bundle, ensure_ascii=False) + "\n")
    return path


def render_harvest(bundle: dict[str, Any]) -> str:
    gates = bundle["gates"]
    lines = [
        f"harvest @ {bundle['project']}",
        f"  domain={bundle.get('domain')}  modules={','.join(bundle.get('modules', [])) or '—'}",
        f"  gates: {'PASS' if gates['passed'] else 'FAIL'} "
        f"({gates['hard_passed']}/{gates['hard_total']} hard, "
        f"{gates['advisory_warnings']} advisory warn)",
        f"  signals: {json.dumps(bundle['signals'], ensure_ascii=False)}",
    ]
    if bundle.get("custom_signals"):
        lines.append(f"  custom signals: {len(bundle['custom_signals'])}")
    if bundle.get("recorded"):
        lines.append(f"  recorded -> {bundle['recorded']}")
    return "\n".join(lines)
