
from datetime import datetime

from app.extensions import db


class CareerGoal(db.Model):
    __tablename__ = "career_goals"

    id = db.Column(db.Integer, primary_key=True)

    # Temporary student identifier until authentication is implemented.
    student_name = db.Column(db.String(120), nullable=False)

    career_path = db.Column(db.String(120), nullable=False)
    current_skill_level = db.Column(db.String(50), nullable=False)

    daily_minutes = db.Column(db.Integer, nullable=False, default=30)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="ACTIVE"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
