from datetime import date, timedelta

from app import create_app
from app.extensions import db
from app.models import (
    CareerGoal,
    LearningActivity,
    RoadmapTask,
    StudentAchievement,
)
from app.services.achievement_service import (
    calculate_streak,
    get_learning_progress,
    record_learning_activity,
)


def setup_test_app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    return app


def test_empty_activity_has_zero_streak():
    assert calculate_streak([]) == {
        "current_streak": 0,
        "best_streak": 0,
    }


def test_three_consecutive_days_have_three_day_streak():
    today = date.today()
    dates = [today - timedelta(days=2), today - timedelta(days=1), today]

    assert calculate_streak(dates, today=today) == {
        "current_streak": 3,
        "best_streak": 3,
    }


def test_missed_day_breaks_current_streak():
    today = date.today()
    dates = [
        today - timedelta(days=3),
        today - timedelta(days=2),
        today,
    ]

    assert calculate_streak(dates, today=today) == {
        "current_streak": 1,
        "best_streak": 2,
    }


def test_stale_activity_has_no_current_streak():
    today = date.today()
    dates = [
        today - timedelta(days=5),
        today - timedelta(days=4),
    ]

    assert calculate_streak(dates, today=today) == {
        "current_streak": 0,
        "best_streak": 2,
    }


def test_duplicate_dates_do_not_inflate_streak():
    today = date.today()
    dates = [today, today, today - timedelta(days=1)]

    assert calculate_streak(dates, today=today) == {
        "current_streak": 2,
        "best_streak": 2,
    }


def test_learning_progress_returns_none_for_missing_goal():
    app = setup_test_app()

    with app.app_context():
        db.create_all()
        try:
            assert get_learning_progress(99999) is None
        finally:
            db.session.remove()
            db.drop_all()


def test_record_activity_unlocks_first_step_once():
    app = setup_test_app()

    with app.app_context():
        db.create_all()
        try:
            goal = CareerGoal(
                student_name="Test Student",
                career_path="Data Analyst",
                current_skill_level="Beginner",
                daily_minutes=30,
            )
            db.session.add(goal)
            db.session.flush()

            task = RoadmapTask(
                career_goal_id=goal.id,
                week_number=1,
                day_number=1,
                title="Test task",
                description="A task for automated testing",
                estimated_minutes=30,
                status="COMPLETED",
            )
            db.session.add(task)
            db.session.flush()

            progress = record_learning_activity(task)
            db.session.commit()

            assert progress["current_streak"] == 1
            assert progress["best_streak"] == 1
            assert "FIRST_STEP" in {
                item["code"] for item in progress["achievements"]
            }
            assert LearningActivity.query.filter_by(
                career_goal_id=goal.id
            ).count() == 1
            assert StudentAchievement.query.filter_by(
                career_goal_id=goal.id,
                achievement_code="FIRST_STEP",
            ).count() == 1
        finally:
            db.session.remove()
            db.drop_all()
