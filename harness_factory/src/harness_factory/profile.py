"""Profile a target project: detect its stacks, capabilities, and structure.

Observe-only (M0.4): this *describes* what exists (files present, manifests found)
and never edits the target project. The profile is used two ways: as a weak domain
hint for derivation, and as a **case** for the mutual-learning loop.

All detection is deterministic and bounded (skips heavy/irrelevant dirs, caps the
number of files inspected) so it stays fast and reproducible.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .registry import domains as _domains

_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
    "_archive",
    ".idea",
    ".vscode",
}

_MANIFESTS = {
    "pyproject.toml": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "requirements.txt": "python",
    "environment.yml": "python",
    "Pipfile": "python",
    "package.json": "node",
    "tsconfig.json": "typescript",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "pom.xml": "java",
    "build.gradle": "java",
    "Gemfile": "ruby",
    "composer.json": "php",
}

_EXT_LANG = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".rb": "ruby",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".c": "c",
    ".sh": "shell",
}

_MAX_FILES = 4000
_MAX_DEPTH = 4


@dataclass
class ProjectProfile:
    path: str
    name: str
    stacks: list[str] = field(default_factory=list)
    manifests: list[str] = field(default_factory=list)
    entry_points: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    ci: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    domain_hint: str = "general"
    signals: list[str] = field(default_factory=list)
    file_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _walk(root: Path) -> list[Path]:
    out: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack and len(out) < _MAX_FILES:
        current, depth = stack.pop()
        if depth > _MAX_DEPTH:
            continue
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name not in _SKIP_DIRS and not entry.name.startswith(".git"):
                    stack.append((entry, depth + 1))
            else:
                out.append(entry)
                if len(out) >= _MAX_FILES:
                    break
    return out


def _guess_domain(text: str) -> str:
    best, best_score = "general", 0
    for name, meta in _domains().items():
        if name == "general":
            continue
        score = sum(1 for sig in meta.get("signals", []) if sig in text)
        if score > best_score:
            best, best_score = name, score
    return best


def profile_project(path: str | Path, goal: str | None = None) -> ProjectProfile:
    """Scan ``path`` and return a deterministic :class:`ProjectProfile`."""
    root = Path(path).resolve()
    name = root.name or str(root)
    files = _walk(root)

    rel_names = [str(f.relative_to(root)).replace("\\", "/") for f in files]
    manifests = [rel for rel in rel_names if Path(rel).name in _MANIFESTS]

    stacks: set[str] = set()
    for rel in manifests:
        lang = _MANIFESTS.get(Path(rel).name)
        if lang:
            stacks.add(lang)
    for f in files:
        lang = _EXT_LANG.get(f.suffix.lower())
        if lang:
            stacks.add(lang)

    docs = [
        rel
        for rel in rel_names
        if rel.lower().startswith(("readme", "docs/", "doc/")) or Path(rel).name.lower().startswith("readme")
    ][:10]
    tests = [
        rel
        for rel in rel_names
        if rel.startswith(("tests/", "test/"))
        or Path(rel).name.startswith("test_")
        or Path(rel).name.endswith(("_test.py", ".test.ts", ".test.js", "_test.go"))
    ][:10]
    ci = [
        rel
        for rel in rel_names
        if rel.startswith(".github/workflows/")
        or Path(rel).name in {".gitlab-ci.yml", "azure-pipelines.yml", "Jenkinsfile"}
    ][:10]
    entry_points = [
        rel
        for rel in rel_names
        if Path(rel).name in {"main.py", "app.py", "cli.py", "__main__.py", "manage.py", "index.js", "main.rs", "main.go"}
    ][:10]

    capabilities: list[str] = []
    signals: list[str] = []
    if tests:
        capabilities.append("has-tests")
        signals.append(f"tests: {len(tests)} file(s)")
    if ci:
        capabilities.append("has-ci")
        signals.append(f"ci: {', '.join(ci[:3])}")
    if docs:
        capabilities.append("has-docs")
        signals.append(f"docs: {len(docs)} file(s)")
    if manifests:
        capabilities.append("packaged")
        signals.append(f"manifests: {', '.join(manifests[:4])}")
    if "typescript" in stacks or any(Path(r).name == "py.typed" for r in rel_names):
        capabilities.append("typed")
    if any(Path(r).name in {"Dockerfile", "docker-compose.yml"} for r in rel_names):
        capabilities.append("containerized")
    if any(Path(r).name in {"AGENTS.md", "CLAUDE.md"} for r in rel_names) or any(
        r.startswith(".harness/") for r in rel_names
    ):
        capabilities.append("agent-ready")
    if re.search(r"\b(CLI|command[- ]line|console script)\b", " ".join(rel_names), re.IGNORECASE):
        capabilities.append("has-cli")

    domain_text = " ".join([name, goal or "", " ".join(stacks), " ".join(rel_names[:200])]).lower()
    domain_hint = _guess_domain(domain_text)

    return ProjectProfile(
        path=str(root),
        name=name,
        stacks=sorted(stacks),
        manifests=sorted(manifests),
        entry_points=sorted(entry_points),
        docs=sorted(docs),
        tests=sorted(tests),
        ci=sorted(ci),
        capabilities=sorted(set(capabilities)),
        domain_hint=domain_hint,
        signals=signals,
        file_count=len(files),
    )


def render_profile_md(profile: ProjectProfile, goal: str | None = None) -> str:
    """Bilingual Markdown form (used inside the emitted harness)."""
    lines = [
        "# PROFILE — target project · 目标项目画像",
        "",
        f"**Path:** `{profile.path}`  ·  **Files scanned:** {profile.file_count}",
    ]
    if goal:
        lines.append(f"**Goal:** {goal}")
    lines += [
        "",
        "> 中文速览：本文件是 harness-factory 对**目标项目**的只读扫描结果（技术栈 / 已有能力 / 结构）。",
        "> 它用于把 harness 适配到该项目的真实情况；本工具不修改目标项目（M0.4）。",
        "",
        "## Stacks · 技术栈",
        "",
        ", ".join(profile.stacks) or "_(none detected)_",
        "",
        "## Capabilities · 已有能力",
        "",
        "| capability | evidence |",
        "|---|---|",
        "\n".join(f"| {c} | |" for c in profile.capabilities) or "| _(none)_ | |",
        "",
        "## Structure · 结构",
        "",
        f"- Manifests: {', '.join(profile.manifests) or '—'}",
        f"- Entry points: {', '.join(profile.entry_points) or '—'}",
        f"- Docs: {', '.join(profile.docs) or '—'}",
        f"- Tests: {', '.join(profile.tests) or '—'}",
        f"- CI: {', '.join(profile.ci) or '—'}",
        f"- Domain hint: **{profile.domain_hint}**",
        "",
    ]
    if profile.signals:
        lines.append("## Signals · 证据")
        lines.append("")
        lines += [f"- {s}" for s in profile.signals]
        lines.append("")
    return "\n".join(lines)


def write_profile(root: str | Path, profile: ProjectProfile) -> list[str]:
    """Persist the profile under ``<root>/updates/profile/`` (JSON + Markdown)."""
    out_dir = Path(root) / "updates" / "profile"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", profile.name.lower()).strip("-") or "project"
    json_path = out_dir / f"{slug}.json"
    md_path = out_dir / f"{slug}.md"
    json_path.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_profile_md(profile), encoding="utf-8")
    return [str(json_path), str(md_path)]
