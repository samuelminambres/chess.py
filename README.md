# chess.py

# Python Chess Engine

A terminal-based chess engine written from scratch in Python. It implements standard FIDE rules and focuses on object-oriented design and custom data structures for move validation and state management.

## Features

* **FIDE Rules:** Handles standard piece movements, en passant, pawn promotion, and castling (including passing-through-check validation).
* **State Detection:** Automatically identifies check, checkmate, and stalemate conditions.
* **Move Validation:** Simulates possible moves by deep-copying the board state to ensure the king is never left in check.
* **Undo System:** Uses a custom history tracker to safely revert moves and restore previous board states.

## Technical Implementation

Instead of relying entirely on native Python lists for state history, this project uses custom data structures to handle the game flow:

* **Custom Stack and Linked List:** Move history is managed by a `Stack` and `LinkedList` built from scratch (`src/stack.py`). This allows for clean handling of history nodes and straightforward state retrieval for the undo functionality.
* **Object-Oriented Design:** The core logic is modularized:
  * `pieces.py`: Base and derived classes that define piece-specific movement vectors and logic.
  * `chessboard.py`: Handles grid management, piece placement, and coordinate updates.
  * `game.py`: The main controller that orchestrates turns, global rules, and the game loop.

## Running the game

Requires Python 3.10 or higher.

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/REPO-NAME.git](https://github.com/YOUR-USERNAME/REPO-NAME.git)

2. Navigate to the project directory
    ```bash
    cd REPO-NAME

3. Run the main script:
    ```bash
    python src/main.py

4. Enter your moves using standard coordinate notation (e.g., e2 to e4, mayus allowed too).

## Future scope

* [ ] Add a graphical user interface (GUI) using pygame.

* [ ] Implement a basic Minimax AI with alpha-beta pruning.

## License

* This project is licensed under the MIT License - see the LICENSE file for details.