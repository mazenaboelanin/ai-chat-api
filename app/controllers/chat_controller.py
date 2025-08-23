from flask import request, jsonify
from ..services.db.chat_db_service import create_new_message, get_all_messages, get_messages_by_user_id
from ..utils.db_validators import validate_user_exists
from ..utils.input_validators import validate_user_input
from ..utils.chat_utils import map_ai_agent_request_data
from ..services.ai_agent_api_service import request_ai_agent


# @desc       get chat history for specific user
# @route      GET api/v1/chat/history/<user_id>
# @access     Public
def get_chat_history(user_id):
  user, error_response = validate_user_exists(user_id)
  if error_response:
    return error_response

  messages, error = get_messages_by_user_id(user_id)
  if error:
    return jsonify(error), 500

  return jsonify({
    "messages": [
      {
        "id": message.id,
        "answer": message.answer,
        "question": message.question,
        "user_id": message.user_id,
        "created_at": message.created_at.isoformat() if message.created_at else None
      }
        for message in messages
    ]
  }), 200


# @desc       prompt the ai agent with question and get answer
# @route      POST api/v1/chat/ask
# @access     Public
def get_answer():
  data = request.get_json()
  print("########### data", data)

  error_response = validate_user_input(data, ["model", "question", "user_id"])
  if error_response:
      return error_response

  user_id = data["user_id"]

  user, error_response = validate_user_exists(user_id)
  if error_response:
      return error_response

  mapped_data = map_ai_agent_request_data(data)

  try:
    response = request_ai_agent(mapped_data)

    if response:
      print("########### response", response)
      print("######## response type:", type(response))
      print("######## response value:", response)
      message_data = {
        "question": data["question"],
        "answer": response,
        "user_id": user.id, 
      }
      print("######## message_data value:", message_data)


    new_message, error = create_new_message(message_data)
    if error:
      return jsonify(error), 500
    
    return jsonify({
      "success": True,
      "message": "Answer returned successfully",
      "answer": response
    }), 200

  except Exception as e:
    return jsonify({
      "success": False,
      "message": "Failed to get answer",
      "error": str(e)
    }), 500

# @desc       get all chats accross all users
# @route      GET api/v1/chat/all
# @access     Public
def get_all_chats():
  try:

    messages, error  = get_all_messages()
    if error:
      return jsonify(error), 500
    if not messages:
      return jsonify({"error": "No messages found"}), 404

    return jsonify({
      "messages": [
        {
          "id": message.id,
          "answer": message.answer,
          "question": message.question,
          "user_id": message.user_id,
          "created_at": message.created_at.isoformat() if message.created_at else None
        }
        for message in messages
      ]
    }), 200

  except Exception as e:
    return jsonify({
      "success": False,
      "message": "Failed to get chats",
      "error": str(e)
    }), 404

