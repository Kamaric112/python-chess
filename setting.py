import pygame
import sys
import logging


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
        self.HOVER_BUTTON_COLOR = (120, 120, 170)  # Màu khi di chuột qua
        self.ACTIVE_BUTTON_COLOR = (150, 150, 200)  # Màu khi nút đang được chọn

        # Phông chữ
        self.font = pygame.font.Font(None, 36)

        # Các trường nhập liệu
        self.inputs = {
            "player_a": {"label": "Player A:", "value": "", "pos": (100, 100)},
            "player_b": {"label": "Player B:", "value": "", "pos": (100, 160)},
            "time": {"label": "Time (min):", "value": "10", "pos": (100, 220)}
        }

        
        # Nhạc nền
        self.music_options = ["Mute", "Music 1", "Music 2", "Music 3"]
        self.selected_music = 0  # Mặc định chọn Mute
        self.music_files = ["", "./assets/loop1.mp3", "./assets/loop2.mp3", "./assets/loop3.mp3"]
        self.is_music_playing = False  # Biến kiểm tra xem nhạc có đang phát không


        # Nút Save và Return
        self.save_button = pygame.Rect(200, 350, 200, 50)

        # Trạng thái hiện tại
        self.active_input = None

    def draw_text(self, text, pos, color):
        """Vẽ text lên màn hình."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, pos)

    def draw_button(self, rect, text, is_hovered=False, is_active=False):
        """Vẽ nút với hiệu ứng khi di chuột qua và khi nút được chọn."""
        color = self.ACTIVE_BUTTON_COLOR if is_active else (self.HOVER_BUTTON_COLOR if is_hovered else self.BUTTON_COLOR)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        self.draw_text(text, (rect.x + 20, rect.y + 10), self.TEXT_COLOR)

    def run(self):
        """Hàm hiển thị giao diện Setting."""
        running = True

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)

            # Hiển thị các trường nhập liệu
            for key, field in self.inputs.items():
                # Label
                self.draw_text(field["label"], field["pos"], self.TEXT_COLOR)

                # Input box
                input_rect = pygame.Rect(field["pos"][0] + 200, field["pos"][1], 200, 30)
                pygame.draw.rect(self.screen, self.INPUT_COLOR, input_rect)
                text_surface = self.font.render(field["value"], True, self.TEXT_COLOR)
                self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                # Đánh dấu ô đang active
                if self.active_input == key:
                    pygame.draw.rect(self.screen, self.BUTTON_COLOR, input_rect, 2)

            # Hiển thị lựa chọn nhạc nền với các nút 3D
            # self.draw_text("Music:", (100, 280), self.TEXT_COLOR)
            button_width = 120
            spacing = 20
            total_width = len(self.music_options) * button_width + (len(self.music_options) - 1) * spacing
            start_x = (self.SCREEN_WIDTH - total_width) // 2  # Căn giữa các nút

            for i, option in enumerate(self.music_options):
                music_rect = pygame.Rect(start_x + i * (button_width + spacing), 270, button_width, 50)
                is_hovered = music_rect.collidepoint(pygame.mouse.get_pos())
                is_active = i == self.selected_music
                self.draw_button(music_rect, option, is_hovered, is_active)
                if is_hovered and pygame.mouse.get_pressed()[0]:
                    self.selected_music = i
                    self.play_music(self.music_files[self.selected_music])

 

            # Hiển thị nút "Save and Return" với hiệu ứng 3D
            is_hovered = self.save_button.collidepoint(pygame.mouse.get_pos())
            self.draw_button(self.save_button, "Save & Return", is_hovered)

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.collidepoint(event.pos):
                        # Lưu dữ liệu và thoát Setting
                        self.config.time = int(self.inputs["time"]["value"])  # Chuyển đổi thành số nguyên
                        #self.config.playerA = self.inputs["player_a"]["value"] if self.inputs["player_a"]["value"].strip() else 'Player A'
                        #self.config.playerB = self.inputs["player_b"]["value"] if self.inputs["player_b"]["value"].strip() else 'Player B'
                        self.config.playerA = (
                            self.inputs["player_a"]["value"] if self.inputs["player_a"]["value"].strip() else 'Player Blk'
                        )
                        self.config.playerB = (
                            self.inputs["player_b"]["value"] if self.inputs["player_b"]["value"].strip() else 'Player Wht'
                        )
                        print("JSON return:")
                        logging.info(f"Settings updated - player_a: {self.config.playerA}, player_b: {self.config.playerB}, time: {self.config.time}")


                        # return {"player_a": self.inputs["player_a"]["value"],
                        #         "player_b": self.inputs["player_b"]["value"],
                        #         "time": int(self.inputs["time"]["value"])} 

                        return {"player_a": self.config.playerA,
                                "player_b": self.config.playerB,
                                "time": int(self.inputs["time"]["value"])} 

                    # Kiểm tra xem người dùng có click vào ô nhập liệu hay không
                    for key, field in self.inputs.items():
                        input_rect = pygame.Rect(field["pos"][0] + 200, field["pos"][1], 200, 30)
                        if input_rect.collidepoint(event.pos):
                            self.active_input = key
                            break
                    else:
                        self.active_input = None  # Nếu không click vào ô nào thì bỏ active

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
