# GenAI-intelligent-rag-system
Production-Ready GenAI Project — Intelligent Document Q&amp;A System (RAG)

# Production-Ready GenAI Project — Intelligent Document Q&A System (RAG)

## What You Will Build

A production-grade Retrieval-Augmented Generation (RAG) platform where users can:

* Upload PDFs, DOCX, TXT files
* Extract and chunk text
* Create embeddings
* Store vectors in a vector database
* Ask questions using LLMs
* Get grounded answers with citations
* Stream responses in real time
* Maintain chat history
* Deploy with Docker
* Add authentication and observability
* Scale to production

This project teaches:

* Backend APIs
* LLM orchestration
* Vector databases
* Embeddings
* Prompt engineering
* Streaming APIs
* Docker
* Redis caching
* Celery background jobs
* Production deployment
* Monitoring and logging
* Security best practices
* CI/CD

---

# Tech Stack

| Layer            | Technology                    |
| ---------------- | ----------------------------- |
| Frontend         | React + Vite + Tailwind       |
| Backend API      | FastAPI                       |
| LLM Framework    | LangChain                     |
| Vector DB        | ChromaDB                      |
| Embedding Model  | OpenAI text-embedding-3-small |
| LLM              | GPT-4.1 / GPT-4o-mini         |
| Database         | PostgreSQL                    |
| Cache            | Redis                         |
| Background Jobs  | Celery                        |
| Auth             | JWT                           |
| File Storage     | Local / S3                    |
| Monitoring       | Prometheus + Grafana          |
| Containerization | Docker                        |
| Reverse Proxy    | Nginx                         |
| Deployment       | AWS / Azure / GCP             |

---

# High-Level Architecture

```text
                ┌─────────────────┐
                │     Frontend    │
                │ React + Vite UI │
                └────────┬────────┘
                         │ HTTPS
                         ▼
               ┌──────────────────┐
               │      Nginx       │
               │ Reverse Proxy    │
               └────────┬─────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
┌──────────────────┐         ┌──────────────────┐
│   FastAPI App    │         │   FastAPI App    │
│ API + Streaming  │         │ Horizontally     │
└────────┬─────────┘         │ Scaled           │
         │                   └──────────────────┘
         │
         ├─────────────┐
         ▼             ▼
┌────────────────┐ ┌────────────────┐
│   PostgreSQL   │ │     Redis      │
│ Metadata Store │ │ Cache + Queue  │
└────────────────┘ └────────────────┘
         │
         ▼
┌────────────────┐
│    ChromaDB    │
│ Vector Storage │
└────────────────┘
         │
         ▼
┌────────────────┐
│ OpenAI Models  │
│ LLM + Embeds   │
└────────────────┘
```

---

# Complete Folder Structure

```text
intelligent-rag-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── documents.py
│   │   │   │   └── health.py
│   │   │   └── deps.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   │
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── models/
│   │   │       ├── user.py
│   │   │       ├── document.py
│   │   │       └── chat.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── document.py
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── document_service.py
│   │   │   └── retrieval_service.py
│   │   │
│   │   ├── workers/
│   │   │   └── celery_worker.py
│   │   │
│   │   ├── utils/
│   │   │   ├── chunking.py
│   │   │   ├── loaders.py
│   │   │   └── helpers.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── Dockerfile
│
├── nginx/
│   └── nginx.conf
│
├── docker-compose.yml
├── .gitignore
├── README.md
└── Makefile
```

---

# Backend Setup

## requirements.txt

```txt
fastapi
uvicorn
python-dotenv
sqlalchemy
psycopg2-binary
pydantic
pydantic-settings
python-jose
passlib[bcrypt]
redis
celery
langchain
langchain-openai
langchain-community
chromadb
pypdf
python-multipart
openai
httpx
prometheus-fastapi-instrumentator
```

---

# Environment Variables

## .env

```env
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://postgres:postgres@db:5432/ragdb
REDIS_URL=redis://redis:6379
SECRET_KEY=super_secret
CHROMA_PATH=/app/chroma_db
```

---

# Configuration

## app/core/config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    CHROMA_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()
```

Explanation:

* BaseSettings automatically loads environment variables
* Keeps secrets outside source code
* Centralized configuration management
* Used everywhere in the application

---

# Database Setup

## app/db/session.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

Explanation:

* create_engine creates database connection pool
* sessionmaker creates database sessions
* autoflush=False improves control
* autocommit=False ensures explicit transactions

---

# User Model

## app/db/models/user.py

```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

Explanation:

* ORM model mapped to PostgreSQL table
* unique=True prevents duplicate users
* hashed_password stores encrypted passwords only

---

# Document Upload API

## app/api/routes/documents.py

```python
from fastapi import APIRouter, UploadFile, File
from app.services.document_service import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    result = process_document(
        filename=file.filename,
        content=content
    )

    return {
        "message": "Document processed",
        "result": result
    }
```

Line-by-line explanation:

```python
from fastapi import APIRouter, UploadFile, File
```

