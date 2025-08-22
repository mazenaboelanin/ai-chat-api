from flask import Blueprint
from ..controllers.chat_controller import get_answer, get_chat_history, get_all_chats

chat_bp = Blueprint("chat", __name__, url_prefix="/api/v1/chat")

# POST /chat/ask → ask question
@chat_bp.route("/ask", methods=["POST"])
def ask_question():
  return get_answer()

# GET /chat/history/<user_id> → fetch chat history
@chat_bp.route("/history/<user_id>", methods=["GET"])
def chat_history(user_id):
  return get_chat_history(user_id)

# POST /chat/all → fetch all messages with all users
@chat_bp.route("/all", methods=["GET"])
def fetch_all_chats():
  return get_all_chats()