import os
from dotenv import load_dotenv

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


socketio = SocketIO(manage_sessions=False, cors_allowed_origins='*', async_mode='eventlet')
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    load_dotenv()
    if os.getenv('SECRET_KEY') is None:
        raise ValueError('SECRET_KEY is not set in .env')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # blueprint for non-chat pages (index, about, etc)
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # blueprint for chat pages
        from .chat import chat as chat_blueprint
        app.register_blueprint(chat_blueprint)

        # blueprint for HTTPS authentication
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        socketio.init_app(app)
        db.create_all()

        return app
