from app.ai.opportunity_text import build_opportunity_text
from app.ai.semantic_matcher import calculate_similarity


def calculate_opportunity_similarities(
    student_text: str,
    opportunities
):
    results = []

    for opportunity in opportunities:
        opportunity_text = build_opportunity_text(opportunity)

        similarity = calculate_similarity(
            student_text,
            opportunity_text
        )

        results.append({
            "opportunity": opportunity,
            "similarity": similarity
        })

    return results