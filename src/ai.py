from move import Move

class ChessAI:
    """Chess engine opponent implementing minimax with alpha-beta pruning.

    Attributes:
        depth (int): Search depth limit for minimax evaluation.
        color (str): The piece color played by the AI ('W' or 'B').
    """

    def __init__(self, depth = 3, color = "B"):
        """Initializes the ChessAI engine.

        Args:
            depth (int, optional): Search depth for the minimax algorithm (0-5). Defaults to 3.
            color (str, optional): The color played by the AI ('W' or 'B'). Defaults to "B".
        """
        self.depth = depth
        self.color = color

    @property
    def depth(self):
        """Gets the search depth for minimax.

        Returns:
            int: The search depth.
        """
        return self._depth
    
    @depth.setter
    def depth(self, value):
        """Sets the search depth for minimax.

        Args:
            value (int): Search depth between 0 and 5.

        Raises:
            TypeError: If value is not an int.
            ValueError: If value is not between 0 and 5.
        """
        if not isinstance(value, int):
            raise TypeError("Depth must be int")
        if value < 0 or value > 5:
            raise ValueError("Depth must be between 0 and 5")
        self._depth = value

    @property
    def color(self):
        """Gets the color played by the AI.

        Returns:
            str: Color string ('W' or 'B').
        """
        return self._color
    
    @color.setter
    def color(self, value):
        """Sets the color played by the AI.

        Args:
            value (str): Color string ('W' or 'B').

        Raises:
            TypeError: If value is not a str.
            ValueError: If value is not 'W' or 'B'.
        """
        if not isinstance(value, str):
            raise TypeError("Color must be str")
        if value != "W" and value != "B":
            raise ValueError('Color must be "W" or "B"')
        self._color = value

    def get_best_move(self, game):
        """Finds the best move for the AI using minimax with alpha-beta pruning.

        Args:
            game (Game): The current chess game instance.

        Returns:
            tuple or None: A tuple of (start, end) coordinates representing the best move,
                or None if no legal moves exist.
        """
        legal_moves = game.get_all_legal_moves()
        if not legal_moves:
            return None
        best_eval = float("-inf") if self.color == "W" else float("inf")
        for start, end in legal_moves:
            piece = game.board.get_piece_at(start)
            target = game.board.get_piece_at(end)
            move = game.board.move(start, end)
            if not move:
                continue
            if game.pawn_promotion(end):
                game.promotion_to("Q", end)
            game.swap_turn()
            is_maximizing = self.color == "B"
            eval = self.minimax(game, depth = self.depth - 1, is_maximizing = is_maximizing)
            game.history.append(Move(start, end, piece, target, game.board.en_passant_target, piece.has_moved, game.half_move_clock))
            game.undo_move()
            game.swap_turn()
            best_eval = max(best_eval, eval) if self.color == "W" else min(best_eval, eval)
            if eval == best_eval:
                best_move = (start, end)
        return best_move

    def minimax(self, game, depth, is_maximizing, alpha = float("-inf"), beta = float("inf")):
        """Evaluates game positions recursively using minimax with alpha-beta pruning.

        Args:
            game (Game): The current chess game instance.
            depth (int): Remaining depth to search.
            is_maximizing (bool): True if evaluating for the maximizing player, False otherwise.
            alpha (float, optional): Best score that the maximizer can guarantee. Defaults to -inf.
            beta (float, optional): Best score that the minimizer can guarantee. Defaults to inf.

        Returns:
            float: Evaluated positional score.
        """
        if depth == 0:
            return self.evaluate(game.board)
        legal_moves = game.get_all_legal_moves()
        if not legal_moves:
            return self.evaluate(game.board)
        if is_maximizing:
            max_eval = float("-inf")
            for start, end in legal_moves:
                piece = game.board.get_piece_at(start)
                target = game.board.get_piece_at(end)
                move = game.board.move(start, end)
                if not move:
                    continue
                if game.pawn_promotion(end):
                    game.promotion_to("Q", end)
                game.swap_turn()
                eval = self.minimax(game, depth = depth - 1, is_maximizing = False, alpha = alpha, beta = beta)
                game.history.append(Move(start, end, piece, target, game.board.en_passant_target, piece.has_moved, game.half_move_clock))
                game.undo_move()
                game.swap_turn()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for start, end in legal_moves:
                piece = game.board.get_piece_at(start)
                target = game.board.get_piece_at(end)
                move = game.board.move(start, end)
                if not move:
                    continue
                if game.pawn_promotion(end):
                    game.promotion_to("Q", end)
                game.swap_turn()
                eval = self.minimax(game, depth = depth - 1, is_maximizing = True, alpha = alpha, beta = beta)
                game.history.append(Move(start, end, piece, target, game.board.en_passant_target, piece.has_moved, game.half_move_clock))
                game.undo_move()
                game.swap_turn()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, board):
        """Computes a static heuristic evaluation of the board state.

        Args:
            board (Chessboard): The chessboard instance to evaluate.

        Returns:
            float: The heuristic score where positive favors White and negative favors Black.
        """
        evaluation = 0
        for x, y in board.white_pieces_coords:
            piece = board.get_piece_at((x, y))
            evaluation += piece.value + piece.piece_square_table[y][x]
        for x, y in board.black_pieces_coords:
            piece = board.get_piece_at((x, y))
            evaluation -= piece.value + piece.piece_square_table[7-y][x]
        return evaluation