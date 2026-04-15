import pygame
import sys
from game import Game
from gui import Gui
import time

gui = Gui()
game = Game()
game.setup_standard_board()

running = True

selected_square = None
while running:
    gui.update_display(game, selected_square)
    if not gui.timer(game):
        gui.show_result(game, "TIMEOUT")
        pygame.time.wait(5000)
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if selected_square is None:
                selected_square = gui.translate_coords(x_mouse, y_mouse)
                if x_mouse > 800:
                    # undo button
                    if 825 < x_mouse < 975 and 725 < y_mouse < 775:
                        if len(game.history) == 0:
                            print("\nError: no moves to undo, try again\n")
                            continue
                        game.undo_move()
                        game.turn = "B" if game.turn == "W" else "W"
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
                    continue
                if result == "SUCCESS":
                    print("Succesful movement!\n")
                    continue
                else:
                    gui.show_result(game, result)
                    pygame.time.wait(5000)
                    running = False
pygame.quit()
sys.exit()