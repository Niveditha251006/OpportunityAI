from types import SimpleNamespace

from app.matching.match_engine import calculate_interest_match


def test_matches_configured_synonyms():
    student = SimpleNamespace(
        interests=["Python", "artificial intelligence", "software development"]
    )

    score, matched = calculate_interest_match(
        student,
        "Technical education involving AI and software engineering."
    )

    assert score == 2 / 3
    assert matched == ["artificial intelligence", "software development"]


def test_no_interests_returns_zero():
    student = SimpleNamespace(interests=[])

    score, matched = calculate_interest_match(
        student,
        "Technical education and programming."
    )

    assert score == 0.0
    assert matched == []


def test_unknown_interest_uses_exact_phrase():
    student = SimpleNamespace(interests=["robotics"])

    score, matched = calculate_interest_match(
        student,
        "Scholarship support for robotics students."
    )

    assert score == 1.0
    assert matched == ["robotics"]