"""Lightweight typed state for the research_foodie LangGraph pipeline."""
import operator
from typing import TypedDict, List, Dict, Optional, Annotated

class PipelineState(TypedDict, total=False):
    paper_id: str
    parsed_md: str
    evidence_chunks: List[str]
    candidates: List[Dict[str, object]]
    papers: List[Dict[str, object]]   # resolved multi-paper evidence pool (S_lit)
    taxonomy: Dict[str, object]
    outline: Dict[str, object]
    perspectives: List[str]          # L-2 STORM-style reader perspectives (S_org)
    source_windows: List[Dict]       # L-1 re-rank provenance (per-paper windows the extractor saw)
    claims: List[Dict]
    dropped_claims: List[Dict]
    draft: str
    iteration: Annotated[int, operator.add]
    output: str
    validation: Dict[str, object]