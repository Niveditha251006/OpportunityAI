from flask import Blueprint, jsonify

from app.models.opportunity import Opportunity


opportunities_bp = Blueprint("opportunities", __name__)


@opportunities_bp.route("/opportunities", methods=["GET"])
def get_opportunities():
    opportunities = Opportunity.query.all()

    results = []

    for opportunity in opportunities:
        results.append({
            "id": opportunity.id,
            "title": opportunity.title,
            "organization": opportunity.organization,
            "description": opportunity.description,
            "type": opportunity.type,
            "education_level": opportunity.education_level,
            "fields": opportunity.fields,
            "states": opportunity.states,
            "max_income": float(opportunity.max_income)
            if opportunity.max_income is not None
            else None,
            "amount": float(opportunity.amount)
            if opportunity.amount is not None
            else None,
            "application_url": opportunity.application_url,
            "source_url": opportunity.source_url,
        })

    return jsonify({
        "count": len(results),
        "opportunities": results
    })
