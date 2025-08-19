from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from routes.chat_routes import chat_bp

app = Flask(__name__)

app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
