from fastapi import FastAPI
from app.api.routes import chat, documents

app = FastAPI(title="Production RAG System")

app.include_router(chat.router, prefix="/chat")
app.include_router(documents.router, prefix="/documents")

@app.get("/")
def health_check():
    return {"status": "running"}