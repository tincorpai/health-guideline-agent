from pydantic import BaseModel, Field
from typing import List, Optional

class EvidenceChunk(BaseModel):
    source_id: str               # e.g., "v1/htn_screening_demo.txt"
    chunk_id: str                # e.g., "0003"
    text: str
    score: float

class Citation(BaseModel):
    source_id: str
    chunk_id: str

class CitedAnswer(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    refusal: bool = False
    reason: Optional[str] = None
    evidence: List[EvidenceChunk] = Field(default_factory=list)
