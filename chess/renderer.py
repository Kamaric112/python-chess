import pygame
import os
import random
from pieces.piece import Piece,King
import math
import logging
import secrets

logging.basicConfig(
    filename='log/chess_game_event.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ChessRenderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.WHITE = (255, 255, 255)
        self.BLACK = (128, 128, 128)
        self.HIGHLIGHT_COLOR = (124, 252, 0)
        self.RED = (255, 0, 0)
        # Adjust board size to leave space for users
        self.SQUARE_SIZE = min(width, height - 200) // 8  # Reduced to leave space
        self.start_x = (width - self.SQUARE_SIZE * 8) // 2
        # Adjust start_y to center the board between users
        self.start_y = 100 + (height - 200 - self.SQUARE_SIZE * 8) // 2
        self.pieces_images = self.load_pieces()
        self.font = pygame.font.Font(None, 36)
        self.game_state = "playing"
        self.back_button_color = (34, 139, 34)
        self.back_button_rect = pygame.Rect(5, 300, 90, 40)
        self.rewind_button_color = (34, 139, 34)
        self.rewind_button_rect = pygame.Rect(5, 350, 90, 40)

        self.sparkle_timer = 0
        self.sparkle_positions = []
        pygame.mixer.init() 
        self.check_sound = pygame.mixer.Sound(os.path.join('assets', 'alert.mp3'))
        self.check_played = False  # Track if sound has been played
        #self.check_sound = pygame.mixer.Sound('assets/alert.mp3')
        self.sparkle_colors = [(255,215,0), (255,255,0), (255,223,0)]  # Gold colors for sparkling

        #Bomb button
        self.bomb_button_color = (139, 0, 0)  # Dark red
        self.bomb_button_rect = pygame.Rect(5, 400, 90, 40)
        self.bomb_image = pygame.image.load(os.path.join('assets', 'bomb.png'))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
        self.bomb_sound = pygame.mixer.Sound(os.path.join('assets', 'bomb.mp3'))
        self.bomb_effect_start = 0
        self.bomb_position = None
        self.flash_interval = 100  

        #RPS game
        self.rps_button_color = (70, 130, 180)  # Steel blue
        self.rps_button_rect = pygame.Rect(5, 450, 90, 40)
        self.rps_images = {
        'rock': pygame.image.load(os.path.join('assets', 'rock.jpeg')),
        'paper': pygame.image.load(os.path.join('assets', 'paper.jpeg')),
        'scissor': pygame.image.load(os.path.join('assets', 'scissor.jpeg'))
        }
        for key in self.rps_images:
            self.rps_images[key] = pygame.transform.scale(self.rps_images[key], (80, 80))

        self.player_rps_choice = None
        self.computer_rps_choice = None
        self.rps_bottom = True
        self.rps_result_text = None

        # Add rectangles for user profiles
        #self.user_a_profile_rect = pygame.Rect(0, 0, 100, 100)
        #self.user_b_profile_rect = pygame.Rect(width-110, 10, 100, 100)
        self.user_a_name_rect = pygame.Rect(120, 30, 200, 40)  # Added clickable name box
        self.user_b_name_rect = pygame.Rect(120, self.height - 70, 200, 40)  # Added clickable name box

        #wheel of forfune game
        self.promotion_options = ['queen', 'rook', 'knight', 'bishop']
        self.wheel_active = False
        self.wheel_spinning = False
        self.wheel_angle = 0
        self.wheel_speed = 0
        self.wheel_result = None
 
        pygame.font.init()

    def draw_users(self, user_a, user_b):
        # Draw background rectangles for user sections
        user_background = (139, 69, 19)  # Saddle brown color
        top_rect = pygame.Rect(0, 0, self.width, 100)
        bottom_rect = pygame.Rect(0, self.height - 100, self.width, 100)
        pygame.draw.rect(self.screen, user_background, top_rect)
        pygame.draw.rect(self.screen, user_background, bottom_rect)

        # Create clickable areas for users
        self.user_a_profile_rect = pygame.Rect(2, 2, 80, 80)
        self.user_b_profile_rect = pygame.Rect(2, self.height - 90, 80, 80)

        # Draw User A at the top with clickable area
        pygame.draw.rect(self.screen, (100, 50, 10), self.user_a_profile_rect)  
        # Darker brown for clickable area
        if user_a.image:
            user_a_image = pygame.image.load(user_a.image)
            user_a_image = pygame.transform.scale(user_a_image,
                                                  (self.user_a_profile_rect.width, self.user_a_profile_rect.height))
            self.screen.blit(user_a_image, self.user_a_profile_rect)

        # Draw User A name box with border
        pygame.draw.rect(self.screen, (100, 50, 10), self.user_a_name_rect)
        pygame.draw.rect(self.screen, (150, 75, 15), self.user_a_name_rect, 2)  # Border
        user_a_text = self.font.render(user_a.name, True, self.WHITE)
        text_rect = user_a_text.get_rect(center=self.user_a_name_rect.center)
        self.screen.blit(user_a_text, text_rect)

        # Draw User B at the bottom with clickable area
        pygame.draw.rect(self.screen, (100, 50, 10), self.user_b_profile_rect)  # Darker brown for clickable area
        if user_b.image:
            user_b_image = pygame.image.load(user_b.image)
            user_b_image = pygame.transform.scale(user_b_image,
                                                  (self.user_b_profile_rect.width, self.user_b_profile_rect.height))
            self.screen.blit(user_b_image, self.user_b_profile_rect)

        # Draw User B name box with border
        pygame.draw.rect(self.screen, (100, 50, 10), self.user_b_name_rect)
        pygame.draw.rect(self.screen, (150, 75, 15), self.user_b_name_rect, 2)  
        # Border
        user_b_text = self.font.render(user_b.name, True, self.WHITE)
        text_rect = user_b_text.get_rect(center=self.user_b_name_rect.center)
        self.screen.blit(user_b_text, text_rect)

    def draw_timers(self, timer_a, timer_b):
        # Draw timer for User A
        minutes_a = int(timer_a // 60)
        seconds_a = int(timer_a % 60)
        timer_text_a = f"{minutes_a:02d}:{seconds_a:02d}"
        timer_surface_a = self.font.render(timer_text_a, True, self.WHITE)
        self.screen.blit(timer_surface_a, (self.width - 150, 40))

        # Draw timer for User B
        minutes_b = int(timer_b // 60)
        seconds_b = int(timer_b % 60)
        timer_text_b = f"{minutes_b:02d}:{seconds_b:02d}"
        timer_surface_b = self.font.render(timer_text_b, True, self.WHITE)
        self.screen.blit(timer_surface_b, (self.width - 150, self.height - 60))

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

    def draw_board(self, game, user_a, user_b):
        if self.game_state == "playing":
            self.screen.fill((60, 25, 60))
            self.draw_squares(game)
            self.draw_users(user_a, user_b)
            self.draw_turn_indicator(game.board.current_turn)
            self.draw_back_button()
            self.draw_rewind_button()
            self.draw_bomb_button()
            self.draw_bomb_effect(game)
            self.draw_rps_button()
            #self.show_rps_result(game)  # Add this line

             # Draw RPS results if choices exist
            if self.player_rps_choice and self.computer_rps_choice:
                player_x = self.width - 80
                player_y = self.height - 80 if self.rps_bottom else 0
                computer_x = self.width - 80
                computer_y = 0 if self.rps_bottom else self.height - 80
                
                self.screen.blit(self.rps_images[self.player_rps_choice], (player_x, player_y))
                self.screen.blit(self.rps_images[self.computer_rps_choice], (computer_x, computer_y))

            self.draw_timers(game.timer_a, game.timer_b)
            
            if self.rps_result_text:
                winner, action = self.rps_result_text.split(" ")
                winner_surface = self.font.render(winner, True, self.WHITE)
                action_surface = self.font.render(action, True, self.WHITE)
                
                winner_rect = winner_surface.get_rect(center=(660, 315))
                action_rect = action_surface.get_rect(center=(660, 345))
                
                self.screen.blit(winner_surface, winner_rect)
                self.screen.blit(action_surface, action_rect)

            if game.board.last_move and game.board.is_pawn_promotion(game.board.last_move):
                self.wheel_active = True
                #row, col = game.board.last_move
                end_pos = game.board.last_move
                row, col =end_pos
                #self.draw_wheel(game.board.squares[row][col].color)
                final_option = self.draw_wheel(game.board.squares[row][col].color)
                if final_option:
                    game.board.promote_pawn(end_pos, final_option)
            
            pygame.display.flip()

        elif self.game_state == "victory":
            winner = game.board.is_checkmate()
            self.show_victory_screen(f"{winner} Win")

    def draw_sparkle(self, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.sparkle_timer > 100:  # Update sparkles every 100ms
            self.sparkle_timer = current_time
            self.sparkle_positions = [(pos[0] + random.randint(-20,20), 
                                    pos[1] + random.randint(-20,20)) 
                                    for _ in range(5)]
        
        for pos in self.sparkle_positions:
            color = random.choice(self.sparkle_colors)
            pygame.draw.circle(self.screen, color, pos, random.randint(2,4))

    def draw_promoted_piece_sparkle(self, pos, start_time):
        current_time = pygame.time.get_ticks()
        if current_time - start_time < 5000:  # 5 seconds
            self.draw_sparkle(pos)
            return True
        return False

    def draw_red_warning(self, pos):
        """Draw a flashing red warning square at the specified position."""
        current_time = pygame.time.get_ticks()
        flash_period = 500  # Flash every 500ms
        
        # Calculate position
        x = pos[0] - self.SQUARE_SIZE//2
        y = pos[1] - self.SQUARE_SIZE//2
        
        # Create flashing effect by alternating visibility
        if (current_time // flash_period) % 2 == 0:
            warning_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
            warning_surface.set_alpha(128)  # Semi-transparent
            warning_surface.fill((255, 0, 0))  # Red color
            self.screen.blit(warning_surface, (x, y))


   

    def draw_squares(self, game):
        king_positions = {}  
        for row in range(8):
            for col in range(8):
                x = self.start_x + col * self.SQUARE_SIZE
                y = self.start_y + row * self.SQUARE_SIZE
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                piece = game.board.squares[row][col]
                if piece:
                    if isinstance(piece, King):
                        king_positions[piece.color] = (
                            x + self.SQUARE_SIZE//2,
                            y + self.SQUARE_SIZE//2
                        )

         # Second pass - draw pieces and effects
        for row in range(8):
            for col in range(8):
                x= self.start_x + col * self.SQUARE_SIZE
                y = self.start_y + row * self.SQUARE_SIZE

                # Draw valid moves for selected piece
                if (row, col) in game.valid_moves:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(128)
                    s.fill(self.HIGHLIGHT_COLOR)
                    self.screen.blit(s, (x, y))

                # Draw hover moves with different alpha
                if (row, col) in game.hover_moves:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(64)  # More transparent than selected highlights
                    s.fill(self.HIGHLIGHT_COLOR)
                    self.screen.blit(s, (x, y))

                piece = game.board.squares[row][col]
                if piece:
                    piece_name = f'{piece.color}_{piece.__class__.__name__.lower()}'
                    piece_image = self.pieces_images[piece_name]
                    self.screen.blit(piece_image, (x, y))

                    if hasattr(piece, 'needs_sparkle') and piece.needs_sparkle:
                        screen_pos = (x + self.SQUARE_SIZE//2, y + self.SQUARE_SIZE//2)
                        still_sparkling = self.draw_promoted_piece_sparkle(screen_pos, piece.promotion_time)
                        if not still_sparkling:
                            piece.needs_sparkle = False

        for color, pos in king_positions.items():
            if game.board.is_king_in_check(color):
                self.draw_red_warning(pos)
                if not self.check_played:  # Only play if not already playing
                    #pygame.mixer.stop() 
                    self.check_sound.play()
                    self.check_played = True
            #else:
                #pygame.mixer.stop()  # Stop sound when king is safe
                #self.check_played = False

           

    def draw_turn_indicator(self, current_turn):
        turn_text = f"{current_turn.capitalize()}'s Turn"
        text_surface = self.font.render(turn_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2 + 100, 50))

        box_rect = text_rect.copy()
        box_rect.inflate_ip(20 * 2, 20)
        pygame.draw.rect(self.screen, (34, 139, 34), box_rect, border_radius=10)
        self.screen.blit(text_surface, text_rect)

    
    def draw_back_button(self):
        pygame.draw.rect(self.screen, self.back_button_color, self.back_button_rect, border_radius=10)
        back_text = self.font.render("Back", True, self.WHITE)
        text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, text_rect)

    def draw_rewind_button(self):
        pygame.draw.rect(self.screen, self.rewind_button_color, self.rewind_button_rect,border_radius=10)
        rewind_text = self.font.render("Rewind", True, self.WHITE)
        text_rect = rewind_text.get_rect(center=self.rewind_button_rect.center)
        self.screen.blit(rewind_text, text_rect)
        # self.screen.blit(rewind_text, (self.rewind_button_rect.centerx - 10, 
        #                               self.rewind_button_rect.centery - 10))

    def draw_bomb_button(self):
        pygame.draw.rect(self.screen, self.bomb_button_color, self.bomb_button_rect, border_radius=10)
        bomb_text = self.font.render("Bomb", True, self.WHITE)
        text_rect = bomb_text.get_rect(center=self.bomb_button_rect.center)
        self.screen.blit(bomb_text, text_rect)

    def draw_bomb_effect(self, game):
        if self.bomb_position:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.bomb_effect_start

            if elapsed < 6000: 
                if (elapsed // self.flash_interval) % 2 == 0:
                    x = self.start_x + self.bomb_position[1] * self.SQUARE_SIZE
                    y = self.start_y + self.bomb_position[0] * self.SQUARE_SIZE
                    self.screen.blit(self.bomb_image, (x, y))
            else:
                self.bomb_position = None

    def draw_rps_button(self):
        pygame.draw.rect(self.screen, self.rps_button_color, self.rps_button_rect, border_radius=10)
        rps_text = self.font.render("RPS", True, self.WHITE)
        text_rect = rps_text.get_rect(center=self.rps_button_rect.center)
        self.screen.blit(rps_text, text_rect)

    def draw_input_box(self, text):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.width // 4, self.height // 3, self.width // 2, 100))
        text_surface = self.font.render(text, True, self.WHITE)
        self.screen.blit(text_surface, (self.width // 4 + 10, self.height // 3 + 40))
        pygame.display.flip()

    def show_rps_selection(self):
        choices = ['rock', 'paper', 'scissor']
        spacing = 120
        start_x = (self.width - spacing * 3) // 2
        start_y = self.height // 2 - 50
        
        rects = []
        for i, choice in enumerate(choices):
            x = start_x + i * spacing
            rect = pygame.Rect(x, start_y, 100, 100)
            rects.append((rect, choice))
            self.screen.blit(self.rps_images[choice], rect)
        
        pygame.display.flip()
        return rects
    
    def show_rps_result(self, player_choice, computer_choice, bottom=True):
        self.player_rps_choice = player_choice
        self.computer_rps_choice = computer_choice
        self.rps_bottom = bottom
            
    def draw_wheel(self, color):
        if not self.wheel_active:
            return

        if not self.wheel_spinning:
            self.wheel_spinning = True
            self.wheel_speed = secrets.randbelow(15 - 8 + 1) + 8
        
        slice_angle = 360 / len(self.promotion_options)
        initial_offset = slice_angle / 2

        while self.wheel_speed >= 0.1:
            self.wheel_angle += self.wheel_speed
            self.wheel_speed *= 0.98  # Gradually slow down

            # Clear the screen
            #self.screen.fill((0, 0, 0))

            center_x = self.width // 2
            center_y = self.height // 2
            radius = 150
            #slice_angle = 360 / len(self.promotion_options)

            # Draw the wheel border
            circle_color = self.BLACK if color == 'white' else self.WHITE
            circle_color_opposite = self.BLACK if color == 'black' else self.WHITE
            self.screen.fill(circle_color)
            #logging.info("circle_color: %s", circle_color)
            pygame.draw.circle(self.screen, circle_color_opposite, (center_x, center_y), radius, 3)

            # Draw dividing lines between options
            for i in range(len(self.promotion_options)):
                #angle = math.radians(i * slice_angle + self.wheel_angle)
                start_angle = math.radians(i * slice_angle + self.wheel_angle)
                #end_angle = math.radians((i + 1) * slice_angle + self.wheel_angle)
                start_x = center_x + radius * math.cos(start_angle)
                start_y = center_y + radius * math.sin(start_angle)
                pygame.draw.line(self.screen, circle_color_opposite,
                                (center_x, center_y), (start_x, start_y), 2)

            # Draw pieces on the wheel
            for i, option in enumerate(self.promotion_options):
                mid_angle = math.radians((i * slice_angle + slice_angle / 2) + self.wheel_angle)
                x = center_x + (radius * 0.7) * math.cos(mid_angle)  # Position closer to the center
                y = center_y + (radius * 0.7) * math.sin(mid_angle)

                piece_img = self.pieces_images[f'{color}_{option}']
                piece_rect = piece_img.get_rect(center=(x, y))
                self.screen.blit(piece_img, piece_rect)

            # Draw inward-facing needle
            pygame.draw.polygon(self.screen, (255, 0, 0),
                                [(center_x, center_y + radius -10),  # Needle tip inside circle
                                (center_x - 10, center_y + radius + 20), 
                                (center_x + 10, center_y + radius + 20)])

            pygame.display.flip()
            pygame.time.delay(50)

        # Determine final option
        if self.wheel_speed < 0.1:
            

            normalized_angle = (-self.wheel_angle+ initial_offset) % 360  # Adjust angle for clockwise rotation
            #slice_angle = 360 / len(self.promotion_options)
            selected_index = round(normalized_angle / slice_angle) % len(self.promotion_options)
            final_option = self.promotion_options[selected_index]
            logging.info(f"Selected option: {final_option}")
            self.wheel_spinning = False
            self.wheel_active = False
            return final_option

        return None

    def show_victory_screen(self, winner):
        if not winner:
            return

        victory_font = pygame.font.Font(None, 74)
        text = f"{winner}"

        self.screen.fill((60, 25, 60))
        text_surface = victory_font.render(text, True, (255, 215, 0))
        continue_text = self.font.render("Press ENTER to return to menu", True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 100))

        self.screen.blit(text_surface, text_rect)
        self.screen.blit(continue_text, continue_rect)
        pygame.display.flip()

    def reset(self):
        self.game_state = "playing"
        # Clear any temporary drawing surfaces if needed
        self.screen.fill((60, 25, 60))
