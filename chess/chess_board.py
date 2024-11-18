from chess.event_handler import ChessEventHandler
from chess.game_logic import ChessGame
from chess.renderer import ChessRenderer



class ChessBoard:
    def __init__(self, screen, width, height):
        self.game = ChessGame()
        self.renderer = ChessRenderer(screen, width, height)
        self.event_handler = ChessEventHandler(self.game, self.renderer)

    def draw(self):
        while True:
            result = self.event_handler.handle_events()
            if result == "menu":
                self.game.reset_game()
                return "menu"
            self.renderer.draw_board(self.game)
