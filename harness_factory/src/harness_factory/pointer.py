"""The emitted ``.harness/pointer.json`` — how a target project *finds* its factory.

A generated harness must not depend on the user re-typing the factory path at the
start of every new conversation.  So ``init`` records the **resolved** factory
root here, and both ``harness doctor`` and the runtime gate can verify that the
pointer still resolves.

Two distinct questions, deliberately kept apart:

* **Pointer resolves?** — is the factory reachable at the recorded absolute path
  (``SKILL.md`` + the reference docs readable)?  This is *hard* information, but
  it is environment-dependent: on another machine the path may legitimately be
  absent, so the runtime gate treats it as **advisory**.
* **Standing reference present?** — does the project's rules file (``AGENTS.md`` /
    ``CLAUDE.md``) carry the standing-reference block (revocable via
    ``stop using harness_factory``)?  That is what makes the reference *always on*.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from harness_factory import skill as _skill

POINTER = ".harness/pointer.json"
REVOKE = "stop using harness_factory"

#: Docs an agent must be able to reach, relative to the factory root.  Derived
#: from the skill index (the ``overview`` + ``reference`` groups) so the pointer
#: can never drift from the load-index: if a doc is loadable via ``harness
#: skill``, the pointer also locates it by absolute path.  This is what lets an
#: emitted harness use the *whole* capability reference, not a frozen subset.
ENTRY_DOCS: tuple[str, ...] = tuple(
    entry.path for entry in _skill.index() if entry.group in {"overview", "reference"}
)
#: Project rules files scanned for the standing-reference block.
RULES_FILES = ("AGENTS.md", "CLAUDE.md", ".cursor/rules/harness-factory.mdc")


def build(factory_root: str | None, *, created: str, version: str) -> dict:
    """The pointer payload. ``factory_root`` must be a live checkout, else ``None``."""
    root = None
    if factory_root:
        candidate = Path(factory_root)
        if (candidate / "SKILL.md").is_file():
            root = candidate
    return {
        "generated": created,
        "version": version,
        "harness_factory": str(root) if root else None,
        "skill_md": str(root / "SKILL.md") if root else None,
        "entry_docs": {rel: str(root / rel) for rel in ENTRY_DOCS} if root else {},
        "capabilities_local": ".harness/capabilities.local.md",
        "how_to_use": (
            "Read skill_md first; route via entry_docs['reference/capability-router.md'] and load "
            "ONLY the files the matching row names; for a vague/under-aimed ask run "
            "entry_docs['reference/requirement-refinement.md'] (R0-R5) and wait for confirmation. "
            "The remaining entry_docs are the full loadable set (field->instrument->outlet maps, "
            "cross-language, derivation rules; same as `harness skill`)."
        ),
        "revoke": REVOKE,
        "note": (
            "Absolute path to the harness_factory checkout that generated this harness "
            "(null if it was not reachable at generation time). Not a dependency: this project "
            "works without it; the pointer only locates the shared capability reference."
        ),
    }


def render(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def verify(target_root: str | Path) -> dict:
    """Check whether ``target_root``'s pointer resolves and carries the convention.

    Returns ``{"pointer", "found", "factory", "ok", "standing_reference", "problems"}``
    where ``ok`` is about *reachability* only and ``standing_reference`` is advisory.
    """
    base = Path(target_root)
    path = base / ".harness" / "pointer.json"
    result: dict = {
        "pointer": str(path),
        "found": False,
        "factory": None,
        "ok": False,
        "standing_reference": False,
        "problems": [],
    }

    if not path.is_file():
        result["problems"].append(f"no {path.name} at {path} (re-run `harness init --force`)")
    else:
        result["found"] = True
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            result["problems"].append(f"pointer is not valid JSON: {exc}")
            data = None
        if isinstance(data, dict):
            root = data.get("harness_factory")
            result["factory"] = root
            if not root:
                result["problems"].append(
                    "pointer records no factory path (generated without the docs on disk)"
                )
            elif not (Path(root) / "SKILL.md").is_file():
                result["problems"].append(f"factory not reachable at {root} (SKILL.md missing)")
            else:
                missing = [rel for rel in ENTRY_DOCS if not (Path(root) / rel).is_file()]
                if missing:
                    result["problems"].append(f"factory is missing entry docs: {missing}")
        elif data is not None:
            result["problems"].append("pointer is not a JSON object")

    for name in RULES_FILES:
        candidate = base / name
        if candidate.is_file():
            try:
                if REVOKE in candidate.read_text(encoding="utf-8"):
                    result["standing_reference"] = True
                    break
            except OSError:
                pass

    result["ok"] = not result["problems"]
    return result


def render_verify(result: dict) -> str:
    lines = [f"pointer @ {result['pointer']}"]
    if result["factory"]:
        lines.append(f"  factory : {result['factory']}")
    lines.append(f"  reachable: {'yes' if result['ok'] else 'no'}")
    lines.append(
        "  standing reference in rules file: "
        + ("yes" if result["standing_reference"] else "no (paste the block into AGENTS.md/CLAUDE.md)")
    )
    for problem in result["problems"]:
        lines.append(f"  - {problem}")
    return "\n".join(lines)
