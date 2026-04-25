# Hybrid Product Search

A modular system for building hybrid search experiences combining keyword-based retrieval with semantic vector search.

This project is designed to explore and implement modern search architectures, including embedding pipelines, structured data indexing, and ranking strategies.

---

## System Overview

The system is composed of independent services that work together to enable hybrid search:

Client → API layer → Search service → Elasticsearch  
                      ↘  
                       Embedding service

---

## Services

### Vector Embedder
Generates semantic embeddings for structured product data.

- Location: `apps/vector-embedder`
- Endpoint: https://embed.danielreagan.dev
- Docs: https://embed.danielreagan.dev/docs
- Responsibility:
  - Extract text fields from structured input
  - Generate embeddings using SentenceTransformers
  - Return structured vectors for downstream indexing

---

## Architecture Goals

- Combine keyword and semantic search (hybrid retrieval)
- Support structured product data with field-level embeddings
- Keep services modular and independently deployable
- Enable scalable indexing and ranking pipelines

---

## Current Status

- ✅ Embedding service deployed and running in production (AWS EC2 + nginx + HTTPS)
- 🚧 Search service (Elasticsearch integration)
- 🚧 Hybrid ranking (keyword + vector scoring)

---

## Future Work

- Integrate embeddings into Elasticsearch index
- Implement hybrid search endpoint (`/search`)
- Add ranking strategies (BM25 + vector similarity)
- Introduce query understanding / expansion
- Add monitoring and performance metrics

---

## Repository Structure

apps/
  vector-embedder/   # embedding service (FastAPI)

---

## Notes

This repository is focused on backend search systems and infrastructure rather than UI.

Each service is designed to be independently runnable and deployable.