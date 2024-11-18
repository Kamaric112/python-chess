from pieces.pawn import Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self):
        self.squares = self.initialize_board()
        self.current_turn = 'white'

    def initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Place pawns
        for col in range(8):
            board[1][col] = Pawn('black', (1, col))
            board[6][col] = Pawn('white', (6, col))

        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            board[0][col] = piece_order[col]('black', (0, col))
            board[7][col] = piece_order[col]('white', (7, col))

        return board

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if self.is_valid_move(start, end):
            piece = self.squares[start_row][start_col]
            if piece.color == self.current_turn:  # Add this check
                self.squares[end_row][end_col] = piece
                self.squares[start_row][start_col] = None
                piece.position = end
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'

                return True
        return False

    def is_valid_move(self, start, end):
        start_row, start_col = start
        piece = self.squares[start_row][start_col]

        if piece is None:
            return False

        valid_moves = piece.get_valid_moves(self.squares)
        return end in valid_moves

    def is_checkmate(self):
        # TODO maybe optimze this
        white_king_exists = False
        black_king_exists = False

        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if isinstance(piece, King):
                    if piece.color == 'white':
                        white_king_exists = True
                    else:
                        black_king_exists = True

        if not white_king_exists:
            return 'Black'
        if not black_king_exists:
            return 'White'
        return None

