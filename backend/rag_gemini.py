import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_classic.chains import RetrievalQA

load_dotenv(dotenv_path=Path(__file__).resolve().with_name(".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

textos_projeto = [
    "O projeto utiliza GeoDjango e PostGIS para análise geoespacial.",
    "A arquitetura do sistema segue princípios SOLID para garantir manutenção.",
    "O deploy é feito via Docker no Hugging Face Spaces.",
    "O banco de dados principal é o Supabase."
    "O projeto é desenvolvido em Python e utiliza FastAPI para a API."
]

vectorstore = Chroma.from_texts(
    textos_projeto, 
    embedding=embeddings
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7, 
    api_key=GOOGLE_API_KEY
)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

pergunta = "O que você sabe sobre o projeto?"
resposta = rag_chain.invoke(pergunta)

print(f"Pergunta: {pergunta}")
print(f"Resposta da IA: {resposta['result']}")
