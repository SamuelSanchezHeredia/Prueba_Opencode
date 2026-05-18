from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/cv_ats"
    keywords_path: str = "./data/keywords.json"


settings = Settings()
