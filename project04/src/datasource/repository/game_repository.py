import json
from src.datasource.db import db
from src.datasource.model.game import GameModel


class GameRepository:
    def save(self, game_model):
        existing = GameModel.query.get(game_model.id)
        if existing:
            existing.field_data = game_model.field_data
            existing.state = game_model.state
            existing.player_x = game_model.player_x
            existing.player_o = game_model.player_o
        else:
            db.session.add(game_model)
        db.session.commit()

    def get(self, game_id):
        return GameModel.query.get(game_id)

    def find_available(self):
        return GameModel.query.filter_by(state='waiting').all()
