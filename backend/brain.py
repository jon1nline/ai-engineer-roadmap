import chromadb
from chromadb.utils import embedding_functions


client = chromadb.Client()

collection = client.get_or_create_collection(name="meu_conhecimento")

collection.add(
    documents=[
        "O FastAPI é um framework web moderno e rápido para Python.",
        "O React é uma biblioteca JavaScript para construir interfaces de usuário.",
        "Embeddings transformam palavras em listas de números decimais.",
        "A similaridade de cosseno mede o ângulo entre dois vetores."
    ],
    metadatas=[
        {"categoria": "backend"},
        {"categoria": "frontend"},
        {"categoria": "ia"},
        {"categoria": "ia"}
    ],
    ids=["id1", "id2", "id3", "id4"]
)

pergunta = "Como o computador entende o significado de um texto?"

resultado = collection.query(
    query_texts=[pergunta],
    n_results=2
)

print(f"Pergunta: {pergunta}\n")
print("Resultados encontrados no banco:")
for doc in resultado['documents'][0]:
    print(f"- {doc}")