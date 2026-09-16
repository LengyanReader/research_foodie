"""
Integration test for the P2 minimal-vertical pipeline (S_lit discovery → graph → L6 gate).

Modes:
  mock  — ephemeral mock OpenAI server; validates discovery, graph structure,
          claim parsing, and the deterministic L6 gate end-to-end (seconds).
  real  — opencode CLI free model (default `opencode/big-pickle`); full LLM
          integration (minutes).

Usage:
  python -m tools.pipeline.test_pipeline mock
  python -m tools.pipeline.test_pipeline real [MODEL]

Exits 0 on full pass, 1 on any failure.
"""
from __future__ import annotations

import io
import json
import socket
import subprocess
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tools.llm.client import LLMClient, Message  # noqa: E402
from tools.pipeline.graph import Pipeline         # noqa: E402

# ---------------------------------------------------------------------------
# Demo input (MinerU-parsed Liang 2023)
# ---------------------------------------------------------------------------
MD_PATH = "_demo_downloads/mineru_out_ds0509/liang2023_test/auto/liang2023_test.md"
PAPER_ID = "2304.02819"          # Liang et al. 2023 (matched by discovery)
QUESTION = "GPT detectors bias against non-native English writers"


def _free_port() -> int:
    s = socket.socket(); s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]; s.close(); return port


def _start_mock(port: int) -> subprocess.Popen:
    proc = subprocess.Popen(
        [sys.executable, "-m", "tools.llm.mock_openai_server",
         "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    base = f"http://127.0.0.1:{port}/v1"
    deadline = time.time() + 20
    c = LLMClient(backend="openai", base_url=base, model="mock")
    while time.time() < deadline:
        if c.is_reachable():
            return proc
        time.sleep(0.3)
    raise RuntimeError("mock server did not start")


# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------

def _assert(cond: bool, msg: str, failures: list) -> None:
    if not cond:
        failures.append(msg)
        print(f"  FAIL: {msg}", flush=True)
    else:
        print(f"  PASS: {msg}", flush=True)


def _run_test(client: LLMClient, mode: str) -> int:
    pipeline = Pipeline(client, max_revisions=2)
    t0 = time.time()
    result = pipeline.run(question=QUESTION)   # discovery-led entry
    elapsed = time.time() - t0

    failures: list[str] = []

    print(f"\n== {mode} mode | elapsed={elapsed:.1f}s ==", flush=True)

    _assert("output" in result, "final state has 'output' key", failures)
    output = result.get("output", "")
    _assert(len(output) > 50, f"output length={len(output)} > 50", failures)
    _assert(PAPER_ID in output or "liang2023" in output, "output references paper_id", failures)

    candidates = result.get("candidates", [])
    _assert(len(candidates) >= 1, f"discovery candidates={len(candidates)} >= 1", failures)
    _assert(any(c.get("arxiv_id") == PAPER_ID for c in candidates),
            f"top candidates include {PAPER_ID}", failures)

    papers = result.get("papers", [])
    _assert(len(papers) >= 1, f"evidence pool papers={len(papers)} >= 1", failures)

    claims = result.get("claims", [])
    _assert(len(claims) >= 1, f"claims count={len(claims)} >= 1", failures)
    _assert(any(isinstance(c, dict) and c.get("paper_id") for c in claims),
            "claims carry per-source paper_id attribution", failures)

    draft = result.get("draft", "")
    _assert(len(draft) > 500, f"survey-draft length={len(draft)} > 500", failures)
    _assert("\n## " in result.get("output", ""),
            "output carries per-section heading markers", failures)

    iteration = result.get("iteration", 0)
    _assert(1 <= iteration <= 3, f"iteration={iteration} in [1,3]", failures)

    taxonomy = result.get("taxonomy", {})
    topics = taxonomy.get("topics", [])
    _assert(len(topics) >= 1, f"topics count={len(topics)} >= 1", failures)

    outline = result.get("outline", {})
    sections = outline.get("sections", []) if isinstance(outline, dict) else []
    _assert(len(sections) >= 1, f"STORM outline sections={len(sections)} >= 1", failures)
    _assert(any(s.get("heading") for s in sections if isinstance(s, dict)),
            "outline sections carry headings", failures)

    validation = result.get("validation", {})
    _assert(validation.get("passed") is True, "validation gate passed", failures)
    _assert(validation.get("checks", {}).get("structure", {}).get("ok") is True,
            "validation: structure ok", failures)
    _assert(validation.get("checks", {}).get("cites", {}).get("ok") is True,
            "validation: cites well-formed", failures)
    _assert(validation.get("checks", {}).get("grounding", {}).get("ok") is True,
            "validation: quotes grounded (5-gram)", failures)
    _assert(validation.get("score", 0) > 0.5,
            f"validation score={validation.get('score')} > 0.5", failures)
    _assert(validation.get("n_papers_cited", 0) >= 1,
            f"multi-paper n_papers_cited={validation.get('n_papers_cited')} >= 1", failures)

    judge = validation.get("judge", {})
    _assert(isinstance(judge, dict) and judge.get("label") in ("pass", "revise", "fail"),
            f"P3 judge verdict={judge.get('label') if isinstance(judge, dict) else judge}",
            failures)
    _assert(isinstance(judge, dict) and len(judge.get("checks", {})) == 4,
            "P3 judge rubric checks (groundedness/structure/bilingual/clarity)", failures)
    if mode == "mock":
        _assert(judge.get("label") == "pass" and judge.get("score", 0) >= 4,
                f"P3 judge (mock) pass with score={judge.get('score')} >= 4", failures)

    if failures:
        print(f"\n==== {len(failures)} FAILED ====", flush=True)
        return 1
    print("\n==== ALL PASS ====", flush=True)
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    mode = argv[0] if argv else "mock"

    if mode == "mock":
        port = _free_port()
        proc = _start_mock(port)
        try:
            base = f"http://127.0.0.1:{port}/v1"
            client = LLMClient(backend="openai", base_url=base, model="mock")
            rc = _run_test(client, "mock")
        finally:
            proc.terminate(); proc.wait(timeout=5)
        return rc

    elif mode == "real":
        model = argv[1] if len(argv) > 1 else None
        client = LLMClient(backend="opencode", **({"model": model} if model else {}))
        if not client.is_reachable():
            print("opencode CLI unreachable — SKIP", flush=True)
            return 0
        return _run_test(client, f"real ({client.model})")

    else:
        print(f"unknown mode {mode!r}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())