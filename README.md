# Projeto AI - Fullstack (Frontend + Backend)

Este repositorio foi criado para registrar o estudo de IA Generativa e RAG que estou aprendendo na pratica.

Projeto fullstack com:
- Frontend em Next.js (App Router)
- Backend em FastAPI
- Pipeline RAG com ChromaDB + embeddings + Google Gemini
- Orquestracao com Docker Compose

## Visao Geral

O frontend envia perguntas para o backend.
O backend busca contexto no banco vetorial (Chroma), monta um prompt com historico da conversa e retorna a resposta da IA.

Fluxo resumido:
1. Usuario envia pergunta no frontend.
2. Backend recebe em `POST /api/v1/perguntar`.
3. Backend faz busca semantica no Chroma.
4. Backend consulta o modelo Gemini.
5. Frontend renderiza a resposta.

## Estrutura do Projeto

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/v1/chat.py
|   |   |-- core/config.py
|   |   |-- schemas/chat.py
|   |   |-- services/ai_engine.py
|   |   `-- services/vector_db.py
|   |-- chroma_db/
|   |-- Dockerfile
|   |-- requirements.txt
|   `-- .env.example
|-- frontend/
|   |-- src/app/
|   |-- Dockerfile
|   |-- package.json
|   `-- next.config.ts
|-- docker-compose.yml
`-- README.md
```

## Pre-requisitos

- Docker + Docker Compose
- (Opcional para rodar sem Docker) Python 3.11+ e Node.js 22+

## Variaveis de Ambiente

Crie um arquivo `backend/.env` baseado em `backend/.env.example`.

Exemplo:

```env
GOOGLE_API_KEY=sua_chave_google_aqui
CHROMA_PATH=./chroma_db
```

Observacoes:
- `GOOGLE_API_KEY` e obrigatoria para respostas da IA.
- `CHROMA_PATH` define onde os vetores ficam persistidos.

## Rodando com Docker (recomendado)

Na raiz do projeto:

```bash
docker compose up --build
```

Servicos:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Docs FastAPI: http://localhost:8000/docs

Para parar:

```bash
docker compose down
```

Para limpar volumes/imagens nao usados (opcional):

```bash
docker system prune -f
```

## Rodando sem Docker

### 1. Backend (FastAPI)

Na pasta `backend/`:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (Next.js)

Na pasta `frontend/`:

```bash
npm install
npm run dev
```

A aplicacao fica em http://localhost:3000.

## Endpoints Principais

### `POST /api/v1/perguntar`

Envia uma pergunta com historico opcional.

Request:

```json
{
  "pergunta": "O que e RAG?",
  "historico": [
    { "role": "user", "content": "Oi" },
    { "role": "assistant", "content": "Ola!" }
  ]
}
```

Response:

```json
{
  "resposta": "RAG e...",
  "fonte": ["manual", "documentacao"]
}
```

### `POST /api/v1/contexto`

Adiciona textos ao banco vetorial.

Request:

```json
{
  "textos": ["Texto 1", "Texto 2"],
  "source": "manual"
}
```

Response:

```json
{
  "adicionados": 2,
  "source": "manual"
}
```

## Teste Rapido com cURL

### Ingerir contexto

```bash
curl -X POST http://localhost:8000/api/v1/contexto \
  -H "Content-Type: application/json" \
  -d '{"textos": ["RAG combina busca e geracao"], "source": "manual"}'
```

### Perguntar

```bash
curl -X POST http://localhost:8000/api/v1/perguntar \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Explique RAG em 1 frase", "historico": []}'
```

## Dicas de Troubleshooting

- Erro de CORS:
  - confirme que o frontend esta em `http://localhost:3000`.
- Erro de chave da IA:
  - valide `GOOGLE_API_KEY` no `backend/.env`.
- Frontend sem comunicar com backend no Docker:
  - reconstrua com `docker compose up --build`.




