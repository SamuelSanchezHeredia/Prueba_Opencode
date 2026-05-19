import re
from typing import Dict, List


WEAK_PHRASES = [
    "encargado",
    "responsable",
    "participe",
    "ayude",
    "apoye",
    "colabore",
    "apoyar",
    "apoyo",
    "colaboracion",
    "tareas",
]

ACTION_STARTERS = [
    "desarrolle",
    "implement",
    "optim",
    "lider",
    "mejor",
    "coord",
    "gestion",
    "dise",
]


def _split_fragments(text: str) -> List[str]:
    fragments = re.split(r"[\n\r]|(?<=[.!?])\s+", text)
    return [fragment.strip() for fragment in fragments if fragment.strip()]


def _needs_metrics(fragment: str) -> bool:
    return not re.search(r"\d+", fragment)


def analyze_experience(experience_text: str) -> List[Dict[str, str]]:
    if not experience_text:
        return []

    fragments = _split_fragments(experience_text)
    suggestions: List[Dict[str, str]] = []

    for fragment in fragments:
        lowered = fragment.lower()
        starts_action = any(lowered.startswith(prefix) for prefix in ACTION_STARTERS)
        has_weak = any(phrase in lowered for phrase in WEAK_PHRASES)
        if len(fragment) < 25:
            continue
        if _needs_metrics(fragment) and (starts_action or has_weak):
            suggestions.append(
                {
                    "original_text": fragment,
                    "suggested_text": "Logre resultados medibles, por ejemplo, reduciendo tiempos un 20% o aumentando conversiones un 15%.",
                    "explanation": "Falta impacto cuantificable o contexto de resultados.",
                    "category": "impacto",
                }
            )

    if not suggestions and fragments:
        suggestions.append(
            {
                "original_text": fragments[0],
                "suggested_text": "Incluye metricas concretas (porcentaje, volumen o ahorro) para reforzar el impacto.",
                "explanation": "No se detectaron metricas en la experiencia.",
                "category": "impacto",
            }
        )

    return suggestions


def detect_semantic_issues(experience_text: str) -> List[str]:
    if not experience_text:
        return []
    lowered = experience_text.lower()
    issues = []
    if not re.search(r"\d+", experience_text):
        issues.append("Sin metricas de proyectos")
    if any(phrase in lowered for phrase in WEAK_PHRASES):
        issues.append("Falta de verbos de accion")

    return issues
