"""
Smoke test for the unified LLM client (tools/llm/client.py).

Modes
-----
`opencode`        — test against the opencode CLI (hosted free model, default);
                    the pipeline's primary real backend since 2026-09-16.
`mock`            — start an ephemeral OpenAI-compatible mock server on a free
                    port and test the client end-to-end (no keys required).

Usage
-----
    python tools/llm/smoke_test.py opencode
    python tools/llm/smoke_test.py mock

Three prompt categories are exercised (mirroring pipeline needs):
  1. Bilingual reply             (README/runbook convention)
  2. JSON extraction (json_mode) (structured evidence fields)
  3. Claim list with cites       (L4 claim plans; judge later)
"""
from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tools.llm.client import LLMClient, Message  # noqa: E402


PROMPTS = [
    {
        "name": "bilingual",
        "messages": [Message(role="user", content="Translate to Chinese and English concisely: 'research_foodie is a proactive pipeline.'")],
        "expect": ["pipeline"],
    },
    {
        "name": "json-extract",
        "messages": [Message(role="system", content="You extract structured JSON from text."),
                     Message(role="user", content="JSON extraction from: 'GPT detectors are biased against non-native English writers' (year 2023). Return {\"title\": str, \"year\": int}.")],
        "json_mode": True,
        "expect": ["GPT detectors are biased"],
    },
    {
        "name": "claim-list",
        "messages": [Message(role="system", content="Return JSON, a list of 2 academic claims with a cite field."),
                     Message(role="user", content="List of 2 academic claims about transformers, each with 'claim' and 'cite'. The cite field must be an arXiv ID in the form arXiv:NNNN.NNNNN.")],
        "json_mode": True,
        "expect_regex": [r"arXiv:\d{4}\.\d+"],
    },
]


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _start_mock() -> subprocess.Popen:
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "tools.llm.mock_openai_server", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    base = f"http://127.0.0.1:{port}/v1"
    deadline = time.time() + 20
    client = LLMClient(backend="openai", base_url=base, model="mock-api")
    while time.time() < deadline:
        if client.is_reachable():
            return proc, base
        time.sleep(0.5)
    raise RuntimeError("mock server did not start in time")


def run(mode: str) -> None:
    if mode == "mock":
        proc, base = _start_mock()
        client = LLMClient(backend="openai", base_url=base, model="mock-api")
        print(f"== mock backend @ {base} ==", flush=True)
    elif mode == "opencode":
        client = LLMClient(backend="opencode")
        print(f"== opencode backend, model={client.model} ==", flush=True)
        if not client.is_reachable():
            print("   (opencode CLI unreachable — install it or fix PATH)", flush=True)
            return
    else:
        raise SystemExit(f"unknown mode {mode!r} (expected 'opencode' | 'mock')")

    failures = 0
    for p in PROMPTS:
        name = p["name"]
        print(f"-- {name} --", flush=True)
        try:
            t0 = time.time()
            resp = client.chat(p["messages"], json_mode=p.get("json_mode", False))
            dt = time.time() - t0
            print(f"   {dt:6.2f}s  model={resp.model}", flush=True)
            print(f"   text: {resp.text[:300]!r}", flush=True)
            ok = all(e in resp.text for e in p.get("expect", []))
            if "expect_regex" in p:
                ok = ok and any(re.search(pat, resp.text) for pat in p["expect_regex"])
            if p.get("json_mode"):
                try:
                    json.loads(resp.text)
                except Exception as e:
                    ok = False
                    print(f"   invalid JSON: {e}", flush=True)
            print(f"   => {'PASS' if ok else 'FAIL'}", flush=True)
            failures += 0 if ok else 1
        except Exception as e:
            print(f"   ERROR: {type(e).__name__}: {e}", flush=True)
            failures += 1

    if mode == "mock" and proc:
        proc.terminate()
        proc.wait(timeout=5)

    print(f"\n==== {'ALL PASS' if failures == 0 else f'{failures} FAILED'} ====", flush=True)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "mock")