import pygame
import sys

class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height

        # Màu sắc
        self.BACKGROUND_COLOR = (30, 30, 60)
        self.BUTTON_COLOR = (70, 70, 70)
        self.BUTTON_HOVER_COLOR = (100, 100, 150)
        self.TEXT_COLOR = (255, 255, 255)
        self.SHADOW_COLOR = (40, 40, 40)

        # Phông chữ
        self.font_title = pygame.font.Font(None, 64)
        self.font_button = pygame.font.Font(None, 36)

        # Danh sách nút
        self.buttons = ["Play", "Setting", "About", "Exit"]
        self.button_width, self.button_height = 200, 50
        self.button_positions = [
            (self.SCREEN_WIDTH // 2 - self.button_width // 2, 150),
            (self.SCREEN_WIDTH // 2 - self.button_width // 2, 220),
            (self.SCREEN_WIDTH // 2 - self.button_width // 2, 290),
            (self.SCREEN_WIDTH // 2 - self.button_width // 2, 360)  # Vị trí nút About
        ]

        # Âm thanh
        pygame.mixer.init()
        self.hover_sound = pygame.mixer.Sound("./assets/hover.mp3")
        self.last_hovered = -1

        # Tải ảnh nền
        try:
            self.background = pygame.image.load("./assets/bg.png")
            self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except FileNotFoundError:
            self.background = None
            print("Warning: Background image not found.")

    def draw_button(self, text, x, y, width, height, active=False):
        """Vẽ nút với hiệu ứng 3D."""
        shadow_offset = 5 if not active else 2
        shadow_rect = (x + shadow_offset, y + shadow_offset, width, height)

        # Vẽ bóng
        pygame.draw.rect(self.screen, self.SHADOW_COLOR, shadow_rect, border_radius=8)

        # Nút chính
        color = self.BUTTON_HOVER_COLOR if active else self.BUTTON_COLOR
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=8)

        # Văn bản
        text_surface = self.font_button.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)


    def run(self):
        """Hàm hiển thị menu chính."""
        running = True
        selected_index = -1

        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(self.BACKGROUND_COLOR)

            title_surface = self.font_title.render("CHESS GAME", True, self.TEXT_COLOR)
            title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 80))
            self.screen.blit(title_surface, title_rect)

            mouse_pos = pygame.mouse.get_pos()

            # Xác định nút nào đang được hover
            for i, position in enumerate(self.button_positions):
                button_rect = pygame.Rect(position[0], position[1], self.button_width, self.button_height)
                if button_rect.collidepoint(mouse_pos):
                    if selected_index != i:
                        pygame.mixer.Sound.play(self.hover_sound)
                    selected_index = i
                    break
            else:
                selected_index = -1

            # Vẽ các nút
            for i, position in enumerate(self.button_positions):
                self.draw_button(self.buttons[i], *position, self.button_width, self.button_height, active=(i == selected_index))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if selected_index == 0:  # Play
                        return "start"
                    elif selected_index == 1:  # Setting
                        from setting import Setting
                        setting = Setting(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                        settings_data = setting.run()
                        print(settings_data)
                        
                    elif selected_index == 2:  # About
                        from about import About
                        about = About(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                        about.run()  # Gọi trang About

                    elif selected_index == 3:  # Exit
                        pygame.quit()
                        sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(self.buttons)
                    elif event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:
                            return "start"
                        elif selected_index == 1:
                            from setting import Setting
                            setting = Setting(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                            settings_data = setting.run()
                            print(settings_data)

                        elif selected_index == 2:  # About
                            from about import About
                            about = About(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                            about.run()  # Gọi trang About

                        elif selected_index == 3:
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
