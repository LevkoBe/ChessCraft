from typing import List, Tuple
import pygame
from pygame.locals import *

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import white_black_division
from Gameset import Gameset
from PieceMapping import PieceMapping

BACKGROUND_COLOR = "#8B4513"
BOARD_COLOR = "#D2B48C"
square_size = 80
HIGHLIGHT_COLOR = (255, 255, 0)

PLAYER1_COLOR = "#45ab89"
PLAYER2_COLOR = "#FFD833"


def render_board(screen, board, rows, columns, possible_moves: List[Tuple[int, int]], selected_square: Tuple[int, int]):
    screen.fill(BACKGROUND_COLOR)
    # board
    for row in range(rows):
        for col in range(columns):
            color = BOARD_COLOR if (row + col) % 2 == 0 else BACKGROUND_COLOR
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

    # pieces
    for row in range(rows):
        for col in range(columns):
            piece = board.board[row][col]
            if piece is not None:
                symbol = piece.piece
                font = pygame.font.Font(None, 36)
                if piece.color == 'b':
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
    
    pygame.display.flip()


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


def process_mouse_click(board: ChessBoard, piece_mapping: PieceMapping, player_turn: str, selected_square: Tuple[int, int], possible_moves: List[Tuple[int, int]], white_pieces: List[Tuple[str, int, int]], black_pieces: List[Tuple[str, int, int]]) -> Tuple[List[Tuple[int, int]], str, Tuple[int, int]]:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked_row = mouse_y // square_size
    clicked_col = mouse_x // square_size
    print(f"Clicked on square ({clicked_row}, {clicked_col})")

    # select piece
    if selected_square is None:
        possible_moves, selected_square = board.select_piece(piece_mapping, player_turn, clicked_row, clicked_col)

    # move piece
    elif (clicked_row, clicked_col) in possible_moves:
        white_pieces, black_pieces = board.move_piece(selected_square, white_pieces, black_pieces, clicked_row, clicked_col, piece_mapping)
        print(f"Move from {selected_square} to ({clicked_row}, {clicked_col})")
        player_turn = 'b' if player_turn == 'w' else 'w'
        selected_square = None
        possible_moves = []

        # evaluate position
        value_of_position = board.evaluate_position(white_pieces, black_pieces, piece_mapping)
        print(f"Position is evaluated as {value_of_position}")

        # find best move (currently i will put this functionality here
        best_move = board.find_best_move(white_pieces, black_pieces, piece_mapping, player_turn)
        print(f"best move is by {best_move[1]} from {best_move[2]}, {best_move[3]} to {best_move[0]}")
    else:
        # unselect piece
        print(f"Invalid move from {selected_square} to ({clicked_row}, {clicked_col})")
        selected_square = None
        possible_moves = []

    return possible_moves, player_turn, selected_square, white_pieces, black_pieces


def play_game(game: Gameset):
    set_window_dimensions(game.board.rows, game.board.columns)
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("NO-Chess Game")

    clock = pygame.time.Clock()

    player_turn = 'w'
    running = True
    selected_square: Tuple[int, int] = None
    possible_moves: List[Tuple[int, int]] = []
    white_pieces, black_pieces = white_black_division(game.board)

    render_board(screen, game.board, game.board.rows, game.board.columns, possible_moves, selected_square)
    while running:
        # move pieces
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                possible_moves, player_turn, selected_square, white_pieces, black_pieces = \
                    process_mouse_click(game.board, game.piece_mapping, player_turn, selected_square, possible_moves, white_pieces, black_pieces)
        
                # check winners
                if not any(game.piece_mapping.get_piece(p[0]).is_special for p in white_pieces):
                    print("Second player won!")
                    break
                if not any(game.piece_mapping.get_piece(p[0]).is_special for p in black_pieces):
                    print("First player won!")
                    break

                # render board
                render_board(screen, game.board, game.board.rows, game.board.columns, possible_moves, selected_square)

        clock.tick(30)

    pygame.quit()
