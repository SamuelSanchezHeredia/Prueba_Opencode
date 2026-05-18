import json
from typing import Any, Dict

from openai import OpenAI

from ..config import settings


SYSTEM_PROMPT = (
    "Eres un Reclutador Tecnico Senior. Analiza experiencia laboral y reescribe "
    "frases debiles con impacto medible. Devuelve solo JSON con el contrato solicitado."
)


def call_semantic_llm(experience_text: str, target_sector: str) -> Dict[str, Any]:
    if not settings.openai_api_key:
        return {
            "primary_hypothesis": "Sin API key de LLM configurada.",
            "alternatives": [],
            "next_check": "Configurar OPENAI_API_KEY para analisis semantico real.",
            "short_explanation": "Se uso modo stub.",
            "confidence": 0.0,
        }

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "Sector objetivo: "
        + target_sector
        + "\n"
        + "Experiencia:\n"
        + experience_text
        + "\n"
        + "Contrato JSON:\n"
        + json.dumps(
            {
                "primary_hypothesis": "",
                "alternatives": [],
                "next_check": "",
                "short_explanation": "",
                "confidence": 0.0,
            },
            ensure_ascii=False,
        )
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_output_tokens=300,
    )

    raw = response.output_text
    return json.loads(raw)
