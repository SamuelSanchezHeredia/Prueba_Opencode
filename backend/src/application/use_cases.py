from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

from src.infrastructure.models import AiCorrection, CvSectionExtracted, CvSession, OperationalLog
from src.infrastructure.services.ats import detect_format_issues, evaluate_format
from src.infrastructure.services.keywords import load_keywords, match_keywords
from src.infrastructure.services.llm import call_semantic_llm
from src.infrastructure.services.semantic import analyze_experience, detect_semantic_issues


def start_session(db: Session, filename: str, target_sector: str, sections: Dict[str, str]):
    session = CvSession(
        filename=filename,
        target_sector=target_sector,
        started_at=datetime.utcnow(),
        status="parsed",
    )
    db.add(session)
    db.flush()

    for name, raw_text in sections.items():
        db.add(
            CvSectionExtracted(
                session_id=session.session_id,
                section_name=name,
                raw_text=raw_text,
                clean_json={},
            )
        )

    db.commit()
    return session


def analyze_session(db: Session, session: CvSession, extracted: Dict[str, str], keywords_path: str):
    raw_text = "\n".join(extracted.values())
    ats_score, missing_sections = evaluate_format(raw_text)
    keyword_map = load_keywords(keywords_path)
    keyword_score, found_keywords, missing_keywords = match_keywords(
        raw_text, session.target_sector, keyword_map
    )

    experience_text = extracted.get("experience") or extracted.get("experiencia") or raw_text
    corrections = analyze_experience(experience_text)
    detected_issues: List[str] = []
    detected_issues.extend(detect_format_issues(raw_text))
    detected_issues.extend(detect_semantic_issues(experience_text))
    semantic_contract = call_semantic_llm(experience_text, session.target_sector)

    for correction in corrections:
        db.add(
            AiCorrection(
                session_id=session.session_id,
                original_text=correction["original_text"],
                suggested_text=correction["suggested_text"],
                explanation=correction["explanation"],
                category=correction["category"],
                created_at=datetime.utcnow(),
            )
        )

    db.add(
        OperationalLog(
            session_id=session.session_id,
            module_name="semantic_core",
            input_payload={"experience": experience_text[:5000]},
            output_payload={
                "corrections": corrections,
                "detected_issues": detected_issues,
                "semantic_contract": semantic_contract,
            },
            created_at=datetime.utcnow(),
        )
    )

    semantic_score = 0 if not corrections else max(40, 100 - (len(corrections) * 10))
    overall_score = int((ats_score * 0.4) + (keyword_score * 0.3) + (semantic_score * 0.3))

    session.ats_score = ats_score
    session.keyword_score = keyword_score
    session.semantic_score = semantic_score
    session.overall_score = overall_score
    session.status = "analyzed"
    db.commit()

    return {
        "scores": {
            "ats_score": ats_score,
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "overall_score": overall_score,
            "missing_sections": missing_sections,
            "missing_keywords": missing_keywords,
            "found_keywords": found_keywords,
        },
        "raw_text": raw_text,
        "detected_issues": detected_issues,
        "semantic_contract": semantic_contract,
        "corrections": corrections,
    }
