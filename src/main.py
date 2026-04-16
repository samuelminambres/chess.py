import pygame
import sys
from game import Game
from gui import Gui
import time

gui = Gui()
game = Game()
game.setup_standard_board()

running = True
promotion = False
selected_square = None
while running:
    gui.update_display(game, selected_square, promotion)
    if not gui.timer(game):
        gui.show_result(game, "TIMEOUT")
        pygame.time.wait(5000)
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if promotion:
                if 340 < y_mouse < 460:
                    if 315 < x_mouse < 435:
                        game.promotion_to("Q", end[0], end[1])
                        promotion = False
                        game.swap_turn()
                    elif 465 < x_mouse < 585:
                        game.promotion_to("R", end[0], end[1])
                        promotion = False
                        game.swap_turn()
                    if 615 < x_mouse < 715:
                        game.promotion_to("B", end[0], end[1])
                        promotion = False
                        game.swap_turn()
                    if 765 < x_mouse < 865:
                        game.promotion_to("N", end[0], end[1])
                        promotion = False
                        game.swap_turn()

            elif selected_square is None:
                selected_square = gui.translate_coords(x_mouse, y_mouse)
                if x_mouse > 800:
                    # undo button
                    if 825 < x_mouse < 975 and 725 < y_mouse < 775:
                        if len(game.history) == 0:
                            print("\nError: no moves to undo, try again\n")
                            continue
                        game.undo_move()
                        game.swap_turn()
                        game.turn_time = time.time()
                        print("Move undone succesfully!\n")
                    # restart button
                    elif 1025 < x_mouse < 1175 and 725 < y_mouse < 775:
                        game = Game()
                        game.setup_standard_board()
                        print("\nNew game!\n")
                    selected_square = None
                elif game.board.get_piece_at(selected_square[0], selected_square[1]) is None:
                    selected_square = None
            else:
                end = gui.translate_coords(x_mouse, y_mouse)
                result = game.play_move(selected_square, end)
                selected_square = None
                if result == "INVALID":
                    print("Illegal movement, try again\n")
                elif result == "SUCCESS":
                    promotion = game.pawn_promotion(end[0], end[1])
                    if not promotion:
                        game.swap_turn()
                else:
                    gui.show_result(game, result)
                    pygame.time.wait(5000)
                    running = False
        # scroll
        elif event.type == pygame.MOUSEWHEEL:
            scroll_sens = 5
            gui.scroll_y += event.y * scroll_sens
                
pygame.quit()
sys.exit()