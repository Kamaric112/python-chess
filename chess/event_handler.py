import pygame
import sys

from chess import renderer


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
                    result = self._handle_mouse_click()
                    if result == "menu":
                        return result
            elif event.type == pygame.KEYDOWN and self.renderer.game_state == "victory":
                if event.key == pygame.K_RETURN:
                    return "menu"

    def _handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()

        # Handle user A profile click
        if self.renderer.user_a_profile_rect.collidepoint(mouse_pos):
            self.game.user_a.change_image()
            return

         # Handle user A name click
        if self.renderer.user_a_name_rect.collidepoint(mouse_pos):
            self.game.user_a.change_name()
            return

         # Handle user B name click
        if self.renderer.user_b_name_rect.collidepoint(mouse_pos):
            self.game.user_b.change_name()
            return

        # Handle user B profile click
        if self.renderer.user_b_profile_rect.collidepoint(mouse_pos):
            self.game.user_b.change_image()
            return

        # add back button handling
        if self.renderer.back_button_rect.collidepoint(mouse_pos):
            return "menu"

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
