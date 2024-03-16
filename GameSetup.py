from typing import List, Tuple

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece


def setup_pieces(rows: int, columns: int) -> List[ChessPiece]:
    pieces: List[ChessPiece] = []
    while True:
        action = input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ")
        if action == 'add':
            piece = add_piece()
            pieces.append(piece)
            print(f"{piece.name} added successfully.")
        elif action == 'next':
            break
        elif action == 'quit':
            return pieces
        else:
            print("Invalid command. Please try again.")
    return pieces


def setup_board(rows: int, columns: int) -> ChessBoard:
    board = ChessBoard(rows, columns)
    
    print("Please fill the board with the figures:")
    for i in range(rows):
        row_input = input().split()
        color = "+" if i <= rows // 2 else "-"
        for j in range(columns):
            if j < len(row_input):
                board.place_piece(i, j, row_input[j], color)
            else:
                board.board[i][j] = None
    return board


def add_piece() -> ChessPiece:
    name = input("Please, enter the name of the piece: ")
    symbol = input("Please, enter the character to represent the piece: ")
    directions = input("Please, enter the possible directions of moves (++, or +2,-3 format): ").split(' ')
    steps = input("Please, enter the maximum number of steps in any direction: ")

    return ChessPiece(name, symbol, directions, steps)


def white_black_division(board: ChessBoard):
    white_pieces: List[Tuple[str, int, int]] = []
    black_pieces: List[Tuple[str, int, int]] = []
    for row in range(board.rows):
        for col in range(board.columns):
            piece = board.board[row][col]
            if piece is not None:
                if piece.color == '-':
                    white_pieces.append((piece.piece, row, col))
                else:
                    black_pieces.append((piece.piece, row, col))
    return white_pieces, black_pieces

