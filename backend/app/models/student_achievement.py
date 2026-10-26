
from datetime import datetime

from app.extensions import db


class StudentAchievement(db.Model):
    __tablename__ = "student_achievements"

    id = db.Column(db.Integer, primary_key=True)

    career_goal_id = db.Column(
        db.Integer,
        db.ForeignKey("career_goals.id"),
        nullable=False,
    )

    achievement_code = db.Column(
        db.String(60),
        nullable=False,
    )

    unlocked_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "career_goal_id",
            "achievement_code",
            name="uq_student_achievement_goal_code",
        ),
    )
