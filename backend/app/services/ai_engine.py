from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class AIService:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_PATH, 
            embedding_function=self.embeddings
        )
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, 
            google_api_key=settings.GOOGLE_API_KEY
        )

    def process_pdf(self, file_path: str):
        loader = PyPDFLoader(file_path)
        paginas = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            )
        chunks = text_splitter.split_documents(paginas)
        self.vectorstore.add_documents(chunks)
        return len(chunks)

    def ask_question(self, question: str, historico: List):
        docs = self.vectorstore.similarity_search(question, k=3)
        contexto_docs = "\n".join([d.page_content for d in docs])
        
        prompt = f"Use o contexto abaixo para responder \n{contexto_docs}\n\nPergunta: {question}"
        
        texto_historico = ""

        for msg in historico[-5:]:
            label = "Usuário" if msg.role == "user" else "Assistente"
            texto_historico += f"{label}: {msg.content}\n"

        prompt = f"""
        Você é um tutor dedicado ao projeto aprendendo RAG. 
        Use o CONTEXTO abaixo para responder, levando em conta o HISTÓRICO da conversa.
    
        CONTEXTO DOS DOCUMENTOS:
        {contexto_docs}
    
        HISTÓRICO RECENTE:
        {texto_historico}
    
        PERGUNTA ATUAL: {question}
        Resposta:"""    

        response = self.llm.invoke(prompt)

        fontes = []
        for doc in docs:
            source = doc.metadata.get("source", "desconhecida")
            if source not in fontes:
                fontes.append(source)

        return {
            "resposta": response.content,
            "fonte": fontes,
        }