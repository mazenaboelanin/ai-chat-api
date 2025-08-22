from config.db import db
from datetime import datetime


class Message(db.Model):
  __tablename__ = "messages"

  id = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.Text, nullable=False)
  answer = db.Column(db.Text)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  user = db.relationship("User", back_populates="messages")
