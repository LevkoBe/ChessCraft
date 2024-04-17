
import os
import pygame
from ChessBoard import ChessBoard
from PieceMapping import PieceMapping


BACKGROUND_COLOR = "#8B4513"
BOARD_COLOR = "#D2B48C"
HIGHLIGHT_COLOR = (255, 255, 0)

PLAYER1_COLOR = "#45ab89"
PLAYER2_COLOR = "#FFD833"
SVG_FOLDER = "./SVGs"
PIECE_SIZE = (64, 64)


class GameUI:
    def __init__(self, board: ChessBoard):
        self.square_size = 80
        screen_width, screen_height = self.set_window_dimensions(board.rows, board.columns)
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("NO-Chess Game")
        self.clock = pygame.time.Clock()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def render_board(self, board: ChessBoard, rows: int, columns: int, possible_moves: list[tuple[int, int]],
                    selected_square: tuple[int, int], piece_mapping: PieceMapping):
        self.screen.fill(BACKGROUND_COLOR)
        # board
        for row in range(rows):
            for col in range(columns):
                color = BOARD_COLOR if (row + col) % 2 == 0 else BACKGROUND_COLOR
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

        # pieces
        for row in range(rows):
            for col in range(columns):
                piece = board.board[row][col]
                if piece is not None: # todo: and is visible
                    if piece_mapping.get_piece(piece.piece).invisible:
                        continue
                    
                    symbol = piece.piece
                    font = pygame.font.Font(None, 36)
                    if piece.color == 'b':
                        player_color = PLAYER1_COLOR
                    else:
                        player_color = PLAYER2_COLOR
                    # Check if SVG file exists for the symbol
                    svg_file = os.path.join(SVG_FOLDER, f"{symbol}.svg")
                    if os.path.exists(svg_file):
                        # Change SVG color dynamically
                        with open(svg_file, "r", encoding='utf-8') as f:
                            content = f.read()
                        new_SVG = content.replace("black", player_color)
                        new_svg_file = "tmp/modified.svg"
                        with open(new_svg_file, "w", encoding='utf-8') as f:
                            f.write(new_SVG)
                        piece_image = pygame.image.load(new_svg_file)
                        piece_image.set_colorkey(pygame.Color(player_color))
                        piece_image = pygame.transform.scale(piece_image, PIECE_SIZE)
                        piece_rect = piece_image.get_rect(center=(col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2))
                        self.screen.blit(piece_image, piece_rect)
                    else:
                        # Render text if SVG file doesn't exist
                        text = font.render(symbol, True, player_color)
                        text_rect = text.get_rect(center=(col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2))
                        self.screen.blit(text, text_rect)

        # selected piece
        if selected_square is not None:
            row, col = selected_square
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)

        # possible moves
        for move in possible_moves:
            row, col, _ = move
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)
        
        pygame.display.flip()

    def get_mouse_click(self) -> tuple[int, int]:
        cheatcode = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    return mouse_y // self.square_size, mouse_x // self.square_size, cheatcode
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        cheatcode = ""
                    elif event.key == pygame.K_RETURN:
                        print(cheatcode)
                    elif event.unicode.isprintable():
                        cheatcode += event.unicode
            self.clock.tick(30)

    def set_window_dimensions(self, rows: int, columns: int):
        screen_width = 800
        screen_height = 600
        max_horizontal_squares = screen_width // columns
        max_vertical_squares = screen_height // rows
        self.square_size = min(max_horizontal_squares, max_vertical_squares)
        screen_width = columns * self.square_size
        screen_height = rows * self.square_size
        return screen_width, screen_height
