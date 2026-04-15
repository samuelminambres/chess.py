# chess.py

# Python chess engine

A chess engine written from scratch in Python. Initially terminal-based, the project has now evolved and features a complete **Graphical User Interface (GUI)**. It implements standard FIDE rules and maintains a strong focus on object-oriented design for move validation and game state management.

## Features

* **FIDE Rules:** Handles standard movements for all pieces, en passant captures, pawn promotion, and castling (including passing-through-check validation).
* **State Detection:** Automatically identifies check, checkmate, and stalemate conditions.
* **Move Validation:** Simulates possible moves by internally checking the board state to ensure the player does not leave their own king in check.
* **Undo System:** Uses a history tracker to safely revert moves and restore previous board states.
* **Interactive GUI:** Allows intuitive gameplay using the mouse, displays a real-time timer for each player, a side panel with the game log, and built-in buttons to undo the last move or restart the game entirely.

## Technical Implementation

The core of the project is highly modularized following object-oriented programming principles:
* **pieces.py**: Base and derived classes that define the logic and specific movement vectors for each chess piece.
* **chessboard.py**: Responsible for grid management, piece storage, and updating coordinates and special states (like the target square for en passant).
* **game.py**: Main controller that orchestrates turns, timers, global rules, and the game loop.
* **gui.py**: Visual module that uses the Pygame library to render the window, draw the board, load textures, and display the information panel.
* **main.py**: The entry point of the application, responsible for handling the user event loop (such as mouse clicks) and synchronizing the logic with the screen rendering.
* **utils.py**: Auxiliary functions for coordinate translations and time formatting.

## Requirements and Execution

To play, you need to have Python 3.10 or higher and the Pygame library installed on your system.

1. Clone the repository to your computer.
2. Navigate to the root directory of the project.
3. Install the Pygame dependency using your standard Python package manager.
4. Start the application by executing the main file located inside the source folder.
5. Control the game by left-clicking on the piece you want to move, and then clicking on the destination square.

## Future Work

* [x] Add a graphical user interface (GUI) using pygame.
* [ ] Implement a basic AI using the Minimax algorithm with alpha-beta pruning to play against the computer.

## License

This project is distributed under the MIT License. See the license file included in the repository for more details.
