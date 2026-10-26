
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import CareerGoal

career_bp = Blueprint("career", __name__)


@career_bp.route("/career/goals", methods=["POST"])
def create_career_goal():
    data = request.get_json(silent=True) or {}

    student_name = data.get("student_name")
    career_path = data.get("career_path")
    current_skill_level = data.get("current_skill_level")
    daily_minutes = data.get("daily_minutes", 30)

    if not all([student_name, career_path, current_skill_level]):
        return jsonify({
            "error": (
                "student_name, career_path, and "
                "current_skill_level are required"
            )
        }), 400

    if not isinstance(daily_minutes, int) or isinstance(daily_minutes, bool):
        return jsonify({"error": "daily_minutes must be an integer"}), 400

    if not 1 <= daily_minutes <= 480:
        return jsonify({
            "error": "daily_minutes must be between 1 and 480"
        }), 400

    goal = CareerGoal(
        student_name=student_name.strip(),
        career_path=career_path.strip(),
        current_skill_level=current_skill_level.strip(),
        daily_minutes=daily_minutes,
    )

    if not goal.student_name or not goal.career_path or not goal.current_skill_level:
        return jsonify({"error": "Required fields cannot be blank"}), 400

    try:
        db.session.add(goal)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not save career goal"}), 500

    return jsonify({
        "message": "Career goal created successfully",
        "goal": {
            "id": goal.id,
            "student_name": goal.student_name,
            "career_path": goal.career_path,
            "current_skill_level": goal.current_skill_level,
            "daily_minutes": goal.daily_minutes,
            "status": goal.status,
        }
    }), 201

@career_bp.route("/career/goals", methods=["GET"])
def list_career_goals():
    goals = CareerGoal.query.order_by(
        CareerGoal.created_at.desc()
    ).all()

    return jsonify({
        "goals": [
            {
                "id": goal.id,
                "student_name": goal.student_name,
                "career_path": goal.career_path,
                "current_skill_level": goal.current_skill_level,
                "daily_minutes": goal.daily_minutes,
                "status": goal.status,
            }
            for goal in goals
        ]
    }), 200
