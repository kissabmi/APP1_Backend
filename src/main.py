import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_jwt_extended import JWTManager

from src.datasource.db import db
from src.di.container import Container


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        if 'games' in inspector.get_table_names():
            cols = [c['name'] for c in inspector.get_columns('games')]
            if 'created_at' not in cols:
                with db.engine.connect() as conn:
                    conn.execute(text(
                        "ALTER TABLE games ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT NOW()"
                    ))
                    conn.commit()

    container = Container()
    app.register_blueprint(container.get_auth_blueprint())
    app.register_blueprint(container.get_game_blueprint())

    return app


if __name__ == "__main__":
    app = create_app()
    print("Server running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
