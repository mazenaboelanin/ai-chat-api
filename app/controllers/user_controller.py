from flask import request, jsonify
from ..models.user import User
from config.db import db

def create_user():
  data = request.get_json()

  print('=== data', data)


  if not data or "name" not in data or "email" not in data:
      return jsonify({"error": "Name and Email is required"}), 400

  new_user = User(name=data["name"], email=data["email"])
  db.session.add(new_user)
  db.session.commit()

  return jsonify({
      "id": new_user.id,
      "name": new_user.name,
      "email": new_user.email,
      "created_at": new_user.created_at.isoformat() if new_user.created_at else None
  }), 201


def get_user(user_id):
  print('=== USER ID', user_id)
  user = User.query.get(user_id)

  if not user:
      return jsonify({"error": "User not found"}), 404

  return jsonify({
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "created_at": user.created_at.isoformat() if user.created_at else None
  }), 200
