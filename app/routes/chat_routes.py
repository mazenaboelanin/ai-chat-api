from flask import Blueprint
from controllers.chat_controller import create_chat, get_chat_history

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# POST /chat → create new message
@chat_bp.route("/", methods=["GET"])
def chat_post():
  return create_chat()

# GET /chat/history → fetch chat history
@chat_bp.route("/history", methods=["GET"])
def chat_history():
  return get_chat_history()

