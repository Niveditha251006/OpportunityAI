
from app.services.career_chat_service import respond_to_career_message


def test_python_message_recommends_python_developer():
    result = respond_to_career_message(
        "I enjoy Python programming and building APIs"
    )

    assert result["needs_more_information"] is False
    assert result["recommendations"][0]["career_path"] == "Python Developer"
    assert "first step" in result["reply"].lower()


def test_unclear_message_asks_follow_up_question():
    result = respond_to_career_message(
        "I don't know which career to choose"
    )

    assert result["needs_more_information"] is True
    assert result["reply"]
    assert len(result["suggested_interests"]) == 3


def test_data_interests_recommend_data_analyst():
    result = respond_to_career_message(
        "I like SQL, dashboards and analysing data"
    )

    assert result["needs_more_information"] is False
    assert result["recommendations"][0]["career_path"] == "Data Analyst"


def test_empty_message_is_handled():
    result = respond_to_career_message("")

    assert result["needs_more_information"] is True
    assert result["reply"]
    assert result["recommendations"] == []


def test_ai_interests_recommend_ai_ml_engineer():
    result = respond_to_career_message(
        "I want to explore artificial intelligence and machine learning"
    )

    assert result["needs_more_information"] is False
    assert result["recommendations"][0]["career_path"] == "AI/ML Engineer"
