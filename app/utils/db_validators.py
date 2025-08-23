# app/utils/db_validators.py

from flask import jsonify
from ..models.user import User
from config.db import db


def validate_user_exists(user_id):
  user = db.session.get(User, user_id)
  print("==USER", user)
  if not user:
    return None, (jsonify({"error": f"No user found with id {user_id}"}),  404)
  return user, None
