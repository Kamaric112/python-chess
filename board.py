from pieces.piece import Pawn, Rook, Knight, Bishop, Queen, King
import random
import pygame
import logging
logging.basicConfig(
    filename='log/chess_game_event.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Board:
    def __init__(self):
        self.squares = self.initialize_board()
        self.current_turn = 'white'
        self.extra_move = False
        self.move_count = 0
        self.last_move = None




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
            if piece.color == self.current_turn:
                self.squares[end_row][end_col] = piece
                self.squares[start_row][start_col] = None
                piece.position = end

                self.last_move = (end_row, end_col)

                if not self.extra_move or self.move_count == 1:
                    self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                    self.extra_move = False
                    self.move_count = 0
                else:
                    self.move_count += 1
                return True
            
                #self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                #logging.info(f"Attempting move: {piece.__class__.__name__} from {start} to {end}")
                #logging.info(f"Current turn: {self.current_turn}")

            
        return False

    def is_valid_move(self, start, end):
        start_row, start_col = start
        piece = self.squares[start_row][start_col]

        if piece is None:
            return False

        valid_moves = piece.get_valid_moves(self.squares)
        return end in valid_moves

    def is_checkmate(self):
        # TODO maybe improve this
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
    
    def is_king_in_check(self,color):
        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    king_pos = (row, col)
                    break
        if not king_pos:
            return False
            
        # Check if any opponent piece can capture king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == opponent_color:
                    valid_moves = piece.get_valid_moves(self.squares)
                    if king_pos in valid_moves:
                        return True
        return False
    

    def is_pawn_promotion(self, end_pos):
        row, col = end_pos
        piece = self.squares[row][col]
        return (isinstance(piece, Pawn) and 
                ((piece.color == 'white' and row == 0) or 
                (piece.color == 'black' and row == 7)))
    
    def promote_pawn(self, end_pos, piece_type):
        """Promotes a pawn to the selected piece type."""
        row,col=end_pos
        current_piece = self.squares[row][col]
        color = current_piece.color
        #original_type = current_piece.__class__.__name__
        
        # Create new piece based on selected type
        if piece_type == 'queen':
            new_piece = Queen(color,end_pos)
        elif piece_type == 'rook':
            new_piece = Rook(color,end_pos)
        elif piece_type == 'bishop':
            new_piece = Bishop(color,end_pos)
        elif piece_type == 'knight':
            new_piece = Knight(color,end_pos)
        elif piece_type == 'pawn':
            new_piece = Pawn(color,end_pos)
             
        # Replace pawn with new piece
        self.squares[row][col] = new_piece
        new_piece.has_moved = True
        new_piece.promotion_time = pygame.time.get_ticks()  # Add timestamp
        new_piece.needs_sparkle = True  # Flag for sparkle effect
        new_piece.original_type = 'Pawn'  # Store original type for undo