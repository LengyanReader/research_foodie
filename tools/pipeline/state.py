"""Lightweight typed state for the research_foodie LangGraph pipeline."""
import operator
from typing import TypedDict, List, Dict, Optional, Annotated

class PipelineState(TypedDict, total=False):
    paper_id: str
    parsed_md: str
    evidence_chunks: List[str]
    candidates: List[Dict[str, object]]
    taxonomy: Dict[str, object]
    outline: Dict[str, object]
    claims: List[Dict]
    dropped_claims: List[Dict]
    draft: str
    iteration: Annotated[int, operator.add]
    output: str
    validation: Dict[str, object]