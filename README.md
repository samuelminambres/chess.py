# Python Chess Engine

A complete chess engine and graphical interface developed from scratch. This project implements standard FIDE rules, strict move validation, and an Artificial Intelligence engine capable of playing against the user using the Minimax algorithm with alpha-beta pruning.

The main goal of this project is to apply software architecture skills: Object-Oriented Programming (OOP) principles, separation of concerns, and efficient data structures for game state management.

<img width="1204" height="824" alt="game_demo" src="https://github.com/user-attachments/assets/21474807-d0fe-46c7-8913-f546bac4a38b" />

<img width="1204" height="829" alt="coronation_menu" src="https://github.com/user-attachments/assets/3977219f-c7dc-4b21-8149-a32f07b4cce8" />

## Key Features

* **Complete FIDE Rules Engine:** Implementation of all standard and special moves, including En Passant, pawn promotion, and castling (with passing-through-check validation).
* **Artificial Intelligence (Minimax):** Player vs Environment (PvE) mode powered by an algorithmic bot that evaluates the board using Piece-Square Tables and alpha-beta pruning to optimize the decision tree.
* **Robust State Validation:** Automatic and real-time detection of Check, Checkmate, and Stalemate conditions, preventing the player from making moves that leave their own king in danger.
* **Undo System:** Move history management using a Stack system that allows reverting changes and accurately restoring previous board states and timers.
* **Interactive Graphical Interface:** Developed with Pygame, offering a smooth experience with mouse controls, square highlighting, real-time timers, move logging, and game mode selection menus.

## Architecture and Technical Design

The core of the project is highly modularized, clearly separating business logic from the presentation layer.

* **pieces.py (Inheritance and Polymorphism):** Contains an abstract base class and derived classes for each piece. Each piece is responsible for knowing its own movement vectors and evaluating basic displacement rules.
* **chessboard.py (Data Structure):** Manages the 8x8 grid, piece placement, updated king coordinates, and target squares for En Passant captures.
* **game.py (State Controller):** The main orchestrator. Validates the final legality of moves (ensuring they do not break check rules), handles turns, timers, and updates the history.
* **ai.py (Algorithms):** Implements the computer's decision-making logic. Completely isolates the calculation engine from the regular game flow.
* **gui.py (Presentation Layer):** Exclusively responsible for visual rendering, loading textures, fonts, and capturing user input events.
* **main.py (Main Loop):** Synchronizes game logic, AI, and interface in a continuous and resource-efficient game loop.

## Technologies Used

* **Language:** Python 3.10+
* **Libraries:** Pygame (graphical rendering and I/O interaction)
* **Patterns:** OOP, Modular Architecture, Stack Systems (History).

## Installation and Execution

1. Clone this repository using your preferred git client.
2. Navigate to the project directory in your terminal.
3. Install the necessary dependencies using your package manager (for example, pip install pygame).
4. Start the application by running the main.py file located inside the src folder.

## How to Play

1. Upon starting the application, select the game mode: **1vs1** (Local multiplayer) or **vs AI** (Against the algorithm).
2. Left-click on the piece you want to move; you will see the highlighted square.
3. Click on the destination square to complete the turn.
4. Use the side panel to review the move history, watch the timer, undo your last move, or restart the game.

## Future Work and Improvements

* AI engine optimization using Bitboards to speed up move generation and increase search depth.
* Forsyth-Edwards Notation (FEN) support to load custom board states.
* Integration of an opening database for more natural AI behavior in the early turns.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
