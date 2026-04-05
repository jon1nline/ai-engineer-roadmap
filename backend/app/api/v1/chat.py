from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse, ContextIngestRequest, ContextIngestResponse
from app.services.ai_engine import AIService
from app.services.vector_db import VectorDBService


router = APIRouter()


@router.post("/perguntar", response_model=ChatResponse)
async def ask_ai(request: ChatRequest):
    ai_service = AIService()
    resultado = ai_service.ask_question(
        request.pergunta,
        request.historico or []
    )
    return resultado


@router.post("/contexto", response_model=ContextIngestResponse)
async def ingest_context(request: ContextIngestRequest):
    vector_service = VectorDBService()
    total = vector_service.add_context(texts=request.textos, source=request.source)
    return {"adicionados": total, "source": request.source}