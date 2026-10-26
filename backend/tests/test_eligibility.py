from types import SimpleNamespace
from decimal import Decimal
from app.matching.eligibility import get_eligibility_status
from app.matching.eligibility import check_eligibility


def make_student(**overrides):
    data = {
        "education_level": "undergraduate",
        "field": "computer science",
        "annual_income": 250000,
        "state": "Andhra Pradesh",
        "rural": False,
        "first_generation": False,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def make_opportunity(**overrides):
    data = {
        "education_level": "undergraduate",
        "fields": "computer science",
        "states": "Andhra Pradesh",
        "min_income": None,
        "max_income": Decimal("500000"),
        "rural_eligible": False,
        "first_generation_eligible": False,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_income_above_maximum_is_rejected():
    student = make_student(annual_income=600000)
    opportunity = make_opportunity(max_income=Decimal("500000"))

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is False
    assert any("income" in reason.lower() for reason in reasons)


def test_income_below_minimum_is_rejected():
    student = make_student(annual_income=50000)
    opportunity = make_opportunity(min_income=Decimal("100000"))

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is False
    assert any("income" in reason.lower() for reason in reasons)


def test_state_must_match_a_complete_state_name():
    student = make_student(state="Andhra Pradesh")
    opportunity = make_opportunity(states="Pradesh")

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is False
    assert any("state" in reason.lower() for reason in reasons)


def test_equivalent_cse_field_is_accepted():
    student = make_student(field="CSE")
    opportunity = make_opportunity(fields="computer science")

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is True
    assert reasons == []


def test_matching_profile_passes_existing_rules():
    student = make_student()
    opportunity = make_opportunity()

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is True
    assert reasons == []


def test_unknown_rural_status_does_not_count_as_confirmed_no():
    student = make_student(rural=None)
    opportunity = make_opportunity(rural_eligible=True)

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is False
    assert any("rural" in reason.lower() for reason in reasons)


def test_unknown_first_generation_status_does_not_count_as_confirmed_no():
    student = make_student(first_generation=None)
    opportunity = make_opportunity(first_generation_eligible=True)

    eligible, reasons = check_eligibility(student, opportunity)

    assert eligible is False
    assert any("first-generation" in reason.lower() for reason in reasons)

def test_status_is_eligible_when_all_checks_pass():
    student = make_student()
    opportunity = make_opportunity()

    assert get_eligibility_status(student, opportunity) == "ELIGIBLE"


def test_status_is_ineligible_when_a_known_requirement_fails():
    student = make_student(rural=False)
    opportunity = make_opportunity(rural_eligible=True)

    assert get_eligibility_status(student, opportunity) == "INELIGIBLE"


def test_status_needs_information_when_required_background_is_unknown():
    student = make_student(rural=None)
    opportunity = make_opportunity(rural_eligible=True)

    assert (
        get_eligibility_status(student, opportunity)
        == "NEEDS_INFORMATION"
    )


def test_missing_income_needs_information_when_income_limit_applies():
    student = make_student(annual_income=None)
    opportunity = make_opportunity(max_income=Decimal("500000"))

    assert get_eligibility_status(student, opportunity) == "NEEDS_INFORMATION"
    eligible, reasons = check_eligibility(student, opportunity)
    assert eligible is False
    assert any("income" in reason.lower() for reason in reasons)


def test_missing_education_needs_information_when_required():
    student = make_student(education_level=None)
    opportunity = make_opportunity(education_level="undergraduate")

    assert get_eligibility_status(student, opportunity) == "NEEDS_INFORMATION"


def test_missing_field_needs_information_when_field_is_restricted():
    student = make_student(field=None)
    opportunity = make_opportunity(fields="computer science")

    assert get_eligibility_status(student, opportunity) == "NEEDS_INFORMATION"


def test_missing_state_needs_information_when_state_is_restricted():
    student = make_student(state=None)
    opportunity = make_opportunity(states="Andhra Pradesh")

    assert get_eligibility_status(student, opportunity) == "NEEDS_INFORMATION"


def test_confirmed_failure_takes_precedence_over_missing_information():
    student = make_student(
        annual_income=None,
        rural=False,
    )
    opportunity = make_opportunity(rural_eligible=True)

    assert get_eligibility_status(student, opportunity) == "INELIGIBLE"
