from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel


class SectionPayload(BaseModel):
    name: str
    raw_text: str


class SessionResponse(BaseModel):
    session_id: UUID
    filename: str
    target_sector: str
    sections: List[SectionPayload]


class ScoreResponse(BaseModel):
    ats_score: int
    keyword_score: int
    semantic_score: int = 0
    overall_score: int
    missing_sections: List[str]
    missing_keywords: List[str]


class AnalysisResponse(BaseModel):
    session_id: UUID
    scores: ScoreResponse
    extracted_sections: Dict[str, str]
    raw_text: str
    keywords_checked: Dict[str, Any]
