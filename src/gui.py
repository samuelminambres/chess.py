import pygame
import os
from utils import seg_to_min_seg
import time

class Gui:

    def __init__(self):
        pygame.init()
        self.height = 800
        self.width = 1200
        self.square_size = self.height // 8
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python chess engine")
        self.images = {}
        self.load_images()
        self.font = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P.ttf")

    def load_images(self):
        current_directory = os.path.dirname(__file__)
        images_route = os.path.join(current_directory, "..", "assets", "images")
        pieces = ["WPawn", "WRook", "WKnight", "WBishop", "WQueen", "WKing", "BPawn", "BRook", "BKnight", "BBishop", "BQueen", "BKing"]
        for piece in pieces:
            png_route = os.path.join(images_route, f"{piece}.png")
            image = pygame.image.load(png_route)
            self.images[piece] = pygame.transform.scale(image, (self.square_size, self.square_size))

    def draw_board(self):
        light_color = (240, 217, 181)
        dark_color = (181, 136, 99)
        for y in range(8):
            for x in range(8):
                color = light_color if (x + y) % 2 == 0 else dark_color
                square = (x * self.square_size, y * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.display, color, square)

    def draw_pieces(self, board):
        for y in range(8):
            for x in range(8):
                piece = board.get_piece_at(x, y)
                if piece is None:
                    continue
                texture = piece.color + type(piece).__name__
                x_pixel = x * self.square_size
                y_pixel = y * self.square_size
                self.display.blit(self.images[texture], (x_pixel, y_pixel))

    def draw_information(self, game):
        pygame.draw.rect(self.display, (139, 90, 43), (800, 0, 400, 800))
        current_time = time.time()
        time_spent = current_time - game.turn_time
        if game.turn == "W":
            turn = pygame.font.Font(self.font, 30).render("Whites' turn", True, (240, 217, 181))
            timer = pygame.font.Font(self.font, 28).render(seg_to_min_seg(game.white_timer - time_spent), True, (240, 217, 181))
        else:
            turn = pygame.font.Font(self.font, 30).render("Blacks' turn", True, (240, 217, 181))
            timer = pygame.font.Font(self.font, 28).render(seg_to_min_seg(game.black_timer - time_spent), True, (240, 217, 181))
        self.display.blit(turn, (825, 50))
        self.display.blit(timer, (930, 100))
        game_history = pygame.font.Font(self.font, 28).render("Game history:", True, (240, 217, 181))
        self.display.blit(game_history, (825, 175))
        history = str(game).split("\n")
        height = 225
        for line in history[::-1]:
            render_line = pygame.font.Font(self.font, 16).render(line, True, (240, 217, 181))
            self.display.blit(render_line, (885, height))
            height += 25
            if height >= 750:
                break

    def translate_coords(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return x_mouse // self.square_size, y_mouse // self.square_size
    
    def update_display(self, game, board, selected_square):
        self.draw_board()
        self.draw_information(game)
        self.draw_pieces(board)
        if selected_square is not None:
            x, y = selected_square
            highlighted_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            color = (100, 200, 255, 60)
            highlighted_surface.fill(color)
            x_pixel = x * self.square_size
            y_pixel = y * self.square_size
            self.display.blit(highlighted_surface, (x_pixel, y_pixel))
        pygame.display.flip()