* APIRouter creates modular APIs
* UploadFile handles uploaded files efficiently
* File(...) marks field as required multipart upload

```python
router = APIRouter()
```

* Creates isolated route group

```python
@router.post("/upload")
```

* HTTP POST endpoint
* Accessible at /upload

```python
async def upload_document(file: UploadFile = File(...)):
```

* Async endpoint for non-blocking I/O
* Receives uploaded file

```python
content = await file.read()
```

* Reads uploaded file bytes asynchronously

```python
result = process_document(
    filename=file.filename,
    content=content
)
```

* Calls processing pipeline
* Extracts text
* Chunks text
* Generates embeddings
* Stores vectors

---

# Document Processing Pipeline

## app/services/document_service.py

```python
from app.utils.chunking import chunk_text
from app.services.embedding_service import create_embeddings
from app.services.vector_service import store_vectors
from langchain_community.document_loaders import PyPDFLoader


def process_document(filename: str, content: bytes):
    temp_path = f"/tmp/{filename}"

    with open(temp_path, "wb") as f:
        f.write(content)

    loader = PyPDFLoader(temp_path)
    pages = loader.load()

    full_text = "\n".join([page.page_content for page in pages])

    chunks = chunk_text(full_text)

    embeddings = create_embeddings(chunks)

    store_vectors(chunks, embeddings)

    return {
        "chunks": len(chunks)
    }
```

---

# Chunking Strategy

## app/utils/chunking.py

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_text(text)
```

Why chunking matters:

* LLMs have token limits
* Small chunks improve retrieval accuracy
* Overlap preserves context between chunks

---

# Embedding Service

## app/services/embedding_service.py

```python
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

embedding_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    model="text-embedding-3-small"
)


def create_embeddings(chunks):
    return embedding_model.embed_documents(chunks)
```

Explanation:

* Converts text into numerical vectors
* Similar meaning → closer vectors
* Enables semantic search

---

# Vector Database Service

## app/services/vector_service.py

```python
import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
collection = client.get_or_create_collection("documents")


def store_vectors(chunks, embeddings):
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
```

Explanation:

* ChromaDB stores vector embeddings
* Semantic similarity search becomes possible
* IDs uniquely identify chunks

---

# Retrieval Service

## app/services/retrieval_service.py

```python
from app.services.vector_service import collection
from app.services.embedding_service import embedding_model


def retrieve_context(query: str):
    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]
```

What happens:

1. User asks question
2. Query converted into embedding
3. Vector DB searches nearest vectors
4. Best matching chunks returned

---

# LLM Service

## app/services/llm_service.py

```python
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def ask_llm(question: str, context: list):
    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
```

Critical RAG concept:

* Context grounding reduces hallucinations
* LLM answers only from retrieved documents
* Better trust and accuracy

---

# Chat API

## app/api/routes/chat.py

```python
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import retrieve_context
from app.services.llm_service import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: ChatRequest):
    context = retrieve_context(request.question)

    answer = ask_llm(
        request.question,
        context
    )

    return {
        "answer": answer,
        "context": context
    }
```

End-to-end flow:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Context Retrieval
   ↓
Prompt Construction
   ↓
LLM Generation
   ↓
Response
```

---

# Main Application

## app/main.py

```python
from fastapi import FastAPI
from app.api.routes import chat, documents

app = FastAPI(title="Production RAG System")

app.include_router(chat.router, prefix="/chat")
app.include_router(documents.router, prefix="/documents")

@app.get("/")
def health_check():
    return {"status": "running"}
```

---

# Frontend Example

## React Chat Component

```jsx
import { useState } from "react"

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")

  const askQuestion = async () => {
    const response = await fetch("http://localhost:8000/chat/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question
      })
    })

    const data = await response.json()

    setAnswer(data.answer)
  }

  return (
    <div>
      <h1>AI Document Q&A</h1>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <p>{answer}</p>
    </div>
  )
}

export default App
```

---

# Docker Setup

## backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# docker-compose.yml

```yaml
version: '3.9'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - redis
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  redis:
    image: redis:7

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ragdb
```

---

# Build & Run Steps

## Step 1 — Clone Project

```bash
git clone <repo>
cd intelligent-rag-system
```

---

## Step 2 — Add API Key

```env
OPENAI_API_KEY=your_key
```

---

## Step 3 — Start Docker

```bash
docker-compose up --build
```

---

## Step 4 — Verify APIs

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:3000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# Testing the System

## Upload Document

```bash
curl -X POST \
  http://localhost:8000/documents/upload \
  -F "file=@sample.pdf"
```

---

## Ask Question

```bash
curl -X POST http://localhost:8000/chat/ask \
-H "Content-Type: application/json" \
-d '{
  "question": "What is the revenue mentioned in the report?"
}'
```

---

# Production Improvements

## 1. Authentication

Add:

* JWT access tokens
* Refresh tokens
* RBAC authorization

---

## 2. Observability

Use:

* Prometheus
* Grafana
* Loki
* OpenTelemetry

