import pygame

from menu import init_menu

pygame.init()
res=(720,720)
screen=pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()

if __name__ == "__main__":
    while True:
        action = init_menu(screen, width, height)