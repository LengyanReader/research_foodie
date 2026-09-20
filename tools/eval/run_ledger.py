"""
Durable resume ledger for long CLI runs (WS-F run memory).

Solves "跑到一半断线了/死机了 → 重开后应该可以继续". Each driver (bench_eval,
variance_run, pools battery, etc.) writes one row per scenario as soon as the
row is produced, so an interrupted run leaves a truthful record on disk; on
restart the driver opens the same ledger, skips already-done ids, and continues
with the remainder instead of re-paying LLM cost from scratch.

Layout under _eval_out/ledgers/:
    bench_eval.json          # {fingerprint: ledger}  — one entry per run profile+idset
    <driver>.json            # same shape for other drivers

Each ledger:
    {
      "command": "bench_eval",
      "fingerprint": "free-opencode|P-A,P-B,P-C",   # profile + exact idset → a rerun
                                                    # with different models/ids must NOT resume
      "run_id": "uuid12",
      "status": "running" | "done" | "interrupted",
      "started_at": "iso", "updated_at": "iso",
      "done": {"P-A": {row}, "P-B": {row}}           # completed rows (JSON-safe)
    }
"""
from __future__ import annotations

import json
import os
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

LEDGER_DIR = Path(__file__).resolve().parents[2] / "_eval_out" / "ledgers"

_STATUSES = ("running", "done", "interrupted")


def _iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


class ResumeLedger:
    """Persistent per-driver resume state, written atomically on each mutation.

    Usage (driver side):
        led = ResumeLedger.open("bench_eval", fingerprint)   # reuse if resumable
        remaining = led.pending(ids)
        for tid in remaining:
            row = run_one(tid)
            led.record(tid, row)                            # durable immediately
        led.finish("done")  # or "interrupted" on exception / Ctrl-C
    """

    _lock = threading.Lock()

    def __init__(self, command: str, fingerprint: str, data: Optional[dict] = None):
        self.command = command
        self.fingerprint = fingerprint
        self.path = LEDGER_DIR / f"{command}.json"
        self.data = data or self._blank()
        self.data["command"] = command
        self.data["fingerprint"] = fingerprint

    @staticmethod
    def _blank() -> dict:
        return {
            "run_id": uuid.uuid4().hex[:12],
            "status": "running",
            "started_at": _iso(),
            "updated_at": _iso(),
            "done": {},
        }

    # ----- constructors -----------------------------------------------------

    @classmethod
    def open(cls, command: str, fingerprint: str, force: bool = False) -> "ResumeLedger":
        """Reuse an interrupted/running ledger for the same fingerprint (continue),
        or start fresh. `force=True` always starts a fresh run."""
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        prior = cls._load(command)
        if not force and prior and prior.get("fingerprint") == fingerprint:
            # a `done` ledger is *also* reuseable: the caller still decides via
            # pending() which rows are missing (none → instant no-op report).
            return cls(command, fingerprint, prior)
        return cls(command, fingerprint)

    @classmethod
    def _load(cls, command: str) -> Optional[dict]:
        p = LEDGER_DIR / f"{command}.json"
        if not p.is_file():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    @classmethod
    def status_files(cls) -> List[str]:
        """Ledger file names for the dashboard (read-only summary)."""
        if not LEDGER_DIR.is_dir():
            return []
        return sorted(f.name for f in LEDGER_DIR.glob("*.json"))

    # ----- state ------------------------------------------------------------

    def status(self) -> str:
        return self.data.get("status", "running")

    def done(self) -> Dict[str, dict]:
        return self.data.get("done", {})

    def pending(self, ids: List[str]) -> List[str]:
        done = self.done()
        return [i for i in ids if i not in done]

    def is_done(self, tid: str) -> bool:
        return tid in self.done()

    def as_summary(self) -> dict:
        return {
            "command": self.command,
            "fingerprint": self.fingerprint,
            "run_id": self.data.get("run_id"),
            "status": self.status(),
            "started_at": self.data.get("started_at"),
            "updated_at": self.data.get("updated_at"),
            "n_done": len(self.done()),
            "done_ids": sorted(self.done()),
        }

    # ----- mutation (atomic write after each change) -------------------------

    def record(self, tid: str, row: dict) -> None:
        with self._lock:
            self.data["done"][tid] = row
            self._touch()

    def finish(self, status: str = "done") -> None:
        assert status in _STATUSES, status
        with self._lock:
            self.data["status"] = status
            if status != "running":
                self.data["updated_at"] = _iso()
            self._touch()

    def _touch(self) -> None:
        self.data["updated_at"] = _iso()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, self.path)  # atomic — a crash never yields a half-written ledger