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