import pygame
import sys
from game import Game
from gui import Gui

gui = Gui()
game = Game()
game.setup_standard_board()

running = True

start = None
while running:
    gui.update_display(game, game.board, start)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start is None:
                start = gui.translate_coords(event)
                if game.board.get_piece_at(start[0], start[1]) is None:
                    start = None
            else:
                end = gui.translate_coords(event)
                result = game.play_move(start, end)
                start = None
                if result == "INVALID":
                    print("Illegal movement, try again\n")
                    continue
                if result == "SUCCESS":
                    print("Succesful movement!\n")
                    continue
                elif result == "CHECKMATE":
                    print("¡CHECKMATE! You lose")
                elif result == "STALEMATE":
                    print("¡STALEMATE! Tie")
                else:
                    print("Time is out, you lose")
                running = False

pygame.quit()
sys.exit()