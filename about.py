import pygame
import sys


class About:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height
        self.BACKGROUND_COLOR = (60, 25, 60)

        self.TEXT_COLOR = (255, 255, 255)
        try:
            self.font_title = pygame.font.Font("./assets/Roboto/Roboto-Regular.ttf", 62)
            self.font_body = pygame.font.Font("./assets/Roboto/Roboto-Regular.ttf", 25)
        except FileNotFoundError:
            print("Phông chữ không tìm thấy! Hãy kiểm tra đường dẫn.")
            sys.exit()

        self.about_text = [
            "Đồ Án Python - Nhóm 20",
            "------",
            "Nguyễn Quang Trường (nhóm trưởng) - 23210303",
            "Nguyễn Ngọc Thành - 23210278",
            "Trần Quang Kiên - 23210232",
            "Nguyễn Hữu Nhật - 23210258",
            "Võ Thành Đạt - 23210206",
            "Phạm Phan Phương - 23210266",

        ]

        self.quit_button_pos = (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT - 100)

    def draw_text(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, x, y, width, height, active=False):
        color = (255, 99, 71) if active else (200, 60, 60)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
        text_surface = self.font_body.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_text(self.about_text[0], self.SCREEN_WIDTH // 2, 100, self.font_title, self.TEXT_COLOR)
            y_offset = 200
            for line in self.about_text[1:]:
                self.draw_text(line, self.SCREEN_WIDTH // 2, y_offset, self.font_body, self.TEXT_COLOR)
                y_offset += 50

            mouse_pos = pygame.mouse.get_pos()
            quit_button_rect = pygame.Rect(self.quit_button_pos[0], self.quit_button_pos[1], 300, 60)

            if quit_button_rect.collidepoint(mouse_pos):
                self.draw_button("Back to Menu", *self.quit_button_pos, 300, 60, active=True)
            else:
                self.draw_button("Back to Menu", *self.quit_button_pos, 300, 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if quit_button_rect.collidepoint(mouse_pos):
                        running = False

            pygame.display.flip()