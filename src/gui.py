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
        # background
        pygame.draw.rect(self.display, (139, 90, 43), (self.square_size * 8, 0, self.width - self.square_size * 8, self.height))
        # timers
        self.timer(game)
        # game history
        game_history = pygame.font.Font(self.font, 28).render("Game history:", True, (240, 217, 181))
        self.display.blit(game_history, (825, 175))
        history = str(game).split("\n")
        height = 225
        for line in history[::-1]:
            render_line = pygame.font.Font(self.font, 16).render(line, True, (240, 217, 181))
            self.display.blit(render_line, (885, height))
            height += 25
            if height >= 700:
                break
        # undo button
        pygame.draw.rect(self.display, (181, 136, 99), (825, 725, 150, 50))
        undo = pygame.font.Font(self.font, 20).render("UNDO", True, (240, 217, 181))
        self.display.blit(undo, (860, 741))
        # restart button
        pygame.draw.rect(self.display, (181, 136, 99), (1025, 725, 150, 50))
        restart = pygame.font.Font(self.font, 20).render("RESTART", True, (240, 217, 181))
        self.display.blit(restart, (1031, 741))

    def timer(self, game):
        time_spent = time.time() - game.turn_time
        if game.turn == "W":
            current_time = game.white_timer - time_spent  
            turn = "Whites'"
        else:
            current_time = game.black_timer - time_spent
            turn = "Blacks'"
        if current_time <= 0:
            return False
        turn_line = pygame.font.Font(self.font, 32).render(f"{turn}turn", True, (240, 217, 181))
        timer = pygame.font.Font(self.font, 28).render(seg_to_min_seg(current_time), True, (240, 217, 181))
        self.display.blit(turn_line, (825, 50))
        self.display.blit(timer, (930, 100))
        
        return True


    def translate_coords(self, x_mouse, y_mouse):
        return x_mouse // self.square_size, y_mouse // self.square_size
    
    def show_result(self, game, result):
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 80))
        self.display.blit(background, (0, 0))
        pygame.draw.rect(self.display, (181, 136, 99), (200, 200, 800, 400))
        if result == "CHECKMATE" or "TIMEOUT":
            if result == "CHECKMATE":
                line_1 = pygame.font.Font(self.font, 80).render("CHECKMATE!", True, (240, 217, 181))
            else:
                line_1 = pygame.font.Font(self.font, 100).render("TIMEOUT!", True, (240, 217, 181))
            winner = "Blacks" if game.turn == "W" else "Whites"
            line_2 = pygame.font.Font(self.font, 60).render(f"{winner} win", True, (240, 217, 181))
            self.display.blit(line_2, (310, 425))
        elif result == "STALEMATE":
            line_1 = pygame.font.Font(self.font, 80).render("STALEMATE!", True, (240, 217, 181))
            line_2 = pygame.font.Font(self.font, 60).render("Tie", True, (240, 217, 181))
            self.display.blit(line_2, (505, 425))
        self.display.blit(line_1, (215, 325))
        pygame.display.flip()
    
    def update_display(self, game, selected_square):
        self.draw_board()
        self.draw_information(game)
        # highlight selected square
        if selected_square is not None and selected_square[0] <= 7:
            x, y = selected_square
            highlighted_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            color = (100, 200, 255, 90)
            highlighted_surface.fill(color)
            x_pixel = x * self.square_size
            y_pixel = y * self.square_size
            self.display.blit(highlighted_surface, (x_pixel, y_pixel))
        self.draw_pieces(game.board)
        pygame.display.flip()