from board import Board
import pygame
import sys
import os


class ChessBoard:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.WHITE = (255, 255, 255)
        self.BLACK = (128, 128, 128)
        self.SQUARE_SIZE = min(width, height) // 8
        self.start_x = (width - self.SQUARE_SIZE * 8) // 2
        self.start_y = (height - self.SQUARE_SIZE * 8) // 2
        self.board = Board()
        self.pieces_images = self.load_pieces()
        self.HIGHLIGHT_COLOR = (124, 252, 0)
        self.valid_moves = []
        self.selected_piece = None
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

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
    def reset_game(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None

    def draw(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle piece selection
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_row = (mouse_pos[1] - self.start_y) // self.SQUARE_SIZE
                    clicked_col = (mouse_pos[0] - self.start_x) // self.SQUARE_SIZE

                    if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
                        if self.selected_piece:
                            if (clicked_row, clicked_col) in self.valid_moves:
                                self.board.move_piece(self.selected_piece.position, (clicked_row, clicked_col))
                                # Check for winner after each move
                                winner = self.board.is_checkmate()
                                if winner:
                                    result = self.show_victory_screen(winner)
                                    if result == "menu":
                                        self.reset_game()
                                        return "menu"
                            self.selected_piece = None
                            self.valid_moves = []
                        else:
                            piece = self.board.squares[clicked_row][clicked_col]
                            if piece and piece.color == self.board.current_turn:
                                self.selected_piece = piece
                                self.valid_moves = piece.get_valid_moves(self.board.squares)

            # Fill background
            self.screen.fill((60, 25, 60))

            # Draw the chess board
            for row in range(8):
                for col in range(8):
                    x = self.start_x + col * self.SQUARE_SIZE
                    y = self.start_y + row * self.SQUARE_SIZE
                    color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                    pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                    # Normal square color
                    color = self.WHITE if (row + col) % 2 == 0 else self.BLACK

                    # Draw the square
                    pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                    # Highlight valid moves
                    if (row, col) in self.valid_moves:
                        s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                        s.set_alpha(128)
                        s.fill(self.HIGHLIGHT_COLOR)
                        self.screen.blit(s, (x, y))

                    # Draw pieces
                    piece = self.board.squares[row][col]
                    if piece:
                        piece_name = f'{piece.color}_{piece.__class__.__name__.lower()}'
                        piece_image = self.pieces_images[piece_name]
                        self.screen.blit(piece_image, (x, y))

                # Enhanced turn display with background box
            turn_text = f"{self.board.current_turn.capitalize()}'s Turn"
            text_surface = self.font.render(turn_text, True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, 30))

            # Draw background box
            box_rect = text_rect.copy()
            box_rect.inflate_ip(20 * 2, 20)
            pygame.draw.rect(self.screen, (34, 139, 34), box_rect, border_radius=10)

            # Draw text
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def show_victory_screen(self, winner):
        victory_font = pygame.font.Font(None, 74)
        text = f"{winner} Wins!"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "menu"

            # Draw victory screen
            self.screen.fill((60, 25, 60))

            # Create text surfaces
            text_surface = victory_font.render(text, True, (255, 215, 0))
            continue_text = self.font.render("Press ENTER to return to menu", True, (255, 255, 255))

            # Position text
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 100))

            # Draw text
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(continue_text, continue_rect)

            pygame.display.flip()

