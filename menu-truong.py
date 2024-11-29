import pygame
import sys


class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.titlefont = pygame.font.SysFont('Corbel', 60)

        # Text renders
        self.title_text = self.titlefont.render('CHESS GAME', True, self.color)
        self.start_text = self.smallfont.render('start', True, self.color)
        self.quit_text = self.smallfont.render('quit', True, self.color)

        # Button rectangles
        self.start_button = pygame.Rect(width / 2 - 60, height / 2 - 20, 120, 40)
        self.quit_button = pygame.Rect(width / 2 - 60, height / 2 + 50, 120, 40)

    def run(self):
        while True:
            self.screen.fill((60, 25, 60))  # Dark purple background
            mouse = pygame.mouse.get_pos()

            # draw title text
            title_rect = self.title_text.get_rect(center=(self.width / 2, self.height / 3))
            self.screen.blit(self.title_text, title_rect)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(mouse):
                        return "start"
                    if self.quit_button.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

            # Button hover effects
            self._handle_button_hover(mouse)

            pygame.display.update()

    def _handle_button_hover(self, mouse):
        # Start button hover effect
        if self.start_button.collidepoint(mouse):
            pygame.draw.rect(self.screen, self.color_light, self.start_button)
        else:
            pygame.draw.rect(self.screen, self.color_dark, self.start_button)

        # Quit button hover effect
        if self.quit_button.collidepoint(mouse):
            pygame.draw.rect(self.screen, self.color_light, self.quit_button)
        else:
            pygame.draw.rect(self.screen, self.color_dark, self.quit_button)

        # Superimpose text on buttons
        self.screen.blit(self.start_text, (self.start_button.x + 20, self.start_button.y + 5))
        self.screen.blit(self.quit_text, (self.quit_button.x + 30, self.quit_button.y + 5))
