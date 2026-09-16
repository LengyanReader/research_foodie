"""P3 AI judge gate — DAS-Bench-style rubric review of the final draft.

Runs AFTER the deterministic L6 gate (validate.py): the mechanical gate guards
*factual* integrity (structure/cites/grounding) with zero LLM cost; the judge
adds a calibrated subjective review of the assembled draft.

Convention (DAS / DeepResearch-Bench): human-usability review runs best with a
cloud ≥300B-class judge. In this env that has no API keys, so the judge uses
the SAME LLMClient as the pipeline — by default the opencode free model — and
the verdict is labelled `judge_model` for the record. Swap to a stronger model
by passing an OpenAI-backed client; nothing else changes.

judge_draft() is defensive: it never raises. On any parse failure it returns a
`fail` verdict with the reason so the graph always terminates.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from tools.llm.client import LLMClient, Message
from tools.pipeline.validate import parse_json_dict

JUDGE_RUBRIC = (
    "You are a rigorous research-paper reviewer. Score the final draft 0-5 on "
    "four axes:\n"
    "- groundedness: every factual sentence is backed by a claim whose cite is "
    "an arXiv ID or DOI; no uncited assertions\n"
    "- structure: the draft follows the given outline sections\n"
    "- bilingual: both English and 中文 are present and the Chinese is faithful "
    "to the English meaning\n"
    "- clarity: precise, dense, no hedging filler\n"
    "Respond ONLY as JSON {\"label\": \"pass\"|\"revise\"|\"fail\", "
    "\"score\": int(1-5), \"checks\": {\"groundedness\": bool, "
    "\"structure\": bool, \"bilingual\": bool, \"clarity\": bool}, "
    "\"feedback\": str}."
)

_LABELS = ("pass", "revise", "fail")


def _pick_label(score: int, checks: Dict[str, bool]) -> str:
    if (score >= 4 and checks.get("groundedness") and checks.get("structure")
            and checks.get("bilingual")):
        return "pass"
    if score >= 3:
        return "revise"
    return "fail"


def judge_draft(state: Dict[str, Any], client: LLMClient) -> Dict[str, Any]:
    """Return a DAS-Bench-style verdict dict for the graph's `validation`."""
    paper_id = state.get("paper_id", "")
    draft = state.get("draft", "") or ""
    outline = state.get("outline", {}) or {}
    outline_txt = json.dumps(outline, ensure_ascii=False)
    claims = state.get("claims", []) or []
    claims_txt = json.dumps(claims[:4], ensure_ascii=False)

    r = client.chat(
        [
            Message(role="system", content=JUDGE_RUBRIC),
            Message(role="user",
                    content=f"Paper: {paper_id}\n\nOutline: {outline_txt}\n"
                            f"Claims: {claims_txt}\n\nDraft:\n{draft}"),
        ],
        json_mode=True,
        max_tokens=400,
    )
    obj = parse_json_dict(r.text)
    if not isinstance(obj, dict):
        return {
            "label": "fail",
            "score": 0,
            "checks": {},
            "feedback": f"unparseable judge reply: {r.text[:120]!r}",
            "judge_model": getattr(client, "model", "?"),
        }

    label_raw = str(obj.get("label", "")).strip().lower()
    try:
        score = int(obj.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    checks = obj.get("checks") or {}
    if not isinstance(checks, dict):
        checks = {}
    label = label_raw if label_raw in _LABELS else _pick_label(score, checks)
    return {
        "label": label,
        "score": score,
        "checks": {k: bool(checks.get(k)) for k in
                   ("groundedness", "structure", "bilingual", "clarity")},
        "feedback": str(obj.get("feedback", ""))[:300],
        "judge_model": getattr(client, "model", "?"),
    }