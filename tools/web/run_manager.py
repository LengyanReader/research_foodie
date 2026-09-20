"""In-memory run orchestrator for the local web dashboard (Phase F, WS-B).

Spawns a pipeline/eval CLI as a subprocess (`$PY -X utf8 -m <module>`), tails its
stdout line-by-line into an in-memory buffer + a per-run log file, and exposes
SSE consumption (`events()`) plus cooperative cancel (Windows process-tree kill).

Threading model: one thread per run reads the pipe; SSE readers poll the buffer
with a small keep-alive. Single-user localhost app — no cross-process locking.
"""
from __future__ import annotations

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


class Run:
    """A single background run: status + line buffer + log file."""

    def __init__(self, title: str, cmd: List[str], env_profile: str = "opencode-default"):
        self.id = uuid.uuid4().hex[:12]
        self.title = title
        self.cmd = cmd
        self.env_profile = env_profile
        self.status = "pending"  # pending | running | done | cancelled | failed
        self.returncode: Optional[int] = None
        self.started = time.time()
        self.finished: Optional[float] = None
        self.lines: List[str] = []
        self.cond = threading.Condition()
        self._proc: Optional[subprocess.Popen] = None
        self.log_path = LOG_DIR / f"{self.id}.log"
        LOG_DIR.mkdir(parents=True, exist_ok=True)

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

    # -- lifecycle -----------------------------------------------------------

    def run(self) -> None:
        self.status = "running"
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
            self.finished = time.time()
            self.returncode = rc
            if self.status == "cancelled":
                pass
            elif rc == 0:
                self.status = "done"
            else:
                self.status = "failed"
            self.append(f"\n[run] exit code = {rc} ({self.status})\n")
            with self.cond:
                self.cond.notify_all()

    def cancel(self) -> str:
        """Kill the process tree (Windows taskkill /T /F), not just the parent —
        the opencode CLI and MinerU spawn children that must not orphan."""
        self.status = "cancelled"
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
        end = self.finished or time.time()
        return end - self.started


class RunManager:
    def __init__(self) -> None:
        self.runs: Dict[str, Run] = {}
        self.lock = threading.Lock()

    def start(self, title: str, args: List[str], env_profile: str = "opencode-default") -> Run:
        cmd = [sys.executable, "-X", "utf8"] + args
        run = Run(title, cmd, env_profile)
        with self.lock:
            self.runs[run.id] = run
        threading.Thread(target=run.run, daemon=True, name=f"run-{run.id}").start()
        return run

    def get(self, run_id: str) -> Optional[Run]:
        return self.runs.get(run_id)

    def cancel(self, run_id: str) -> Optional[str]:
        run = self.get(run_id)
        return run.cancel() if run else None

    def list(self) -> List[Run]:
        with self.lock:
            return sorted(self.runs.values(), key=lambda r: r.started, reverse=True)


manager = RunManager()