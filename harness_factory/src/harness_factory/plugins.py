"""Plugin protocol for third-party domains and templates (P4).

Plugins are **read-only extensions** discovered from disk; the single-source-of-
truth catalogs (``data/*.json``) are never mutated. A plugin is a directory that
contains a ``plugin.json`` manifest. Two kinds are supported:

``domain``
    Adds a domain so ``--domain <id>`` becomes selectable, optionally with its own
    weighted rubric. It must declare ``title_en``, ``summary``, ``artifact`` (a
    closed-vocabulary value), ``grounding`` (closed vocabulary), and ``signals``.
    It may list ``extra_templates`` (names of template plugins) that are emitted
    alongside the harness.

``template``
    Registers a reusable emitted-file template ``<name>.tmpl``. It must declare
    ``name`` (matching the ``.tmpl`` file) and ``target`` (the output path relative
    to the harness root).

Discovery order: ``HARNESS_PLUGINS_DIR`` (one or more directories, separated by
``os.pathsep``), else ``<data>/plugins``. A plugin id may **not** shadow a built-in
domain or rubric; such a plugin is reported by :func:`problems` and ignored.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .spec import ARTIFACTS, GROUNDING

_MANIFEST_NAME = "plugin.json"
_KINDS = ("domain", "template")


@dataclass
class Plugin:
    id: str
    kind: str
    version: str
    path: Path
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "version": self.version,
            "path": str(self.path),
            "errors": list(self.errors),
        }


def plugin_dirs() -> list[Path]:
    """Resolve the plugin search path."""
    override = os.environ.get("HARNESS_PLUGINS_DIR")
    if override:
        return [Path(p) for p in override.split(os.pathsep) if p]
    from .registry import data_dir

    return [data_dir() / "plugins"]


def _iter_manifests() -> list[tuple[Path, dict[str, Any], list[str]]]:
    found: list[tuple[Path, dict[str, Any], list[str]]] = []
    for base in plugin_dirs():
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            manifest = child / _MANIFEST_NAME
            if not manifest.exists():
                continue
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                found.append((child, {}, [f"plugin.json is not valid JSON: {exc}"]))
                continue
            if not isinstance(data, dict):
                found.append((child, {}, ["plugin.json is not a JSON object"]))
                continue
            found.append((child, data, []))
    return found


def _validate(path: Path, data: dict[str, Any], errors: list[str]) -> list[str]:
    problems = list(errors)
    pid = data.get("id")
    if not isinstance(pid, str) or not pid:
        problems.append("missing string 'id'")
    elif pid != path.name:
        problems.append(f"id {pid!r} must match the directory name {path.name!r}")
    elif pid in _builtin_ids("domains"):
        problems.append(f"id {pid!r} shadows a built-in domain (ignored)")

    kind = data.get("kind")
    if kind not in _KINDS:
        problems.append(f"kind must be one of {_KINDS}, got {kind!r}")
        return problems
    if not isinstance(data.get("version"), str) or not data.get("version"):
        problems.append("missing string 'version'")

    if kind == "domain":
        for key in ("title_en", "summary"):
            if not isinstance(data.get(key), str) or not data.get(key):
                problems.append(f"missing string {key!r}")
        if data.get("artifact") not in ARTIFACTS:
            problems.append(f"artifact must be one of {ARTIFACTS}, got {data.get('artifact')!r}")
        if data.get("grounding") not in GROUNDING:
            problems.append(f"grounding must be one of {GROUNDING}, got {data.get('grounding')!r}")
        signals = data.get("signals")
        if not isinstance(signals, list) or not all(isinstance(s, str) for s in signals):
            problems.append("'signals' must be a list of strings")
        elif len(set(signals)) != len(signals):
            problems.append("'signals' contains duplicates")
        problems.extend(_rubric_problems(data.get("rubric")))
        for ref in data.get("extra_templates", []) or []:
            if not isinstance(ref, str):
                problems.append("'extra_templates' must be a list of template names")
    else:  # template
        name = data.get("name")
        target = data.get("target")
        if not isinstance(name, str) or not name:
            problems.append("missing string 'name'")
        elif not (path / f"{name}.tmpl").exists():
            problems.append(f"missing template file {name}.tmpl")
        if not isinstance(target, str) or not target:
            problems.append("missing string 'target'")
        elif Path(target).is_absolute() or ".." in Path(target).parts:
            problems.append(f"'target' must be a relative in-tree path, got {target!r}")
    return problems


def _rubric_problems(rubric: Any) -> list[str]:
    if rubric is None:
        return []
    if not isinstance(rubric, dict):
        return ["'rubric' must be an object"]
    dims = rubric.get("dimensions")
    if not isinstance(dims, list) or not dims:
        return ["'rubric.dimensions' must be a non-empty list"]
    total = 0.0
    for dim in dims:
        if not isinstance(dim, dict) or not isinstance(dim.get("dim"), str):
            return ["each rubric dimension needs a string 'dim'"]
        weight = dim.get("weight")
        if not isinstance(weight, (int, float)):
            return [f"rubric dimension {dim.get('dim')!r} needs a numeric 'weight'"]
        total += float(weight)
    if not 0.98 <= round(total, 3) <= 1.02:
        return [f"rubric weights must sum to ~1.0, got {total:.3f}"]
    return []


def _builtin_ids(what: str) -> set[str]:
    from .registry import builtin_domains

    if what == "domains":
        return set(builtin_domains())
    return set()


def discover() -> list[Plugin]:
    """Return every syntactically parseable plugin (including invalid ones)."""
    out: list[Plugin] = []
    for path, data, errors in _iter_manifests():
        pid = data.get("id") if isinstance(data.get("id"), str) else path.name
        kind = data.get("kind") if isinstance(data.get("kind"), str) else "unknown"
        version = data.get("version") if isinstance(data.get("version"), str) else ""
        out.append(
            Plugin(
                id=pid,
                kind=kind,
                version=version,
                path=path,
                data=data,
                errors=_validate(path, data, errors),
            )
        )
    return out


def problems() -> list[str]:
    """All validation problems across discovered plugins (for ``harness plugins``)."""
    out: list[str] = []
    for plugin in discover():
        for err in plugin.errors:
            out.append(f"{plugin.path.name}: {err}")
    return out


def _valid() -> list[Plugin]:
    return [p for p in discover() if not p.errors]


def domain_entries() -> dict[str, dict[str, Any]]:
    """Valid ``domain`` plugins as ``{id: domain-meta}`` (SSOT shape)."""
    out: dict[str, dict[str, Any]] = {}
    for plugin in _valid():
        if plugin.kind != "domain":
            continue
        data = plugin.data
        out[plugin.id] = {
            "faculty": data.get("faculty", "general"),
            "title_en": data["title_en"],
            "name_zh": data.get("name_zh", data["title_en"]),
            "summary": data["summary"],
            "workflow": list(data.get("workflow", [])),
            "artifact": data["artifact"],
            "grounding": data["grounding"],
            "signals": list(data.get("signals", [])),
            "plugin": str(plugin.path),
        }
    return out


def rubric_entries() -> dict[str, dict[str, Any]]:
    """Rubrics declared by valid ``domain`` plugins as ``{id: rubric}``."""
    out: dict[str, dict[str, Any]] = {}
    for plugin in _valid():
        rubric = plugin.data.get("rubric")
        if plugin.kind == "domain" and isinstance(rubric, dict):
            out[plugin.id] = rubric
    return out


def template_entries() -> dict[str, dict[str, Any]]:
    """Valid ``template`` plugins as ``{name: {target, path}}``."""
    out: dict[str, dict[str, Any]] = {}
    for plugin in _valid():
        if plugin.kind != "template":
            continue
        name = plugin.data["name"]
        out[name] = {
            "target": plugin.data["target"],
            "path": plugin.path / f"{name}.tmpl",
        }
    return out


def domain_template_targets(domain_id: str) -> dict[str, Path]:
    """Resolve a domain plugin's ``extra_templates`` -> ``{target: tmpl_path}``."""
    for plugin in _valid():
        if plugin.kind == "domain" and plugin.id == domain_id:
            templates = template_entries()
            out: dict[str, Path] = {}
            for name in plugin.data.get("extra_templates", []) or []:
                entry = templates.get(name)
                if entry:
                    out[entry["target"]] = entry["path"]
            return out
    return {}


def clear_caches() -> None:
    """Drop the registry/standard caches so a plugin-path change takes effect."""
    from . import registry, standard

    registry.clear_caches()
    standard.clear_cache()
