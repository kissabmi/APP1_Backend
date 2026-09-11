from src.datasource.db import db
from src.datasource.model.game import GameModel
from sqlalchemy import text


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

    def find_finished_for_user(self, user_id):
        return GameModel.query.filter(
            (GameModel.player_x == user_id) | (GameModel.player_o == user_id),
            GameModel.state.in_(['victory_x', 'victory_o', 'draw'])
        ).order_by(GameModel.created_at.desc()).all()

    def get_leaderboard(self, n):
        sql = text("""
            WITH finished AS (
                SELECT player_x AS user_id, state FROM games
                WHERE state IN ('victory_x', 'victory_o', 'draw')
                UNION ALL
                SELECT player_o AS user_id, state FROM games
                WHERE state IN ('victory_x', 'victory_o', 'draw')
            ),
            wins_for_user AS (
                SELECT player_x AS user_id FROM games WHERE state = 'victory_x'
                UNION ALL
                SELECT player_o AS user_id FROM games WHERE state = 'victory_o'
            ),
            stats AS (
                SELECT
                    f.user_id,
                    COUNT(*) AS total,
                    (SELECT COUNT(*) FROM wins_for_user w WHERE w.user_id = f.user_id) AS wins
                FROM finished f
                GROUP BY f.user_id
            ),
            ratios AS (
                SELECT user_id,
                       CASE WHEN total > 0 THEN ROUND(wins::numeric / total, 4) ELSE 0 END AS win_ratio
                FROM stats
            )
            SELECT u.id AS uuid, u.login, COALESCE(r.win_ratio, 0) AS win_ratio
            FROM users u
            LEFT JOIN ratios r ON u.id = r.user_id
            ORDER BY r.win_ratio DESC NULLS LAST
            LIMIT :limit
        """)
        return db.session.execute(sql, {"limit": n}).fetchall()
