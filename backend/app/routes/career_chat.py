
from flask import Blueprint, jsonify, request

from app.services.career_chat_service import respond_to_career_message

career_chat_bp = Blueprint("career_chat", __name__)


@career_chat_bp.route("/career-guidance/chat", methods=["POST"])
def career_chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    message = data.get("message")
    conversation_history = data.get("conversation_history", [])

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message must be a non-empty string"}), 400

    if not isinstance(conversation_history, list):
        return jsonify({"error": "conversation_history must be a list"}), 400

    result = respond_to_career_message(
        message=message,
        conversation_history=conversation_history,
    )

    return jsonify(result), 200
