from flask import Blueprint, jsonify, request

from app.ai.opportunity_text import build_opportunity_text
from app.matching.eligibility import get_eligibility_status
from app.matching.match_engine import build_match_result
from app.matching.ranking import rank_matches
from app.models.opportunity import Opportunity
from app.schemas.student import StudentProfile


match_bp = Blueprint("match", __name__)


def serialize_student_profile(student):
    """Return the student profile in a consistent API format."""
    return {
        "education_level": student.education_level,
        "field": student.field,
        "annual_income": student.annual_income,
        "state": student.state,
        "rural": student.rural,
        "first_generation": student.first_generation,
        "interests": student.interests,
    }


@match_bp.route("/match", methods=["POST"])
def match_opportunities():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    interests = data.get("interests", [])

    if not isinstance(interests, list):
        return jsonify({
            "error": "interests must be a list."
        }), 400

    student = StudentProfile(
        education_level=data.get("education_level"),
        field=data.get("field"),
        annual_income=data.get("annual_income"),
        state=data.get("state"),
        rural=data.get("rural"),
        first_generation=data.get("first_generation"),
        interests=interests,
    )

    # Construct text from the supplied profile for semantic matching.
    profile_parts = [
        student.education_level,
        student.field,
        student.state,
        *student.interests,
    ]

    if student.annual_income is not None:
        profile_parts.append(
            f"Annual family income {student.annual_income}"
        )

    if student.rural is not None:
        profile_parts.append(
            "Rural background" if student.rural
            else "Urban background"
        )

    if student.first_generation is not None:
        profile_parts.append(
            "First-generation college student"
            if student.first_generation
            else "Not a first-generation college student"
        )

    student_text = ". ".join(
        str(part).strip()
        for part in profile_parts
        if part is not None and str(part).strip()
    )

    results = []

    for opportunity in Opportunity.query.all():
        result = build_match_result(
            student,
            opportunity,
            student_text,
        )

        result["eligibility_status"] = get_eligibility_status(
            student,
            opportunity,
        )

        results.append({
            "id": result["opportunity_id"],
            "title": result["title"],
            "organization": opportunity.organization,
            "eligible": result["eligible"],
            "eligibility_status": result["eligibility_status"],
            "reasons": result["eligibility_reasons"],
            "semantic_similarity": result["semantic_similarity"],
            "interest_match": result["interest_match"],
            "matched_interests": result["matched_interests"],
            "explanation": result["explanation"],
        })

    results = rank_matches(results)

    return jsonify({
        "student_profile": serialize_student_profile(student),
        "matches": results,
    })
@match_bp.route("/match-from-text", methods=["POST"])
def match_from_text():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    profile_text = data.get("profile_text")

    if not isinstance(profile_text, str) or not profile_text.strip():
        return jsonify({
            "error": "profile_text is required."
        }), 400

    # Build a structured student profile from the supplied text.
    from app.ai.profile_service import build_student_profile

    student = build_student_profile(profile_text)

    results = []

    for opportunity in Opportunity.query.all():
        result = build_match_result(
            student,
            opportunity,
            profile_text,
        )

        eligibility_status = get_eligibility_status(
            student,
            opportunity,
        )

        results.append({
            "id": result["opportunity_id"],
            "title": result["title"],
            "organization": opportunity.organization,
            "eligible": eligibility_status == "ELIGIBLE",
            "eligibility_status": eligibility_status,
            "reasons": result["eligibility_reasons"],
            "semantic_similarity": result["semantic_similarity"],
            "interest_match": result["interest_match"],
            "matched_interests": result["matched_interests"],
            "explanation": result["explanation"],
        })

    results = rank_matches(results)

    return jsonify({
        "student_profile": serialize_student_profile(student),
        "matches": results,
    })
