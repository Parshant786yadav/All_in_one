# rag.py
# Model is lazy-loaded to avoid OOM on startup (e.g. Render 512MB).

import numpy as np
import json

_model = None
MODEL_NAME = "all-MiniLM-L6-v2"


def _get_model():
    """Load sentence-transformers model on first use (saves ~300MB at startup)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def split_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks


def create_embedding(text):
    model = _get_model()
    embedding = model.encode(text)
    return embedding.tolist()


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))