import os

from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://samuelsanchezheredia@localhost:5432/cv_ats",
    )
    keywords_path: str = os.getenv("KEYWORDS_PATH", "./data/keywords.json")
    faqs_path: str = os.getenv("FAQS_PATH", "./data/faqs.json")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")


settings = Settings()
