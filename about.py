import pygame
import sys

class About:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height

        # Màu nền và chữ hài hòa với board.py
        self.BACKGROUND_COLOR = (60, 25, 60)  # Màu nền xám đậm
       

        self.TEXT_COLOR = (255, 255, 255)  # Màu chữ trắng

        # Phông chữ tùy chỉnh (cần thay đường dẫn tới phông chữ thực tế)
        try:
            self.font_title = pygame.font.Font("./assets/Roboto/Roboto-Regular.ttf", 62)
            self.font_body = pygame.font.Font("./assets/Roboto/Roboto-Regular.ttf", 25)
        except FileNotFoundError:
            print("Phông chữ không tìm thấy! Hãy kiểm tra đường dẫn.")
            sys.exit()

        # Dữ liệu về đội ngũ phát triển
        self.about_text = [
            "Đồ Án Python - Nhóm 20",
            "------",
            "Nguyễn Quang Trường (nhóm trưởng)",
            "Nguyễn Ngọc Thành",
            "Trần Quang Kiên",
            "Nguyễn Hữu Nhật",
            "Võ Thành Đạt",
            "Phạm Phan Phương",
           
        ]

        # Nút thoát với màu sắc hài hòa
        self.quit_button_pos = (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT - 100)

    def draw_text(self, text, x, y, font, color):
        """Vẽ chữ lên màn hình."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, x, y, width, height, active=False):
        """Vẽ nút thoát."""
        color = (255, 99, 71) if active else (200, 60, 60)  # Màu đỏ sáng cho nút
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=8)

        # Vẽ chữ trên nút
        text_surface = self.font_body.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        """Hiển thị trang About."""
        running = True
        while running:
            self.screen.fill(self.BACKGROUND_COLOR)

            # Tiêu đề
            self.draw_text(self.about_text[0], self.SCREEN_WIDTH // 2, 100, self.font_title, self.TEXT_COLOR)

            # In thông tin về đội ngũ phát triển, xuống từng dòng
            y_offset = 200  # Vị trí bắt đầu in các dòng thông tin
            for line in self.about_text[1:]:
                self.draw_text(line, self.SCREEN_WIDTH // 2, y_offset, self.font_body, self.TEXT_COLOR)
                y_offset += 50  # Tăng khoảng cách giữa các dòng, có thể điều chỉnh giá trị này để tăng giảm khoảng cách

            # Vẽ nút thoát
            mouse_pos = pygame.mouse.get_pos()
            quit_button_rect = pygame.Rect(self.quit_button_pos[0], self.quit_button_pos[1], 300, 60)

            if quit_button_rect.collidepoint(mouse_pos):  # Khi chuột hover qua nút
                self.draw_button("Back to Menu", *self.quit_button_pos, 300, 60, active=True)
            else:
                self.draw_button("Back to Menu", *self.quit_button_pos, 300, 60)

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Chuột trái
                    if quit_button_rect.collidepoint(mouse_pos):  # Nhấn vào nút thoát
                        running = False  # Quay lại menu

            # Cập nhật màn hình
            pygame.display.flip()
