from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from config.db import db, init_db

load_dotenv()

from .routes.chat_routes import chat_bp
from .routes.user_routes import user_bp


app = Flask(__name__)
db = init_db(app)
migrate = Migrate(app, db)

# Import models so Flask-Migrate can detect them
from .models.user import User
from .models.message import Message


app.register_blueprint(chat_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run(debug=True)
