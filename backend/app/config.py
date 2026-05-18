import os

from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://samuelsanchezheredia@localhost:5432/cv_ats",
    )
    keywords_path: str = os.getenv("KEYWORDS_PATH", "./data/keywords.json")
    faqs_path: str = os.getenv("FAQS_PATH", "./data/faqs.json")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
