"""A tiny dependency-free ``{{key}}`` template engine.

Unknown keys are left untouched on purpose: the checker gate in
:mod:`harness_factory.check` fails on any remaining ``{{`` in emitted files, so a
missing variable is caught rather than silently blanked.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

_TEMPLATES = Path(__file__).resolve().parent / "templates"
_PATTERN = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def templates_dir() -> Path:
    return _TEMPLATES


def template_path(name: str) -> Path:
    return _TEMPLATES / name


def render(text: str, context: Mapping[str, Any]) -> str:
    def _sub(match: re.Match[str]) -> str:
        key = match.group(1)
        value = context.get(key)
        return str(value) if value is not None else match.group(0)

    return _PATTERN.sub(_sub, text)


def render_template(name: str, context: Mapping[str, Any]) -> str:
    return render(template_path(name).read_text(encoding="utf-8"), context)
