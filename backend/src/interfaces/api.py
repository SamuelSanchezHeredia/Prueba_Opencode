from pathlib import Path
from typing import Dict

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.config import settings
from src.infrastructure.db import get_db
from src.infrastructure.models import CvSectionExtracted, CvSession
from src.infrastructure.services.faq import load_faqs, load_faqs_from_db, match_faq
from src.infrastructure.services.parser import parse_document
from src.interfaces.schemas import (
    AnalysisResponse,
    ChatRequest,
    ChatResponse,
    CorrectionPayload,
    FaqRequest,
    FaqResponse,
    ScoreResponse,
    SectionPayload,
    SessionResponse,
)
from src.application.use_cases import analyze_session, start_session


app = FastAPI(title="CV ATS Optimizer POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/session/start", response_model=SessionResponse)
def session_start(
    file: UploadFile = File(...),
    target_sector: str = Form(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename required")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_path = Path(f"/tmp/{file.filename}")
    with temp_path.open("wb") as handle:
        handle.write(file.file.read())

    sections = parse_document(temp_path)
    temp_path.unlink(missing_ok=True)

    session = start_session(db, file.filename, target_sector, sections)

    section_payloads = [SectionPayload(name=name, raw_text=text) for name, text in sections.items()]
    return SessionResponse(
        session_id=session.session_id,
        filename=session.filename,
        target_sector=session.target_sector,
        sections=section_payloads,
    )


@app.post("/session/analyze", response_model=AnalysisResponse)
def session_analyze(
    session_id: str = Form(...),
    db: Session = Depends(get_db),
):
    session = db.query(CvSession).filter(CvSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    sections = db.query(CvSectionExtracted).filter(CvSectionExtracted.session_id == session_id).all()
    extracted: Dict[str, str] = {section.section_name: section.raw_text for section in sections}
    analysis = analyze_session(db, session, extracted, settings.keywords_path)

    score = ScoreResponse(**analysis["scores"])
    return AnalysisResponse(
        session_id=session.session_id,
        scores=score,
        extracted_sections=extracted,
        raw_text=analysis["raw_text"],
        keywords_checked={
            "sector": session.target_sector,
            "total": len(analysis["scores"]["found_keywords"])
            + len(analysis["scores"]["missing_keywords"]),
        },
        corrections=[CorrectionPayload(**item) for item in analysis["corrections"]],
        detected_issues=analysis["detected_issues"],
        semantic_contract=analysis["semantic_contract"],
    )


@app.post("/faq", response_model=FaqResponse)
def faq_matcher(payload: FaqRequest):
    faqs = load_faqs()
    answer, matched = match_faq(payload.question, faqs)
    return FaqResponse(answer=answer, matched_question=matched)


@app.post("/chat", response_model=ChatResponse)
def faq_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    faqs = load_faqs_from_db(db)
    if not faqs:
        faqs = load_faqs()
    answer, matched = match_faq(payload.message, faqs)
    return ChatResponse(answer=answer, matched_question=matched)
