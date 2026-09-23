"""Knowledge library — durable index + user state over the manuscript corpus.

Files are the source of truth (`_eval_out/manuscripts/` and `mock_manuscripts/`);
SQLite (stdlib, no new deps) holds a derived *index* plus *user state* (tags,
favorite, deletions). `sync()` re-scans the disk and upserts/purges so the
library always mirrors what actually exists.

Schema (items):
  key           TEXT PK   — artifact base name, e.g. "P-A_manuscript"
  kind          TEXT      — 'survey' | 'mock-survey' | 'bench'
  title         TEXT      — human title (run title or bare filename)
  question      TEXT      — survey question when known
  path_md       TEXT      — relative path of the markdown source ("" if none)
  path_pdf      TEXT      — relative path of the dry-goods PDF ("" if none)
  path_preprint TEXT      — relative path of the preprint PDF ("" if none)
  status        TEXT      — 'done' (only finished work is indexed)
  mode          TEXT      — 'real' | 'mock' (survey provenance)
  verdict       TEXT      — 'pass' | 'fail' | ''
  judge         TEXT      — mean judge score when recorded
  claims        INTEGER   — grounded-claim count from the survey summary
  papers        INTEGER   — papers cited from the survey summary
  elapsed_s     REAL      — survey duration in seconds
  tags          TEXT      — comma-separated user tags
  favorite      INTEGER   — 0/1
  created_at    REAL      — first seen (unix)
  updated_at    REAL      — last sync touch (unix)
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Optional

from .run_manager import manager, REPO_ROOT

EVAL_OUT = REPO_ROOT / "_eval_out"
DB_PATH = EVAL_OUT / "knowledge.db"
PREFIX_MD = "path_md"
PREFIX_PDF = "path_pdf"
PREFIX_PREPRINT = "path_preprint"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  key           TEXT PRIMARY KEY,
  kind          TEXT NOT NULL DEFAULT 'bench',
  title         TEXT NOT NULL DEFAULT '',
  question      TEXT NOT NULL DEFAULT '',
  path_md       TEXT NOT NULL DEFAULT '',
  path_pdf      TEXT NOT NULL DEFAULT '',
  path_preprint TEXT NOT NULL DEFAULT '',
  status        TEXT NOT NULL DEFAULT 'done',
  mode          TEXT NOT NULL DEFAULT '',
  verdict       TEXT NOT NULL DEFAULT '',
  judge         TEXT NOT NULL DEFAULT '',
  claims        INTEGER NOT NULL DEFAULT 0,
  papers        INTEGER NOT NULL DEFAULT 0,
  elapsed_s     REAL NOT NULL DEFAULT 0,
  tags          TEXT NOT NULL DEFAULT '',
  favorite      INTEGER NOT NULL DEFAULT 0,
  created_at    REAL NOT NULL DEFAULT 0,
  updated_at    REAL NOT NULL DEFAULT 0
);
"""

_ITEM_FIELDS = ("key", "kind", "title", "question", "path_md", "path_pdf",
                "path_preprint", "status", "mode", "verdict", "judge",
                "claims", "papers", "elapsed_s", "tags", "favorite",
                "created_at", "updated_at")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init() -> None:
    with _connect() as c:
        c.executescript(_SCHEMA)


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["favorite"] = bool(d.get("favorite"))
    return d


# --------------------------------------------------------------------------
# Scanning & sync
# --------------------------------------------------------------------------

def _survey_summaries() -> Dict[str, dict]:
    """Map manuscript basename → `[survey-result]` summary from live run logs."""
    out: Dict[str, dict] = {}
    for run in manager.list():
        for ln in reversed(run.lines):
            if ln.startswith("[survey-result] "):
                try:
                    s = json.loads(ln[len("[survey-result] "):].strip())
                except Exception:
                    continue
                for p in (s.get("manuscript") or ""):
                    if p:
                        out.setdefault(Path(p).stem, s)
                break
    return out


def _scan_disk() -> List[dict]:
    """Enumerate the manuscript corpus into raw item candidates."""
    surveys = _survey_summaries()
    items: Dict[str, dict] = {}
    for d in (EVAL_OUT / "manuscripts", EVAL_OUT / "mock_manuscripts"):
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if not f.is_file():
                continue
            rel = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
            base = f.stem
            # preprint files (name.preprint.pdf) attach to their base, not a new item
            if f.suffix.lower() != ".pdf" or base.endswith(".preprint"):
                if base.endswith(".preprint"):
                    root_item = items.get(base[: -len(".preprint")])
                    if root_item is not None:
                        root_item["path_preprint"] = rel
                    continue
                it = items.setdefault(base, {"key": base, "title": base,
                                             "kind": "bench", "question": "",
                                             "path_md": "", "path_pdf": "",
                                             "path_preprint": "",
                                             "mode": "", "verdict": "", "judge": "",
                                             "claims": 0, "papers": 0, "elapsed_s": 0.0})
                it["path_md"] = rel
            else:
                it = items.setdefault(base, {"key": base, "title": base,
                                             "kind": "bench", "question": "",
                                             "path_md": "", "path_pdf": "",
                                             "path_preprint": "",
                                             "mode": "", "verdict": "", "judge": "",
                                             "claims": 0, "papers": 0, "elapsed_s": 0.0})
                it["path_pdf"] = rel
    # enrich survey provenance from run summaries
    for base, it in items.items():
        s = surveys.get(base)
        if not s:
            continue
        it["kind"] = "survey" if s.get("mode") != "mock" else "mock-survey"
        it["title"] = it["title"] if it["question"] else (s.get("question") or it["title"])
        it["question"] = s.get("question", it["question"])
        it["mode"] = s.get("mode", it["mode"])
        it["verdict"] = "pass" if s.get("gate_passed") else "fail"
        it["judge"] = s.get("judge_label") or s.get("judge") or ""
        it["claims"] = int(s.get("claims", 0) or 0)
        it["papers"] = int(s.get("n_papers_cited", 0) or 0)
        it["elapsed_s"] = float(s.get("elapsed_s", 0) or 0)
    return sorted(items.values(), key=lambda i: i["key"].lower())


