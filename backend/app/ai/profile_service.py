from app.ai.profile_extractor import extract_student_profile
from app.schemas.student import StudentProfile


def build_student_profile(text: str) -> StudentProfile:
    data = extract_student_profile(text)

    return StudentProfile(
        education_level=data.get("education_level"),
        field=data.get("field"),
        annual_income=data.get("annual_income"),
        state=data.get("state"),
        rural=data.get("rural"),
        first_generation=data.get("first_generation"),
        interests=data.get("interests", []),
    )