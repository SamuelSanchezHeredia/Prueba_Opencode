from typing import List

from sentence_transformers import SentenceTransformer

from src.config import settings


_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embeddings_model)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()
