import uuid
import json
from datetime import datetime, timezone
from src.datasource.db import db


class GameModel(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    field_data = db.Column(db.Text, nullable=False, default='[[0,0,0],[0,0,0],[0,0,0]]')
    state = db.Column(db.String(20), nullable=False, default='waiting')
    player_x = db.Column(db.String(36), nullable=True)
    player_o = db.Column(db.String(36), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __init__(self, game_id=None, field_data=None, state=None, player_x=None, player_o=None):
        self.id = game_id or str(uuid.uuid4())
        self.field_data = field_data or json.dumps([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.state = state or 'waiting'
        self.player_x = player_x
        self.player_o = player_o

    def get_field(self):
        return json.loads(self.field_data)

    def set_field(self, field):
        self.field_data = json.dumps(field)
