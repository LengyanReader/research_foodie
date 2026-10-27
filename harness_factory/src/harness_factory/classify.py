"""Classify a task into a :class:`FeatureVector`.

Deterministic keyword rules are the default. An optional LLM classifier
(:mod:`harness_factory.llm`) may fill gaps when explicitly requested; its output
is schema-validated and only overrides values the rules could not determine. The
classifier never invents task content -- it only labels (M0.4).
"""

from __future__ import annotations

import re
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
    "long-term",
    "week",
    "数周",
    "几周",
    "每周",
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
# "review" as a bare word is NOT a cue (P36): it is also the deliverable noun in
# "literature review" / "systematic review" / "survey", and that false positive
# once reached the scored holdout (lit-review pinned M8 from the misfire). The
# compound verb-request forms below stay high-precision; "review the" is
# deliberately absent because "review the literature" is exactly the false hit.
_HUMAN_REVIEW = [
    "code review",
    "peer review",
    "reviewer",
    "review my",
    "review our",
    "review comments",
    "team",
    "handoff",
    "评审",
    "复核",
    "同事",
    "交接",
]

# Artifact cues: an explicit deliverable noun in the task text beats the domain
# default. Only high-precision cues belong here -- a cue that fires on ordinary
# prose turns a preference into a wrong answer.
_ART_CUES: tuple[tuple[str, list[str]], ...] = (
    (
        "knowledge_base",
        [
            "knowledge base",
            "knowledge graph",
            "ontology",
            "知识图谱",
            "知识库",
            "本体库",
            "本体",
        ],
    ),
    ("dataset", ["dataset", "data set", "csv", "corpus", "data cleaning", "数据集", "语料", "数据清洗"]),
    (
        "code",
        [
            "codebase",
            "code base",
            "source code",
            "package",
            "module",
            "script",
            "refactor",
            "unit test",
            "unit tests",
            "type hints",
            "type annotations",
            "代码",
            "程序",
            "脚本",
            "单元测试",
            "类型注解",
            "内存泄漏",
        ],
    ),
    (
        "document",
        [
            "report",
            "paper",
            "essay",
            "memo",
            "chapter",
            "slides",
            "deck",
            "documentation",
            "readme",
            "报告",
            "文档",
            "论文",
            "文章",
            "幻灯片",
            "讲稿",
            "说明书",
            "随笔",
        ],
    ),
    ("plan", ["proposal", "roadmap", "project plan", "行动计划", "路线图", "提案", "方案书"]),
)

# Grounding cues. "required" is raised only by an explicit demand for sources;
# nothing lowers it, because a task that needs no sources does not usually say so
# and a false "off" is worse than a false "preferred".
_GROUND_REQUIRED = [
    "citation",
    "citations",
    "cite",
    "cited",
    "bibliography",
    "references",
    "with sources",
    "sourced",
    "grounded in",
    "evidence-based",
    "provenance",
    "引用",
    "出处",
    "参考文献",
    "注明来源",
    "可溯源",
    "有据可查",
]
_GROUND_OFF = ["no external knowledge", "without external knowledge", "不用外部知识", "不要引用"]

# Selection intent. The model-selection domain's own signals are exact phrases
# ("model selection", "选型"), and generic neighbours outvote them: a task that
# says "选一个模型 … 做一个评测" scores 模型+评测 for data-science and only one
# exact phrase for model-selection, so the domain was effectively unreachable
# from text (P19). These cues name a *choice* rather than a comparison, and an
# explicit choice outranks the domain default - the same rule P18 applied to
# artifact and grounding cues. "模型对比"/"model comparison" is deliberately not
# a cue: that is also how an ablation or a literature review is described.
_SELECTION_CUES = [
    "which model",
    "choose a model",
    "choose between models",
    "pick a model",
    "select a model",
    "model choice",
    "model selection",
    "选一个模型",
    "选个模型",
    "选模型",
    "挑一个模型",
    "挑模型",
    "哪个模型",
    "用哪个模型",
    "选型",
    "模型选型",
]

_SIG_RES: dict[str, re.Pattern[str]] = {}


def _sig_hit(signal: str, text: str) -> bool:
    """Match a signal at a **word start**, not inside a longer word.

    Substring matching produced real false positives: the devops signal ``ci``
    fired on "exercises", ``art`` on "partial", and ``ops`` on "devops" while
    missing the task that literally said devops. Latin signals must begin a word
    (inflections still match: ``deploy`` matches "deployment"); CJK and multi-word
    signals stay plain substrings, since Chinese has no word spaces.
    """
    if not signal.isascii() or " " in signal or "-" in signal:
        return signal in text
    pattern = _SIG_RES.get(signal)
    if pattern is None:
        pattern = re.compile(r"(?<![a-z0-9])" + re.escape(signal))
        _SIG_RES[signal] = pattern
    return pattern.search(text) is not None


def _has(text: str, keywords: list[str]) -> bool:
    return any(_sig_hit(k, text) for k in keywords)


def domain_scores(text: str) -> list[tuple[str, int]]:
    """Signal-score every domain, best first (``general`` excluded).

    Shared with :func:`derive` for the near-domain report (P31): intersections
    are invisible unless the runner-up is named.
    """
    scored = []
    for name, meta in _domains().items():
        if name == "general":
            continue
        score = sum(1 for sig in meta.get("signals", []) if _sig_hit(sig, text))
        scored.append((name, score))
    # Stable sort: ties keep the registry's insertion order (the historical
    # tie-break; alphabetical order would silently re-route tie cases).
    scored.sort(key=lambda pair: -pair[1])
    return scored


def _guess_domain(text: str) -> str:
    # An explicit choice of model outranks the domain default: generic
    # neighbours (data-science carries "model"/"模型"/"eval"/"评测") otherwise
    # outvote the selection domain's exact phrases by count.
    if _has(text, _SELECTION_CUES):
        return "model-selection"
    scores = domain_scores(text)
    if not scores:
        return "general"
    return scores[0][0] if scores[0][1] > 0 else "general"


def _guess_artifact(text: str) -> str | None:
    """Return the artifact named by an explicit cue, or ``None``."""
    for artifact, cues in _ART_CUES:
        if _has(text, cues):
            return artifact
    return None


def _guess_grounding(text: str) -> str | None:
    """Return ``required``/``off`` only when the text says so explicitly."""
    if _has(text, _GROUND_OFF):
        return "off"
    if _has(text, _GROUND_REQUIRED):
        return "required"
    return None


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

    # The domain is a *scenario prior*; an explicit cue in the text is evidence
    # about this task and wins (M0.1). Nothing here invents content: the cue only
    # selects an already-declared artifact/source level.
    cue_artifact = _guess_artifact(text)
    if cue_artifact:
        feats.artifact = cue_artifact
    cue_grounding = _guess_grounding(text)
    if cue_grounding:
        feats.grounding = cue_grounding

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
