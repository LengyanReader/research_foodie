"""D-5 key hygiene — a deterministic, model-free audit that the repo commits
no hard-coded credentials.

`AGENTS.md` and Phase D keep a single secret rule: **keys exist only as
environment variables, never in git or the web bundle.** This module enforces
that mechanically instead of by convention — it walks the tracked source tree
and reports every high-signal secret *literal* it finds (OpenAI-style ``sk-``
keys, AWS/GCP/Slack/HuggingFace/GitHub tokens, PEM private-key blocks, and
long literals assigned to ``*_key`` / ``*_token`` / ``*_secret`` names).

Design notes
  * Stdlib only, no network, no LLM — safe for ``self_check`` and CI.
  * It scans the patterns of *real* secrets, not variable *names*: a reference
    like ``os.environ["OPENAI_API_KEY"]`` is legitimate and never matches.
  * Matches are **masked** before they are ever printed, so running the audit
    cannot itself leak a secret into a log or a report.
  * Vendored / generated / binary-heavy trees are skipped (see ``SKIP_DIRS``)
    so the invariant is about *our* committed source, not third-party fixtures.

A clean tree yields zero findings; the guard in ``test_capability.py`` asserts
exactly that AND that a synthetic secret is caught, so the check cannot pass
vacuously.

Usage:
    $PY -X utf8 -m tools.eval.key_hygiene [--out _eval_out/key_hygiene.md]
    # non-zero exit if any finding (usable as a pre-commit hook)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO = Path(__file__).resolve().parents[2]
EVAL_OUT = REPO / "_eval_out"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

# Trees that are third-party / generated / not our authored source.
SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", "external",
    "_demo_downloads", "_eval_out", "dist", "build", ".pytest_cache",
    ".mypy_cache", ".idea", ".vscode",
}
# File suffixes worth auditing (text source). Everything else is ignored.
SCAN_SUFFIXES = {
    ".py", ".ps1", ".sh", ".js", ".ts", ".json", ".yaml", ".yml",
    ".toml", ".md", ".env", ".txt", ".cfg", ".ini",
}

# name -> compiled pattern. Each is a *value* shape, not an identifier.
PATTERNS: Dict[str, re.Pattern] = {
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA|ABIA|ACCA|AIDA|AROA)[0-9A-Z]{16}\b"),
    "gcp_api_key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[0-9A-Za-z_\-]{10,}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "huggingface_token": re.compile(r"\bhuggingface_[A-Za-z0-9]{34,}\b"),
    "private_key_block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{24,}\b"),
    # long literal assigned to a secret-bearing name:  foo_api_key = "…"
    "secret_assignment": re.compile(
        r"(?i)\b[\w.\-]{0,40}(api[_\-]?key|secret|token|passwd|password)"
        r"[\w.\-]{0,20}\b\s*[=:]\s*[\"']([A-Za-z0-9._\-]{20,})[\"']"
    ),
}

# A single-line escape hatch for intentional, reviewed placeholders.
ALLOW_MARKER = "key-hygiene-allow"


def _mask(secret: str) -> str:
    """Show the shape, never the value, so reports/logs can't leak."""
    if len(secret) <= 8:
        return secret[:2] + "*" * (len(secret) - 2)
    return f"{secret[:4]}…{secret[-2:]} ({len(secret)} chars)"


def scan_text(text: str) -> List[Tuple[str, int, str]]:
    """Return (pattern_name, line_no, masked) for every secret literal in a
    string of source. Lines tagged with ``ALLOW_MARKER`` are skipped."""
    findings: List[Tuple[str, int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        for name, pat in PATTERNS.items():
            m = pat.search(line)
            if m:
                # For assignment patterns the secret is the value group.
                val = m.group(1) if name == "secret_assignment" and m.groups() else m.group(0)
                findings.append((name, lineno, _mask(val.strip())))
                break  # one finding per line is enough to fail
    return findings


def _iter_source(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = set(path.relative_to(root).parts[:-1])
        if rel_parts & SKIP_DIRS:
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        yield path


def scan_repo(root: Path = REPO) -> Dict[str, object]:
    """Audit every tracked source file under ``root``."""
    findings: List[Dict[str, object]] = []
    scanned = 0
    for path in _iter_source(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        for name, lineno, masked in scan_text(text):
            findings.append({
                "file": str(path.relative_to(root)).replace("\\", "/"),
                "line": lineno,
                "pattern": name,
                "masked": masked,
            })
    return {
        "root": str(root),
        "files_scanned": scanned,
        "findings": findings,
        "clean": not findings,
    }


def build_report(result: Dict[str, object]) -> str:
    stamp = _dt.date.today().isoformat()
    n = len(result["findings"])
    lines = [
        "# D-5 Key Hygiene Audit",
        "",
        f"_Generated {stamp} by `tools.eval.key_hygiene` (deterministic, model-free)._",
        "",
        f"- Source files scanned: **{result['files_scanned']}**",
        f"- Hard-coded credential findings: **{n}**",
        f"- Verdict: **{'CLEAN — no committed secrets' if result['clean'] else 'LEAK — reviewed literals found'}**",
        "",
        "Keys live only in environment variables (AGENTS.md secret policy); this",
        "audit scans for secret *values*, never variable *names*, and masks any",
        "match so running it cannot itself leak. Vendored/generated trees are skipped.",
    ]
    if n:
        lines += ["", "| file | line | pattern | masked match |", "|---|---|---|---|"]
        for f in result["findings"]:  # type: ignore[index]
            lines.append(f"| {f['file']} | {f['line']} | {f['pattern']} | {f['masked']} |")
    return "\n".join(lines) + "\n"


def run(out: Path | None = None, root: Path = REPO) -> Dict[str, object]:
    result = scan_repo(root)
    dest = out if out is not None else (EVAL_OUT / "key_hygiene.md")
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(build_report(result), encoding="utf-8")
        result["path"] = str(dest)
    except OSError:
        result["path"] = "(not written)"
    return result


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="D-5 deterministic key-hygiene audit")
    ap.add_argument("--out", default=None, help="report path (default _eval_out/key_hygiene.md)")
    ap.add_argument("--repo", default=str(REPO), help="root to scan")
    args = ap.parse_args(argv)
    out = Path(args.out) if args.out else None
    res = run(out=out, root=Path(args.repo))
    for f in res["findings"]:  # type: ignore[index]
        print(f"  LEAK {f['file']}:{f['line']} [{f['pattern']}] {f['masked']}")
    print(f"[key_hygiene] scanned {res['files_scanned']} files -> "
          f"{'CLEAN (0 findings)' if res['clean'] else str(len(res['findings'])) + ' FINDING(S)'}"
          f" -> {res['path']}")
    return 0 if res["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
