import re
from typing import Dict, List, Tuple


REQUIRED_SECTIONS = ["experiencia", "educacion", "habilidades"]
BAD_FORMAT_HINTS = ["|", "▓", "█", "■", "●"]


def evaluate_format(text: str) -> Tuple[int, List[str]]:
    lowered = text.lower()
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in lowered]

    penalty = 0
    for hint in BAD_FORMAT_HINTS:
        if hint in text:
            penalty += 5

    if re.search(r"\b(arial|times new roman|calibri)\b", lowered) is None:
        penalty += 5

    score = max(0, 100 - (len(missing_sections) * 15) - penalty)
    return score, missing_sections


def detect_format_issues(text: str) -> List[str]:
    issues = []
    for hint in BAD_FORMAT_HINTS:
        if hint in text:
            issues.append("Uso de barras de progreso graficas")
            break

    lowered = text.lower()
    if any(section not in lowered for section in REQUIRED_SECTIONS):
        issues.append("Faltan secciones obligatorias")

    return issues
