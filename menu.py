import pygame
import sys

from chess import init_chess


def init_menu(screen, width, height):
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    smallfont = pygame.font.SysFont('Corbel', 35)
    titlefont = pygame.font.SysFont('Corbel',60)

    # Text renders
    title_text = titlefont.render('CHESS GAME', True, color)
    start_text = smallfont.render('start', True, color)
    quit_text = smallfont.render('quit', True, color)

    # Button rectangles
    start_button = pygame.Rect(width / 2 - 60, height / 2 - 20, 120, 40)
    quit_button = pygame.Rect(width / 2 - 60, height / 2 + 50, 120, 40)
    while True:
        screen.fill((60, 25, 60))  # Dark purple background
        mouse = pygame.mouse.get_pos()
        # draw title text
        title_rect = title_text.get_rect(center=(width / 2, height / 3))
        screen.blit(title_text, title_rect)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse):
                    init_chess(screen, width, height)
                if quit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        # Start button hover effect
        if start_button.collidepoint(mouse):
            pygame.draw.rect(screen, color_light, start_button)
        else:
            pygame.draw.rect(screen, color_dark, start_button)

        # Quit button hover effect
        if quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, color_light, quit_button)
        else:
            pygame.draw.rect(screen, color_dark, quit_button)

        # Superimpose text on buttons
        screen.blit(start_text, (start_button.x + 20, start_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 30, quit_button.y + 5))

        pygame.display.update()
