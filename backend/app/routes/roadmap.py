from datetime import datetime, timezone

from flask import Blueprint, jsonify

from app.extensions import db
from app.models import CareerGoal, RoadmapTask
from app.services.roadmap_service import generate_weekly_roadmap
from app.services.learning_resources import get_learning_resources
from app.services.achievement_service import (
    get_learning_progress,
    record_learning_activity,
)
roadmap_bp = Blueprint("roadmap", __name__)


@roadmap_bp.route(
    "/career/goals/<int:career_goal_id>/roadmap/generate",
    methods=["POST"],
)
def create_weekly_roadmap(career_goal_id):
    try:
        tasks, error = generate_weekly_roadmap(career_goal_id)
    except Exception:
        return jsonify({
            "error": "Could not generate roadmap"
        }), 500

    if error == "Career goal not found":
        return jsonify({"error": error}), 404

    if error:
        return jsonify({"error": error}), 409

    goal = db.session.get(CareerGoal, career_goal_id)

    if goal is None:
        return jsonify({"error": "Career goal not found"}), 404

    return jsonify({
        "message": "Weekly roadmap created successfully",
        "goal_id": career_goal_id,
        "week_number": 1,
        "tasks": [
            {
                "id": task.id,
                "day_number": task.day_number,
                "title": task.title,
                "description": task.description,
                "estimated_minutes": task.estimated_minutes,
                "status": task.status,
                "resources": get_learning_resources(
                    task.title,
                    goal.career_path,
                ),
            }
            for task in tasks
        ],
    }), 201


@roadmap_bp.route(
    "/career/goals/<int:career_goal_id>/roadmap",
    methods=["GET"],
)
def get_career_roadmap(career_goal_id):
    goal = db.session.get(CareerGoal, career_goal_id)

    if goal is None:
        return jsonify({"error": "Career goal not found"}), 404

    tasks = RoadmapTask.query.filter_by(
        career_goal_id=career_goal_id
    ).order_by(
        RoadmapTask.week_number.asc(),
        RoadmapTask.day_number.asc(),
    ).all()

    return jsonify({
        "goal_id": career_goal_id,
        "career_path": goal.career_path,
        "tasks": [
            {
                "id": task.id,
                "week_number": task.week_number,
                "day_number": task.day_number,
                "title": task.title,
                "description": task.description,
                "estimated_minutes": task.estimated_minutes,
                "status": task.status,
                "resources": get_learning_resources(
                    task.title,
                    goal.career_path,
                ),
                "completed_at": (
                    task.completed_at.isoformat()
                    if task.completed_at else None
                ),
            }
            for task in tasks
        ],
    }), 200



@roadmap_bp.route(
    "/roadmap/tasks/<int:task_id>/complete",
    methods=["PATCH"],
)
def complete_roadmap_task(task_id):
    task = db.session.get(RoadmapTask, task_id)

    if task is None:
        return jsonify({"error": "Roadmap task not found"}), 404

    # Do not count the same task completion twice.
    if task.status == "COMPLETED":
        return jsonify({
            "message": "Task is already completed",
            "task_id": task.id,
            "status": task.status,
            "completed_at": (
                task.completed_at.isoformat()
                if task.completed_at else None
            ),
        }), 200

    task.status = "COMPLETED"
    task.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    try:
        progress = record_learning_activity(task)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Could not complete task"
        }), 500

    return jsonify({
        "message": "Task completed successfully",
        "task_id": task.id,
        "status": task.status,
        "completed_at": task.completed_at.isoformat(),
        "learning_progress": progress,
    }), 200

@roadmap_bp.route(
    "/career/goals/<int:career_goal_id>/learning-progress",
    methods=["GET"],
)
def get_career_learning_progress(career_goal_id):
    progress = get_learning_progress(career_goal_id)

    if progress is None:
        return jsonify({"error": "Career goal not found"}), 404

    return jsonify({
        "goal_id": career_goal_id,
        **progress,
    }), 200
