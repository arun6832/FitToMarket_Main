from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Overridden by env in production

    from . import routes
    app.register_blueprint(routes.bp)

    return app
