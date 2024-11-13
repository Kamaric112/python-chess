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
                            # If a piece is already selected, try to move it
                            if (clicked_row, clicked_col) in self.valid_moves:
                                self.board.move_piece(self.selected_piece.position, (clicked_row, clicked_col))
                            self.selected_piece = None
                            self.valid_moves = []
                        else:
                            # Select the piece and get its valid moves
                            piece = self.board.squares[clicked_row][clicked_col]
                            if piece:
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

            pygame.display.flip()
