
from datetime import date, datetime, timedelta

from sqlalchemy import func

from app.extensions import db
from app.models import (
    CareerGoal,
    LearningActivity,
    RoadmapTask,
    StudentAchievement,
)


ACHIEVEMENTS = {
    "FIRST_STEP": {
        "title": "First Step",
        "description": "Complete your first roadmap task.",
    },
    "THREE_DAY_SPARK": {
        "title": "Three-Day Spark",
        "description": "Learn on three consecutive days.",
    },
    "WEEK_WARRIOR": {
        "title": "Week Warrior",
        "description": "Learn on seven consecutive days.",
    },
    "ROADMAP_EXPLORER": {
        "title": "Roadmap Explorer",
        "description": "Complete all tasks in a roadmap week.",
    },
}


def calculate_streak(activity_dates, today=None):
    """Return current and best streak from distinct activity dates."""
    today = today or date.today()
    dates = sorted(set(activity_dates))

    if not dates:
        return {"current_streak": 0, "best_streak": 0}

    best = 0
    run = 0
    previous = None

    for activity_date in dates:
        if previous is not None and activity_date == previous + timedelta(days=1):
            run += 1
        else:
            run = 1

        best = max(best, run)
        previous = activity_date

    if dates[-1] not in (today, today - timedelta(days=1)):
        current = 0
    else:
        current = 1
        cursor = dates[-1]

        for activity_date in reversed(dates[:-1]):
            if activity_date == cursor - timedelta(days=1):
                current += 1
                cursor = activity_date
            else:
                break

    return {"current_streak": current, "best_streak": best}


def _unlock_achievement(career_goal_id, code):
    """Create a badge once; the database constraint prevents duplicates."""
    existing = StudentAchievement.query.filter_by(
        career_goal_id=career_goal_id,
        achievement_code=code,
    ).first()

    if existing:
        return

    db.session.add(
        StudentAchievement(
            career_goal_id=career_goal_id,
            achievement_code=code,
        )
    )


def record_learning_activity(task):
    """Record a completed task, update badges, and return streak data."""
    goal = db.session.get(CareerGoal, task.career_goal_id)

    if goal is None:
        raise ValueError("Career goal not found")

    today = date.today()

    activity = LearningActivity.query.filter_by(
        career_goal_id=task.career_goal_id,
        activity_date=today,
    ).first()

    if activity is None:
        activity = LearningActivity(
            career_goal_id=task.career_goal_id,
            activity_date=today,
            tasks_completed=1,
        )
        db.session.add(activity)
    else:
        activity.tasks_completed += 1

    db.session.flush()

    completed_count = RoadmapTask.query.filter_by(
        career_goal_id=task.career_goal_id,
        status="COMPLETED",
    ).count()

    if completed_count >= 1:
        _unlock_achievement(task.career_goal_id, "FIRST_STEP")

    dates = [
        row[0]
        for row in db.session.query(
            LearningActivity.activity_date
        ).filter_by(
            career_goal_id=task.career_goal_id,
        ).order_by(
            LearningActivity.activity_date.asc()
        ).all()
    ]

    streak = calculate_streak(dates, today=today)

    if streak["best_streak"] >= 3:
        _unlock_achievement(task.career_goal_id, "THREE_DAY_SPARK")

    if streak["best_streak"] >= 7:
        _unlock_achievement(task.career_goal_id, "WEEK_WARRIOR")

    completed_weeks = db.session.query(
        RoadmapTask.week_number
    ).filter_by(
        career_goal_id=task.career_goal_id,
        week_number=task.week_number,
    ).filter(
        RoadmapTask.status != "COMPLETED"
    ).count()

    if completed_weeks == 0:
        _unlock_achievement(task.career_goal_id, "ROADMAP_EXPLORER")

    db.session.flush()

    return {
        **streak,
        "achievements": [
            {
                "code": achievement.achievement_code,
                **ACHIEVEMENTS.get(
                    achievement.achievement_code,
                    {
                        "title": achievement.achievement_code,
                        "description": "",
                    },
                ),
                "unlocked_at": achievement.unlocked_at.isoformat(),
            }
            for achievement in StudentAchievement.query.filter_by(
                career_goal_id=task.career_goal_id
            ).order_by(StudentAchievement.unlocked_at.asc()).all()
        ],
    }


def get_learning_progress(career_goal_id):
    """Return streak data and earned badges for a career goal."""
    goal = db.session.get(CareerGoal, career_goal_id)

    if goal is None:
        return None

    dates = [
        row[0]
        for row in db.session.query(
            LearningActivity.activity_date
        ).filter_by(
            career_goal_id=career_goal_id,
        ).order_by(
            LearningActivity.activity_date.asc()
        ).all()
    ]

    streak = calculate_streak(dates)

    achievements = StudentAchievement.query.filter_by(
        career_goal_id=career_goal_id
    ).order_by(StudentAchievement.unlocked_at.asc()).all()

    return {
        **streak,
        "activity_days": len(set(dates)),
        "achievements": [
            {
                "code": item.achievement_code,
                **ACHIEVEMENTS.get(
                    item.achievement_code,
                    {
                        "title": item.achievement_code,
                        "description": "",
                    },
                ),
                "unlocked_at": item.unlocked_at.isoformat(),
            }
            for item in achievements
        ],
    }
