from typing import List, Tuple
import pygame
from pygame.locals import *

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import white_black_division

BACKGROUND_COLOR = "#8B4513"
BOARD_COLOR = "#D2B48C"
square_size = 80
HIGHLIGHT_COLOR = (255, 255, 0)

PLAYER1_COLOR = "#45ab89"
PLAYER2_COLOR = "#FFD833"


def render_board(screen, board, rows, columns, possible_moves: List[Tuple[int, int]], selected_square: Tuple[int, int]):
    for row in range(rows):
        for col in range(columns):
            color = BOARD_COLOR if (row + col) % 2 == 0 else BACKGROUND_COLOR
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

    for row in range(rows):
        for col in range(columns):
            piece = board.board[row][col]
            if piece is not None:
                symbol = piece.piece
                font = pygame.font.Font(None, 36)
                if piece.color == '+':
                    text_color = PLAYER1_COLOR
                else:
                    text_color = PLAYER2_COLOR
                text = font.render(symbol, True, text_color)
                text_rect = text.get_rect(center=(col * square_size + square_size // 2, row * square_size + square_size // 2))
                screen.blit(text, text_rect)

    if selected_square is not None:
        row, col = selected_square
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * square_size, row * square_size, square_size, square_size), 3)

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



def process_mouse_click(board: ChessBoard, pieces: List[ChessPiece], player_turn: str, selected_square: Tuple[int, int], possible_moves: List[Tuple[int, int]], white_pieces: List[Tuple[str, int, int]], black_pieces: List[Tuple[str, int, int]], special: str) -> Tuple[List[Tuple[int, int]], str, Tuple[int, int]]:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked_row = mouse_y // square_size
    clicked_col = mouse_x // square_size
    print(f"Clicked on square ({clicked_row}, {clicked_col})")

    if selected_square is None:
        board_piece = board.board[clicked_row][clicked_col]
        if board_piece is None or board_piece.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            return possible_moves, player_turn, selected_square, white_pieces, black_pieces
        selected_square = (clicked_row, clicked_col)
        position = board.indices_to_position(clicked_row, clicked_col)
        possible_moves = board.get_possible_moves(position, pieces)
        if not possible_moves:
            print(f"No possible moves from {selected_square} to ({clicked_row}, {clicked_col})")
            selected_square = None
            return possible_moves, player_turn, selected_square, white_pieces, black_pieces
        print(f"Possible moves: {possible_moves}")
    elif board.indices_to_position(clicked_row, clicked_col) in possible_moves:
        print(f"Move from {selected_square} to ({clicked_row}, {clicked_col})")
        target_cell = board.board[clicked_row][clicked_col]
        current_piece = board.board[selected_square[0]][selected_square[1]]
        if current_piece.color == '-':
            white_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in white_pieces]
        else:
            black_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in black_pieces]
        board.board[clicked_row][clicked_col] = current_piece
        if target_cell is not None:
            if target_cell.color == '+':
                black_pieces = [piece for piece in black_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
            else:
                white_pieces = [piece for piece in white_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
        board.board[selected_square[0]][selected_square[1]] = None
        player_turn = '+' if player_turn == '-' else '-'
        selected_square = None
        possible_moves = []
    else:
        print(f"Invalid move from {selected_square} to ({clicked_row}, {clicked_col})")
        selected_square = None

    return possible_moves, player_turn, selected_square, white_pieces, black_pieces



def play_game(board: ChessBoard, pieces: List[ChessPiece], special: str, rows: int, columns: int):
    set_window_dimensions(rows, columns)
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("NO-Chess Game")

    clock = pygame.time.Clock()

    player_turn = '-'
    running = True
    selected_square: Tuple[int, int] = None
    possible_moves: List[Tuple[int, int]] = []
    white_pieces, black_pieces = white_black_division(board)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                possible_moves, player_turn, selected_square, white_pieces, black_pieces = process_mouse_click(board, pieces, player_turn, selected_square, possible_moves, white_pieces, black_pieces, special)
        if special not in [p[0] for p in white_pieces]:
            print("Second player won!")
            break
        if special not in [p[0] for p in black_pieces]:
            print("First player won!")
            break

        screen.fill(BACKGROUND_COLOR)
        numerical_possible_moves = [board.position_to_indices(move) for move in possible_moves] if possible_moves else []
        render_board(screen, board, rows, columns, numerical_possible_moves, selected_square)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()