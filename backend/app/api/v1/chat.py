from fastapi import APIRouter, UploadFile, File
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

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    ai_service = AIService()
    num_chunks = ai_service.process_pdf(temp_path)
    return{"message": f"PDF processado com sucesso {num_chunks} trechos adicionados ao conhecimento."}