import uuid
from src.domain.model.game_field import GameField
from src.domain.model.game_state import GameState


class CurrentGame:
    def __init__(self, game_field=None, game_id=None, state=None, player_x=None, player_o=None):
        self.game_field = game_field or GameField()
        self.game_id = game_id or str(uuid.uuid4())
        self.state = state or GameState.WAITING
        self.player_x = player_x
        self.player_o = player_o

    def get_field(self):
        return self.game_field

    def get_id(self):
        return self.game_id

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_player_x(self):
        return self.player_x

    def get_player_o(self):
        return self.player_o
