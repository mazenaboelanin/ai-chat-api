from sqlalchemy import desc
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


def get_messages_by_user_id(user_id):
  try:
    stmt = (
      db.select(Message)
      .where(Message.user_id == user_id)
      .order_by(desc(Message.created_at))
    )
    messages = db.session.execute(stmt).scalars().all()
    return messages, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}

def get_all_messages():
  try:
    stmt = db.select(Message).order_by(desc(Message.created_at))
    messages = db.session.execute(stmt).scalars().all()
    return messages, None
  except Exception as e:
    db.session.rollback()
    return None, {"error": str(e)}
