from app.models.opportunity import Opportunity


def build_opportunity_text(opportunity: Opportunity) -> str:
    return f"""
Title: {opportunity.title}

Organization: {opportunity.organization}

Description: {opportunity.description}

Type: {opportunity.type}

Education level: {opportunity.education_level or "Not specified"}

Fields: {opportunity.fields or "Not specified"}

States: {opportunity.states or "Not specified"}

Maximum income: {opportunity.max_income or "Not specified"}

Amount: {opportunity.amount or "Not specified"}
""".strip()