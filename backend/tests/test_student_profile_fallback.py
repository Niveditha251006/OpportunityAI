from app.ai.profile_extractor import _fallback_extract_student_profile


def test_rural_status_is_true_when_explicitly_stated():
    profile = _fallback_extract_student_profile(
        "I live in a rural area."
    )
    assert profile["rural"] is True


def test_rural_status_is_false_when_explicitly_denied():
    profile = _fallback_extract_student_profile(
        "I live in an urban area and I am not rural."
    )
    assert profile["rural"] is False


def test_rural_status_is_unknown_when_not_mentioned():
    profile = _fallback_extract_student_profile(
        "I am an undergraduate computer science student."
    )
    assert profile["rural"] is None


def test_first_generation_is_true_when_explicitly_stated():
    profile = _fallback_extract_student_profile(
        "I am the first person in my family to attend college."
    )
    assert profile["first_generation"] is True


def test_first_generation_is_false_when_explicitly_denied():
    profile = _fallback_extract_student_profile(
        "I am not a first-generation student."
    )
    assert profile["first_generation"] is False


def test_first_generation_is_unknown_when_not_mentioned():
    profile = _fallback_extract_student_profile(
        "I am an undergraduate computer science student."
    )
    assert profile["first_generation"] is None
