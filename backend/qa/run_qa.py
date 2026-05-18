import argparse
import json
from pathlib import Path

from app.services.ats import evaluate_format
from app.services.keywords import load_keywords, match_keywords
from app.services.semantic import analyze_experience


def load_expected(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def summarize_result(filename: str, sector: str, text: str, keywords_path: str):
    ats_score, missing_sections = evaluate_format(text)
    keyword_map = load_keywords(keywords_path)
    keyword_score, found_keywords, missing_keywords = match_keywords(text, sector, keyword_map)
    corrections = analyze_experience(text)
    return {
        "filename": filename,
        "ats_score": ats_score,
        "keyword_score": keyword_score,
        "missing_sections": missing_sections,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "corrections": corrections,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", default="expected_issues.json")
    parser.add_argument("--text-dir", default="./fixtures_text")
    parser.add_argument("--keywords", default="../data/keywords.json")
    args = parser.parse_args()

    fixtures_path = Path(args.fixtures)
    text_dir = Path(args.text_dir)
    expected = load_expected(fixtures_path)

    results = []
    for filename, meta in expected.items():
        text_file = text_dir / f"{filename}.txt"
        if not text_file.exists():
            results.append({"filename": filename, "error": "Missing text fixture"})
            continue
        text = text_file.read_text(encoding="utf-8")
        results.append(summarize_result(filename, meta["target_sector"], text, args.keywords))

    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
