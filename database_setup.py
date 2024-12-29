import mysql.connector
import logging
from uuid import uuid4




class ChessDatabase:
    def __init__(self):
        logging.info("Attemping database connection")
        self.conn = None  # Initialize conn attribute before try block
        self.cursor = None
        self.game_id = None
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="chess_db"
            )
            self.cursor = self.conn.cursor()
            self.game_id = str(uuid4())
            
            print(f"Database connection established. Game ID: {self.game_id}")
            logging.info(f"Database connection established. Game ID: {self.game_id}")


        except Exception as e:
            print(f"Database connection failed: {e}")
            print("Game will run without move history storage")
            logging.error(f"Database connection error: {e}")
            logging.warning("Game will run without move history storage")
            
        
    def save_move(self, piece_type, start_pos, end_pos, move_number,captured_piece=None):
        if not self.conn:
            return
        try:
            captured_piece_type = None
            captured_piece_color = None
            if captured_piece:
                captured_piece_type = captured_piece.__class__.__name__
                captured_piece_color = captured_piece.color
            query = """INSERT INTO chess_moves 
                    (game_id, move_number, piece_type, start_pos, end_pos,captured_piece_type,captured_piece_color) 
                    VALUES (%s, %s, %s, %s, %s,%s,%s)"""
            self.cursor.execute(query, (self.game_id, move_number, piece_type, 
                                    str(start_pos), str(end_pos),captured_piece_type,captured_piece_color))
            self.conn.commit()
        except Exception as e:
            print(f"Failed to save move: {e}")
            logging.error(f"Failed to save move: {e}")
        


    def get_previous_move(self, current_move):
        if not self.conn:
            return None
        try:
            query = """SELECT piece_type, start_pos, end_pos,captured_piece_type, captured_piece_color FROM chess_moves 
                    WHERE game_id = %s AND move_number = %s"""
            self.cursor.execute(query, (self.game_id, current_move ))
            move=self.cursor.fetchone()
            #self.cursor.close()

            if move:
                # Convert string representations back to tuples for positions
                start_pos = eval(move[1])  # Safely convert string "(x,y)" to tuple
                end_pos = eval(move[2])    # Safely convert string "(x,y)" to tuple
                return {
                    'piece_type': move[0],
                    'start_pos': start_pos,
                    'end_pos': end_pos,
                    'captured_piece_type': move[3],
                    'captured_piece_color': move[4]
                }
        except Exception as e:
            print(f"Failed to get previous move: {e}")
            logging.error(f"Failed to get previous move: {e}")
        return None
    
    def delete_move00(self, move_number):
        query = """DELETE FROM chess_moves 
                WHERE game_id = %s AND move_number = %s"""
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(query, (self.game_id, move_number))
        self.conn.commit()
        cursor.close()

    def delete_move(self, move_number):
        if not self.conn:
            return
        try:
            query = """DELETE FROM chess_moves 
                    WHERE game_id = %s AND move_number = %s"""
            cursor = self.conn.cursor(buffered=True)
            cursor.execute(query, (self.game_id, move_number))
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Failed to delete move: {e}")
            logging.error(f"Failed to delete move: {e}")
    
    # def get_last_move(self, move_number):
    #     self.cursor.execute('''
    #         SELECT piece_type, start_pos, end_pos, captured_piece_type, captured_piece_color 
    #         FROM moves 
    #         WHERE move_number = ?
    #     ''', (move_number,))
    #     move = self.cursor.fetchone()
    #     if move:
    #         # Convert string representations back to tuples for positions
    #         start_pos = eval(move[1])  # Safely convert string "(x,y)" to tuple
    #         end_pos = eval(move[2])    # Safely convert string "(x,y)" to tuple
    #         return {
    #             'piece_type': move[0],
    #             'start_pos': start_pos,
    #             'end_pos': end_pos,
    #             'captured_piece_type': move[3],
    #             'captured_piece_color': move[4]
    #         }
    #     return None


        #while self.cursor.nextset():
        #    pass
        #self.cursor = self.conn.cursor()