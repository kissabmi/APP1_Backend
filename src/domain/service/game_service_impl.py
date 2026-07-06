import json
from src.domain.model.game_field import GameField
from src.domain.model.current_game import CurrentGame
from src.domain.model.game_state import GameState
from src.domain.service.game_service_interface import GameServiceInterface
from src.datasource.repository.game_repository import GameRepository
from src.datasource.model.game import GameModel


class GameService(GameServiceInterface):
    def __init__(self, repository):
        self._repository = repository

    def create_game(self, player_x, player_o):
        game = CurrentGame(player_x=player_x, player_o=player_o)
        if player_o == 'computer':
            game.set_state(GameState.PLAYER_X_TURN)
        else:
            game.set_state(GameState.WAITING)
        self._save(game)
        return game

    def join_game(self, game_id, player_o):
        game = self.get_game(game_id)
        if game is None:
            return None
        if game.get_state() != GameState.WAITING:
            return None
        game.player_o = player_o
        game.set_state(GameState.PLAYER_X_TURN)
        self._save(game)
        return game

    def get_game(self, game_id):
        model = self._repository.get(game_id)
        if model is None:
            return None
        return self._to_domain(model)

    def get_available_games(self):
        models = self._repository.find_available()
        return [self._to_domain(m) for m in models]

    def get_finished_games(self, user_id):
        models = self._repository.find_finished_for_user(user_id)
        return [
            {
                "game_id": m.id,
                "field": m.get_field(),
                "state": m.state,
                "player_x": m.player_x,
                "player_o": m.player_o,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in models
        ]

    def get_leaderboard(self, n):
        rows = self._repository.get_leaderboard(n)
        return [
            {"uuid": row.uuid, "login": row.login, "win_ratio": float(row.win_ratio)}
            for row in rows
        ]

    def make_move(self, game_id, field, user_id):
        previous = self.get_game(game_id)
        if previous is None:
            return None, "game not found"

        state = previous.get_state()
        if state == GameState.DRAW or state.startswith('victory'):
            return None, "game is over"

        if state == GameState.WAITING:
            return None, "game is waiting for players"

        is_player_x = (user_id == previous.get_player_x())
        is_player_o = (user_id == previous.get_player_o())

        if not is_player_x and not is_player_o:
            return None, "you are not in this game"

        if state == GameState.PLAYER_X_TURN and not is_player_x:
            return None, "not your turn"
        if state == GameState.PLAYER_O_TURN and not is_player_o:
            return None, "not your turn"

        new_game = CurrentGame(GameField(field), game_id)
        new_game.set_state(state)
        new_game.player_x = previous.get_player_x()
        new_game.player_o = previous.get_player_o()

        if not self.validate_field(new_game, previous):
            return None, "invalid move"

        result = self.check_game_over(new_game)
        if result == GameField.PLAYER_X:
            new_game.set_state(GameState.VICTORY_X)
        elif result == GameField.PLAYER_O:
            new_game.set_state(GameState.VICTORY_O)
        elif result == -1:
            new_game.set_state(GameState.DRAW)
        else:
            if state == GameState.PLAYER_X_TURN:
                new_game.set_state(GameState.PLAYER_O_TURN)
            else:
                new_game.set_state(GameState.PLAYER_X_TURN)

            if new_game.get_state() == GameState.PLAYER_O_TURN and previous.get_player_o() == 'computer':
                self.get_next_move(new_game)
                result2 = self.check_game_over(new_game)
                if result2 == GameField.PLAYER_O:
                    new_game.set_state(GameState.VICTORY_O)
                elif result2 == -1:
                    new_game.set_state(GameState.DRAW)
                else:
                    new_game.set_state(GameState.PLAYER_X_TURN)

        self._save(new_game)
        return new_game, None

    def get_next_move(self, current_game):
        field = current_game.get_field()
        best_score = -999
        best_move = None

        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if field.is_empty(row, col):
                    field.set_cell(row, col, GameField.PLAYER_O)
                    score = self._minimax(field, 0, False)
                    field.set_cell(row, col, GameField.EMPTY)
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move is not None:
            field.set_cell(best_move[0], best_move[1], GameField.PLAYER_O)
        return current_game

    def _minimax(self, field, depth, is_computer_turn):
        winner = self._check_winner(field)
        if winner == GameField.PLAYER_O:
            return 10 - depth
        if winner == GameField.PLAYER_X:
            return depth - 10
        if self._is_full(field):
            return 0

        if is_computer_turn:
            best = -999
            for row in range(GameField.SIZE):
                for col in range(GameField.SIZE):
                    if field.is_empty(row, col):
                        field.set_cell(row, col, GameField.PLAYER_O)
                        best = max(best, self._minimax(field, depth + 1, False))
                        field.set_cell(row, col, GameField.EMPTY)
            return best
        else:
            best = 999
            for row in range(GameField.SIZE):
                for col in range(GameField.SIZE):
                    if field.is_empty(row, col):
                        field.set_cell(row, col, GameField.PLAYER_X)
                        best = min(best, self._minimax(field, depth + 1, True))
                        field.set_cell(row, col, GameField.EMPTY)
            return best

    def validate_field(self, current_game, previous_game):
        curr = current_game.get_field()
        prev = previous_game.get_field()
        changed = 0
        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if curr.get_cell(row, col) != prev.get_cell(row, col):
                    if prev.get_cell(row, col) != GameField.EMPTY:
                        return False
                    changed += 1
        if changed != 1:
            return False
        return True

    def check_game_over(self, current_game):
        winner = self._check_winner(current_game.get_field())
        if winner != GameField.EMPTY:
            return winner
        if self._is_full(current_game.get_field()):
            return -1
        return 0

    def _check_winner(self, field):
        lines = []
        for i in range(GameField.SIZE):
            lines.append([field.get_cell(i, j) for j in range(GameField.SIZE)])
            lines.append([field.get_cell(j, i) for j in range(GameField.SIZE)])
        lines.append([field.get_cell(i, i) for i in range(GameField.SIZE)])
        lines.append([field.get_cell(i, GameField.SIZE - 1 - i) for i in range(GameField.SIZE)])

        for line in lines:
            if line[0] != GameField.EMPTY and all(c == line[0] for c in line):
                return line[0]
        return GameField.EMPTY

    def _is_full(self, field):
        for row in range(GameField.SIZE):
            for col in range(GameField.SIZE):
                if field.is_empty(row, col):
                    return False
        return True

    def _save(self, domain_game):
        model = GameModel(
            game_id=domain_game.get_id(),
            field_data=json.dumps(domain_game.get_field().get_field()),
            state=domain_game.get_state(),
            player_x=domain_game.get_player_x(),
            player_o=domain_game.get_player_o()
        )
        self._repository.save(model)

    def _to_domain(self, model):
        field = GameField(model.get_field())
        return CurrentGame(field, model.id, model.state, model.player_x, model.player_o)


