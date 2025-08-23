from flask import request, jsonify
from ..services.db.user_db_service import create_new_user, get_users
from ..utils.db_validators import validate_user_exists
from ..utils.input_validators import validate_user_input

# @desc       create new user
# @route      POST api/v1/users
# @access     Public
def create_user():
  data = request.get_json()

  print('=== data', data)

  error_response = validate_user_input(data, ["name", "email"])
  if error_response:
    return error_response

  new_user, error = create_new_user(data)
  if error:
    return jsonify(error), 400

  return jsonify({
      "id": new_user.id,
      "name": new_user.name,
      "email": new_user.email,
      "created_at": new_user.created_at.isoformat() if new_user.created_at else None
  }), 201


# @desc       get specific user
# @route      GET api/v1/users/<user_id>
# @access     Public
def get_user(user_id):
  user, error_response = validate_user_exists(user_id)
  if error_response:
    return error_response

  return jsonify({
      "id": user.id,
      "name": user.name,
      "email": user.email,
      "created_at": user.created_at.isoformat() if user.created_at else None
  }), 200

# @desc       get all users
# @route      GET api/v1/users/
# @access     Public
def get_all_users():
  users, error = get_users()
  if error:
      return jsonify(error), 500
  if not users:
      return jsonify({"error": "No users found"}), 404

  return jsonify({
    "users": [
        {
          "id": u.id,
          "name": u.name,
          "email": u.email,
          "created_at": u.created_at.isoformat() if u.created_at else None
        }
        for u in users
      ]
  }), 200