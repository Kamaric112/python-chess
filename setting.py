import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import os


class Setting:
    def __init__(self, screen, width, height, config):
        self.config = config

        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height

        # Màu sắc
        self.BACKGROUND_COLOR = (60, 25, 60)
        self.TEXT_COLOR = (255, 255, 255)
        self.INPUT_COLOR = (70, 70, 70)
        self.BUTTON_COLOR = (100, 100, 150)
        self.HOVER_BUTTON_COLOR = (120, 120, 170)
        self.ACTIVE_BUTTON_COLOR = (150, 150, 200)

        self.font = pygame.font.Font(None, 36)

        self.inputs = {
            "player_a": {"label": "Player A:", "value": config.playerA, "pos": (100, 100),
                         "image": config.playerA_image if hasattr(config, 'playerA_image') else os.path.join('assets',
                                                                                                             'black-bishop.png')},
            "player_b": {"label": "Player B:", "value": config.playerB, "pos": (100, 160),
                         "image": config.playerB_image if hasattr(config, 'playerB_image') else os.path.join('assets',
                                                                                                             'white-bishop.png')},
            "time": {"label": "Time (min):", "value": str(config.time), "pos": (100, 220)}
        }

        self.music_options = ["Mute", "Music 1", "Music 2", "Music 3"]
        self.selected_music = 0
        self.music_files = ["", "./assets/loop1.mp3", "./assets/loop2.mp3", "./assets/loop3.mp3"]
        self.is_music_playing = False

        self.save_button = pygame.Rect(200, 350, 200, 50)
        self.active_input = None
        self.image_rects = {}

    def draw_text(self, text, pos, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, pos)

    def draw_button(self, rect, text, is_hovered=False, is_active=False):
        color = self.ACTIVE_BUTTON_COLOR if is_active else (
            self.HOVER_BUTTON_COLOR if is_hovered else self.BUTTON_COLOR)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        self.draw_text(text, (rect.x + 20, rect.y + 10), self.TEXT_COLOR)

    def draw_image(self, image_path, pos):
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (30, 30))
            image_rect = image.get_rect(topleft=pos)
            self.screen.blit(image, image_rect)
            return image_rect
        except pygame.error as e:
            print(f"Error loading image: {image_path} - {e}")
            return None

    def run(self):
        running = True

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)

            for key, field in self.inputs.items():
                self.draw_text(field["label"], field["pos"], self.TEXT_COLOR)

                input_rect = pygame.Rect(field["pos"][0] + 200, field["pos"][1], 200, 30)
                pygame.draw.rect(self.screen, self.INPUT_COLOR, input_rect)
                text_surface = self.font.render(field["value"], True, self.TEXT_COLOR)
                self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                if self.active_input == key:
                    pygame.draw.rect(self.screen, self.BUTTON_COLOR, input_rect, 2)

                if key in ["player_a", "player_b"]:
                    image_pos = (input_rect.right + 10, field["pos"][1])
                    image_rect = self.draw_image(field["image"], image_pos)
                    if image_rect:
                        self.image_rects[key] = image_rect

            button_width = 120
            spacing = 20
            total_width = len(self.music_options) * button_width + (len(self.music_options) - 1) * spacing
            start_x = (self.SCREEN_WIDTH - total_width) // 2

            for i, option in enumerate(self.music_options):
                music_rect = pygame.Rect(start_x + i * (button_width + spacing), 270, button_width, 50)
                is_hovered = music_rect.collidepoint(pygame.mouse.get_pos())
                is_active = i == self.selected_music
                self.draw_button(music_rect, option, is_hovered, is_active)
                if is_hovered and pygame.mouse.get_pressed()[0]:
                    self.selected_music = i
                    self.play_music(self.music_files[self.selected_music])

            is_hovered = self.save_button.collidepoint(pygame.mouse.get_pos())
            self.draw_button(self.save_button, "Save & Return", is_hovered)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.collidepoint(event.pos):
                        self.config.time = int(self.inputs["time"]["value"])  # Chuyển đổi thành số nguyên
                        self.config.playerA = self.inputs["player_a"]["value"]
                        self.config.playerB = self.inputs["player_b"]["value"]
                        self.config.playerA_image = self.inputs["player_a"]["image"]
                        self.config.playerB_image = self.inputs["player_b"]["image"]

                        print("JSON return:")
                        return {"player_a": self.inputs["player_a"]["value"],
                                "player_b": self.inputs["player_b"]["value"],
                                "time": int(self.inputs["time"]["value"]),
                                "player_a_image": self.inputs["player_a"]["image"],
                                "player_b_image": self.inputs["player_b"]["image"]}

                    # Kiểm tra xem người dùng có click vào ô nhập liệu hay không
                    for key, field in self.inputs.items():
                        input_rect = pygame.Rect(field["pos"][0] + 200, field["pos"][1], 200, 30)
                        if input_rect.collidepoint(event.pos):
                            self.active_input = key
                            break
                    else:
                        self.active_input = None  # Nếu không click vào ô nào thì bỏ active

                    # Handle image clicks
                    for key, rect in self.image_rects.items():
                        if rect and rect.collidepoint(event.pos):
                            self.change_image(key)
                            break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if not self.active_input:
                            self.active_input = list(self.inputs.keys())[0]
                        else:
                            input_keys = list(self.inputs.keys())
                            current_index = input_keys.index(self.active_input)
                            next_index = (current_index + 1) % len(input_keys)
                            self.active_input = input_keys[next_index]
                    elif self.active_input:
                        # Handle Backspace
                        if event.key == pygame.K_BACKSPACE:
                            current_value = self.inputs[self.active_input]["value"]
                            # Remove the last character if there's any input
                            if len(current_value) > 0:
                                self.inputs[self.active_input]["value"] = current_value[:-1]

                        # Append new characters
                        elif self.active_input == "time" and event.unicode.isdigit():
                            self.inputs[self.active_input]["value"] += event.unicode
                        elif self.active_input != "time" and len(self.inputs[self.active_input]["value"]) < 20:
                            self.inputs[self.active_input]["value"] += event.unicode
                        # Handle Tab key to switch between input fields

            # Cập nhật màn hình
            pygame.display.flip()

    def play_music(self, music_file):
        """Chạy nhạc nền, nếu có lỗi sẽ bỏ qua."""
        if self.is_music_playing and music_file == "":
            pygame.mixer.music.stop()
            self.is_music_playing = False
        elif music_file and not self.is_music_playing:
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)  # Phát nhạc lặp lại vô hạn
                self.is_music_playing = True
            except pygame.error:
                print("Error loading music file. Skipping music.")
        elif music_file and self.is_music_playing:
            pygame.mixer.music.stop()  # Dừng nhạc hiện tại
            pygame.mixer.music.load(music_file)  # Tải nhạc mới
            pygame.mixer.music.play(-1)  # Phát nhạc mới

    def change_image(self, player_key):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.inputs[player_key]["image"] = file_path