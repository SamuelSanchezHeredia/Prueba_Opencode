from datetime import datetime
from pathlib import Path
from typing import Dict

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models import CvSectionExtracted, CvSession
from .schemas import AnalysisResponse, ScoreResponse, SectionPayload, SessionResponse
from .services.ats import evaluate_format
from .services.keywords import load_keywords, match_keywords
from .services.parser import parse_document


app = FastAPI(title="CV ATS Optimizer POC")


@app.post("/session/start", response_model=SessionResponse)
def start_session(
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

    session = CvSession(
        filename=file.filename,
        target_sector=target_sector,
        started_at=datetime.utcnow(),
        status="parsed",
    )
    db.add(session)
    db.flush()

    section_payloads = []
    for name, raw_text in sections.items():
        section_payloads.append(SectionPayload(name=name, raw_text=raw_text))
        db.add(
            CvSectionExtracted(
                session_id=session.session_id,
                section_name=name,
                raw_text=raw_text,
                clean_json={},
            )
        )

    db.commit()

    return SessionResponse(
        session_id=session.session_id,
        filename=session.filename,
        target_sector=session.target_sector,
        sections=section_payloads,
    )


@app.post("/session/analyze", response_model=AnalysisResponse)
def analyze_session(
    session_id: str = Form(...),
    db: Session = Depends(get_db),
):
    session = db.query(CvSession).filter(CvSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    sections = db.query(CvSectionExtracted).filter(CvSectionExtracted.session_id == session_id).all()
    extracted: Dict[str, str] = {section.section_name: section.raw_text for section in sections}
    raw_text = "\n".join(extracted.values())

    ats_score, missing_sections = evaluate_format(raw_text)
    keyword_map = load_keywords(settings.keywords_path)
    keyword_score, _, missing_keywords = match_keywords(raw_text, session.target_sector, keyword_map)

    overall_score = int((ats_score * 0.6) + (keyword_score * 0.4))

    session.ats_score = ats_score
    session.keyword_score = keyword_score
    session.overall_score = overall_score
    session.status = "analyzed"
    db.commit()

    score = ScoreResponse(
        ats_score=ats_score,
        keyword_score=keyword_score,
        overall_score=overall_score,
        missing_sections=missing_sections,
        missing_keywords=missing_keywords,
    )

    return AnalysisResponse(
        session_id=session.session_id,
        scores=score,
        extracted_sections=extracted,
        raw_text=raw_text,
        keywords_checked={"sector": session.target_sector, "total": len(keyword_map.get(session.target_sector, []))},
    )
