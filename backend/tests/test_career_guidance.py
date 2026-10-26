
from app.services.career_guidance_service import recommend_career_paths


def test_python_interests_recommend_python_developer_first():
    result = recommend_career_paths(["python", "apis"])

    assert result["needs_more_information"] is False
    assert result["recommendations"][0]["career_path"] == "Python Developer"
    assert result["recommendations"][0]["match_count"] == 2


def test_data_interests_recommend_data_analyst_first():
    result = recommend_career_paths(["sql", "dashboards", "statistics"])

    assert result["recommendations"][0]["career_path"] == "Data Analyst"
    assert result["recommendations"][0]["match_count"] == 3


def test_ai_interests_recommend_ai_ml_engineer_first():
    result = recommend_career_paths(["machine learning", "deep learning"])

    assert result["recommendations"][0]["career_path"] == "AI/ML Engineer"
    assert result["recommendations"][0]["match_count"] == 2


def test_no_matching_interests_asks_follow_up_question():
    result = recommend_career_paths(["music", "painting"])

    assert result["needs_more_information"] is True
    assert result["follow_up_question"]
    assert len(result["recommendations"]) == 3


def test_skill_level_is_preserved():
    result = recommend_career_paths(["python"], skill_level="intermediate")

    assert all(
        item["skill_level"] == "intermediate"
        for item in result["recommendations"]
    )
