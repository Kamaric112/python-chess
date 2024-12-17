import pygame

from board import Board


class ChessGameLogic:
    def __init__(self,config):
        self.config = config

        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None
        self.user_a = config.playerA
        self.user_b = config.playerB

        self.hover_moves = []
        self.timer_a = config.time*60
        self.timer_b = config.time*60
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
         # If a new piece of same color is clicked, switch selection to it
        if piece and piece.color == self.board.current_turn:
            self.selected_piece = piece
            self.valid_moves = piece.get_valid_moves(self.board.squares)
            return True
        return False

        # If same piece is selected again, deselect it
        # if self.selected_piece and (row, col) == self.selected_piece.position:
        #     self.selected_piece = None
        #     self.valid_moves = []
        #     return True
        # return False

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
        self.timer_a = self.config.time * 60
        self.timer_b = self.config.time * 60
        self.last_time = pygame.time.get_ticks()
