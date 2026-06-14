from move import Move

class ChessAI:

    def __init__(self, depth = 3, color = "B"):
        self.depth = depth
        self.color = color

    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, value):
        if not isinstance(value, int):
            raise TypeError("Depth must be int")
        if value < 0 or value > 5:
            raise ValueError("Depth must be between 0 and 5")
        self._depth = value

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError("Color must be str")
        if value != "W" and value != "B":
            raise ValueError('Color must be "W" or "B"')
        self._color = value

    def get_best_move(self, game):
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
        evaluation = 0
        for x, y in board.white_pieces_coords:
            piece = board.get_piece_at((x, y))
            evaluation += piece.value + piece.piece_square_table[y][x]
        for x, y in board.black_pieces_coords:
            piece = board.get_piece_at((x, y))
            evaluation -= piece.value + piece.piece_square_table[7-y][x]
        return evaluation