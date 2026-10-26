
from app.matching.ranking import calculate_match_score, rank_matches


def test_score_combines_semantic_and_interest_match():
    result = {
        "eligible": True,
        "semantic_similarity": 0.75,
        "interest_match": 0.50,
    }

    assert calculate_match_score(result) == 70.0


def test_ineligible_opportunity_gets_zero_score():
    result = {
        "eligible": False,
        "semantic_similarity": 0.95,
        "interest_match": 1.0,
    }

    assert calculate_match_score(result) == 0.0


def test_missing_interest_match_defaults_to_zero():
    result = {
        "eligible": True,
        "semantic_similarity": 0.75,
    }

    assert calculate_match_score(result) == 60.0


def test_scores_are_clamped_to_valid_range():
    result = {
        "eligible": True,
        "semantic_similarity": 1.5,
        "interest_match": -1.0,
    }

    assert calculate_match_score(result) == 80.0


def test_rank_matches_sorts_highest_score_first():
    results = [
        {
            "id": 1,
            "eligible": True,
            "semantic_similarity": 0.40,
            "interest_match": 0.0,
        },
        {
            "id": 2,
            "eligible": True,
            "semantic_similarity": 0.85,
            "interest_match": 1.0,
        },
        {
            "id": 3,
            "eligible": False,
            "semantic_similarity": 0.99,
            "interest_match": 1.0,
        },
    ]

    ranked = rank_matches(results)

    assert [item["id"] for item in ranked] == [2, 1, 3]
    assert [item["match_score"] for item in ranked] == [
        88.0, 32.0, 0.0
    ]
