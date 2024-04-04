from typing import List, Tuple

from ChessBoard import ChessBoard
from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece
from UserSupervisor import string_input, list_input


def setup_pieces(rows: int, cols: int) -> List[ChessPiece]:
    pieces: List[ChessPiece] = []
    while True:
        action = string_input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ", input_type="select", options=["add", "next", "quit"])
        if action == 'add':
            piece = add_piece([p.symbol for p in pieces], rows, cols)
            pieces.append(piece)
            print(f"{piece.name} added successfully.")
        elif action == 'next':
            break
        elif action == 'quit':
            return pieces
        else:
            print("Invalid command. Please try again.")
    return pieces


def setup_board(rows: int, columns: int, pieces: List[str]) -> ChessBoard:
    board = ChessBoard(rows, columns)
    
    print("Please fill the board with the figures:")
    for i in range(rows):
        row_input = list_input("", "select", options=pieces + [''])
        color = "b" if i <= rows // 2 else "w"
        for j in range(columns):
            if j < len(row_input) and row_input[j]:
                board.board[i][j] = ChessBoardPiece(row_input[j], color)
            else:
                board.board[i][j] = None
    return board


def add_piece(pieces: List[str], rows:int, cols:int) -> ChessPiece:
    name = input("Please, enter the name of the piece: ")
    symbol = string_input("Please, enter the character to represent the piece: ", "regex", options=r"^.$", prohibited=pieces)
    directions = list_input("Please, enter the possible directions of moves (++, or +2,-3 format): ", "regex", options=r"^[+-0][+-0]$|^[+-]\d+,[+-]\d+$")
    steps = int(string_input("Please, enter the maximum number of steps in any direction: ", "regex", options=r"^\d+$"))
    optional = list_input("Optional parameters: ", "select", options=['n', 'p', 'c', 's', 'v', 'u', 'd', 'i', 'g', 'f', ''])
    piece = ChessPiece(name, symbol, directions, steps, optional)
    piece.calculate_reachable_cells_stats(rows, cols)
    return piece


def white_black_division(board: ChessBoard):
    white_pieces: List[Tuple[str, int, int]] = []
    black_pieces: List[Tuple[str, int, int]] = []
    for row in range(board.rows):
        for col in range(board.columns):
            piece = board.board[row][col]
            if piece is not None:
                if piece.color == 'w':
                    white_pieces.append((piece.piece, row, col))
                else:
                    black_pieces.append((piece.piece, row, col))
    return white_pieces, black_pieces