def sync() -> List[dict]:
    """Refresh the index from disk (upsert new/changed, purge gone rows)."""
    _init()
    now = time.time()
    fresh = _scan_disk()
    seen: set[str] = set()
    with _connect() as c:
        for it in fresh:
            seen.add(it["key"])
            c.execute(
                """INSERT INTO items (key, kind, title, question, path_md, path_pdf,
                   path_preprint, status, mode, verdict, judge, claims, papers,
                   elapsed_s, tags, favorite, created_at, updated_at)
                   VALUES (:key,:kind,:title,:question,:path_md,:path_pdf,
                   :path_preprint,'done',:mode,:verdict,:judge,:claims,:papers,
                   :elapsed_s, COALESCE((SELECT tags FROM items WHERE key=:key),''),
                   COALESCE((SELECT favorite FROM items WHERE key=:key),0),
                   COALESCE((SELECT created_at FROM items WHERE key=:key),:now), :now)
                ON CONFLICT(key) DO UPDATE SET
                   title=excluded.title, question=excluded.question,
                   path_md=excluded.path_md, path_pdf=excluded.path_pdf,
                   path_preprint=excluded.path_preprint, status='done',
                   mode=excluded.mode, verdict=excluded.verdict, judge=excluded.judge,
                   claims=excluded.claims, papers=excluded.papers,
                   elapsed_s=excluded.elapsed_s, updated_at=excluded.updated_at""",
                {**it, "now": now},
            )
        # purge rows whose files no longer exist
        cur = c.execute("SELECT key, path_md, path_pdf, path_preprint FROM items")
        for row in cur.fetchall():
            alive = False
            for p in (row["path_md"], row["path_pdf"], row["path_preprint"]):
                if p and (REPO_ROOT / Path(p)).is_file():
                    if Path(p).stem == row["key"] or Path(p).name.startswith(row["key"]):
                        alive = True
                        break
            if not alive:
                c.execute("DELETE FROM items WHERE key=?", (row["key"],))
    return _list()


# --------------------------------------------------------------------------
# Queries & CRUD
# --------------------------------------------------------------------------

def _list() -> List[dict]:
    _init()
    with _connect() as c:
        rows = c.execute("SELECT * FROM items ORDER BY created_at DESC, key").fetchall()
    return [_row_to_dict(r) for r in rows]


def get(key: str) -> Optional[dict]:
    _init()
    with _connect() as c:
        row = c.execute("SELECT * FROM items WHERE key=?", (key,)).fetchone()
    return _row_to_dict(row) if row else None


def set_tags(key: str, tags: List[str]) -> Optional[dict]:
    _init()
    clean = [t.strip() for t in tags if t and t.strip()]
    clean = list(dict.fromkeys(clean))
    with _connect() as c:
        c.execute("UPDATE items SET tags=?, updated_at=? WHERE key=?",
                  (", ".join(clean), time.time(), key))
    return get(key)


def toggle_favorite(key: str) -> Optional[dict]:
    _init()
    with _connect() as c:
        c.execute("UPDATE items SET favorite = 1 - favorite, updated_at=? WHERE key=?",
                  (time.time(), key))
    return get(key)


def files_of(item: dict) -> List[Path]:
    """Resolve the item's declared files (absolute). Delete must stay scoped."""
    out: List[Path] = []
    for p in (item.get("path_md"), item.get("path_pdf"), item.get("path_preprint")):
        if p:
            abs_p = (REPO_ROOT / Path(p)).resolve()
            if abs_p.is_file():
                out.append(abs_p)
    return out


def delete_item(key: str) -> dict:
    """Remove the index row and the item's declared files on disk.

    Files are removed *only* for paths recorded in this row — never a directory
    sweep. Run logs under `_eval_out/web_runs/` are never touched.
    """
    _init()
    item = get(key)
    if not item:
        return {"ok": False, "error": "not found"}
    paths = files_of(item)
    for p in paths:
        try:
            p.unlink()
        except OSError:
            pass
    with _connect() as c:
        c.execute("DELETE FROM items WHERE key=?", (key,))
    return {"ok": True, "deleted": [str(p) for p in paths]}