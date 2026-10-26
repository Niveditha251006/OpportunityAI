
from app.ai.opportunity_text import build_opportunity_text
from app.ai.semantic_matcher import calculate_similarity
from app.matching.eligibility import check_eligibility


def calculate_interest_match(student_profile, opportunity_text):
    interests = [
        interest.strip().lower()
        for interest in student_profile.interests
        if interest.strip()
    ]

    if not interests:
        return 0.0, []

    text = opportunity_text.lower()

    # Related technical terms for basic interest matching.
    synonyms = {
        "python": ["python", "programming", "coding"],
        "artificial intelligence": [
            "artificial intelligence", "ai", "machine learning",
            "intelligent systems"
        ],
        "software development": [
            "software development", "software engineering",
            "application development", "programming"
        ],
        "web development": [
            "web development", "web applications", "frontend", "backend"
        ],
        "data science": [
            "data science", "data analysis", "analytics", "machine learning"
        ],
        "cybersecurity": [
            "cybersecurity", "cyber security", "information security",
            "application security"
        ],
    }

    matched_interests = []

    for interest in interests:
        terms = synonyms.get(interest, [interest])

        if any(term in text for term in terms):
            matched_interests.append(interest)

    score = len(matched_interests) / len(interests)

    return score, matched_interests


def build_match_result(student_profile, opportunity, student_text):
    eligible, reasons = check_eligibility(
        student_profile,
        opportunity,
    )

    opportunity_text = build_opportunity_text(opportunity)

    similarity = calculate_similarity(
        student_text,
        opportunity_text,
    )

    interest_match, matched_interests = calculate_interest_match(
        student_profile,
        opportunity_text,
    )

    explanation = []

    if eligible:
        explanation.append(
            "All eligibility checks represented in the database passed."
        )
    else:
        explanation.extend(reasons)

    if matched_interests:
        explanation.append(
            "Interests found in the opportunity description: "
            + ", ".join(matched_interests)
            + "."
        )
    elif student_profile.interests:
        explanation.append(
            "No complete student interest phrases were found "
            "in the opportunity description."
        )

    return {
        "opportunity_id": opportunity.id,
        "title": opportunity.title,
        "eligible": eligible,
        "eligibility_reasons": reasons,
        "semantic_similarity": similarity,
        "interest_match": interest_match,
        "matched_interests": matched_interests,
        "explanation": explanation,
    }
