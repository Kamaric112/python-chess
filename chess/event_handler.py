import pygame
import sys
import logging
from database import Database

logging.basicConfig(filename='chess/chess_game_event.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ChessEventHandler:
    def __init__(self, game, renderer, config):
        self.game = game
        self.renderer = renderer
        self.config = config
        self.database = Database(config)
        print(self.config.playerB, self.config.playerA)

    def handle_events(self):
        logging.info(f"Game State: {self.renderer.game_state}")
        logging.info(f"Current Turn: {self.game.board.current_turn}")
        if self.renderer.game_state == "playing":
            time_winner = self.game.update_timer()

            if time_winner:
                logging.info(f"Timer Update: {time_winner}")
                self.renderer.game_state = "victory"
                self.renderer.show_victory_screen(f"{time_winner} (Time)")
                self._save_match(time_winner)
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

        # add back button handling
        if self.renderer.back_button_rect.collidepoint(mouse_pos):
            return "menu"

        clicked_row = (mouse_pos[1] - self.renderer.start_y) // self.renderer.SQUARE_SIZE
        clicked_col = (mouse_pos[0] - self.renderer.start_x) // self.renderer.SQUARE_SIZE

        if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
            if self.game.selected_piece:
                clicked_piece = self.game.board.squares[clicked_row][clicked_col]
                if clicked_piece and clicked_piece.color == self.game.board.current_turn:
                    self.game.select_piece(clicked_row, clicked_col)
                    return
                if self.game.make_move(self.game.selected_piece.position, (clicked_row, clicked_col)):
                    winner = self.game.board.is_checkmate()
                    if winner:
                        self.renderer.game_state = "victory"
                        self.renderer.show_victory_screen(f"{winner} (Checkmate)")
                        self._save_match(winner)  # Save match on checkmate

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

    def _save_match(self, winner):
        if winner == "white":
            winner_name = self.config.playerB
        elif winner == "black":
            winner_name = self.config.playerA
        else:
            winner_name = winner  # In case of time win, winner is the color
        print(winner, self.config.playerB, self.config.playerA)
        self.database.save_match(winner_name)
