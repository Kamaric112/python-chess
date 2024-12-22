import pygame

from chess.chess_board import ChessBoard
from menu import Menu

from config import Config  #Phuong: Import Config


pygame.init()
pygame.display.set_caption("Chess Champion")

res = (720, 720)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()

config = Config()

def main():

    menu = Menu(screen, width, height, config)

    while True:
        action = menu.run()
        if action == "start":
            chess_board = ChessBoard(screen, width, height, config)
            game_result = chess_board.draw()
            if game_result == "menu":
                continue

        pygame.display.flip()


if __name__ == "__main__":
    main()