from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def calculate_similarity(text1, text2):
    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)
    similarity = 1 - cosine(embedding1, embedding2)

    return similarity

beta_frase = "The quick brown fox jumps over the lazy dog."

test_cases = [
    "The dog is lazy and the fox is quick.",  
    "A fast fox jumps over a lazy dog.",
    "The cat is sleeping on the couch.",
]

print(f"Beta phrase: '{beta_frase}'\n")
print('-' * 50)

for test_case in test_cases:
    similarity = calculate_similarity(beta_frase, test_case)
    print(f"Similarity with '{test_case}': {similarity:.4f}")
