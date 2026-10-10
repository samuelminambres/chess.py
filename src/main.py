import sys
import time
import pygame
from game import Game
from gui import Gui
from ai import ChessAI

# Initialization
gui = Gui()
game = Game()
game.setup_standard_board()

bot = None
ai_mode = False
menu = True
promotion = False
promotion_square = None
selected_square = None
running = True

while running:
    # 1. Render interface
    gui.update_display(game, selected_square, promotion, menu)

    # 2. AI turn
    if not menu and ai_mode and game.turn == "B":
        start, end = bot.get_best_move(game)
        result = game.play_move(start, end)
        if result == "SUCCESS":
            if game.pawn_promotion(end):
                game.promotion_to("Q", end)
            game.swap_turn()
        else:
            gui.show_result(game, result)
            pygame.time.wait(5000)
            running = False

    # 3. Time check
    if not menu and not gui.timer(game):
        gui.show_result(game, "TIMEOUT")
        pygame.time.wait(5000)
        running = False

    # 4. Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            gui.handle_scroll(event.y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Case A: Game mode selection menu
            if menu:
                choice = gui.get_menu_selection(mouse_pos)
                if choice == "ai":
                    bot = ChessAI()
                    ai_mode = True
                    menu = False
                    game.white_timer.start()
                elif choice == "1vs1":
                    ai_mode = False
                    menu = False
                    game.white_timer.start()

            # Case B: Pawn promotion menu
            elif promotion:
                piece_choice = gui.get_promotion_selection(mouse_pos)
                if piece_choice:
                    game.promotion_to(piece_choice, promotion_square)
                    promotion = False
                    promotion_square = None
                    game.swap_turn()

            # Case C: Sidebar interaction (Buttons)
            elif not gui.is_in_board(mouse_pos):
                button_clicked = gui.get_sidebar_button(mouse_pos)
                if button_clicked == "undo":
                    if len(game.history) == 0:
                        print("Error: no moves to undo")
                        continue
                    if ai_mode:
                        game.undo_move()
                        game.undo_move()
                    else:
                        game.undo_move()
                        game.swap_turn()
                    game.turn_time = time.time()
                elif button_clicked == "restart":
                    game = Game()
                    game.setup_standard_board()
                    game.white_timer.start()
                selected_square = None

            # Case D: Chessboard interaction
            else:
                board_pos = gui.translate_coords(*mouse_pos)
                if selected_square is None:
                    # Select piece if the clicked square is not empty
                    if game.board.get_piece_at(board_pos) is not None:
                        selected_square = board_pos
                else:
                    # Attempt to execute the move
                    result = game.play_move(selected_square, board_pos)
                    selected_square = None

                    if result == "SUCCESS":
                        if game.pawn_promotion(board_pos):
                            promotion = True
                            promotion_square = board_pos
                        else:
                            game.swap_turn()
                    elif result == "INVALID":
                        # If clicking another friendly piece, change selection
                        clicked_piece = game.board.get_piece_at(board_pos)
                        if clicked_piece and clicked_piece.color == game.turn:
                            selected_square = board_pos
                    else:
                        gui.show_result(game, result)
                        pygame.time.wait(5000)
                        running = False

pygame.quit()
sys.exit()