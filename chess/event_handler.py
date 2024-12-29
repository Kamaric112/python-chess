import pygame
import sys

#from chess import renderer

import logging
logging.basicConfig(filename='log/chess_game_event.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ChessEventHandler:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        


    def handle_events(self):
        if self.renderer.game_state == "playing":
            time_winner = self.game.update_timer()

            if time_winner:
                logging.info(f"Timer Update: {time_winner}")
                self.renderer.game_state = "victory"
                self.renderer.show_victory_screen(f"{time_winner} (Time)")
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.renderer.game_state == "playing":
                    result = self.handle_mouse_click()
                    if result == "menu":
                        return result

            elif event.type == pygame.MOUSEMOTION:
                if self.renderer.game_state == "playing":
                    self.handle_mouse_hover()

            elif event.type == pygame.KEYDOWN and self.renderer.game_state == "victory":
                if event.key == pygame.K_RETURN:
                    return "menu"

    def handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()

        # Handle user A profile click
        if self.renderer.user_a_profile_rect.collidepoint(mouse_pos):
            self.game.user_a.change_image()
            return

        # Handle user A name click
        if self.renderer.user_a_name_rect.collidepoint(mouse_pos):
            self.game.user_a.change_name()
            return

        # Handle user B name click
        if self.renderer.user_b_name_rect.collidepoint(mouse_pos):
            self.game.user_b.change_name()
            return

        # Handle user B profile click
        if self.renderer.user_b_profile_rect.collidepoint(mouse_pos):
            self.game.user_b.change_image()
            return

        # add back button handling
        if self.renderer.back_button_rect.collidepoint(mouse_pos):
            return "menu"
        
        if self.renderer.rewind_button_rect.collidepoint(mouse_pos):
            if self.game.db.conn:
                self.game.rewind_move()
            else:
                print("Database connection not available-Chua ket noi den MySQL")
            return
        
        if self.renderer.bomb_button_rect.collidepoint(mouse_pos):
            #self.game.activate_bomb()
            #return
            bomb_pos = self.game.activate_bomb()
            self.renderer.bomb_position = bomb_pos
            self.renderer.bomb_effect_start = pygame.time.get_ticks()
            self.renderer.bomb_sound.play()
            pygame.time.delay(3000)  
            row, col = bomb_pos
            if self.game.board.squares[row][col]:
                self.game.board.squares[row][col] = None
            
            self.game.board.current_turn = 'black' if self.game.board.current_turn == 'white' else 'white'

            return
        
        
        if self.renderer.rps_button_rect.collidepoint(mouse_pos):
            while True:  # Keep playing until no draw
                rects = self.renderer.show_rps_selection()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for rect, choice in rects:
                            if rect.collidepoint(event.pos):
                                result, computer_choice = self.game.play_rps(choice)
                                logging.info(f"RPS Game - Player chose: {choice}, Computer chose: {computer_choice}, Result: {result}")
                                if self.game.board.current_turn == 'white':
                                    self.renderer.show_rps_result(choice, computer_choice, bottom=True)
                                else:
                                    self.renderer.show_rps_result(choice, computer_choice, bottom=False)

                                if result is None:
                                    self.renderer.rps_result_text = "Game Draw"
                                    #pygame.time.delay(5000)  # Wait 3 seconds
                                    self.renderer.draw_board(self.game, self.game.user_a, self.game.user_b)
                                    #pygame.display.flip()
                                    continue
                                
                                playera = self.game.board.current_turn.capitalize()
                                playerb = "Black" if playera == "White" else "White"


                                #winner = "White" if self.game.board.current_turn == 'white' else "Black"
                                self.renderer.rps_result_text = f"{playera if result else playerb} win"
                                pygame.display.flip()
                                #pygame.time.delay(5000)
                                
                                if result:
                                    self.game.board.extra_move = True
                                    self.game.board.move_count = 0
                                else:
                                    self.game.board.current_turn = 'black' if self.game.board.current_turn == 'white' else 'white'
                                return



        clicked_row = (mouse_pos[1] - self.renderer.start_y) // self.renderer.SQUARE_SIZE
        clicked_col = (mouse_pos[0] - self.renderer.start_x) // self.renderer.SQUARE_SIZE

        if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
            if self.game.selected_piece:
                clicked_piece = self.game.board.squares[clicked_row][clicked_col]
                if clicked_piece and clicked_piece.color == self.game.board.current_turn:
                    self.game.select_piece(clicked_row, clicked_col)  
                    return
                if self.game.make_move(self.game.selected_piece.position, (clicked_row, clicked_col)):
                    winner = self.game.board.is_checkmate()
                    self.renderer.check_played = False
                    if winner:
                        self.renderer.game_state = "victory"
                        self.renderer.show_victory_screen(f"{winner} (Checkmate)")
            else:
                self.game.select_piece(clicked_row, clicked_col)

    def handle_mouse_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_row = (mouse_pos[1] - self.renderer.start_y) // self.renderer.SQUARE_SIZE
        hover_col = (mouse_pos[0] - self.renderer.start_x) // self.renderer.SQUARE_SIZE

        if 0 <= hover_row < 8 and 0 <= hover_col < 8:
            self.game.hover_moves = self.game.get_hover_moves(hover_row, hover_col)
        else:
            self.game.hover_moves = []

    def reset(self):
        self.renderer.game_state = "playing"




