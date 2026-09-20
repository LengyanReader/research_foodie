"""WS-C Phase X self-evolution primitives — E-3 tickets · E-4 dependency
ledger · E-5 feedback corpus + promotion rules (Session 22).

Implements the design in `docs/design/self-evolution-mechanism.md`; the two
hard rules enforced here:
  (a) evolution triggers come ONLY from external measurement (health verdicts,
      gate coverage, variance, dep drift) — never model self-assessment;
  (b) every signal passes variance-aware thresholds before it can open a
      ticket or nominate a promotion (E-5 rule: N>=3 rounds, delta>=2sigma).

Everything in this module is zero-LLM and *writes only* under `_eval_out/`
(tickets · deps · feedback JSONL · revisions) — the loop never edits code or
prompts, never commits; promotion is a HUMAN-GATED ledger entry (E-3/E-5
"honest boundary" in PLAN §8 Phase X).

Artifacts:
    _eval_out/tickets.json         debug-ticket board (E-3), one screen to review
    _eval_out/deps_ledger.json     version & dependency ledger (E-4)
    _eval_out/feedback/*.jsonl     provenance-tagged feedback corpus (E-5)
    _eval_out/revisions.json       numbered prompt/judge revisions (E-5)
    _eval_out/evolution_log.jsonl  one dated line per cadence (E-3)
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_OUT = REPO_ROOT / "_eval_out"
TICKETS_F = EVAL_OUT / "tickets.json"
DEPS_F = EVAL_OUT / "deps_ledger.json"
FEEDBACK_DIR = EVAL_OUT / "feedback"
FEEDBACK_F = FEEDBACK_DIR / "feedback.jsonl"
REVISIONS_F = EVAL_OUT / "revisions.json"
LOG_F = EVAL_OUT / "evolution_log.jsonl"

ARXIV_PROBE = "https://export.arxiv.org/api/query?search_query=all:electron&max_results=1"


def _iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _today() -> str:
    return time.strftime("%Y-%m-%d")


def _load_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _dump_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, p)  # atomic — a crash never leaves a half-written board


# ---------------------------------------------------------------------------
# E-3 · debug tickets (symptom → measured delta → hypothesis → fix class)
# ---------------------------------------------------------------------------

# Heuristic fix-class from the check that failed (design rule: gate failures
# mean "fix the gate, not the prompt"; judge drift means "backend/prompt").
_FIX_CLASS = {
    "mock": "code regression",
    "gate_coverage": "gate (fix the gate, not the prompt)",
    "pools": "evidence/data (network or discovery)",
    "arxiv_probe": "environment/network",
    "deps": "environment/pin",
    "feedback": "data/corpus",
}


def load_tickets() -> Dict[str, Any]:
    return _load_json(TICKETS_F, {"tickets": [], "next_id": 1})


def open_ticket(board: Dict[str, Any], component: str, symptom: str,
                measured_delta: str = "", hypothesis: str = "",
                fix_class: str = "triage") -> Dict[str, Any]:
    """Open OR update-with-evidence a ticket for `component` (dedupe: one open
    ticket per component — cadences append evidence, they don't spam the board)."""
    for t in board["tickets"]:
        if t["status"] == "open" and t["component"] == component:
            t["evidence"].append({"date": _today(), "delta": measured_delta,
                                  "symptom": symptom[:200]})
            t["updated"] = _iso()
            return t
    t = {
        "id": board["next_id"], "component": component,
        "symptom": symptom[:300], "measured_delta": measured_delta,
        "hypothesis": hypothesis, "fix_class": fix_class,
        "status": "open", "opened": _today(), "updated": _iso(),
        "closed": None, "evidence": [{"date": _today(), "delta": measured_delta,
                                      "symptom": symptom[:200]}],
    }
    board["next_id"] += 1
    board["tickets"].append(t)
    return t


def close_ticket(board: Dict[str, Any], component: str, note: str) -> int:
    n = 0
    for t in board["tickets"]:
        if t["status"] == "open" and t["component"] == component:
            t["status"] = "closed"
            t["closed"] = _today()
            t["resolution"] = note
            n += 1
    return n


def tickets_from_verdicts(verdicts: List[Dict[str, str]]) -> Dict[str, List]:
    """E-3 core: FAIL/WARN open (or feed) a debug ticket; PASS closes a
    previously-open ticket for the same component (symptom did not reproduce).
    SKIP leaves tickets untouched (measurement absent ≠ fixed)."""
    board = load_tickets()
    actions = {"opened": [], "updated": [], "closed": []}
    for v in verdicts:
        comp = v["check"]
        if v["level"] in ("FAIL", "WARN"):
            prior = next((t for t in board["tickets"]
                          if t["status"] == "open" and t["component"] == comp), None)
            fc = next((cls for key, cls in _FIX_CLASS.items() if key in comp),
                      "judge/backend drift" if comp.startswith("judge") else "triage")
            t = open_ticket(board, comp, v["detail"], v["detail"], fix_class=fc)
            actions["updated" if prior else "opened"].append(t["id"])
        elif v["level"] == "PASS":
            n = close_ticket(board, comp, "PASS in cadence " + _today()
                             + " — symptom did not reproduce")
            if n:
                actions["closed"].append(comp)
    _dump_json(TICKETS_F, board)
    return actions


def open_tickets() -> List[Dict[str, Any]]:
    return [t for t in load_tickets()["tickets"] if t["status"] == "open"]


# ---------------------------------------------------------------------------
# E-4 · version & dependency ledger
# ---------------------------------------------------------------------------

def _cli_version(cmd: List[str], timeout: int = 20) -> str:
    """Probe a CLI's version line. Try a direct exec first; on Windows global
    tool shims (`opencode` -> npm `opencode.ps1`/`.cmd`, not on PATHEXT) the
    direct exec raises, so fall back to a shell which resolves the `.cmd`."""
    tries = [dict(args=cmd, shell=False),
             dict(args=" ".join(cmd), shell=True)]
    for t in tries:
        try:
            proc = subprocess.run(t["args"], capture_output=True, text=True,
                                  encoding="utf-8", timeout=timeout, shell=t["shell"])
            first = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
            if proc.returncode == 0 and first:
                return re.sub(r"\s+", " ", first[0])[:120]
        except Exception:  # noqa: BLE001 — missing/blocked tool is a finding, not a crash
            continue
    return ""


def _pkg_version(name: str) -> str:
    try:
        from importlib import metadata
        return metadata.version(name)
    except Exception:  # noqa: BLE001
        return ""


# severity: "required" missing → FAIL · "optional" missing → WARN · "info" → report only
PINS: List[Dict[str, Any]] = [
    {"name": "python", "how": lambda: platform.python_version(), "severity": "required"},
    {"name": "langgraph", "how": lambda: _pkg_version("langgraph"), "severity": "required"},
    {"name": "mineru", "how": lambda: _pkg_version("mineru") or _cli_version(["mineru", "--version"]),
     "severity": "required"},
    {"name": "opencode_cli", "how": lambda: _cli_version(["opencode", "--version"]),
     "severity": "required"},
    {"name": "default_model", "how": lambda: os.getenv("OPENCODE_MODEL") or "opencode/big-pickle",
     "severity": "info"},
    {"name": "pandoc", "how": lambda: _cli_version(["pandoc", "--version"]), "severity": "optional"},
    {"name": "xelatex", "how": lambda: _cli_version(["xelatex", "--version"]), "severity": "optional"},
    {"name": "paddleocr", "how": lambda: _pkg_version("paddleocr"), "severity": "optional"},
    {"name": "arxiv_api", "how": lambda: _arxiv_state(), "severity": "optional"},
]


def _arxiv_state() -> str:
    try:
        req = urllib.request.Request(ARXIV_PROBE, headers={"User-Agent": "research_foodie/0.1"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return "reachable" if r.status == 200 else "unreachable"
    except Exception:  # noqa: BLE001
        return "unreachable"


def verify_deps() -> Dict[str, Any]:
    """Re-probe every pinned tool; diff vs the last recorded ledger. Returns
    {"tools": {...}, "changed": [...], "missing_required": [...],
     "missing_optional": [...]}. Persists the new ledger (E-4)."""
    prev = _load_json(DEPS_F, {"tools": {}})
    before = prev.get("tools", {})
    now: Dict[str, Any] = {}
    changed: List[str] = []
    missing_required: List[str] = []
    missing_optional: List[str] = []
    for pin in PINS:
        name, sev = pin["name"], pin["severity"]
        try:
            ver = str(pin["how"]() or "").strip()
        except Exception as e:  # noqa: BLE001
            ver = ""
        entry = {
            "version": ver or "MISSING",
            "status": "ok" if ver else ("missing_required" if sev == "required"
                                        else "missing_optional"),
            "severity": sev,
            "first_seen": (before.get(name) or {}).get("first_seen") or _today(),
            "last_verified": _iso(),
        }
        if ver and (before.get(name) or {}).get("version") not in (None, entry["version"]):
            entry["changed_from"] = before[name]["version"]
            changed.append(name)
        if not ver:
            (missing_required if sev == "required" else
             missing_optional if sev == "optional" else changed).append(name) \
                if sev != "info" else None
        now[name] = entry
    _dump_json(DEPS_F, {"as_of": _iso(), "tools": now})
    return {"tools": now, "changed": changed,
            "missing_required": missing_required,
            "missing_optional": missing_optional}


# ---------------------------------------------------------------------------
# E-5 · provenance-tagged feedback corpus + anti-collapse quota
# ---------------------------------------------------------------------------

GOLD_QUOTA_SHARE = 0.5  # >=50% of corpus rows must carry a real-gold anchor
GOLD_QUOTA_MIN = 10     # ...over at least this many rows before the quota bites


def _artifact_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:12]


def append_feedback(kind: str, subject: str, summary: Any,
                    provenance: Optional[Dict[str, Any]] = None,
                    gold_anchored: bool = False,
                    artifact: str = "", note: str = "") -> Dict[str, Any]:
    """One JSONL row in the E-5 corpus. `kind`: judged_run | user_correction |
    gate_reject | cadence_note. Every row is provenance-tagged (model/profile)
    and gold-anchored when a real primary-source check backs it — the
    anti-model-collapse rule (Seddik et al. 2404.05090)."""
    rec = {
        "ts": _iso(), "kind": kind, "subject": subject,
        "provenance": provenance or {},
        "gold_anchored": bool(gold_anchored),
        "artifact_sha": _artifact_hash(artifact) if artifact else "",
        "summary": summary, "note": note[:300],
    }
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    with FEEDBACK_F.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def feedback_stats() -> Dict[str, Any]:
    """Corpus size + real-gold share (the quota that guards against evolving on
    self-generated signals only). WARN if below floor once the corpus is big
    enough for the share to mean anything."""
    rows: List[Dict[str, Any]] = []
    if FEEDBACK_F.is_file():
        for line in FEEDBACK_F.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except ValueError:
                continue
    n = len(rows)
    gold = sum(1 for r in rows if r.get("gold_anchored"))
    share = gold / n if n else 0.0
    enforce = n >= GOLD_QUOTA_MIN
    return {"n": n, "gold": gold, "share": round(share, 3),
            "quota_ok": (share >= GOLD_QUOTA_SHARE) if enforce else True,
            "enforced": enforce}


# ---------------------------------------------------------------------------
# E-5 · promotion rule + numbered revisions (human-gated ledger)
# ---------------------------------------------------------------------------

PROMOTION_MIN_ROUNDS = 3   # N >= 3 cadence rounds of the same signal
PROMOTION_MIN_SIGMA = 2.0  # delta >= 2 * recorded judge sigma


def promotion_check(component: str, current_mean: Optional[float],
                    baseline_mean: Optional[float], sigma: Optional[float],
                    n_rounds: int, regression_ok: bool = True) -> Dict[str, Any]:
    """Apply the E-5 promotion rule WITHOUT touching anything: a candidate
    prompt/judge revision is *eligible* only on a sustained, variance-aware,
    non-regressing signal. Output feeds the sprint report; a human promotes."""
    rule = {"min_rounds": PROMOTION_MIN_ROUNDS, "min_sigma": PROMOTION_MIN_SIGMA,
            "no_mock_or_gold_regression": True}
    if None in (current_mean, baseline_mean, sigma) or sigma in (None, 0):
        return {"component": component, "verdict": "insufficient_data", "rule": rule,
                "detail": "need current/baseline means and a non-zero recorded sigma"}
    delta = current_mean - baseline_mean
    sig = abs(delta) / sigma
    if n_rounds < PROMOTION_MIN_ROUNDS:
        verdict = "not_yet"
    elif sig < PROMOTION_MIN_SIGMA or not regression_ok:
        verdict = "noise" if sig < PROMOTION_MIN_SIGMA else "blocked_regression"
    else:
        verdict = "eligible"
    return {"component": component, "verdict": verdict, "delta": round(delta, 3),
            "sigmas": round(sig, 2), "n_rounds": n_rounds, "rule": rule,
            "detail": f"delta {delta:+.2f} = {sig:.1f} sigma over {n_rounds} rounds"}


def load_revisions() -> Dict[str, Any]:
    return _load_json(REVISIONS_F, {"revisions": {}})


def bump_revision(component: str, evidence: Dict[str, Any], actor: str = "user") -> Dict[str, Any]:
    """Record a NUMBERED revision (matrix v1 -> v2) for `component`. Ledger
    only — the code/prompt edit itself is the human's, after explicit
    green-light (AGENTS.md no-unsolicited-change policy)."""
    reg = load_revisions()
    cur = reg["revisions"].get(component, {"revision": 0, "history": []})
    nxt = int(cur.get("revision", 0)) + 1
    entry = {"revision": nxt, "promoted_at": _iso(), "actor": actor,
             "evidence": evidence, "history": cur.get("history", []) + [
                 {"revision": cur.get("revision"), "at": cur.get("promoted_at")}]}
    reg["revisions"][component] = entry
    _dump_json(REVISIONS_F, reg)
    return entry


# ---------------------------------------------------------------------------
# E-3 · cadence log (one dated line per sprint, feeds drift history)
# ---------------------------------------------------------------------------

def log_cadence(entry: Dict[str, Any]) -> None:
    entry = dict(entry, ts=_iso())
    EVAL_OUT.mkdir(parents=True, exist_ok=True)
    with LOG_F.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cadence_history(limit: int = 12) -> List[Dict[str, Any]]:
    if not LOG_F.is_file():
        return []
    lines = LOG_F.read_text(encoding="utf-8").splitlines()[-limit:]
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def sustained_signal(component: str, levels=("WARN", "FAIL"), min_cadences: int = 3) -> int:
    """How many of the most recent cadence lines flagged `component` at one of
    `levels` — the N-in-a-row counter behind promotion_check's n_rounds."""
    hist = cadence_history(min_cadences)
    streak = 0
    for e in reversed(hist):
        flagged = any(v.get("check") == component and v.get("level") in levels
                      for v in (e.get("verdicts") or []))
        if flagged:
            streak += 1
        else:
            break
    return streak


if __name__ == "__main__":  # tiny zero-LLM self-probe
    print(json.dumps({"deps": verify_deps()["tools"] and "ok",
                      "tickets": load_tickets(), "feedback": feedback_stats()},
                     ensure_ascii=False, indent=1)[:1500])
