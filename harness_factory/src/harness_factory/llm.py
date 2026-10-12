"""Optional LLM-assisted classification.

Off by default and fully env-gated. Uses any OpenAI-compatible
``/chat/completions`` endpoint via the standard library only (no deps):

    HARNESS_LLM_BASE_URL   e.g. https://api.openai.com/v1
    HARNESS_LLM_API_KEY    bearer token
    HARNESS_LLM_MODEL      default: gpt-4o-mini

The model is asked ONLY to label the task on the fixed feature axes. Its reply
is parsed as JSON and validated against the closed vocabularies; anything
unexpected is discarded. It never generates task content (M0.4).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .spec import FEATURE_CHOICES

_SYSTEM = (
    "You classify a task so an agent harness can be selected. "
    "Return STRICT JSON only, with these keys and allowed values:\n"
    "horizon: one_shot|session|multi_session|long_running\n"
    "verifiability: high|medium|low\n"
    "stakes: low|medium|high\n"
    "grounding: off|preferred|required\n"
    "artifact: code|document|dataset|knowledge_base|plan|mixed\n"
    "tool_surface: none|read|read_write|external\n"
    "collaboration: solo|human_review|multi_agent\n"
    "Do not add commentary. Do not invent facts. Label only."
)


def _config() -> tuple[str | None, str | None, str]:
    base = os.environ.get("HARNESS_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    key = os.environ.get("HARNESS_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("HARNESS_LLM_MODEL", "gpt-4o-mini")
    return base, key, model


def available() -> bool:
    base, key, _ = _config()
    return bool(base and key)


def _extract_json(content: str) -> dict[str, Any] | None:
    content = content.strip()
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        parsed = json.loads(content[start : end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def classify_features(task_text: str, timeout: float = 30.0) -> dict[str, Any] | None:
    """Return validated feature labels from the LLM, or ``None`` on any failure."""
    base, key, model = _config()
    if not base or not key:
        return None

    url = base.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": task_text or "(empty task)"},
            ],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None

    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None

    parsed = _extract_json(content)
    if not parsed:
        return None

    cleaned: dict[str, Any] = {}
    for name, choices in FEATURE_CHOICES.items():
        value = parsed.get(name)
        if value in choices:
            cleaned[name] = value
    return cleaned or None


_DISCOVER_SYSTEM = (
    "You surface recent, PRIMARY-SOURCE items (peer-reviewed papers, arXiv preprints, "
    "official repositories, official documentation pages) about AI agent harnesses, "
    "self-evolving agents, context engineering, agent memory, tools/skills, evaluation "
    "gates, provenance, and multi-agent collaboration.\n"
    "Return STRICT JSON only: {\"items\": [{\"title\": str, \"url\": str, "
    "\"external_id\": str, \"kind\": \"paper|repo|doc|post\", \"topics\": [str], "
    "\"summary\": str, \"published\": \"YYYY-MM-DD\"}]}.\n"
    "Every item MUST carry a real, verifiable url or a stable external_id "
    "(arXiv id / DOI). Never invent titles, ids, or urls. Prefer recency. "
    "Omit anything you cannot ground. No commentary outside the JSON."
)


def _chat_content(system: str, user: str, timeout: float) -> str | None:
    base, key, model = _config()
    if not base or not key:
        return None
    url = base.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None
    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None


def _chat(system: str, user: str, timeout: float) -> dict[str, Any] | None:
    content = _chat_content(system, user, timeout)
    if not content:
        return None
    return _extract_json(content)


def discover_items(
    topics: list[dict[str, Any]],
    since: str | None = None,
    max_items: int = 10,
    timeout: float = 60.0,
) -> list[dict[str, Any]]:
    """Return candidate source items proposed by the LLM, or ``[]`` on failure.

    Output is untrusted until :mod:`harness_factory.curate` audits it: items
    without a url/id are dropped, duplicates are removed, and nothing is written
    to the catalogs (M0.4).
    """
    if not topics:
        return []
    lines = ["Topics to probe:"]
    for topic in topics:
        label = topic.get("name_zh") or topic.get("id", "")
        queries = "; ".join(topic.get("queries", [])) or topic.get("id", "")
        lines.append(f"- {topic.get('id', '')} ({label}): {queries}")
    if since:
        lines.append(f"\nOnly include items published on or after {since}.")
    lines.append(f"\nReturn at most {max_items} items total.")

    parsed = _chat(_DISCOVER_SYSTEM, "\n".join(lines), timeout)
    if not parsed:
        return []
    items = parsed.get("items")
    return items if isinstance(items, list) else []


_SUMMARY_SYSTEM = (
    "You summarize ONE AI source item in 1-2 sentences, in the item's own language. "
    "Extract only what the item states; never add facts or opinions. Plain text, no markdown."
)


def summarize(text: str, timeout: float = 30.0) -> str | None:
    """Return a claim-faithful 1-2 sentence summary, or ``None`` if unavailable."""
    if not text:
        return None
    content = _chat_content(_SUMMARY_SYSTEM, text[:6000], timeout)
    return content.strip() if content else None
