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

config = Config() #Phuong: 

def main():

    menu = Menu(screen, width, height, config)
    chess_board = ChessBoard(screen, width, height, config)


    while True:
        action = menu.run()
        if action == "start":
            game_result = chess_board.draw()
            if game_result == "menu":
                continue

        #  TODO update menu (beautify)
        #  TODO add member list
        #  TODO add music
        #  TODO add back button in chess
        #  TODO show list of capture pieces
        pygame.display.flip()


if __name__ == "__main__":
    main()