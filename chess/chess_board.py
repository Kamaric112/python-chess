import os

from chess.event_handler import ChessEventHandler
from chess.game_logic import ChessGameLogic
from chess.renderer import ChessRenderer
from user import User
import logging


logging.basicConfig(
    filename='log/chess_game_event.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ChessBoard:
    def __init__(self, screen, width, height, config):
        self.config = config
        self.game = ChessGameLogic(config)
        self.renderer = ChessRenderer(screen, width, height)
        self.event_handler = ChessEventHandler(self.game, self.renderer)
        self.user_a = User(config.playerA, os.path.join('assets', 'black-bishop.png'))
        self.user_b = User(config.playerB, os.path.join('assets', 'white-bishop.png'))
        #logging.info(f"User A in chess board: {self.user_a.name}, User B: {self.user_b.name}")
        self.game.user_a = self.user_a
        self.game.user_b = self.user_b

    def reset_all(self):
        self.game.reset()
        self.renderer.reset()
        self.event_handler.reset()

    def draw(self):
        #logging.info(f"User A in chess board: {self.user_a.name}, User B: {self.user_b.name}")
        while True:
            result = self.event_handler.handle_events()
            if result == "menu":
                self.reset_all()
                self.game.reset_game()
                return "menu"
            self.renderer.draw_board(self.game, self.user_a, self.user_b)


