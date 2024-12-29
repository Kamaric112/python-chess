# python-chess

This repository contains a Python implementation of a chess game using the Pygame library. It includes a graphical user interface, game logic, and database integration for saving match results.

## Project Structure

The project is organized into several modules, each responsible for a specific aspect of the game:

### Core Game Logic

- **`chess/board.py`**:
  - Defines the `Board` class, which represents the chessboard and its state.
  - Handles the initialization of the board with pieces in their starting positions.
  - Manages piece movement, including validating moves and updating the board state.
  - Includes logic to determine if a checkmate has occurred.
- **`chess/chess_board.py`**:
  - Sets up the main game environment.
  - Initializes the `ChessGameLogic`, `ChessRenderer`, and `ChessEventHandler`.
  - Manages the game loop, handling events and rendering the game state.
  - Creates `User` objects for both players.
- **`chess/game_logic.py`**:
  - Contains the `ChessGameLogic` class, which manages the game's rules and state.
  - Handles piece selection, move validation, and timer updates.
  - Keeps track of the current player's turn.
  - Provides methods to reset the game state.
- **`chess/event_handler.py`**:
  - The `ChessEventHandler` class manages user input and game events.
  - Handles mouse clicks for piece selection and movement.
  - Manages mouse hover events to show valid moves.
  - Processes keyboard events for returning to the menu after a game ends.
  - Saves match results to the database.
- **`chess/renderer.py`**:
  - The `ChessRenderer` class is responsible for drawing the game elements on the screen.
  - Renders the chessboard, pieces, user profiles, timers, and turn indicators.
  - Handles the display of valid moves and hover effects.
  - Displays the victory screen when a game ends.
- **`pieces/piece.py`**:
  - Defines the base `Piece` class and its subclasses for each chess piece type (Pawn, Rook, Knight, Bishop, Queen, King).
  - Each piece subclass implements the `get_valid_moves` method to determine its possible moves based on the current board state.

### User Interface and Configuration

- **`about.py`**:
  - Implements the "About" screen, displaying information about the project and its developers.
  - Uses Pygame to render text and a button for returning to the main menu.
- **`config.py`**:
  - Defines the `Config` class, which stores game settings such as player names, time limits, and database connection details.
  - Provides methods to update these settings.
- **`database.py`**:
  - The `Database` class handles database interactions using MySQL.
  - Establishes a connection to the database.
  - Saves match results, including the winner's name.
  - Includes logging for database events.
- **`game.py`**:
  - The main entry point of the game.
  - Initializes Pygame, sets up the display, and starts the main game loop.
  - Creates instances of the `Menu` and `ChessBoard` classes.
- **`menu.py`**:
  - Implements the main menu of the game.
  - Displays options for starting a new game, accessing settings, viewing the about screen, and exiting the game.
  - Uses Pygame to render buttons and handle user input.
- **`setting.py`**:
  - Provides a settings screen where users can configure player names, time limits, and music.
  - Uses Pygame for rendering and Tkinter for file dialogs.
  - Allows users to select custom images for player profiles.
- **`user.py`**:
  - Defines the `User` class, which represents a player in the game.
  - Stores player names and profile images.
  - Provides methods to change the player's name and image using Tkinter dialogs.

## How to Run

1.  Ensure you have Python 3.6+ and Pygame installed.
2.  Install the required packages using pip:
    ```bash
    pip install pygame mysql-connector-python
    ```
3.  Set up a MySQL database and update the database credentials in `config.py`.
4.  Run the game:
    ```bash
    python game.py
    ```

## Additional Notes

- The game uses a simple logging system to track game events and database interactions.
- The `assets` directory contains images for the chess pieces, background, and music files.
- The game uses Tkinter for file dialogs when changing player images.
- The game supports basic music playback.
- The game uses a simple state machine to manage the game flow.
