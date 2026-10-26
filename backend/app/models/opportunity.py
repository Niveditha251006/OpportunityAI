from datetime import datetime

from app.extensions import db


class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=False)

    type = db.Column(db.String(100), nullable=False)

    education_level = db.Column(db.String(100))
    fields = db.Column(db.Text)
    states = db.Column(db.Text)

    min_income = db.Column(db.Numeric(12, 2))
    max_income = db.Column(db.Numeric(12, 2))

    rural_eligible = db.Column(db.Boolean, default=False)
    first_generation_eligible = db.Column(db.Boolean, default=False)

    deadline = db.Column(db.DateTime)
    amount = db.Column(db.Numeric(12, 2))

    application_url = db.Column(db.Text)
    source_url = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )