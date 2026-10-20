"""Self-check for a generated harness (the tool's own M0.3 gate)."""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST_REL = ".harness/manifest.json"
WORKING_SET_REL = ".harness/working-set.json"
_SCAN_SUFFIXES = {".md", ".py", ".json", ".txt", ".toml", ".cfg"}


def _always_on() -> set[str]:
    """Capabilities whose ``when`` is empty: hard invariants, never evictable (M1.10)."""
    from .capabilities import capabilities

    return {cid for cid, meta in capabilities().items() if not meta.get("when")}


def _known() -> set[str]:
    from .capabilities import capabilities

    return set(capabilities())


def _check_working_set(root: Path, plan: dict, problems: list[str]) -> None:
    """Validate the task's loaded set: no silent drop, no eviction of invariants.

    The file is optional for harnesses emitted before it existed; when the manifest
    lists it, it must be present and consistent (M1.10).
    """
    declared = plan.get("files") or []
    path = root / WORKING_SET_REL
    if not path.exists():
        if WORKING_SET_REL in declared:
            problems.append(f"missing file: {WORKING_SET_REL}")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        problems.append(f"{WORKING_SET_REL} is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        problems.append(f"{WORKING_SET_REL} must be a JSON object")
        return

    matched = data.get("matched")
    active = data.get("active")
    evicted = data.get("evicted")
    for key, value, kind in (
        ("matched", matched, list),
        ("active", active, list),
        ("evicted", evicted, list),
    ):
        if not isinstance(value, kind):
            problems.append(f"{WORKING_SET_REL}: '{key}' must be a {kind.__name__}")
            return

    known = _known()
    for name, ids in (("matched", matched), ("active", active)):
        unknown = sorted(set(ids) - known)
        if unknown:
            problems.append(f"{WORKING_SET_REL}: {name} has unknown capabilities {unknown}")

    if plan.get("capabilities") and list(matched) != list(plan["capabilities"]):
        problems.append(
            f"{WORKING_SET_REL}: 'matched' disagrees with the manifest's capabilities "
            "(re-derive instead of editing it)"
        )

    if len(set(active)) != len(active):
        problems.append(f"{WORKING_SET_REL}: 'active' lists a capability twice")
    if set(active) - set(matched):
        problems.append(
            f"{WORKING_SET_REL}: active capability is not in the matched set: "
            f"{sorted(set(active) - set(matched))}"
        )

    always = _always_on()
    gone = []
    for entry in evicted:
        if not isinstance(entry, dict) or not entry.get("id"):
            problems.append(f"{WORKING_SET_REL}: every eviction needs an 'id'")
            continue
        cid = entry["id"]
        gone.append(cid)
        if cid not in known:
            problems.append(f"{WORKING_SET_REL}: evicted unknown capability {cid!r}")
        if cid in always:
            problems.append(
                f"{WORKING_SET_REL}: {cid!r} is always-on and must not be evicted (M1.10)"
            )
        for field in ("reason", "reload_when"):
            if not str(entry.get(field) or "").strip():
                problems.append(f"{WORKING_SET_REL}: eviction of {cid!r} has no '{field}'")

    if len(set(gone)) != len(gone):
        problems.append(f"{WORKING_SET_REL}: a capability is evicted twice")
    if set(active) & set(gone):
        problems.append(f"{WORKING_SET_REL}: a capability is both active and evicted")
    dropped = sorted(set(matched) - set(active) - set(gone))
    if dropped:
        problems.append(
            f"{WORKING_SET_REL}: silently dropped (neither active nor evicted): {dropped}"
        )


def check_harness(root: str | Path) -> list[str]:
    """Return a list of problems; empty means the harness passes the gate."""
    root = Path(root)
    problems: list[str] = []

    manifest = root / MANIFEST_REL
    if not manifest.exists():
        return [f"missing {MANIFEST_REL}"]

    try:
        plan = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"manifest is not valid JSON: {exc}"]

    files = plan.get("files")
    if not isinstance(files, list) or not files:
        problems.append("manifest has no 'files' list")
        return problems

    for rel in files:
        if not (root / rel).exists():
            problems.append(f"missing file: {rel}")

    for rel in files:
        path = root / rel
        if not path.exists() or path.suffix not in _SCAN_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if "{{" in text:
            problems.append(f"unrendered placeholder: {rel}")

    _check_working_set(root, plan, problems)

    return problems
