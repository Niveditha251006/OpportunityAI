from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(
    student_text: str,
    opportunity_text: str
) -> float:
    student_embedding = model.encode([student_text])
    opportunity_embedding = model.encode([opportunity_text])

    similarity = cosine_similarity(
        student_embedding,
        opportunity_embedding
    )[0][0]

    return float(similarity)