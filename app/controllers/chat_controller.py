from flask import request, jsonify
from ..utils.db_validators import validate_user_exists
from ..utils.input_validators import validate_user_input
from ..utils.chat_utils import map_ai_agent_request_data
from config.db import db
from ..services.ai_agent_api_service import request_ai_agent
from ..models.message import Message
from ..models.user import User
from sqlalchemy import desc


def get_chat_history(user_id):
  user, error_response = validate_user_exists(user_id)
  if error_response:
    return error_response

  stmt = (
    db.select(Message)
    .where(Message.user_id == user_id)
    .order_by(desc(Message.created_at))
  )
  messages = db.session.execute(stmt).scalars().all()

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
      new_message = Message(
        question=data["question"],
        answer=response,
        user_id=user.id, 
      )
      db.session.add(new_message)
      db.session.commit()
    
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

def get_all_chats():
  try:
    stmt = (
      db.select(Message)
      .order_by(desc(Message.created_at))
    )
    messages = db.session.execute(stmt).scalars().all()

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

