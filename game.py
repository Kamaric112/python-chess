import pygame
from menu import Menu
from chess import ChessBoard
from pieces.chess import ChessGame

pygame.init()
res = (720, 720)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()


def main():
    menu = Menu(screen, width, height)
    chess_board = ChessBoard(screen, width, height)
    game = ChessGame()
    # display = BoardDisplay(game.board)

    while True:
        action = menu.run()
        if action == "start":
            chess_board.draw()

        # display.show_board()
        pygame.display.flip()

        # Get player input
        # Make moves
        # Check game state


if __name__ == "__main__":
    main()
