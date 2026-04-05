from pathlib import Path

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import settings


class VectorDBService:
    def __init__(self):
        Path(settings.CHROMA_PATH).mkdir(parents=True, exist_ok=True)
        self.embeddings = SentenceTransformerEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_PATH,
            embedding_function=self.embeddings,
        )

    def add_context(self, texts: list[str], source: str = "manual") -> int:
        cleaned_texts = [text.strip() for text in texts if text and text.strip()]
        if not cleaned_texts:
            return 0

        metadatas = [{"source": source} for _ in cleaned_texts]
        self.vectorstore.add_texts(texts=cleaned_texts, metadatas=metadatas)
        if hasattr(self.vectorstore, "persist"):
            self.vectorstore.persist()
        return len(cleaned_texts)
