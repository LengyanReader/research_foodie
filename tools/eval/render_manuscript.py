"""Render a Markdown research-manuscript to PDF via pandoc + xelatex (CJK).

MAR (DAS-16 "Manuscript Appearance" family) is scored against a *rendered*
manuscript; the pipeline artifact is Markdown, so this turns it into a PDF for
the benchmark judge. Uses the already-installed pandoc + MiKTeX xelatex with
the Microsoft YaHei CJK font (Windows) so the bilingual EN+中文 drafts render.

Usage:
    & $PY -m tools.eval.render_manuscript <input.md> <output.pdf>

Prints `OUT <pdf> PAGES <n>` on success (exit 0) and nothing on failure with a
non-zero exit (so callers treat the PDF as best-effort).
"""
from __future__ import annotations

import shutil
import subprocess
import sys

_PDF_ENGINE = shutil.which("xelatex")
_PANDOC = shutil.which("pandoc")
YAYA = "Microsoft YaHei"


def render_to_pdf(md_path, pdf_path, title: str = "") -> int:
    """Return page count (0 if rendering failed)."""
    if not (_PANDOC and _PDF_ENGINE):
        return 0
    cmd = [
        _PANDOC, str(md_path), "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "-f", "markdown+pipe_tables",
        "-V", "CJKmainfont=" + YAYA,
        "-V", "geometry:margin=2cm",
        "-V", "fontsize=11pt",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "CJKoptions=Scale=0.9",
    ]
    if title:
        cmd += ["-V", f"title={title}", "--metadata", f"title={title}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (subprocess.TimeoutExpired, OSError):
        return 0
    if r.returncode != 0 or not pdf_path.is_file() or pdf_path.stat().st_size < 500:
        return 0
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return 0


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) < 2:
        print(__doc__)
        return 2
    from pathlib import Path
    md_path = Path(argv[0])
    pdf_path = Path(argv[1])
    title = argv[2] if len(argv) > 2 else ""
    pages = render_to_pdf(md_path, pdf_path, title=title)
    if not pages:
        print("render_manuscript: FAILED", file=sys.stderr)
        return 1
    print(f"OUT {pdf_path} PAGES {pages}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())