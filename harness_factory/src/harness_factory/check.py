"""Self-check for a generated harness (the tool's own M0.3 gate)."""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST_REL = ".harness/manifest.json"
_SCAN_SUFFIXES = {".md", ".py", ".json", ".txt", ".toml", ".cfg"}


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

    return problems
