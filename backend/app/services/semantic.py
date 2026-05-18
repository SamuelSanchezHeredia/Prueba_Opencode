import re
from typing import List, Dict


WEAK_PHRASES = [
    "encargado",
    "responsable",
    "participe",
    "ayude",
    "apoye",
]


def analyze_experience(experience_text: str) -> List[Dict[str, str]]:
    sentences = re.split(r"(?<=[.!?])\s+", experience_text.strip())
    suggestions = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(phrase in lowered for phrase in WEAK_PHRASES) and not re.search(r"\d+", sentence):
            suggestions.append(
                {
                    "original_text": sentence,
                    "suggested_text": "Optimice procesos reduciendo tiempos y mejorando resultados medibles.",
                    "explanation": "Falta impacto cuantificable en la frase.",
                    "category": "impacto",
                }
            )
    return suggestions
