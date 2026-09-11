import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from src.datasource.db import db
from src.di.container import Container


def create_app():
    app = Flask(__name__)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Set DATABASE_URL; see RUN.md")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    container = Container()
    app.register_blueprint(container.get_auth_blueprint())
    app.register_blueprint(container.get_game_blueprint())

    return app


if __name__ == "__main__":
    app = create_app()
    print("Server running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
