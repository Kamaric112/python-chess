import pygame
import sys

from chess import renderer


class ChessEventHandler:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer

    def handle_events(self):
        if self.renderer.game_state == "playing":
            time_winner = self.game.update_timer()

            if time_winner:
                self.renderer.game_state = "victory"
                self.renderer.show_victory_screen(f"{time_winner} (Time)")
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.renderer.game_state == "playing":
                    result = self._handle_mouse_click()
                    if result == "menu":
                        return result

            elif event.type == pygame.MOUSEMOTION:
                if self.renderer.game_state == "playing":
                    self._handle_mouse_hover()

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
                        self.renderer.show_victory_screen(f"{winner} (Checkmate)")
            else:
                self.game.select_piece(clicked_row, clicked_col)

    def _handle_mouse_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_row = (mouse_pos[1] - self.renderer.start_y) // self.renderer.SQUARE_SIZE
        hover_col = (mouse_pos[0] - self.renderer.start_x) // self.renderer.SQUARE_SIZE

        if 0 <= hover_row < 8 and 0 <= hover_col < 8:
            self.game.hover_moves = self.game.get_hover_moves(hover_row, hover_col)
        else:
            self.game.hover_moves = []

    def reset(self):
        self.renderer.game_state = "playing"
