
from datetime import datetime

from app.extensions import db


class RoadmapTask(db.Model):
    __tablename__ = "roadmap_tasks"

    id = db.Column(db.Integer, primary_key=True)

    career_goal_id = db.Column(
        db.Integer,
        db.ForeignKey("career_goals.id"),
        nullable=False,
    )

    week_number = db.Column(db.Integer, nullable=False)
    day_number = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    estimated_minutes = db.Column(
        db.Integer,
        nullable=False,
        default=30,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="PENDING",
    )

    completed_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
