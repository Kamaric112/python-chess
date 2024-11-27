import os

from chess.event_handler import ChessEventHandler
from chess.game_logic import ChessGameLogic
from chess.renderer import ChessRenderer
from user import User


class ChessBoard:
    def __init__(self, screen, width, height):
        self.game = ChessGameLogic()
        self.renderer = ChessRenderer(screen, width, height)
        self.event_handler = ChessEventHandler(self.game, self.renderer)
        self.user_a = User('User A', os.path.join('assets', 'black-bishop.png'))
        self.user_b = User('User B', os.path.join('assets', 'white-bishop.png'))
        self.game.user_a = self.user_a
        self.game.user_b = self.user_b

    def reset_all(self):
        self.game.reset()
        self.renderer.reset()
        self.event_handler.reset()

    def draw(self):
        while True:
            result = self.event_handler.handle_events()
            if result == "menu":
                self.reset_all()
                self.game.reset_game()
                return "menu"
            self.renderer.draw_board(self.game, self.user_a, self.user_b)
