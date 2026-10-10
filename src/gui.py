import os
from math import ceil
import pygame

BOARD_DIMENSION = 8
COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (181, 136, 99)
COLOR_SIDEBAR = (139, 90, 43)
COLOR_SCROLL_TRACK = (112, 72, 34)
COLOR_OVERLAY = (0, 0, 0, 80)
COLOR_HIGHLIGHT = (100, 200, 255, 90)
PIECE_NAMES = (
    "WPawn", "WRook", "WKnight", "WBishop", "WQueen", "WKing",
    "BPawn", "BRook", "BKnight", "BBishop", "BQueen", "BKing"
)
PROMOTION_PIECES = ("Queen", "Rook", "Bishop", "Knight")

class Gui:
    """Manages graphical rendering, Pygame windows, menus, and user interactions.

    Attributes:
        height (int): Window height in pixels.
        width (int): Window width in pixels.
        board_size (int): Pixel size of the square chessboard area.
        square_size (int): Pixel dimension of each chessboard square.
        panel_x (int): Horizontal starting offset for the sidebar panel.
        panel_width (int): Width of the sidebar panel in pixels.
        display (pygame.Surface): Main Pygame display surface.
        images (dict): Loaded and scaled piece texture images.
        scroll_y (int): Vertical scroll offset for move history.
        line_h (int): Height of each line of move history text.
    """

    def __init__(self, height: int = 800, width: int = 1200):
        """Initializes the graphical user interface and Pygame window.

        Args:
            height (int, optional): Window height in pixels. Defaults to 800.
            width (int, optional): Window width in pixels. Defaults to 1200.
        """
        pygame.init()
        self.height = height
        self.width = width
        
        self.board_size = self.height
        self.square_size = self.board_size // BOARD_DIMENSION
        self.panel_x = self.square_size * BOARD_DIMENSION
        self.panel_width = self.width - self.panel_x

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python chess engine")

        self.font_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P.ttf"
        )
        self._font_cache = {}

        self.images = {}
        self.load_images()

        self.scroll_y = 0
        self.line_h = 24

        self._init_layout()

    def _init_layout(self):
        """Initializes layout coordinates and bounding rectangles for UI elements."""
        btn_margin = 25
        btn_y = self.height - 75
        btn_h = 50
        btn_w = 150

        self.undo_btn_rect = pygame.Rect(
            self.panel_x + btn_margin, btn_y, btn_w, btn_h
        )
        self.restart_btn_rect = pygame.Rect(
            self.panel_x + self.panel_width - btn_margin - btn_w, btn_y, btn_w, btn_h
        )

        self.bar_w = 10
        self.bar_x = self.restart_btn_rect.right - self.bar_w

        history_x = self.undo_btn_rect.left
        history_gap_bar = 10
        history_width = (self.bar_x - history_gap_bar) - history_x
        
        self.history_rect = pygame.Rect(history_x, 257, history_width, 435)

        self.scroll_track_rect = pygame.Rect(
            self.bar_x, self.history_rect.y, self.bar_w, self.history_rect.height
        )

        self.col_white_x = history_x + 20 + 70
        self.col_black_x = history_x + 180 + 70

        self.col_white_local_x = self.col_white_x - self.history_rect.x
        self.col_black_local_x = self.col_black_x - self.history_rect.x

    def _get_font(self, size: int) -> pygame.font.Font:
        """Retrieves a cached Font instance for the given point size.

        Args:
            size (int): Font size in points.

        Returns:
            pygame.font.Font: Loaded or cached font instance.
        """
        if size not in self._font_cache:
            if os.path.exists(self.font_path):
                self._font_cache[size] = pygame.font.Font(self.font_path, size)
            else:
                self._font_cache[size] = pygame.font.SysFont("sans-serif", size)
        return self._font_cache[size]

    def _render_text(self, text: str, size: int, color, center=None, topleft=None, surface=None):
        """Renders text onto a target surface or the main display.

        Args:
            text (str): The text string to render.
            size (int): Font size in points.
            color (tuple): RGB color tuple for the font.
            center (tuple, optional): Center position (x, y). Defaults to None.
            topleft (tuple, optional): Top-left position (x, y). Defaults to None.
            surface (pygame.Surface, optional): Surface to render onto. Defaults to None.

        Returns:
            pygame.Rect: Bounding rectangle of the drawn text.
        """
        target = surface or self.display
        font = self._get_font(size)
        text_surf = font.render(text, True, color)
        
        if center:
            text_rect = text_surf.get_rect(center=center)
        elif topleft:
            text_rect = text_surf.get_rect(topleft=topleft)
        else:
            text_rect = text_surf.get_rect()
            
        target.blit(text_surf, text_rect)
        return text_rect

    def load_images(self):
        """Loads and scales piece image assets from the assets directory."""
        images_route = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
        for piece in PIECE_NAMES:
            png_route = os.path.join(images_route, f"{piece}.png")
            if os.path.exists(png_route):
                image = pygame.image.load(png_route)
                self.images[piece] = pygame.transform.scale(
                    image, (self.square_size, self.square_size)
                )

    def draw_board(self):
        """Draws the alternating light and dark squares of the chessboard."""
        for y in range(BOARD_DIMENSION):
            for x in range(BOARD_DIMENSION):
                color = COLOR_LIGHT if (x + y) % 2 == 0 else COLOR_DARK
                square = (x * self.square_size, y * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.display, color, square)

    def draw_pieces(self, board):
        """Draws all active chess pieces on their corresponding squares.

        Args:
            board (Chessboard): The chessboard containing the pieces to draw.
        """
        for y in range(BOARD_DIMENSION):
            for x in range(BOARD_DIMENSION):
                piece = board.get_piece_at((x, y))
                if piece is None:
                    continue
                texture = f"{piece.color}{type(piece).__name__}"
                if texture in self.images:
                    x_pixel = x * self.square_size
                    y_pixel = y * self.square_size
                    self.display.blit(self.images[texture], (x_pixel, y_pixel))

    def draw_information(self, game):
        """Renders the sidebar panel including the timer, move history, and buttons.

        Args:
            game (Game): The current game instance.
        """
        pygame.draw.rect(
            self.display,
            COLOR_SIDEBAR,
            (self.panel_x, 0, self.panel_width, self.height)
        )

        self.timer(game)

        panel_center_x = self.panel_x + (self.panel_width // 2)
        self._render_text("Game history:", 28, COLOR_LIGHT, center=(panel_center_x, 165))
        
        self._render_text("Whites", 22, COLOR_LIGHT, center=(self.col_white_x, 215))
        self._render_text("Blacks", 22, COLOR_LIGHT, center=(self.col_black_x, 215))

        history_surface = pygame.Surface(self.history_rect.size, pygame.SRCALPHA)
        history_surface.fill((0, 0, 0, 0))

        self.scrollbar(game)

        history = str(game).split("\n")
        for i, line in enumerate(history):
            if not line.strip():
                continue
            y_offset = (i // 2) * self.line_h + self.scroll_y
            center_y = y_offset + (self.line_h // 2)

            if i % 2 == 0:
                self._render_text(
                    line, 15, COLOR_LIGHT,
                    center=(self.col_white_local_x, center_y),
                    surface=history_surface
                )
            else:
                self._render_text(
                    line, 15, COLOR_LIGHT,
                    center=(self.col_black_local_x, center_y),
                    surface=history_surface
                )

        self.display.blit(history_surface, self.history_rect.topleft)

        pygame.draw.rect(self.display, COLOR_DARK, self.undo_btn_rect)
        self._render_text("UNDO", 20, COLOR_LIGHT, center=self.undo_btn_rect.center)

        pygame.draw.rect(self.display, COLOR_DARK, self.restart_btn_rect)
        self._render_text("RESTART", 20, COLOR_LIGHT, center=self.restart_btn_rect.center)

    def timer(self, game):
        """Renders the active turn player and countdown timer on the sidebar.

        Args:
            game (Game): The current game instance.

        Returns:
            bool: False if the active player's timer has expired, True otherwise.
        """
        turn = "Whites' " if game.turn == "W" else "Blacks' "
        timer = game.white_timer if game.turn == "W" else game.black_timer
        if timer.is_timeout():
            return False

        center_x = self.panel_x + (self.panel_width // 2)
        self._render_text(f"{turn}turn", 30, COLOR_LIGHT, center=(center_x, 60))
        self._render_text(str(timer), 28, COLOR_LIGHT, center=(center_x, 110))
        return True

    def _get_content_height(self, game) -> int:
        """Calculates the total height of move history content in pixels.

        Args:
            game (Game): The current game instance.

        Returns:
            int: The total calculated height in pixels.
        """
        total_rows = ceil(len(game.history) / 2) if hasattr(game, "history") else ceil(len(str(game).split("\n")) / 2)
        return max(1, total_rows * self.line_h)

    def scroll_limits(self, game):
        """Restricts vertical scroll position within view boundaries.

        Args:
            game (Game): The current game instance.

        Returns:
            int: Maximum allowed scroll offset (negative or zero).
        """
        visible_h = self.history_rect.height
        total_h = self._get_content_height(game)

        if total_h > visible_h:
            max_scroll = visible_h - total_h
            self.scroll_y = min(0, max(self.scroll_y, max_scroll))
            return max_scroll
            
        self.scroll_y = 0
        return 0

    def scrollbar(self, game):
        """Renders the scrollbar track and thumb for the move history view.

        Args:
            game (Game): The current game instance.
        """
        self.scroll_limits(game)
        visible_h = self.history_rect.height
        total_h = self._get_content_height(game)

        if total_h <= visible_h:
            return

        pygame.draw.rect(self.display, COLOR_SCROLL_TRACK, self.scroll_track_rect)

        min_thumb_h = 24
        thumb_h = int((visible_h / total_h) * visible_h)
        thumb_h = max(min_thumb_h, min(thumb_h, visible_h))

        scroll_range = total_h - visible_h
        scroll_pct = (-self.scroll_y) / scroll_range if scroll_range > 0 else 0.0

        available_track_travel = visible_h - thumb_h
        thumb_y = self.scroll_track_rect.y + int(scroll_pct * available_track_travel)

        thumb_rect = pygame.Rect(self.bar_x, thumb_y, self.bar_w, thumb_h)
        pygame.draw.rect(self.display, COLOR_LIGHT, thumb_rect)

    def translate_coords(self, x_mouse, y_mouse):
        """Translates pixel mouse coordinates to board square grid coordinates.

        Args:
            x_mouse (int): Mouse x coordinate in pixels.
            y_mouse (int): Mouse y coordinate in pixels.

        Returns:
            tuple[int, int]: The (col, row) coordinates on the chessboard grid.
        """
        return x_mouse // self.square_size, y_mouse // self.square_size

    def show_result(self, game, result):
        """Displays an overlay with the final match outcome dialog.

        Args:
            game (Game): The current game instance.
            result (str): Game termination status ('CHECKMATE', 'TIMEOUT', etc.).
        """
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.display.blit(overlay, (0, 0))

        dialog_w, dialog_h = int(self.width * 0.65), int(self.height * 0.5)
        dialog_rect = pygame.Rect(0, 0, dialog_w, dialog_h)
        dialog_rect.center = (self.width // 2, self.height // 2)

        pygame.draw.rect(self.display, COLOR_DARK, dialog_rect)

        if result in ("CHECKMATE", "TIMEOUT"):
            title = "CHECKMATE!" if result == "CHECKMATE" else "TIMEOUT!"
            winner = "Blacks" if game.turn == "W" else "Whites"
            subtitle = f"{winner} win"
        else:
            title = "STALEMATE!"
            subtitle = "Tie"

        self._render_text(title, 70, COLOR_LIGHT, center=(dialog_rect.centerx, dialog_rect.centery - 50))
        self._render_text(subtitle, 50, COLOR_LIGHT, center=(dialog_rect.centerx, dialog_rect.centery + 50))

        pygame.display.flip()

    def pawn_promotion_menu(self, game):
        """Renders the pawn promotion dialog overlay with selectable pieces.

        Args:
            game (Game): The current game instance.
        """
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.display.blit(overlay, (0, 0))

        dialog_w, dialog_h = 650, 200
        dialog_rect = pygame.Rect(0, 0, dialog_w, dialog_h)
        dialog_rect.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(self.display, COLOR_DARK, dialog_rect)

        card_size = 120
        gap = (dialog_w - (card_size * 4)) // 5
        card_y = dialog_rect.y + (dialog_h - card_size) // 2

        for i, piece_name in enumerate(PROMOTION_PIECES):
            card_x = dialog_rect.x + gap + i * (card_size + gap)
            card_rect = pygame.Rect(card_x, card_y, card_size, card_size)
            pygame.draw.rect(self.display, COLOR_LIGHT, card_rect)

            texture = f"{game.turn}{piece_name}"
            if texture in self.images:
                img_rect = self.images[texture].get_rect(center=card_rect.center)
                self.display.blit(self.images[texture], img_rect)

    def menu(self):
        """Renders the game start menu for selecting the game mode."""
        bg_surface = pygame.Surface((self.width, self.height))
        bg_surface.fill(COLOR_DARK)
        self.display.blit(bg_surface, (0, 0))

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.display.blit(overlay, (0, 0))

        dialog_w, dialog_h = 600, 400
        dialog_rect = pygame.Rect(0, 0, dialog_w, dialog_h)
        dialog_rect.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(self.display, COLOR_DARK, dialog_rect)

        self._render_text(
            "Select game mode:", 28, COLOR_LIGHT, 
            center=(dialog_rect.centerx, dialog_rect.y + 50)
        )

        card_w, card_h = 240, 240
        card_y = dialog_rect.y + 110
        gap = (dialog_w - (card_w * 2)) // 3

        card_ai = pygame.Rect(dialog_rect.x + gap, card_y, card_w, card_h)
        pygame.draw.rect(self.display, COLOR_LIGHT, card_ai)
        self._render_text("vs AI", 42, COLOR_DARK, center=card_ai.center)

        card_1v1 = pygame.Rect(card_ai.right + gap, card_y, card_w, card_h)
        pygame.draw.rect(self.display, COLOR_LIGHT, card_1v1)
        self._render_text("1vs1", 48, COLOR_DARK, center=card_1v1.center)
        
    def handle_scroll(self, y_offset: int, sens: int = 5):
        """Scrolls the move history view vertically.

        Args:
            y_offset (int): Mouse wheel scroll delta.
            sens (int, optional): Scroll sensitivity multiplier. Defaults to 5.
        """
        self.scroll_y += y_offset * sens

    def get_menu_selection(self, pos: tuple[int, int]) -> str | None:
        """Determines which game mode card was clicked in the start menu.

        Args:
            pos (tuple[int, int]): Screen coordinates (x, y) of the click.

        Returns:
            str or None: 'ai' for AI mode, '1vs1' for 2-player mode, or None.
        """
        # Se calculan las mismas cajas definidas en menu()
        dialog_x = (self.width - 600) // 2
        dialog_y = (self.height - 400) // 2
        gap = (600 - (240 * 2)) // 3
        card_y = dialog_y + 110

        ai_rect = pygame.Rect(dialog_x + gap, card_y, 240, 240)
        pvp_rect = pygame.Rect(ai_rect.right + gap, card_y, 240, 240)

        if ai_rect.collidepoint(pos):
            return "ai"
        if pvp_rect.collidepoint(pos):
            return "1vs1"
        return None

    def get_promotion_selection(self, pos: tuple[int, int]) -> str | None:
        """Determines which piece was selected from the promotion menu.

        Args:
            pos (tuple[int, int]): Screen coordinates (x, y) of the click.

        Returns:
            str or None: Piece abbreviation ('Q', 'R', 'B', 'N') or None if not clicked.
        """
        dialog_w, dialog_h = 650, 200
        dialog_rect = pygame.Rect(0, 0, dialog_w, dialog_h)
        dialog_rect.center = (self.width // 2, self.height // 2)

        card_size = 120
        gap = (dialog_w - (card_size * 4)) // 5
        card_y = dialog_rect.y + (dialog_h - card_size) // 2
        
        piece_codes = ["Q", "R", "B", "N"]
        for i, code in enumerate(piece_codes):
            card_x = dialog_rect.x + gap + i * (card_size + gap)
            card_rect = pygame.Rect(card_x, card_y, card_size, card_size)
            if card_rect.collidepoint(pos):
                return code
        return None

    def get_sidebar_button(self, pos: tuple[int, int]) -> str | None:
        """Checks if a sidebar action button was clicked.

        Args:
            pos (tuple[int, int]): Screen coordinates (x, y) of the click.

        Returns:
            str or None: 'undo' or 'restart' if a button was clicked, None otherwise.
        """
        if self.undo_btn_rect.collidepoint(pos):
            return "undo"
        if self.restart_btn_rect.collidepoint(pos):
            return "restart"
        return None

    def is_in_board(self, pos: tuple[int, int]) -> bool:
        """Checks whether the given position lies inside the chessboard area.

        Args:
            pos (tuple[int, int]): Screen coordinates (x, y) of the position.

        Returns:
            bool: True if position is within chessboard bounds, False otherwise.
        """
        x, y = pos
        return 0 <= x < self.panel_x and 0 <= y < self.height

    def update_display(self, game, selected_square, promotion, menu):
        """Redraws the interface elements and flips the display buffer.

        Args:
            game (Game): The current game instance.
            selected_square (tuple or None): The currently selected square (x, y) or None.
            promotion (bool): True if the promotion dialog is active.
            menu (bool): True if the main menu is active.

        Returns:
            None
        """
        if menu:
            self.menu()
            pygame.display.flip()
            return None

        self.draw_board()
        self.draw_information(game)

        if selected_square is not None and selected_square[0] < BOARD_DIMENSION:
            x, y = selected_square
            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight.fill(COLOR_HIGHLIGHT)
            self.display.blit(highlight, (x * self.square_size, y * self.square_size))

        self.draw_pieces(game.board)

        if promotion:
            self.pawn_promotion_menu(game)

        pygame.display.flip()