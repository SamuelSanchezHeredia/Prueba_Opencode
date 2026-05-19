import json
from pathlib import Path
from typing import Dict, List, Tuple

from rapidfuzz import fuzz
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import settings


def load_faqs() -> List[Dict[str, str]]:
    faqs_path = Path(settings.faqs_path)
    if not faqs_path.is_absolute():
        faqs_path = Path(__file__).resolve().parents[2] / "data" / faqs_path.name
    with faqs_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_faqs_from_db(db: Session) -> List[Dict[str, str]]:
    rows = db.execute(text("SELECT question, answer FROM faqs ORDER BY faq_id"))
    return [{"question": row[0], "answer": row[1]} for row in rows]


def fuzzy_match(question: str, faqs: List[Dict[str, str]]) -> Tuple[str, str, int]:
    best_score = -1
    best_answer = ""
    best_question = ""
    for item in faqs:
        score = fuzz.token_set_ratio(question.lower(), item["question"].lower())
        if score > best_score:
            best_score = score
            best_answer = item["answer"]
            best_question = item["question"]
    return best_answer, best_question, best_score


def match_faq(question: str, faqs: List[Dict[str, str]]) -> Tuple[str, str]:
    lowered = question.lower()
    for item in faqs:
        if item["question"].lower() in lowered:
            return item["answer"], item["question"]

    return (
        "No tengo una respuesta exacta. Reformula la pregunta o intenta con palabras clave.",
        "",
    )
