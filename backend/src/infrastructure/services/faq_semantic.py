from typing import Dict, List, Tuple

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infrastructure.services.embeddings import embed_texts


def build_faq_embeddings(db: Session, faqs: List[Dict[str, str]]):
    embeddings = embed_texts([item["question"] for item in faqs])
    for item, vector in zip(faqs, embeddings):
        db.execute(
            text(
                """
                INSERT INTO faq_embeddings (faq_id, embedding)
                VALUES ((SELECT faq_id FROM faqs WHERE question = :question), :embedding)
                ON CONFLICT (faq_id) DO UPDATE SET embedding = :embedding
                """
            ),
            {"question": item["question"], "embedding": vector},
        )
    db.commit()


def semantic_match(db: Session, question: str) -> Tuple[str, str, float]:
    query_embedding = embed_texts([question])[0]
    rows = db.execute(
        text(
            """
            SELECT f.question, f.answer, (e.embedding <=> :embedding) AS distance
            FROM faq_embeddings e
            JOIN faqs f ON f.faq_id = e.faq_id
            ORDER BY e.embedding <=> :embedding
            LIMIT 1
            """
        ),
        {"embedding": query_embedding},
    )
    row = rows.first()
    if not row:
        return "", "", 1.0
    return row[1], row[0], row[2]
