class GameServiceInterface:
    def get_next_move(self, current_game):
        raise NotImplementedError

    def validate_field(self, current_game, previous_game):
        raise NotImplementedError

    def check_game_over(self, current_game):
        raise NotImplementedError

    def make_move(self, game_id, field, user_id):
        raise NotImplementedError

    def create_game(self, player_x, player_o):
        raise NotImplementedError

    def join_game(self, game_id, player_o):
        raise NotImplementedError

    def get_game(self, game_id):
        raise NotImplementedError

    def get_available_games(self):
        raise NotImplementedError

    def get_finished_games(self, user_id):
        raise NotImplementedError

    def get_leaderboard(self, n):
        raise NotImplementedError
