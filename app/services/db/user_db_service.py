from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from app.utils.pagination_util import get_pagination_params
from config.db import db
from ...models.user import User

def create_new_user(user_data):
  try:
    new_user = User(name=user_data["name"], email=user_data["email"])
    db.session.add(new_user)
    db.session.commit()
    return new_user, None
  except IntegrityError as e:
    db.session.rollback()
    return None, {"error": "User with this email already exists"}
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}


def get_users(page = None, per_page= None):
  pagination = get_pagination_params(page, per_page)

  try:
    stmt = (
      db.select(User)
      .order_by(desc(User.created_at))
      .limit(pagination["limit"])
      .offset(pagination["offset"])
    )
    users = db.session.execute(stmt).scalars().all()
    return users, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}
