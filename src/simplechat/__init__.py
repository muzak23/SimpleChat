import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from dotenv import load_dotenv

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    load_dotenv()
    if os.getenv('SECRET_KEY') is None:
        raise ValueError('SECRET_KEY is not set in .env')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # blueprint for non-chat pages (index, about, etc)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for chat pages
    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    socketio.init_app(app)
    return app

