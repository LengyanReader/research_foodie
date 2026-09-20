"""
Per-role model profiles (WS-D D-1).

Answers "which model runs which lane?" as a named, immutable profile resolved
from env at import/startup time (no keys in code/repo):

    LLM_PROFILE          free-opencode (default) | judge-strong
    OPENCODE_MODEL       opencode model (default opencode/big-pickle)
    OPENAI_BASE_URL      OpenAI-compatible endpoint (judge-strong, judge lane)
    OPENAI_MODEL         OpenAI-compatible model (judge-strong, judge lane)
    OPENAI_API_KEY       API key for the OpenAI-compatible endpoint

Lanes (roles):
    draft   S_org / S_write / answer_question  — cheap lane
    qa      extractive / MCQ / yes-no answering — cheap lane
    judge   P3 judge / score_survey / health-check judge — strong lane

Profiles:
    free-opencode   all three lanes -> opencode hosted free model (default).
    judge-strong    draft|qa -> opencode; judge -> OPENAI_* (user-registered
                    OpenAI-compatible provider). Draft stays free even when a
                    strong judge is configured — DAS convention.

Loud-failure rule: an unknown profile name (via LLM_PROFILE) or an unknown
backend value raises ValueError immediately — never a silent fallback.

Usage:
    from tools.llm.profiles import load_profile, clients_for
    prof = load_profile()                 # env-driven
    draft_client, judge_client = clients_for(prof)
    print(profile_header(prof))           # report footer / console header
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Tuple

from tools.llm.client import LLMClient

LANES = ("draft", "qa", "judge")

BACKENDS = ("opencode", "openai")  # ollama removed 2026-09-16 (user decision)

DEFAULT_OPENCODE_MODEL = "opencode/big-pickle"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class Lane:
    backend: str
    model: str
    base_url: str | None = None

    def __str__(self) -> str:
        return f"{self.model}" if self.backend == "opencode" else f"{self.model} @ {self.base_url}"


@dataclass(frozen=True)
class Profile:
    name: str
    lanes: Dict[str, Lane]  # draft/qa/judge

    def lane(self, role: str) -> Lane:
        if role not in self.lanes:
            raise UnknownLane(f"profile {self.name!r} has no lane {role!r} (lanes: {sorted(self.lanes)})")
        return self.lanes[role]

    def as_dict(self) -> Dict[str, dict]:
        return {k: {"backend": v.backend, "model": v.model, "base_url": v.base_url}
                for k, v in self.lanes.items()}


class ProfileError(ValueError):
    """Loud failure for unknown/unsupported profile configuration."""


class UnknownLane(ProfileError):
    pass


def _opencode_lane(model: str) -> Lane:
    return Lane(backend="opencode", model=model or DEFAULT_OPENCODE_MODEL)


def _openai_lane() -> Lane:
    base = (os.getenv("OPENAI_BASE_URL") or DEFAULT_OPENAI_BASE_URL).rstrip("/")
    model = os.getenv("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL
    if not os.getenv("OPENAI_API_KEY"):
        raise ProfileError(
            "profile 'judge-strong' needs OPENAI_API_KEY (env only) for the judge lane"
        )
    return Lane(backend="openai", model=model, base_url=base)


def _build(name: str) -> Profile:
    opencode_model = os.getenv("OPENCODE_MODEL") or DEFAULT_OPENCODE_MODEL
    if name == "free-opencode":
        lanes = {r: _opencode_lane(opencode_model) for r in LANES}
    elif name == "judge-strong":
        lanes = {r: _opencode_lane(opencode_model) for r in ("draft", "qa")}
        lanes["judge"] = _openai_lane()
    else:
        raise ProfileError(
            f"unknown LLM_PROFILE={name!r} — expected one of "
            f"{('free-opencode', 'judge-strong')}; no silent fallback"
        )
    return Profile(name=name, lanes=lanes)


def load_profile(name: str | None = None) -> Profile:
    """Resolve the active profile from env (`LLM_PROFILE`) or explicit `name`."""
    return _build(name or os.getenv("LLM_PROFILE") or "free-opencode")


def clients_for(profile: Profile) -> Tuple[LLMClient, LLMClient]:
    """Return (draft_client, judge_client) from a profile.

    draft_client serves draft|qa lanes (pipeline + answering); judge_client
    serves scoring (P3 judge / score_survey / health-check). Both default to
    the same model under free-opencode; judge-strong splits them.
    """
    dl = profile.lane("draft")
    jl = profile.lane("judge")
    draft = LLMClient(backend=dl.backend, base_url=dl.base_url, model=dl.model)
    judge = LLMClient(backend=jl.backend, base_url=jl.base_url, model=jl.model)
    return draft, judge


def profile_header(profile: Profile) -> str:
    """One-line console/report header showing per-lane models (D-1 accept)."""
    parts = ", ".join(f"{lane}={profile.lane(lane)}" for lane in ("draft", "qa", "judge"))
    return f"[profile {profile.name}] {parts}"