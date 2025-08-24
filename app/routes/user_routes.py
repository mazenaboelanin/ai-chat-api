from flask import Blueprint
from ..controllers.user_controller import create_user, get_user, get_all_users

user_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

# POST /users → create new user
@user_bp.route("/", methods=["POST"])
def add_user():
  return create_user()

# GET /users/id → get specific user
@user_bp.route("/<id>", methods=["GET"])
def fetch_user(id):
  return get_user(id)

# GET /users/ → get all users
@user_bp.route("/", methods=["GET"])
def fetch_users():
  return get_all_users()