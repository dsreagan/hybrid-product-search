"""
Fast API wrapper for the embedding service.

Exposes:
- POST /embed   -> embed structured items
- GET  /health  -> service health check
"""

from fastapi import FastAPI
from .pipeline import embed_items
from typing import List

app = FastAPI()

# Load model once at startup (avoid first-request latency)
@app.on_event("startup")
def load_model():
    from .model import get_embedder
    get_embedder()

@app.post("/embed")
def embed(items: List[dict]) -> list[dict]:
    return embed_items(items)

@app.get("/health")
def health():
    return {"status": "ok"}