Metrics:

* Request latency
* Token usage
* Vector retrieval latency
* Cost per request

---

# 3. Streaming Responses

Use:

```python
StreamingResponse
```

Benefits:

* Better UX
* Real-time response generation
* ChatGPT-like experience

---

# 4. Caching

Cache:

* Embeddings
* LLM responses
* Retrieval results

Use Redis.

---

# 5. Async Processing

Use Celery for:

* PDF ingestion
* OCR jobs
* Large embedding creation

---

# 6. Security Best Practices

Implement:

* Rate limiting
* File validation
* Malware scanning
* Prompt injection protection
* SQL injection protection
* Secrets manager

---

# 7. Prompt Injection Protection

Example:

```python
FORBIDDEN_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt"
]
```

---

# 8. Cost Optimization

Strategies:

* Cache embeddings
* Use smaller models for retrieval
* Hybrid search
* Batch embeddings
* Context compression

---

# 9. Scaling Strategy

Scale:

* Stateless FastAPI containers
* Managed PostgreSQL
* Distributed vector DB
* GPU inference servers
* Kubernetes autoscaling

---

# 10. CI/CD Pipeline

Use:

* GitHub Actions
* Docker Hub
* Kubernetes
* Helm

Pipeline:

```text
Push Code
   ↓
Run Tests
   ↓
Build Docker Images
   ↓
Security Scan
   ↓
Deploy to Staging
   ↓
Run Integration Tests
   ↓
Deploy to Production
```

---

# Advanced Learning Scenarios

## Scenario 1 — Multi-PDF Chat

Goal:

* Upload multiple documents
* Ask cross-document questions

Learn:

* Metadata filtering
* Multi-document retrieval

---

## Scenario 2 — Hybrid Search

Combine:

* BM25 keyword search
* Semantic vector search

Learn:

* Ranking
* Re-ranking

---

## Scenario 3 — Conversational Memory

Add:

* Chat history
* Context windows
* Session memory

Learn:

* Memory management
* Token optimization

---

## Scenario 4 — Agentic RAG

Build AI agents that:

* Search web
* Query SQL
* Read PDFs
* Call APIs

Learn:

* Tool calling
* Function calling
* Agents

---

## Scenario 5 — OCR Pipeline

Handle scanned PDFs using:

* Tesseract OCR
* AWS Textract

Learn:

* Image preprocessing
* OCR pipelines

---

## Scenario 6 — Evaluation Framework

Measure:

* Faithfulness
* Answer relevance
* Hallucination rate

Use:

* RAGAS
* DeepEval

---

## Scenario 7 — Fine-Tuning

Train domain-specific assistants.

Learn:

* SFT
* RLHF basics
* Dataset preparation

---

## Scenario 8 — Multi-Modal RAG

Add:

* Image understanding
* Audio transcription
* Video summarization

---

# Common Interview Questions

## What is RAG?

Retrieval-Augmented Generation combines:

* Information retrieval
* Large language models

to provide grounded and accurate responses.

---

## Why embeddings?

Embeddings convert semantic meaning into vectors so similar concepts are close in vector space.

---

## Why chunk overlap?

Overlap preserves continuity between chunks and improves retrieval quality.

---

## Why vector databases?

They perform efficient nearest-neighbor similarity search.

---

# Real Production Challenges

## Challenge 1 — Hallucinations

Fix:

* Better prompts
* Better retrieval
* Citations
* Confidence scoring

---

## Challenge 2 — Large Documents

Fix:

* Hierarchical chunking
* Summarization
* Parent-child retrieval

---

## Challenge 3 — Latency

Fix:

* Async I/O
* Caching
* Smaller models
* Streaming

---

# Suggested Learning Path

## Beginner

Learn:

* Python
* APIs
* FastAPI
* Docker
* SQL

---

## Intermediate

Learn:

* LangChain
* Vector DBs
* Embeddings
* Prompt engineering

---

## Advanced

Learn:

* Agents
* Fine-tuning
* Multi-modal systems
* Distributed systems
* Kubernetes

---

# Resume Project Description

Built a production-ready Retrieval-Augmented Generation platform using FastAPI, LangChain, ChromaDB, OpenAI, PostgreSQL, Redis, Docker, and React. Implemented document ingestion, semantic search, vector embeddings, grounded LLM responses, streaming APIs, authentication, observability, and scalable microservice deployment.

---

# Next-Level Enhancements

You can extend this into:

* AI Research Assistant
* Legal AI Platform
* Medical Knowledge Assistant
* Enterprise Knowledge Bot
* AI Support Chatbot
* AI Coding Assistant
* Multi-agent autonomous systems

---

# Final Learning Strategy

Do NOT just run the project.

For every file:

1. Read code line-by-line
2. Add print/debug logs
3. Break the code intentionally
4. Fix errors yourself
5. Replace models
6. Change chunk sizes
7. Swap vector databases
8. Add new APIs
9. Measure latency
10. Deploy to cloud

That is how you become production-level in GenAI engineering.
