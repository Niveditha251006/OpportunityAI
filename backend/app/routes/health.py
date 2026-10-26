from flask import Blueprint, jsonify
from app.extensions import db


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(db.text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500