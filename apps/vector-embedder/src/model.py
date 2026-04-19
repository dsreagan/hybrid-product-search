"""
Field-agnostic embedding engine.

This module only embeds lists of strings.
It does not know about ids, fields, or payload structure.
"""

from __future__ import annotations
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from pathlib import Path


MODEL_PATH = str(Path(__file__).resolve().parent.parent / "models" / "all-MiniLM-L12-v2")
_embedder = None # lazy-loaded model cache


def _batch(seq, batch_size):
    for i in range(0, len(seq), batch_size):
        yield seq[i : i + batch_size]


@dataclass
class Embedder:
    model_path: str = MODEL_PATH

    def __post_init__(self):
        self._model = SentenceTransformer(self.model_path)
        self.dims = int(self._model.get_sentence_embedding_dimension())

    def encode_texts(self, texts, batch_size=256):
        """
        Encode a list of texts into vectors.
        Returns vectors aligned with input order.
        """
        output = []

        for batch in _batch(list(texts), batch_size):
            vectors = self._model.encode(
                list(batch),
                normalize_embeddings=True,
                show_progress_bar=False
            )
            output.extend(vectors.tolist())

        return output
    

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder


def embed_texts(texts):
    """
    Embed a list of strings.
    Returns list of vectors in the same order.
    Invalid inputs are replaced with empty strings.
    """
    if not texts or isinstance(texts, (str, bytes)):
        return []
    
    texts = [t if isinstance(t, str) else "" for t in texts]

    embedder = get_embedder()
    return embedder.encode_texts(texts)