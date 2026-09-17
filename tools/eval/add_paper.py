"""Add one arXiv paper to the local MinerU corpus + qa/bench pool — one command.

Replaces the 10-step manual drill (download → pypdf count → windowed `-m txt`
parses with retry/sub-split → merge → register) that Sessions 12–19 did by hand.
Codifies the two known MinerU workarounds:
  * page-window runs MUST use distinct `-o` output dirs (else later windows
    silently overwrite earlier ones);
  * a window that fails 3x gets sub-split (halved) and retried.

Usage:
  $PY -X utf8 -m tools.eval.add_paper 1908.10084 --name sbert
Prints the dictionary entries to add to `tools/pipeline/corpus._LOCAL_MD`
(registering is intentionally left to an explicit edit — a deliberate 2-line
safety step so the corpus mapping never gets silently mutated).

Output lands at `_demo_downloads/{id}.pdf`
and `_demo_downloads/mineru_out_ds0509/{id}/{id}.md`.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from pypdf import PdfReader

MINERU = Path(r"C:\Users\data\miniconda3\envs\ds0509\Scripts\mineru.exe")
MINERU_OUT = Path("_demo_downloads/mineru_out_ds0509")
MAX_WINDOW = 6


def _download(arxiv_id: str, dst: Path) -> Path:
    url = f"https://export.arxiv.org/pdf/{arxiv_id}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urlopen(req, timeout=120).read()
    dst.write_bytes(data)
    return dst


def _parse_window(pdf: Path, out_dir: Path, start: int, end: int, max_tries: int = 3) -> bool:
    mds = list(out_dir.rglob("*.md"))
    if mds:
        return True
    out_dir.mkdir(parents=True, exist_ok=True)
    for _ in range(max_tries):
        subprocess.run(
            [str(MINERU), "-p", str(pdf), "-o", str(out_dir.absolute()),
             "-b", "pipeline", "-m", "txt", "-s", str(start), "-e", str(end)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
            cwd=str(Path.cwd()),
        )
        if list(out_dir.rglob("*.md")):
            return True
    return False


def _parse(pdf: Path, arxiv_id: str) -> Path:
    """Windowed parse with sub-split recovery; returns the merged md."""
    pages = len(PdfReader(str(pdf)).pages)
    windows = [(s, min(s + MAX_WINDOW - 1, pages - 1)) for s in range(0, pages, MAX_WINDOW)]
    print(f"[add_paper] {arxiv_id}: {pages} pages -> windows {windows}")
    done: list[tuple[int, int, Path]] = []
    pending = list(windows)
    while pending:
        s, e = pending.pop(0)
        tag = f"w{s:02d}_{e:02d}"
        out = MINERU_OUT / arxiv_id / tag
        if _parse_window(pdf, out, s, e):
            mds = sorted(out.rglob("*.md"))
            if mds:
                done.append((s, e, mds[0]))
                print(f"  ok   {s}-{e}")
                continue
        if e - s <= 1:
            print(f"  FAIL {s}-{e} (leaf window, giving up)")
            continue
        mid = (s + e) // 2
        pending.insert(0, (mid + 1, e))
        pending.insert(0, (s, mid))
        print(f"  sub-splitting {s}-{e} -> {s}-{mid} + {mid+1}-{e}")
    if not done:
        raise SystemExit(f"[add_paper] no parse produced for {arxiv_id}")
    # merge in page order
    parts = [p.read_text(encoding="utf-8").rstrip() for _, _, p in sorted(done)]
    merged = MINERU_OUT / arxiv_id / f"{arxiv_id}.md"
    merged.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"[add_paper] merged -> {merged} ({len(merged.read_text(encoding='utf-8'))} chars)")
    return merged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("arxiv_id")
    ap.add_argument("--name", default=None, help="optional human label for the dict comment")
    args = ap.parse_args()
    pdf = Path("_demo_downloads") / f"{args.arxiv_id}.pdf"
    _download(args.arxiv_id, pdf)
    print(f"[add_paper] pdf: {pdf} ({pdf.stat().st_size} B)")
    _parse(pdf, args.arxiv_id)
    meta = f'"{args.arxiv_id}": "{args.arxiv_id}/{args.arxiv_id}.md",  # {args.name or ""}'
    print("\n[add_paper] add to tools/pipeline/corpus._LOCAL_MD:\n    " + meta.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())