from board import Board


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None
        self.user_a = None
        self.user_b = None

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
