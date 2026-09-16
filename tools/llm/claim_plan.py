"""
L4 Claim Planner for research_foodie.

Turns a MinerU-parsed paper (markdown) into a structured, evidence-backed
claim plan (JSON) via the unified LLM client (tools/llm/client.py) — any
backend: opencode CLI free model (default) or any OpenAI-compatible API.

Schema produced (one JSON object):
    {
      "paper_id": str,
      "claims": [
        {
          "id": str,
          "claim": str,            # EN, terse
          "claim_zh": str,         # 中文一句话
          "evidence_quote": str,   # verbatim quote from the paper (<=120 chars)
          "section": str,
          "cite": str,
          "confidence": str        # high | medium | low
        }, ...
      ]
    }

Usage:
    from tools.llm.claim_plan import plan_claims
    plan = plan_claims(parsed_md, paper_id="liang2023")

    # CLI:
    python -m tools.llm.claim_plan _demo_downloads/.../liang2023_test.md liang2023

No external deps — stdlib only.
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Dict, Optional

sys.stdout = __import__("io").TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tools.llm.client import LLMClient, Message  # noqa: E402

CLAIM_SYSTEM_PROMPT = (
    "You are the L4 Claim Planner of research_foodie, a local-first academic "
    "research pipeline. Given a parsed paper (markdown from MinerU), extract up to "
    "4 evidence-backed claims. Rules: (1) every claim MUST quote exact supporting "
    "text from the paper; (2) cite = source identifier from the text when present, "
    "else the paper ID; (3) do NOT invent numbers — only report numbers that appear "
    "in the quoted text; (4) return ONLY one JSON object (no prose)."
)

CLAIM_USER_TEMPLATE = (
    "Paper ID: {paper_id}\n\n<paper>\n{markdown}\n</paper>\n\n"
    'Return JSON: {{"paper_id": str, "claims": [{{"id": str, "claim": str (EN, terse), '
    '"claim_zh": str (中文一句话), "evidence_quote": str (verbatim quote from the paper, <=120 chars), '
    '"section": str, "cite": str, "confidence": str (high|medium|low)}}]}}'
)


def plan_claims(
    markdown: str,
    paper_id: str,
    client: Optional[LLMClient] = None,
    max_claims: int = 4,
    max_tokens: int = 1024,
) -> Dict:
    """Run the L4 claim-plan extraction; return the parsed JSON plan dict."""
    cli = client or LLMClient()  # backend/model from env / kwargs
    user = CLAIM_USER_TEMPLATE.format(
        paper_id=paper_id,
        markdown=markdown,
        max_claims=max_claims,
    )
    resp = cli.chat(
        [
            Message(role="system", content=CLAIM_SYSTEM_PROMPT),
            Message(role="user", content=user),
        ],
        json_mode=True,
        max_tokens=max_tokens,
    )
    return {"plan": json.loads(resp.text), "usage": resp.usage, "model": resp.model}


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2:
        print(__doc__.split("Usage:")[-1].strip())
        return 2
    md_path, paper_id = argv[0], argv[1]
    backend = os.getenv("LLM_BACKEND", "opencode")  # opencode (default) | openai
    model = (
        os.getenv("OPENCODE_MODEL") or "opencode/big-pickle"
        if backend == "opencode"
        else os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    )
    client = LLMClient(backend=backend, model=model)
    with open(md_path, encoding="utf-8") as f:
        markdown = f.read()
    t0 = time.time()
    out = plan_claims(markdown, paper_id, client=client)
    print(json.dumps(out["plan"], ensure_ascii=False, indent=2))
    print(
        f"# model={out['model']} elapsed={dt:.1f}s usage={out['usage']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())