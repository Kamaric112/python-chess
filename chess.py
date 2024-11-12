import sys

import pygame

def init_chess(screen, width, height):
    # Chess board colors
    WHITE = (255, 255, 255)
    BLACK = (128, 128, 128)
    # Calculate square size based on screen dimensions
    SQUARE_SIZE = min(width, height) // 8

    # Starting position for centering the board
    start_x = (width - SQUARE_SIZE * 8) // 2
    start_y = (height - SQUARE_SIZE * 8) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill background
        screen.fill((60, 25, 60))  # Matching menu background

        # Draw the chess board
        for row in range(8):
            for col in range(8):
                x = start_x + col * SQUARE_SIZE
                y = start_y + row * SQUARE_SIZE
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        # Update the display
        pygame.display.flip()