"""Load the machine-readable catalogs (modules, domains).

Kept dependency-free; the JSON files are the single source of truth for the
mapping between the human docs in ``core/`` and the tool's decisions (M0.5).
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

_DEFAULT_DATA = Path(__file__).resolve().parent / "data"


def data_dir() -> Path:
    """Return the catalog directory.

    Order: ``HARNESS_DATA_DIR`` -> user home catalog (if seeded) -> bundled data.
    """
    override = os.environ.get("HARNESS_DATA_DIR")
    if override:
        return Path(override)
    from . import config

    catalog = config.catalog_dir()
    if (catalog / "modules.json").exists():
        return catalog
    return _DEFAULT_DATA


def _load(name: str) -> dict[str, Any]:
    with (data_dir() / name).open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def modules() -> dict[str, dict[str, Any]]:
    """Module catalog M0-M8."""
    return _load("modules.json")


@lru_cache(maxsize=1)
def domains() -> dict[str, dict[str, Any]]:
    """Domain catalog."""
    return _load("domains.json")


def module_ids() -> list[str]:
    return list(modules().keys())


def domain_ids() -> list[str]:
    return list(domains().keys())
