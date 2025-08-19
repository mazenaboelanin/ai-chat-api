from flask import request, jsonify

from services.ai_api_service import request_ai_agent

def create_chat():
    message = "welcome"

    return jsonify({
        "status": "success",
        "message": f"Chat message saved: {message}"
    })

def get_chat_history():
    history = [
        {"id": 1, "message": "Hello"},
        {"id": 2, "message": "How are you?"}
    ]
    return jsonify({"chat_history": history})
