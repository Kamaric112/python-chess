import pygame
import sys


class ChessEventHandler:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.renderer.game_state == "playing":
                    self._handle_mouse_click()
            elif event.type == pygame.KEYDOWN and self.renderer.game_state == "victory":
                if event.key == pygame.K_RETURN:
                    return "menu"

    def _handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        clicked_row = (mouse_pos[1] - self.renderer.start_y) // self.renderer.SQUARE_SIZE
        clicked_col = (mouse_pos[0] - self.renderer.start_x) // self.renderer.SQUARE_SIZE

        if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
            if self.game.selected_piece:
                if self.game.make_move(self.game.selected_piece.position, (clicked_row, clicked_col)):
                    winner = self.game.board.is_checkmate()
                    if winner:
                        self.renderer.game_state = "victory"
                        self.renderer.show_victory_screen(winner)
            else:
                self.game.select_piece(clicked_row, clicked_col)
