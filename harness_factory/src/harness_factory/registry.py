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

    Order: ``HARNESS_DATA_DIR`` -> bundled catalogs. A user-home catalog (seeded
    by ``self-update``) is honoured only when ``HARNESS_USE_HOME_CATALOG=1`` is set;
    because packaging is cancelled (L0/L1 are primary), the catalogs that ship with
    the checkout are the source of truth by default.
    """
    override = os.environ.get("HARNESS_DATA_DIR")
    if override:
        return Path(override)
    if os.environ.get("HARNESS_USE_HOME_CATALOG"):
        from . import config

        catalog = config.catalog_dir()
        if (catalog / "modules.json").exists():
            return catalog
    return _DEFAULT_DATA


def data_file(name: str) -> Path:
    """Resolve one catalog file: user home if present, else the bundled default.

    This keeps a partially-seeded user home working after the tool adds new
    catalogs (e.g. ``capabilities.json``, ``harnesses.json``) without a re-seed.
    """
    candidate = data_dir() / name
    if candidate.exists():
        return candidate
    return _DEFAULT_DATA / name


def _load(name: str) -> dict[str, Any]:
    with data_file(name).open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def modules() -> dict[str, dict[str, Any]]:
    """Module catalog M0-M8."""
    return _load("modules.json")


@lru_cache(maxsize=1)
def builtin_domains() -> dict[str, dict[str, Any]]:
    """The bundled domain catalog, *without* any plugins merged in."""
    return _load("domains.json")


@lru_cache(maxsize=1)
def domains() -> dict[str, dict[str, Any]]:
    """Domain catalog: bundled SSOT + valid third-party ``domain`` plugins.

    A plugin may never shadow a built-in id (``setdefault``); such a plugin is
    reported by ``plugins.problems()`` and ignored here.
    """
    from . import plugins

    merged = dict(builtin_domains())
    for domain_id, meta in plugins.domain_entries().items():
        merged.setdefault(domain_id, meta)
    return merged


def clear_caches() -> None:
    """Drop the ``lru_cache`` on the catalogs (used after a plugin-path change)."""
    modules.cache_clear()
    builtin_domains.cache_clear()
    domains.cache_clear()


def module_ids() -> list[str]:
    return list(modules().keys())


def domain_ids() -> list[str]:
    return list(domains().keys())
