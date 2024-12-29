import pygame
import random
import secrets

from board import Board
from pieces.piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from database_setup import ChessDatabase

import logging

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
        

        self.move_number = 0
        self.db = ChessDatabase()
        self.move_history = []

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

    def make_move(self, start_pos, end_pos):
        piece = self.board.squares[start_pos[0]][start_pos[1]]
        # Validate piece exists and it's the correct turn
        if not piece or piece.color != self.board.current_turn:
            return False
        # Get valid moves for the piece
        valid_moves = piece.get_valid_moves(self.board.squares)
        # Check if the end position is in valid moves
        if end_pos not in valid_moves:
            return False
        # Make the move if valid
        captured_piece = self.board.squares[end_pos[0]][end_pos[1]]
        if self.board.move_piece(start_pos, end_pos):
            self.move_number += 1
            self.move_history.append((piece, start_pos, end_pos,captured_piece))
            #self.db.save_move(piece.__class__.__name__, start_pos, end_pos, self.move_number)
              # Save to database only if connection exists
            if self.db:
                try:
                    self.db.save_move(piece.__class__.__name__, start_pos, end_pos, self.move_number,captured_piece)
                except Exception as e:
                    logging.error(f"Failed to save move: {e}")       
            return True
        return False

    def rewind_move(self):
        if self.move_number > 0:
            # Get the last move from database
            last_move = self.db.get_previous_move(self.move_number)
            if last_move:
                piece_type = last_move['piece_type']
                start_pos = last_move['start_pos']
                end_pos = last_move['end_pos']
                captured_piece_type = last_move['captured_piece_type']
                captured_piece_color = last_move['captured_piece_color']
                
                # if hasattr(self.board.squares[end_pos[0]][end_pos[1]], 'original_type'):
                #     piece_type = self.board.squares[end_pos[0]][end_pos[1]].original_type
                

                # Get the piece at current position
                # moving_piece = self.board.squares[end_pos[0]][end_pos[1]]

                # if hasattr(moving_piece, 'original_type'):
                #     piece_type = moving_piece.original_type
                
                #logging.info(f"Moving piece type: {piece_type}")

                # Create piece instances and restore board state
                if piece_type == 'Pawn' and end_pos[0] in [0, 7]:
                    moving_piece = Pawn(
                    'white' if self.board.current_turn == 'black' else 'black',
                    end_pos
                    )
                else:
                    moving_piece = self.board.squares[end_pos[0]][end_pos[1]]
                
                 # Create piece if it doesn't exist
                if moving_piece is None:
                    piece_classes = {
                        'Pawn': Pawn,
                        'Rook': Rook,
                        'Knight': Knight,
                        'Bishop': Bishop,
                        'Queen': Queen,
                        'King': King
                    }
                    moving_piece = piece_classes[piece_type](
                        'white' if self.board.current_turn == 'black' else 'black', 
                        end_pos
                    )
                
                # Move piece back to start position
                self.board.squares[start_pos[0]][start_pos[1]] = moving_piece
                moving_piece.position = start_pos

                # Restore captured piece if any
                if captured_piece_type:
                    # Create new instance of captured piece
                    piece_classes = {
                        'Pawn': Pawn,
                        'Rook': Rook,
                        'Knight': Knight,
                        'Bishop': Bishop,
                        'Queen': Queen,
                        'King': King
                    }
                    captured_piece_class = piece_classes[captured_piece_type]
                    restored_piece = captured_piece_class(captured_piece_color, end_pos)
                    self.board.squares[end_pos[0]][end_pos[1]] = restored_piece
                else:
                    self.board.squares[end_pos[0]][end_pos[1]] = None
                
                self.db.delete_move(self.move_number)
                self.move_number -= 1
                self.board.current_turn = 'black' if self.board.current_turn == 'white' else 'white'

    def activate_bomb(self):
        # Generate random position
        row = secrets.randbelow(8)
        col = secrets.randbelow(8)
        return (row, col)

    def play_rps(self, player_choice):
        choices = ['rock', 'paper', 'scissor']
        computer_choice = secrets.choice(choices)

        if player_choice == computer_choice:
            return (None, computer_choice)  # Draw
        
        wins = {
            'rock': 'scissor',
            'paper': 'rock',
            'scissor': 'paper'
        }

        player_wins = wins[player_choice] == computer_choice
        return (player_wins, computer_choice)  

    def reset(self):
        self.board = Board()
        self.valid_moves = []
        self.selected_piece = None
        self.hover_moves = []
        self.timer_a = self.config.time * 60
        self.timer_b = self.config.time * 60
        self.last_time = pygame.time.get_ticks()



# def rewind_move00(self):
    #     if self.move_number > 0:
    #         #last_move = self.db.get_last_move(self.move_number)

    #         piece, start_pos, end_pos,captured_piece = self.move_history.pop()
    #         #captured_piece = self.board.squares[end_pos[0]][end_pos[1]]

    #         # Reverse the move
    #         self.board.squares[start_pos[0]][start_pos[1]] = piece
    #         self.board.squares[end_pos[0]][end_pos[1]] = captured_piece
    #         piece.position = start_pos
    #         self.move_number -= 1
    #         # Switch turns
    #         self.board.current_turn = 'black' if self.board.current_turn == 'white' else 'white'

    # def rewind_move(self):
    #     if self.move_number > 0:
    #         # Get the last move from database
    #         last_move = self.db.get_previous_move(self.move_number)
    #         if last_move:
    #             # Reconstruct the move from database data
    #             piece_type, start_pos, end_pos, captured_piece_type, captured_piece_color = last_move
    #             # Create piece instances and restore board state
    #             # ... implement piece reconstruction logic here ...
    #             self.move_number -= 1
    #             self.board.current_turn = 'black' if self.board.current_turn == 'white' else 'white'
