"""Inclusive harness compiler.

Given a task, derive and scaffold the agent harness that task needs.
See ``tasks/PLAN.md`` for the architecture and ``core/`` for the pattern definitions.
"""

from __future__ import annotations

from ._version import __version__

from .derive import derive
from .classify import classify
from .assemble import build_files, write_harness
from .check import check_harness
from .collect import Candidate
from .config import ensure_home, home
from .curate import curate, known_keys, trends
from .refresh import apply_accepted, load_watchlist, run_refresh
from .spec import FeatureVector, HarnessPlan, ModulePlan, TaskSpec

__all__ = [
    "__version__",
    "TaskSpec",
    "FeatureVector",
    "ModulePlan",
    "HarnessPlan",
    "classify",
    "derive",
    "build_files",
    "write_harness",
    "check_harness",
    "Candidate",
    "curate",
    "known_keys",
    "trends",
    "run_refresh",
    "apply_accepted",
    "load_watchlist",
    "home",
    "ensure_home",
]
