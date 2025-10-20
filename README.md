## Document Agent (RAG over your PDFs)

A FastAPI-based service to upload PDF documents, chunk and embed them into a vector database (Chroma), and query them via a lightweight RAG pipeline powered by an LLM (default: Ollama).

### Features
- Upload PDF files and persist metadata in SQL (default SQLite; Postgres optional)
- Chunk, embed, and store vectors in Chroma (persistent or client/server)
- Query with top-k context retrieval and LLM-generated answers
- Simple, production-ready FastAPI structure with logging

---

## Prerequisites
- Python 3.13 (project venv already included as `venv/`)
- uv (recommended) or pip
- Optional: Postgres (if not using SQLite)
- Optional: [Ollama](https://ollama.com) running locally if you want on-device LLMs

---

## Quick Start

### Option A) Using uv (recommended)

1) Install uv (one-time):

```bash
# via pipx (recommended)
pipx install uv
# or via pip
pip install --user uv
```

2) Create a virtual environment (managed by uv):

```bash
uv venv
source .venv/bin/activate
```

3) Install dependencies with uv pip:

```bash
uv pip install -r requirements.txt
```

4) Configure environment (create `.env` in repo root as needed):

```bash
# Database
DB_TYPE=sqlite                        # sqlite | postgres
SQLITE_PATH=knowledge_base_local.db   # used when DB_TYPE=sqlite

# For postgres (only if DB_TYPE=postgres)
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=document_agent

# Chroma
CHROMA_MODE=persistent                # persistent | http
CHROMA_DB_PATH=data/chroma            # used for persistent mode
CHROMA_HOST=localhost                 # used for http mode
CHROMA_PORT=8000                      # used for http mode

# LLM
LLM_MODEL=llama3.2:1b                 # example model name for Ollama
```

Notes:
- All settings are loaded via `pydantic-settings` from `.env` and have sane defaults. See `app/db/config.py` for exact names.

5) Run the server:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000` and docs at `http://127.0.0.1:8000/docs`.

### Option B) Using pip (alternative)

1) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run the server:

```bash
uvicorn app.main:app --reload
```

---

## API Reference

### 1) Upload Knowledge Base
- Method: POST
- Path: `/upload/`
- Consumes: `multipart/form-data`

Form fields:
- `file` (required): PDF file
- `document_name` (required): string
- `author` (optional): string
- `source` (optional): string

Example with curl:

```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -F "file=@uploaded_pdfs/sample.pdf" \
  -F "document_name=Sample" \
  -F "author=Alice" \
  -F "source=Internal"
```

Response:
```json
{
  "status": "success",
  "message": "Successfully uploaded knowledge base!",
  "file_name": "sample.pdf"
}
```

Notes:
- Only `application/pdf` is allowed by default (`app/utils/routes_consents.py`).

### 2) Ask a Question
- Method: POST
- Path: `/ask/`
- Body: `application/json`

Schema:
```json
{
  "query": "string",
  "top_k": 3
}
```

Example:
```bash
curl -X POST "http://127.0.0.1:8000/ask/" \
  -H "Content-Type: application/json" \
  -d '{"query": "What does the document say about X?", "top_k": 3}'
```

Response (example):
```json
{
  "status": "success",
  "message": "Successfully retrieved context about query",
  "answer": "..."
}
```

---

## How It Works (High Level)
1) Upload: PDF is validated, saved under `uploaded_pdfs/`, chunked, embedded, and stored in Chroma. Basic metadata is saved in SQL.
2) Query: The query is embedded, top-k similar chunks are retrieved from Chroma, and the LLM produces a concise answer using that context.

---

## Configuration

Database (see `app/db/config.py`):
- Default is SQLite at `knowledge_base_local.db`.
- To use Postgres, set `DB_TYPE=postgres` and provide `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.

Chroma (see `app/db/config.py` and `app/db/vector_db/vector_chromadb.py`):
- Persistent (default): uses `data/chroma` directory.
- HTTP mode: connect to a running Chroma server via `CHROMA_HOST` and `CHROMA_PORT`.

LLM:
- Default `LLM_MODEL` is `llama3.2:1b` for Ollama. Adjust per your environment.

---

## Running with Ollama
Install Ollama and pull a model, e.g.:

```bash
brew install ollama
ollama pull llama3.2:1b
ollama serve
```

Then start the API as usual. The service will call Ollama locally.


## Development

Run with live reload:
```bash
uv run uvicorn app.main:app --reload
```

---

## Docker

### Build and run with Docker

```bash
# Build image
docker build -t document-agent:latest .

# Run container (mounts data and sets default env)
docker run --name document-agent \
  -p 8000:8000 \
  -v $(pwd)/uploaded_pdfs:/app/uploaded_pdfs \
  -v $(pwd)/data/chroma:/app/data/chroma \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  document-agent:latest
```

API will be at `http://127.0.0.1:8000`.

### Using docker-compose (minimal)

```bash
docker compose up --build
```

This starts a single service:
- app: FastAPI server on port 8000, using SQLite and local persistent Chroma directory mounted from the host

Code layout aims for clarity and separation of concerns. Linting is enforced in-editor; adjust to your preferences.

---

## License
MIT (or your preferred license)


