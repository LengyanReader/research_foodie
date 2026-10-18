"""Classify a task into a :class:`FeatureVector`.

Deterministic keyword rules are the default. An optional LLM classifier
(:mod:`harness_factory.llm`) may fill gaps when explicitly requested; its output
is schema-validated and only overrides values the rules could not determine. The
classifier never invents task content -- it only labels (M0.4).
"""

from __future__ import annotations

from typing import Any

from .registry import domains as _domains
from .spec import FEATURE_CHOICES, FEATURE_FIELDS, FeatureVector, TaskSpec

_LONG_RUNNING = ["long-running", "long running", "continuous", "持续运行", "长期运行"]
_MULTI_SESSION = [
    "multi-session",
    "multi session",
    "multi-day",
    "over several sessions",
    "ongoing",
    "长期",
    "持续",
    "多天",
    "多会话",
    "project",
]
_ONE_SHOT = ["one-off", "one off", "single step", "quick", "一次性", "一步"]

_HIGH_VERIFIABILITY = [
    "test",
    "tests",
    "eval",
    "evaluation",
    "metric",
    "benchmark",
    "compile",
    "lint",
    "unit test",
    "测试",
    "评测",
    "指标",
    "基准",
]
_LOW_VERIFIABILITY = [
    "essay",
    "design",
    "creative",
    "taste",
    "opinion",
    "story",
    "copywriting",
    "文案",
    "设计",
    "创意",
    "观点",
]

_HIGH_STAKES = [
    "delete",
    "publish",
    "production",
    "deploy",
    "money",
    "payment",
    "irreversible",
    "legal",
    "contact",
    "email",
    "删除",
    "发布",
    "生产",
    "上线",
    "支付",
    "不可逆",
]
_LOW_STAKES = ["draft", "local", "sandbox", "reversible", "草稿", "本地", "沙盒", "可逆"]

_NO_TOOLS = ["no tools", "without tools", "offline", "不用工具", "离线"]
_EXTERNAL_TOOLS = ["web", "search", "browse", "crawl", "api", "scrape", "联网", "检索", "爬"]
_READ_ONLY = ["read only", "read-only", "只读"]

_MULTI_AGENT = [
    "multi-agent",
    "multi agent",
    "multiple agents",
    "several agents",
    "specialist agents",
    "worker agents",
    "collaborating agents",
    "agents collaborate",
    "agents work together",
    "agent team",
    "agent-team",
    "agent swarm",
    "agent crew",
    "agent graph",
    "agent pipeline",
    "agent collaboration",
    "supervisor agent",
    "orchestrator",
    "sub-agent",
    "subagent",
    "多个 agent",
    "多智能体",
    "多 agent 协作",
]
_HUMAN_REVIEW = ["review", "reviewer", "team", "handoff", "评审", "复核", "同事", "交接"]


def _has(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)


def _guess_domain(text: str) -> str:
    best, best_score = "general", 0
    for name, meta in _domains().items():
        if name == "general":
            continue
        score = sum(1 for sig in meta.get("signals", []) if sig in text)
        if score > best_score:
            best, best_score = name, score
    return best


def _guess_horizon(text: str) -> str:
    if _has(text, _LONG_RUNNING):
        return "long_running"
    if _has(text, _MULTI_SESSION):
        return "multi_session"
    if _has(text, _ONE_SHOT):
        return "one_shot"
    return "session"


def _guess_verifiability(text: str) -> str:
    if _has(text, _HIGH_VERIFIABILITY):
        return "high"
    if _has(text, _LOW_VERIFIABILITY):
        return "low"
    return "medium"


def _guess_stakes(text: str) -> str:
    if _has(text, _HIGH_STAKES):
        return "high"
    if _has(text, _LOW_STAKES):
        return "low"
    return "medium"


def _guess_tool_surface(text: str) -> str:
    if _has(text, _NO_TOOLS):
        return "none"
    if _has(text, _EXTERNAL_TOOLS):
        return "external"
    if _has(text, _READ_ONLY):
        return "read"
    return "read_write"


def _guess_collaboration(text: str) -> str:
    if _has(text, _MULTI_AGENT):
        return "multi_agent"
    if _has(text, _HUMAN_REVIEW):
        return "human_review"
    return "solo"


def classify(
    task: TaskSpec,
    overrides: dict[str, Any] | None = None,
    use_llm: bool = False,
) -> FeatureVector:
    """Return a feature vector for ``task``.

    Precedence: explicit ``overrides`` > LLM suggestions > deterministic rules >
    domain defaults. The chosen ``source`` records which layer dominated.
    """
    overrides = overrides or {}
    text = (task.text or "").lower()

    feats = FeatureVector()
    feats.notes = []

    # Domain first: it seeds artifact + grounding defaults.
    domain = overrides.get("domain") or task.domain or _guess_domain(text)
    if domain not in _domains():
        domain = "general"
    feats.domain = domain
    domain_meta = _domains().get(domain, _domains()["general"])
    feats.artifact = domain_meta.get("artifact", "mixed")
    feats.grounding = domain_meta.get("grounding", "preferred")

    feats.horizon = _guess_horizon(text)
    feats.verifiability = _guess_verifiability(text)
    feats.stakes = _guess_stakes(text)
    feats.tool_surface = _guess_tool_surface(text)
    feats.collaboration = _guess_collaboration(text)
    source = "rules"

    # Optional LLM assist: fills values, never overrides explicit ones.
    if use_llm:
        from . import llm

        suggestion = llm.classify_features(task.text)
        if suggestion:
            changed = False
            for key in FEATURE_FIELDS:
                if key == "domain" or key in overrides:
                    continue
                value = suggestion.get(key)
                if value in FEATURE_CHOICES.get(key, ()):
                    if getattr(feats, key) != value:
                        changed = True
                    setattr(feats, key, value)
            if changed:
                source = "llm"

    # Explicit overrides always win.
    for key, value in overrides.items():
        if value is None:
            continue
        if key == "domain":
            feats.domain = value
            continue
        if value in FEATURE_CHOICES.get(key, ()):
            setattr(feats, key, value)

    if overrides:
        source = "flags"
    feats.source = source

    errors = feats.validate()
    if errors:
        raise ValueError("invalid feature vector: " + "; ".join(errors))
    return feats
