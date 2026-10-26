
CAREER_PATHS = {
    "Python Developer": {
        "interests": {
            "python", "programming", "software development",
            "backend", "automation", "apis",
        },
        "description": (
            "Build applications, APIs, automation tools, "
            "and backend services using Python."
        ),
        "first_step": "Practise Python functions and build a small command-line tool.",
    },
    "Data Analyst": {
        "interests": {
            "data analysis", "data", "sql", "excel",
            "visualization", "visualisation", "statistics",
            "business", "dashboards",
        },
        "description": (
            "Use data, SQL, spreadsheets, statistics, and dashboards "
            "to answer practical questions."
        ),
        "first_step": "Choose a dataset, explore it, and write three useful findings.",
    },
    "AI/ML Engineer": {
        "interests": {
            "artificial intelligence", "ai", "machine learning",
            "ml", "data science", "mathematics", "models",
            "deep learning", "research",
        },
        "description": (
            "Build and evaluate machine-learning systems and "
            "AI-powered applications."
        ),
        "first_step": "Review Python and NumPy, then train a simple machine-learning model.",
    },
}


def recommend_career_paths(interests, skill_level="beginner"):
    """Rank supported career paths using the student's stated interests."""
    if not isinstance(interests, list):
        interests = []

    normalized_interests = {
        str(interest).strip().lower()
        for interest in interests
        if str(interest).strip()
    }

    recommendations = []

    for career_name, details in CAREER_PATHS.items():
        matched_interests = sorted(
            normalized_interests & details["interests"]
        )

        recommendations.append({
            "career_path": career_name,
            "matched_interests": matched_interests,
            "match_count": len(matched_interests),
            "description": details["description"],
            "first_step": details["first_step"],
            "skill_level": (
                skill_level
                if skill_level in {"beginner", "intermediate", "advanced"}
                else "beginner"
            ),
        })

    recommendations.sort(
        key=lambda item: item["match_count"],
        reverse=True,
    )

    # Do not claim a strong match when the student gave no matching interests.
    if not normalized_interests or recommendations[0]["match_count"] == 0:
        return {
            "needs_more_information": True,
            "follow_up_question": (
                "Which activities interest you most: building software, "
                "analysing data, or creating AI and machine-learning systems?"
            ),
            "recommendations": recommendations,
        }

    return {
        "needs_more_information": False,
        "follow_up_question": None,
        "recommendations": recommendations,
    }
