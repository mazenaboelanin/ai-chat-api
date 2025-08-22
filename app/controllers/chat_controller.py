from flask import request, jsonify
from config.db import db
from ..services.ai_agent_api_service import request_ai_agent
from ..models.message import Message
from ..models.user import User
from sqlalchemy import desc


def get_chat_history(user_id):
  if not user_id:
    return jsonify({"error": "user_id is required"}), 400

  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"error": f"No user found with id {user_id}"}), 404

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

  if not data or "model" not in data or "question" not in data:
    return jsonify({"error": "Model and Question must be specified"}), 400
  
  if "user_id" not in data:
    return jsonify({"error": "user_id is required"}), 400

  user_id = data["user_id"]

  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"error": f"No user found with id {user_id}"}), 404


  mappedData = data.copy()
  mappedData["stream"] = False

  if "question" in mappedData:
    mappedData["prompt"] = mappedData.pop("question")

  if "user_id" in mappedData:
    mappedData.pop("user_id")

  try:
    response = request_ai_agent(mappedData)

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

