"""Run orchestrator for the local web dashboard (Phase F, WS-B) with resume memory.

Spawns a pipeline/eval CLI as a subprocess (`$PY -X utf8 -m <module>`), tails its
stdout line-by-line into an in-memory buffer + a per-run log file, and exposes
SSE consumption (`events()`) plus cooperative cancel (Windows process-tree kill).

Run memory (crash/disconnect survival):
  * every run is mirrored to `_eval_out/web_runs/runs.json` on each transition,
    so a server restart re-hydrates the history instead of losing it.
  * a run that was `pending`/`running` when the server died  is re-hydrated as
    `interrupted`; the CLI drivers (D drivers) persist per-row state in
    `_eval_out/ledgers/*.json`, so clicking Resume re-issues the same command
    and the driver *continues* rather than re-running from scratch.

Threading model: one thread per run reads the pipe; SSE readers poll the buffer
with a small keep-alive. Single-user localhost app — no cross-process locking.
"""
from __future__ import annotations

import json
import sys
import time
import uuid
import queue
import threading
import subprocess
from pathlib import Path
from typing import Dict, List, Iterator, Optional

WEB_DIR = Path(__file__).resolve().parent
REPO_ROOT = WEB_DIR.parents[1]
LOG_DIR = REPO_ROOT / "_eval_out" / "web_runs"
MANIFEST = LOG_DIR / "runs.json"
LOCK = threading.Lock()


def _now() -> float:
    return time.time()


def _tokenize(run: "Run") -> dict:
    return {
        "id": run.id,
        "title": run.title,
        "cmd": list(run.cmd),
        "env_profile": run.env_profile,
        "status": run.status,
        "returncode": run.returncode,
        "started": run.started,
        "finished": run.finished,
        "log_path": str(run.log_path),
    }


def _load_manifest() -> Dict[str, dict]:
    if not MANIFEST.is_file():
        return {}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_manifest(runs: Dict[str, "Run"]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST.with_suffix(".tmp")
    tmp.write_text(json.dumps({rid: _tokenize(r) for rid, r in runs.items()},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(MANIFEST)  # atomic — no torn manifest on crash


class Run:
    """A single background run: status + line buffer + log file."""

    def __init__(self, title: str, cmd: List[str], env_profile: str = "opencode-default"):
        self.id = uuid.uuid4().hex[:12]
        self.title = title
        self.cmd = cmd
        self.env_profile = env_profile
        self.status = "pending"  # pending | running | done | cancelled | failed | interrupted
        self.returncode: Optional[int] = None
        self.started = _now()
        self.finished: Optional[float] = None
        self.lines: List[str] = []
        self.cond = threading.Condition()
        self._proc: Optional[subprocess.Popen] = None
        self.log_path = LOG_DIR / f"{self.id}.log"
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        # A field to carry a replay for rehydrated runs (loaded from a log file,
        # not observed live) so the tail still shows something useful.
        self._replayed_from: Optional[Path] = None

    @classmethod
    def hydrate(cls, meta: dict) -> "Run":
        """Rebuild a Run from the manifest (server restart / crash recovery)."""
        r = cls(meta.get("title", "run"), list(meta.get("cmd") or []),
                meta.get("env_profile", "opencode-default"))
        r.id = meta.get("id", r.id)
        r.status = meta.get("status", "interrupted")
        r.returncode = meta.get("returncode")
        r.started = meta.get("started", r.started)
        r.finished = meta.get("finished")
        r._replayed_from = Path(meta.get("log_path", ""))
        # a live process cannot survive a server restart → mark interrupted
        if r.status in ("pending", "running"):
            r.status = "interrupted"
            r.finished = _now()
        return r

    # -- SSE helpers ---------------------------------------------------------

    def tail_from(self, start: int) -> tuple:
        """Return (lines_since_start, new_start, done)."""
        with self.cond:
            ln = len(self.lines)
            if ln <= start:
                return [], start, self.status in ("done", "cancelled", "failed")
            chunk = self.lines[start:]
            return chunk, ln, self.status in ("done", "cancelled", "failed")

    def append(self, line: str) -> None:
        with self.cond:
            self.lines.append(line.rstrip("\n"))
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(line)
            self.cond.notify_all()

    def replay(self) -> None:
        """Pre-fill the line buffer from a prior session's log file."""
        if not self._replayed_from or not self._replayed_from.is_file():
            return
        with self.cond:
            self.lines = [l.rstrip("\n") for l in self._replayed_from.read_text(
                encoding="utf-8", errors="replace").splitlines()]
            self.cond.notify_all()

    # -- lifecycle -----------------------------------------------------------

    def run(self) -> None:
        self.status = "running"
        manager.persist()
        self._proc = subprocess.Popen(
            self.cmd,
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        assert self._proc.stdout is not None
        try:
            for line in iter(self._proc.stdout.readline, ""):
                self.append(line)
        finally:
            rc = self._proc.wait()
            self.finished = _now()
            self.returncode = rc
            if self.status == "cancelled":
                pass
            elif rc == 0:
                self.status = "done"
            else:
                self.status = "failed"
            self.append(f"\n[run] exit code = {rc} ({self.status})\n")
            manager.persist()
            with self.cond:
                self.cond.notify_all()

    def cancel(self) -> str:
        """Kill the process tree (Windows taskkill /T /F), not just the parent —
        the opencode CLI and MinerU spawn children that must not orphan."""
        self.status = "cancelled"
        manager.persist()
        if self._proc and self._proc.poll() is None:
            try:
                subprocess.run(
                    ["taskkill", "/PID", str(self._proc.pid), "/T", "/F"],
                    capture_output=True, timeout=20,
                )
                self.append("\n[run] CANCELLED by user\n")
                return "cancelled"
            except Exception as e:  # noqa: BLE001
                self.append(f"\n[run] cancel failed: {e}\n")
                try:
                    self._proc.terminate()
                except Exception:
                    pass
                return "cancel-error"
        return "already-stopped"

    @property
    def elapsed(self) -> float:
        end = self.finished or _now()
        return end - self.started


class RunManager:
    def __init__(self) -> None:
        with LOCK:
            self.runs: Dict[str, Run] = {}
            for meta in _load_manifest().values():
                run = Run.hydrate(meta)
                run.replay()
                self.runs[run.id] = run

    def start(self, title: str, args: List[str], env_profile: str = "opencode-default") -> Run:
        cmd = [sys.executable, "-X", "utf8"] + args
        run = Run(title, cmd, env_profile)
        with LOCK:
            self.runs[run.id] = run
            _save_manifest(self.runs)
        threading.Thread(target=run.run, daemon=True, name=f"run-{run.id}").start()
        return run

    def resume(self, run: Run) -> Run:
        """Re-issue the same command as a fresh run; CLI drivers pick up their
        per-row ledger and continue from the last completed row."""
        return self.start(f"{run.title} (resume)", run.cmd[2:] if len(run.cmd) > 2 else run.cmd)

    def get(self, run_id: str) -> Optional[Run]:
        return self.runs.get(run_id)

    def cancel(self, run_id: str) -> Optional[str]:
        run = self.get(run_id)
        return run.cancel() if run else None

    def list(self) -> List[Run]:
        with LOCK:
            return sorted(self.runs.values(), key=lambda r: r.started, reverse=True)

    def persist(self) -> None:
        with LOCK:
            _save_manifest(self.runs)


manager = RunManager()