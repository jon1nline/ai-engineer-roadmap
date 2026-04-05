from fastapi import FastAPI
from app.api.v1.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Meu Assistente de IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # URL do seu Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas que criamos
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])

@app.get("/")
def read_root():
    return {"status": "Online", "message": "API de IA pronta para receber perguntas."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)