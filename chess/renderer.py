import pygame
import os


class ChessRenderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.WHITE = (255, 255, 255)
        self.BLACK = (128, 128, 128)
        self.HIGHLIGHT_COLOR = (124, 252, 0)
        # Adjust board size to leave space for users
        self.SQUARE_SIZE = min(width, height - 200) // 8  # Reduced to leave space
        self.start_x = (width - self.SQUARE_SIZE * 8) // 2
        # Adjust start_y to center the board between users
        self.start_y = 100 + (height - 200 - self.SQUARE_SIZE * 8) // 2
        self.pieces_images = self.load_pieces()
        self.font = pygame.font.Font(None, 36)
        self.game_state = "playing"
        self.back_button_color = (34, 139, 34)
        self.back_button_rect = pygame.Rect(5, 300, 60, 40)
        pygame.font.init()

    def draw_users(self, user_a, user_b):
        # Draw background rectangles for user sections
        user_background = (139, 69, 19)  # Saddle brown color
        top_rect = pygame.Rect(0, 0, self.width, 100)
        bottom_rect = pygame.Rect(0, self.height - 100, self.width, 100)
        pygame.draw.rect(self.screen, user_background, top_rect)
        pygame.draw.rect(self.screen, user_background, bottom_rect)
        # Draw User A at the top
        user_image_size = 80
        # Top user
        if user_a.image:
            user_a_image = pygame.image.load(user_a.image)
            user_a_image = pygame.transform.scale(user_a_image, (user_image_size, user_image_size))
            self.screen.blit(user_a_image, (20, 10))
        user_a_text = self.font.render(user_a.name, True, self.WHITE)
        self.screen.blit(user_a_text, (120, 40))

        # Bottom user
        if user_b.image:
            user_b_image = pygame.image.load(user_b.image)
            user_b_image = pygame.transform.scale(user_b_image, (user_image_size, user_image_size))
            self.screen.blit(user_b_image, (20, self.height - 90))
        user_b_text = self.font.render(user_b.name, True, self.WHITE)
        self.screen.blit(user_b_text, (120, self.height - 60))


    def load_pieces(self):
        pieces = {}
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']

        for color in colors:
            for piece_type in piece_types:
                image_path = os.path.join('assets', f'{color}-{piece_type}.png')
                image = pygame.image.load(image_path)
                pieces[f'{color}_{piece_type}'] = pygame.transform.scale(
                    image, (self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
        return pieces

    def draw_board(self, game,user_a,user_b):
        if self.game_state == "playing":
            self.screen.fill((60, 25, 60))
            self._draw_squares(game)
            self.draw_users(user_a, user_b)
            self._draw_turn_indicator(game.board.current_turn)
            self._draw_back_button()
            pygame.display.flip()
        elif self.game_state == "victory":
            self.show_victory_screen(game.board.is_checkmate())

    def _draw_squares(self, game):
        for row in range(8):
            for col in range(8):
                x = self.start_x + col * self.SQUARE_SIZE
                y = self.start_y + row * self.SQUARE_SIZE
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                if (row, col) in game.valid_moves:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(128)
                    s.fill(self.HIGHLIGHT_COLOR)
                    self.screen.blit(s, (x, y))

                piece = game.board.squares[row][col]
                if piece:
                    piece_name = f'{piece.color}_{piece.__class__.__name__.lower()}'
                    piece_image = self.pieces_images[piece_name]
                    self.screen.blit(piece_image, (x, y))

    def _draw_turn_indicator(self, current_turn):
        turn_text = f"{current_turn.capitalize()}'s Turn"
        text_surface = self.font.render(turn_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, 30))

        box_rect = text_rect.copy()
        box_rect.inflate_ip(20 * 2, 20)
        pygame.draw.rect(self.screen, (34, 139, 34), box_rect, border_radius=10)
        self.screen.blit(text_surface, text_rect)

    def _draw_back_button(self):

        pygame.draw.rect(self.screen, self.back_button_color, self.back_button_rect, border_radius=10)
        back_text = self.font.render("Back", True, self.WHITE)
        text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, text_rect)

    def draw_input_box(self, text):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.width // 4, self.height // 3, self.width // 2, 100))
        text_surface = self.font.render(text, True, self.WHITE)
        self.screen.blit(text_surface, (self.width // 4 + 10, self.height // 3 + 40))
        pygame.display.flip()


    def show_victory_screen(self, winner):
        victory_font = pygame.font.Font(None, 74)
        text = f"{winner} Wins!"

        self.screen.fill((60, 25, 60))
        text_surface = victory_font.render(text, True, (255, 215, 0))
        continue_text = self.font.render("Press ENTER to return to menu", True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 100))

        self.screen.blit(text_surface, text_rect)
        self.screen.blit(continue_text, continue_rect)
        pygame.display.flip()
