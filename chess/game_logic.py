import pygame

from board import Board


class ChessGameLogic:
    def __init__(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None
        self.user_a = None
        self.user_b = None

        self.hover_moves = []
        self.timer_a = 600
        self.timer_b = 600
        self.last_time = pygame.time.get_ticks()

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000  # Convert to seconds
        self.last_time = current_time

        if self.board.current_turn == 'white':
            self.timer_b -= elapsed
        else:
            self.timer_a -= elapsed

        if self.timer_a <= 0:
            return 'white'
        elif self.timer_b <= 0:
            return 'black'
        else:
            return None

    def get_hover_moves(self, row, col):
        piece = self.board.squares[row][col]
        if piece and piece.color == self.board.current_turn:
            return piece.get_valid_moves(self.board.squares)
        return []

    def reset_game(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None

    def select_piece(self, row, col):
        piece = self.board.squares[row][col]
        if piece and piece.color == self.board.current_turn:
            self.selected_piece = piece
            self.valid_moves = piece.get_valid_moves(self.board.squares)
            return True
        return False

    def make_move(self, start_pos, end_pos):
        if end_pos in self.valid_moves:
            self.board.move_piece(start_pos, end_pos)
            self.selected_piece = None
            self.valid_moves = []
            return True
        return False

    def reset(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None
        self.hover_moves = []
        self.timer_a = 5
        self.timer_b = 5
        self.last_time = pygame.time.get_ticks()
