from sqlalchemy import desc
from app.utils.pagination_util import get_pagination_params
from config.db import db
from ...models.message import Message

def create_new_message(message_data):
  try:
    new_message = Message(
        question=message_data["question"],
        answer=message_data["answer"],
        user_id=message_data["user_id"], 
      )

    db.session.add(new_message)
    db.session.commit()
    return new_message, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}


def get_messages_by_user_id(user_id, page = None, per_page= None):
  pagination = get_pagination_params(page, per_page)

  try:
    stmt = (
      db.select(Message)
      .where(Message.user_id == user_id)
      .order_by(desc(Message.created_at))
      .limit(pagination["limit"])
      .offset(pagination["offset"])
    )
    messages = db.session.execute(stmt).scalars().all()
    return messages, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}

def get_all_messages(page = None, per_page= None):
  pagination = get_pagination_params(page, per_page)

  try:
    stmt = (
      db.select(Message)
      .order_by(desc(Message.created_at))
      .limit(pagination["limit"])
      .offset(pagination["offset"])
    )
    messages = db.session.execute(stmt).scalars().all()
    return messages, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}
