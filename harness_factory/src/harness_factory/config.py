"""Resolve the tool's user-space home (knowledge base + state).

The tool has **two roots** and they must not be confused:

* **A · tool home** (here) -- catalogs, corpus, refresh output. Lives in user
  space so the tool works from *any* directory, not only this repo.
* **B · target project** -- where a generated harness is emitted (`init --out`).

Resolution order (first wins)::

    CLI flags > ENV (HARNESS_HOME / HARNESS_DATA_DIR / HARNESS_CORPUS_DIR)
              > user config.toml > platform default

No third-party dependencies; ``config.toml`` is optional.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

try:  # py311+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

_PACKAGED_DATA = Path(__file__).resolve().parent / "data"


def _default_home() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "harness-factory"


def home() -> Path:
    """The tool's user-space home directory (override with ``HARNESS_HOME``)."""
    override = os.environ.get("HARNESS_HOME")
    return Path(override) if override else _default_home()


def config_file() -> Path:
    return home() / "config.toml"


def load_config() -> dict[str, Any]:
    """Load ``config.toml`` from the home dir, or ``{}`` if absent/unreadable."""
    path = config_file()
    if tomllib is None or not path.exists():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _cfg_path(key: str) -> Path | None:
    value = load_config().get(key)
    return Path(value) if value else None


def catalog_dir() -> Path:
    """Where the machine-readable catalogs live (user copy)."""
    env = os.environ.get("HARNESS_DATA_DIR")
    if env:
        return Path(env)
    return _cfg_path("data_dir") or home() / "catalog"


def corpus_dir() -> Path:
    """Where the refresh corpus lives (used for dedupe)."""
    env = os.environ.get("HARNESS_CORPUS_DIR")
    if env:
        return Path(env)
    return _cfg_path("corpus_dir") or home() / "corpus"


def updates_dir() -> Path:
    return home() / "updates"


def factory_root() -> Path | None:
    """The harness_factory checkout that provides this code.

    That is the directory containing ``SKILL.md`` (i.e. ``<checkout>/harness_factory``),
    which is what an external task should reference.  Returns ``None`` when the
    package was installed without the docs (a data-only copy), so callers can fall
    back to an explicit placeholder instead of inventing a path.
    """
    candidate = Path(__file__).resolve().parents[2]
    return candidate if (candidate / "SKILL.md").is_file() else None


def seed_catalog(force: bool = False) -> dict[str, list[str]]:
    """Copy packaged ``data/*.json`` into :func:`catalog_dir`.

    Non-destructive by default: existing files are kept (user edits win).
    """
    dest = catalog_dir()
    dest.mkdir(parents=True, exist_ok=True)
    added: list[str] = []
    kept: list[str] = []
    if not _PACKAGED_DATA.exists():
        return {"added": added, "kept": kept}
    for src in sorted(_PACKAGED_DATA.glob("*.json")):
        target = dest / src.name
        if target.exists() and not force:
            kept.append(src.name)
            continue
        shutil.copyfile(src, target)
        added.append(src.name)
    return {"added": added, "kept": kept}


def ensure_home(seed: bool = True) -> Path:
    """Create the home skeleton (catalog, corpus, updates) and seed catalogs."""
    base = home()
    (base).mkdir(parents=True, exist_ok=True)
    catalog_dir().mkdir(parents=True, exist_ok=True)
    corpus_dir().mkdir(parents=True, exist_ok=True)
    updates_dir().mkdir(parents=True, exist_ok=True)
    if seed:
        seed_catalog()
    return base


def resolve_corpus_root(root: str | Path | None = None) -> Path:
    """Pick the corpus root: a checkout's ``review/`` if present, else the home corpus.

    Keeps the tool working both as a repo checkout (``<root>/review``) and as a
    globally-installed tool (``~/.…/harness-factory/corpus``).
    """
    if root is not None:
        candidate = Path(root) / "review"
        if candidate.exists():
            return Path(root) / "review"
    return corpus_dir()
