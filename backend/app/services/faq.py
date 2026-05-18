import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_faqs() -> List[Dict[str, str]]:
    faqs_path = Path(__file__).resolve().parents[2] / "data" / "faqs.json"
    with faqs_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def match_faq(question: str, faqs: List[Dict[str, str]]) -> Tuple[str, str]:
    lowered = question.lower()
    for item in faqs:
        if item["question"].lower() in lowered:
            return item["answer"], item["question"]

    return (
        "No tengo una respuesta exacta. Reformula la pregunta o intenta con palabras clave.",
        "",
    )
