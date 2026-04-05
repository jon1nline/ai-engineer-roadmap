from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    pergunta: str
    historico: Optional[List[Message]] = None

class ChatResponse(BaseModel):
    resposta: str
    fonte: list[str]


class ContextIngestRequest(BaseModel):
    textos: list[str]
    source: str = "manual"


class ContextIngestResponse(BaseModel):
    adicionados: int
    source: str
        

