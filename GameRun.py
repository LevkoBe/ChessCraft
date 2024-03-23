from typing import List, Tuple
import pygame
from pygame.locals import *

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from Gameset import Gameset
from GameSetup import white_black_division

BACKGROUND_COLOR = "#8B4513"
BOARD_COLOR = "#D2B48C"
square_size = 80
HIGHLIGHT_COLOR = (255, 255, 0)

PLAYER1_COLOR = "#45ab89"
PLAYER2_COLOR = "#FFD833"


def render_board(screen, board, rows, columns, possible_moves: List[Tuple[int, int]], selected_square: Tuple[int, int], pieces: List[ChessPiece]):
    # board
    for row in range(rows):
        for col in range(columns):
            color = BOARD_COLOR if (row + col) % 2 == 0 else BACKGROUND_COLOR
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

    # pieces
    for row in range(rows):
        for col in range(columns):
            piece = board.board[row][col]
            if piece is not None: # and is visible
                chess_piece = next((p for p in pieces if p.symbol == piece.piece), None)
                if chess_piece is not None and chess_piece.invisible:
                    continue
                
                symbol = piece.piece
                font = pygame.font.Font(None, 36)
                if piece.color == '+':
                    text_color = PLAYER1_COLOR
                else:
                    text_color = PLAYER2_COLOR
                text = font.render(symbol, True, text_color)
                text_rect = text.get_rect(center=(col * square_size + square_size // 2, row * square_size + square_size // 2))
                screen.blit(text, text_rect)

    # selected piece
    if selected_square is not None:
        row, col = selected_square
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * square_size, row * square_size, square_size, square_size), 3)

    # possible moves
    for move in possible_moves:
        row, col = move
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * square_size, row * square_size, square_size, square_size), 3)


def set_window_dimensions(rows: int, columns: int):
    global square_size, screen_width, screen_height
    screen_width = 800
    screen_height = 600

    max_horizontal_squares = screen_width // columns
    max_vertical_squares = screen_height // rows

    square_size = min(max_horizontal_squares, max_vertical_squares)

    screen_width = columns * square_size
    screen_height = rows * square_size
    return screen_width, screen_height


def process_mouse_click(board: ChessBoard, pieces: List[ChessPiece], player_turn: str, selected_square: Tuple[int, int], \
                        possible_moves: List[Tuple[int, int]], white_pieces: List[Tuple[str, int, int]], \
                        black_pieces: List[Tuple[str, int, int]], optional: str) -> Tuple[List[Tuple[int, int]], str, Tuple[int, int]]:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked_row = mouse_y // square_size
    clicked_col = mouse_x // square_size
    print(f"Clicked on square ({clicked_row}, {clicked_col})")

    # select piece
    if selected_square is None:
        possible_moves, selected_square, optional = board.select_piece(pieces, player_turn, clicked_row, clicked_col)

    # move piece
    elif (clicked_row, clicked_col) in possible_moves:
        pieces_chars = [p.symbol for p in pieces]
        white_pieces, black_pieces = board.move_piece(selected_square, white_pieces, black_pieces, clicked_row, clicked_col, optional, pieces_chars)
        player_turn = '+' if player_turn == '-' else '-'
        selected_square = None
        possible_moves = []
    else:
        # unselect piece
        print(f"Invalid move from {selected_square} to ({clicked_row}, {clicked_col})")
        selected_square = None
        possible_moves = []

    return possible_moves, player_turn, selected_square, white_pieces, black_pieces, optional


def play_game(game: Gameset):
    set_window_dimensions(game.board.rows, game.board.columns)
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("NO-Chess Game")

    clock = pygame.time.Clock()

    player_turn = '-'
    running = True
    optional = ""
    selected_square: Tuple[int, int] = None
    possible_moves: List[Tuple[int, int]] = []
    white_pieces, black_pieces = white_black_division(game.board)
    while running:
        # move pieces
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                possible_moves, player_turn, selected_square, white_pieces, black_pieces, optional = \
                    process_mouse_click(game.board, game.pieces, player_turn, selected_square, \
                                        possible_moves, white_pieces, black_pieces, optional)
        
        # check winners
        if game.special not in [p[0] for p in white_pieces]:
            print("Second player won!")
            break
        if game.special not in [p[0] for p in black_pieces]:
            print("First player won!")
            break

        # render board
        screen.fill(BACKGROUND_COLOR)
        render_board(screen, game.board, game.board.rows, game.board.columns, possible_moves, selected_square, game.pieces)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
