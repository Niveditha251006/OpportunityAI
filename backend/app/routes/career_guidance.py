
from flask import Blueprint, jsonify, request

from app.services.career_guidance_service import recommend_career_paths

career_guidance_bp = Blueprint("career_guidance", __name__)


@career_guidance_bp.route("/career-guidance/recommend", methods=["POST"])
def recommend_career():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    interests = data.get("interests", [])
    skill_level = data.get("skill_level", "beginner")

    if not isinstance(interests, list):
        return jsonify({"error": "interests must be a list"}), 400

    if not all(isinstance(item, str) for item in interests):
        return jsonify({"error": "Each interest must be a string"}), 400

    if not isinstance(skill_level, str):
        return jsonify({"error": "skill_level must be a string"}), 400

    result = recommend_career_paths(
        interests=interests,
        skill_level=skill_level,
    )

    return jsonify(result), 200
