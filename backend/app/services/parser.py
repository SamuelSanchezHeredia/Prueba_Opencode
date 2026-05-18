import re
from pathlib import Path
from typing import Dict, List

import fitz
from docx import Document


SECTION_HEADERS = {
    "experience": ["experiencia", "experience", "trayectoria"],
    "education": ["educacion", "educación", "education", "formacion", "formación"],
    "skills": ["habilidades", "skills", "competencias", "tecnologias", "tecnologías"],
}


def _clean_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def _extract_sections(text: str) -> Dict[str, str]:
    lowered = text.lower()
    positions: List[tuple[str, int]] = []
    for section, headers in SECTION_HEADERS.items():
        for header in headers:
            index = lowered.find(header)
            if index != -1:
                positions.append((section, index))

    if not positions:
        return {"full_text": text}

    positions.sort(key=lambda item: item[1])
    sections: Dict[str, str] = {}
    for i, (section, start) in enumerate(positions):
        end = positions[i + 1][1] if i + 1 < len(positions) else len(text)
        sections[section] = _clean_text(text[start:end])
    return sections


def parse_document(file_path: Path) -> Dict[str, str]:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text("text") for page in doc)
    elif suffix == ".docx":
        doc = Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type")

    cleaned = _clean_text(text)
    return _extract_sections(cleaned)
