import pygame
import os
from utils import seg_to_min_seg
import time
from math import ceil

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
        self.scroll_y = 0
        self.light_color = (240, 217, 181)
        self.dark_color = (181, 136, 99)

    def load_images(self):
        current_directory = os.path.dirname(__file__)
        images_route = os.path.join(current_directory, "..", "assets", "images")
        pieces = ["WPawn", "WRook", "WKnight", "WBishop", "WQueen", "WKing", "BPawn", "BRook", "BKnight", "BBishop", "BQueen", "BKing"]
        for piece in pieces:
            png_route = os.path.join(images_route, f"{piece}.png")
            image = pygame.image.load(png_route)
            self.images[piece] = pygame.transform.scale(image, (self.square_size, self.square_size))

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                color = self.light_color if (x + y) % 2 == 0 else self.dark_color
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
        game_history = pygame.font.Font(self.font, 28).render("Game history:", True, self.light_color)
        self.display.blit(game_history, (825, 165))
        whites = pygame.font.Font(self.font, 22).render("Whites", True, self.light_color)
        self.display.blit(whites, (850, 215))
        blacks = pygame.font.Font(self.font, 22).render("Blacks", True, self.light_color)
        self.display.blit(blacks, (1025, 215))
        # scrollable history
        history_space = pygame.Surface((self.width - self.square_size * 8, 435), pygame.SRCALPHA)
        history_space.fill((0,0,0,0))
        history = str(game).split("\n")
        self.scrollbar(game)
        for i, line in enumerate(history):
            render_line = pygame.font.Font(self.font, 15).render(line, True, self.light_color)
            # Whites
            if i % 2 == 0:
                history_space.blit(render_line, (55, i*15 + self.scroll_y))
            # Blacks
            else:
                history_space.blit(render_line, (230, (i-1)*15 + self.scroll_y))
        self.display.blit(history_space, (800, 257))
        # undo button
        pygame.draw.rect(self.display, self.dark_color, (825, 725, 150, 50))
        undo = pygame.font.Font(self.font, 20).render("UNDO", True, self.light_color)
        self.display.blit(undo, (860, 741))
        # restart button
        pygame.draw.rect(self.display, self.dark_color, (1025, 725, 150, 50))
        restart = pygame.font.Font(self.font, 20).render("RESTART", True, self.light_color)
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
        turn_line = pygame.font.Font(self.font, 32).render(f"{turn}turn", True, self.light_color)
        timer = pygame.font.Font(self.font, 28).render(seg_to_min_seg(current_time), True, self.light_color)
        self.display.blit(turn_line, (825, 50))
        self.display.blit(timer, (930, 100))
        return True
    
    def scroll_limits(self, game):
        history_pixel_length = ceil(len(game.history)/2)*30 - 15
        if history_pixel_length > 435:
            if self.scroll_y > 0:
                self.scroll_y = 0
            if self.scroll_y < 435 - history_pixel_length:
                self.scroll_y = 435 - history_pixel_length
            return 435 - history_pixel_length
        self.scroll_y = 0
        return False
    
    def scrollbar(self, game):
        scroll_difference = self.scroll_limits(game)
        if not scroll_difference:
            return None
        bar = pygame.Surface((10, 435 + scroll_difference))
        bar.fill(self.light_color)
        self.display.blit(bar, (1170, 257 - self.scroll_y))

    def translate_coords(self, x_mouse, y_mouse):
        return x_mouse // self.square_size, y_mouse // self.square_size
    
    def show_result(self, game, result):
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 80))
        self.display.blit(background, (0, 0))
        pygame.draw.rect(self.display, self.dark_color, (200, 200, 800, 400))
        if result == "CHECKMATE" or "TIMEOUT":
            if result == "CHECKMATE":
                line_1 = pygame.font.Font(self.font, 80).render("CHECKMATE!", True, self.light_color)
            else:
                line_1 = pygame.font.Font(self.font, 100).render("TIMEOUT!", True, self.light_color)
            winner = "Blacks" if game.turn == "W" else "Whites"
            line_2 = pygame.font.Font(self.font, 60).render(f"{winner} win", True, self.light_color)
            self.display.blit(line_2, (310, 425))
        elif result == "STALEMATE":
            line_1 = pygame.font.Font(self.font, 80).render("STALEMATE!", True, self.light_color)
            line_2 = pygame.font.Font(self.font, 60).render("Tie", True, self.light_color)
            self.display.blit(line_2, (505, 425))
        self.display.blit(line_1, (215, 325))
        pygame.display.flip()

    def pawn_promotion_menu(self, game):
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 80))
        self.display.blit(background, (0, 0))
        pygame.draw.rect(self.display, self.dark_color, (275, 300, 650, 200))
        pygame.draw.rect(self.display, self.light_color, (315, 340, 120, 120))
        pygame.draw.rect(self.display, self.light_color, (465, 340, 120, 120))
        pygame.draw.rect(self.display, self.light_color, (615, 340, 120, 120))
        pygame.draw.rect(self.display, self.light_color, (765, 340, 120, 120))
        self.display.blit(self.images[f"{game.turn}Queen"], (325, 350))
        self.display.blit(self.images[f"{game.turn}Rook"], (475, 350))
        self.display.blit(self.images[f"{game.turn}Bishop"], (625, 350))
        self.display.blit(self.images[f"{game.turn}Knight"], (775, 350))
    
    def update_display(self, game, selected_square, promotion):
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
        if promotion:
            self.pawn_promotion_menu(game)
        pygame.display.flip()