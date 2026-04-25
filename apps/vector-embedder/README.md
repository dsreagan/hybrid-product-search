# Vector Embedder

Lightweight text embedding service built with SentenceTransformers.

Designed as a component in a hybrid search system, this service enables semantic vector generation for downstream retrieval and ranking.

This project takes structured input data, extracts text fields, generates vector embeddings, and returns the results in the original structure. It supports both command-line usage and an HTTP API through FastAPI.

## Features

- Generate embeddings from structured JSON input
- Preserve original item structure in the output
- Run from the command line or as an API service
- Use a local SentenceTransformers model
- Simple, modular pipeline design

## Project Structure

models/
└── all-MiniLM-L12-v2/   # local model files

src/
├── model.py             # loads model and generates embeddings
├── pipeline.py          # flattens text fields and rebuilds output structure
├── cli.py               # stdin/stdout interface
└── api.py               # FastAPI HTTP interface

## Architecture

Client → nginx (80/443) → uvicorn (127.0.0.1:8000) → FastAPI → pipeline → model

Adapters:
- cli.py → command-line / stdin-stdout interface
- api.py → HTTP interface via FastAPI

Core processing:
- pipeline.py → maps structured items -> text batches -> structured embeddings
- model.py → loads the embedding model and processes lists of strings

Flow:

    embed_items()
       /      \
     cli      api

## Requirements

- Python 3.11
- sentence-transformers
- fastapi
- uvicorn

## Setup

Create and activate a virtual environment:

    py -3.11 -m venv .venv
    source .venv/Scripts/activate

Install dependencies:

    pip install sentence-transformers fastapi uvicorn

## Download the Model

Run the following once to download and save the model locally:

    python - <<'PY'
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    model.save("./models/all-MiniLM-L12-v2")
    PY 

## CLI Usage

Pass JSON into the CLI through stdin:

    echo '[{"id":1,"fields":{"desc":"test"}}]' | python -m src.cli

## API Usage

Start the server:

    uvicorn src.api:app --reload

Example request:

    curl -X POST http://127.0.0.1:8000/embed \
      -H "Content-Type: application/json" \
      -d '[{"id":1,"fields":{"desc":"test"}}]'

## Input Format

Expected input:

    [
      {
        "id": 1,
        "fields": {
          "desc": "text",
          ...
        }
      },
      ...
    ]

## Output Format

Returned output:

    [
      {
        "id": 1,
        "embeddings": {
          "desc": [ ... ],
          ...
        }
      },
      ...
    ]

## Example Use Case

This service is useful when you need to generate embeddings for structured records such as:

- product descriptions
- catalog metadata
- search documents
- internal content records

It allows structured application data to be transformed into embedding-ready vectors without losing field relationships.

## Deployment

This service is deployed on AWS EC2 using nginx as a reverse proxy with HTTPS.

Live endpoint:
https://embed.danielreagan.dev

API docs:
https://embed.danielreagan.dev/docs

### Example request (production)

curl -X POST https://embed.danielreagan.dev/embed \
  -H "Content-Type: application/json" \
  -d '[{"id":1,"fields":{"desc":"hello world"}}]'

### Infrastructure

- AWS EC2 (Ubuntu)
- FastAPI + uvicorn
- nginx reverse proxy
- systemd service for process management
- Let's Encrypt (certbot) for HTTPS

## Notes

- The model is stored locally under `models/all-MiniLM-L12-v2`
- The CLI is useful for pipelines and scripting
- The API is useful for integrating embeddings into other services
- The pipeline separates input/output shaping from model inference for easier extension