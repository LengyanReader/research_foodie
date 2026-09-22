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

# Two render flavors from the SAME .md source ("一套源·双渲染"):
#   plain    — reading-grade default: dense, 11pt, 2cm margins, blue links.
#   preprint — arXiv preprint style: A4 2.6cm margins, 10pt, numbered sections,
#              neutral links, centred title/author/date block (publication look).
_STYLES = {
    "plain": {
        "geometry": "margin=2cm", "fontsize": "11pt", "linkcolor": "blue",
        "number_sections": False,
    },
    "preprint": {
        "geometry": "margin=2.6cm", "fontsize": "10pt", "linkcolor": "black",
        "number_sections": True,
    },
}


def render_to_pdf(md_path, pdf_path, title: str = "", style: str = "plain",
                  author: str = "", date: str = "") -> int:
    """Return page count (0 if rendering failed).

    `style` is one of `_STYLES`. `author`/`date` only apply to the preprint
    flavour (arXiv needs a title/author/date block; the plain read keeps none).
    """
    if not (_PANDOC and _PDF_ENGINE):
        return 0
    cfg = _STYLES.get(style, _STYLES["plain"])
    cmd = [
        _PANDOC, str(md_path), "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "-f", "markdown+pipe_tables",
        "-V", "CJKmainfont=" + YAYA,
        "-V", "CJKoptions=Scale=0.9",
        "-V", f"geometry:{cfg['geometry']}",
        "-V", f"fontsize={cfg['fontsize']}",
        "-V", "colorlinks=true",
        "-V", f"linkcolor={cfg['linkcolor']}",
        "-V", "urlcolor=black",
        "-V", "papersize=a4",
    ]
    if cfg["number_sections"]:
        cmd += ["--number-sections"]
    if title:
        cmd += ["-V", f"title={title}", "--metadata", f"title={title}"]
    if author:
        cmd += ["-V", f"author={author}", "--metadata", f"author={author}"]
    if date:
        cmd += ["-V", f"date={date}", "--metadata", f"date={date}"]
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
    import argparse
    ap = argparse.ArgumentParser(description="render a Markdown manuscript to PDF")
    ap.add_argument("md")
    ap.add_argument("out")
    ap.add_argument("--title", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--style", choices=list(_STYLES), default="plain")
    args = ap.parse_args(argv)
    pages = render_to_pdf(Path(args.md), Path(args.out), title=args.title,
                          style=args.style, author=args.author, date=args.date)
    if not pages:
        print("render_manuscript: FAILED", file=sys.stderr)
        return 1
    print(f"OUT {args.out} PAGES {pages} STYLE {args.style}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())