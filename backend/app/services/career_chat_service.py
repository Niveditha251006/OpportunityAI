
from app.services.career_guidance_service import recommend_career_paths


CAREER_INTERESTS = {
    "Python Developer": [
        "python",
        "programming",
        "coding",
        "software",
        "backend",
        "apis",
        "automation",
        "building software",
        "build apps",
    ],
    "Data Analyst": [
        "data analyst",
        "data analysis",
        "analysing data",
        "analyzing data",
        "data",
        "sql",
        "excel",
        "statistics",
        "dashboard",
        "visualization",
        "visualisation",
    ],
    "AI/ML Engineer": [
        "ai/ml",
        "ai ml",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data science",
        " ai ",
        " ml ",
    ],
}

CAREER_DESCRIPTIONS = {
    "Python Developer": (
        "Build applications, APIs, automation tools, "
        "and backend services using Python."
    ),
    "Data Analyst": (
        "Use data, SQL, spreadsheets, statistics, and dashboards "
        "to answer practical questions."
    ),
    "AI/ML Engineer": (
        "Build and evaluate machine-learning systems and "
        "AI-powered applications."
    ),
}

CAREER_FIRST_STEPS = {
    "Python Developer": (
        "Practise Python functions and build a small command-line tool."
    ),
    "Data Analyst": (
        "Choose a dataset, explore it, and write three useful findings."
    ),
    "AI/ML Engineer": (
        "Review Python and NumPy, then train a simple machine-learning model."
    ),
}

FOLLOW_UP_QUESTION = (
    "Let's figure it out together. Which sounds most interesting: "
    "building software, analysing data, or exploring AI and machine learning?"
)


def _detect_careers(text):
    """Find career paths explicitly mentioned in a message."""
    normalized = f" {text.lower().strip()} "
    detected = []

    for career, keywords in CAREER_INTERESTS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(career)

    return detected


def _history_messages(conversation_history):
    """Accept only simple user/assistant messages."""
    if not isinstance(conversation_history, list):
        return []

    messages = []

    for item in conversation_history[-20:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})

    return messages


def _career_recommendations(careers):
    """Build recommendations for selected career paths."""
    recommendations = []

    for career in careers:
        recommendations.append({
            "career_path": career,
            "description": CAREER_DESCRIPTIONS[career],
            "first_step": CAREER_FIRST_STEPS[career],
            "match_count": 1,
            "matched_interests": [],
            "skill_level": "beginner",
        })

    return recommendations


def respond_to_career_message(message, conversation_history=None):
    """
    Give rule-based career guidance and use recent conversation context
    to interpret short follow-up answers.
    """
    if not isinstance(message, str) or not message.strip():
        return {
            "reply": "Tell me a little about what you enjoy doing.",
            "needs_more_information": True,
            "recommendations": [],
            "suggested_interests": [],
        }

    history = _history_messages(conversation_history)
    text = message.strip().lower()
    detected_careers = _detect_careers(text)

    # Interpret a student's selection from the previous assistant question.
    if not detected_careers:
        if any(phrase in text for phrase in (
            "the first one",
            "option one",
            "number one",
            "building software",
        )):
            detected_careers = ["Python Developer"]
        elif any(phrase in text for phrase in (
            "the second one",
            "option two",
            "number two",
            "analysing data",
            "analyzing data",
        )):
            detected_careers = ["Data Analyst"]
        elif any(phrase in text for phrase in (
            "the third one",
            "option three",
            "number three",
            "the last one",
        )):
            detected_careers = ["AI/ML Engineer"]

    if not detected_careers:
        return {
            "reply": FOLLOW_UP_QUESTION,
            "needs_more_information": True,
            "recommendations": [],
            "suggested_interests": [
                "Building software",
                "Analysing data",
                "AI and machine learning",
            ],
        }

    recommendations = _career_recommendations(detected_careers)
    primary = recommendations[0]

    if len(recommendations) > 1:
        reply = (
            "You mentioned interests across several career paths. "
            "Here are the options to compare. "
            + " ".join(
                f"{item['career_path']}: {item['description']} "
                f"A first step is {item['first_step']}"
                for item in recommendations
            )
        )
    else:
        reply = (
            f"Based on what you shared, {primary['career_path']} "
            f"could be worth exploring. {primary['description']} "
            f"A practical first step is: {primary['first_step']} "
            "Would you like to explore this path or compare it with another?"
        )

    # Use history to acknowledge that this is a continuing conversation.
    if history:
        reply = "Thanks for sharing that. " + reply

    return {
        "reply": reply,
        "needs_more_information": False,
        "recommendations": recommendations,
        "suggested_interests": detected_careers,
    }
