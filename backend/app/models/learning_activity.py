
from datetime import date, datetime

from app.extensions import db


class LearningActivity(db.Model):
    __tablename__ = "learning_activities"

    id = db.Column(db.Integer, primary_key=True)

    career_goal_id = db.Column(
        db.Integer,
        db.ForeignKey("career_goals.id"),
        nullable=False,
    )

    activity_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today,
    )

    tasks_completed = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "career_goal_id",
            "activity_date",
            name="uq_learning_activity_goal_date",
        ),
        db.CheckConstraint(
            "tasks_completed >= 1",
            name="ck_learning_activity_tasks_completed_positive",
        ),
    )
