
from app.models.opportunity import Opportunity
from app.schemas.student import StudentProfile


def get_missing_information(
    student: StudentProfile,
    opportunity: Opportunity,
) -> list[str]:
    """Identify unknown student details needed for configured checks."""
    missing = []

    if (
        opportunity.min_income is not None
        or opportunity.max_income is not None
    ) and student.annual_income is None:
        missing.append("Please provide your annual family income.")

    if (
        opportunity.education_level
        and not student.education_level
    ):
        missing.append("Please provide your education level.")

    if (
        opportunity.fields
        and opportunity.fields.strip().casefold() != "all"
        and not student.field
    ):
        missing.append("Please provide your field of study.")

    if (
        opportunity.states
        and opportunity.states.strip().casefold() != "all"
        and not student.state
    ):
        missing.append("Please provide your state.")

    if opportunity.rural_eligible and student.rural is None:
        missing.append(
            "Please provide your rural/urban background to confirm eligibility."
        )

    if (
        opportunity.first_generation_eligible
        and student.first_generation is None
    ):
        missing.append(
            "Please provide your first-generation status to confirm eligibility."
        )

    return missing

def check_eligibility(
    student: StudentProfile,
    opportunity: Opportunity,
) -> tuple[bool, list[str]]:
    """Check eligibility while preserving the existing return format."""
    reasons = []

    # Income checks
    if (
        student.annual_income is None
        and (
            opportunity.min_income is not None
            or opportunity.max_income is not None
        )
    ):
        reasons.append(
            "Please provide your annual family income."
        )
    if (
        student.annual_income is not None
        and opportunity.min_income is not None
        and student.annual_income < float(opportunity.min_income)
    ):
        reasons.append(
            "Annual income is below the opportunity minimum."
        )

    if (
        student.annual_income is not None
        and opportunity.max_income is not None
        and student.annual_income > float(opportunity.max_income)
    ):
        reasons.append(
            "Annual income exceeds the opportunity limit."
        )

    # Education check
    if (
        student.education_level
        and opportunity.education_level
        and student.education_level.strip().casefold()
        != opportunity.education_level.strip().casefold()
    ):
        reasons.append("Education level does not match.")

    # Field check
    if (
        student.field
        and opportunity.fields
        and opportunity.fields.strip().casefold() != "all"
    ):
        student_field = student.field.strip().casefold()

        opportunity_fields = {
            item.strip().casefold()
            for item in opportunity.fields.split(",")
            if item.strip()
        }

        field_groups = {
            "engineering": {
                "engineering",
                "computer science",
                "cse",
                "information technology",
                "it",
                "software engineering",
                "electronics",
                "electrical engineering",
                "mechanical engineering",
                "civil engineering",
            },
            "technology": {
                "technology",
                "computer science",
                "cse",
                "information technology",
                "it",
                "software engineering",
            },
        }

        student_aliases = {student_field}

        for group_name, group_fields in field_groups.items():
            if student_field in group_fields:
                student_aliases.add(group_name)
                student_aliases.update(group_fields)

        if not opportunity_fields.intersection(student_aliases):
            reasons.append("Field of study does not match.")

    # State check: compare complete comma-separated state names
    if (
        student.state
        and opportunity.states
        and opportunity.states.strip().casefold() != "all"
    ):
        allowed_states = {
            item.strip().casefold()
            for item in opportunity.states.split(",")
            if item.strip()
        }

        if student.state.strip().casefold() not in allowed_states:
            reasons.append("State eligibility does not match.")

    # Rural eligibility
    if opportunity.rural_eligible:
        if student.rural is False:
            reasons.append(
                "Rural eligibility requirement is not satisfied."
            )
        elif student.rural is None:
            reasons.append(
                "Please provide your rural/urban background "
                "to confirm eligibility."
            )

    # First-generation eligibility
    if opportunity.first_generation_eligible:
        if student.first_generation is False:
            reasons.append(
                "First-generation eligibility requirement "
                "is not satisfied."
            )
        elif student.first_generation is None:
            reasons.append(
                "Please provide your first-generation status "
                "to confirm eligibility."
            )

    return len(reasons) == 0, reasons


def get_eligibility_status(
    student: StudentProfile,
    opportunity: Opportunity,
) -> str:
    """Return ELIGIBLE, INELIGIBLE, or NEEDS_INFORMATION."""
    eligible, reasons = check_eligibility(student, opportunity)

    # Confirmed unmet requirements take priority over missing details.
    if any(
        reason not in get_missing_information(student, opportunity)
        for reason in reasons
    ):
        return "INELIGIBLE"

    if get_missing_information(student, opportunity):
        return "NEEDS_INFORMATION"

    if eligible:
        return "ELIGIBLE"

    return "INELIGIBLE"
