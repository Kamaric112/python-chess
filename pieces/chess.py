from board import Board

import pygame
import sys


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
        self.move_history = []

    def make_move(self, start, end):
        # Execute moves and handle special cases
        pass

    def check_game_state(self):
        # Check for check, checkmate, stalemate
        pass


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

    def draw(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill background
            self.screen.fill((60, 25, 60))

            # Draw the chess board
            for row in range(8):
                for col in range(8):
                    x = self.start_x + col * self.SQUARE_SIZE
                    y = self.start_y + row * self.SQUARE_SIZE
                    color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                    pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

            pygame.display.flip()
