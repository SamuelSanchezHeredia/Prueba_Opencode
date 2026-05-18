import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_keywords(path: str) -> Dict[str, List[str]]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def match_keywords(text: str, sector: str, keyword_map: Dict[str, List[str]]) -> Tuple[int, List[str], List[str]]:
    lowered = text.lower()
    sector_keywords = keyword_map.get(sector, [])
    found = [kw for kw in sector_keywords if kw.lower() in lowered]
    missing = [kw for kw in sector_keywords if kw.lower() not in lowered]

    if not sector_keywords:
        return 0, found, missing

    score = int((len(found) / len(sector_keywords)) * 100)
    return score, found, missing
