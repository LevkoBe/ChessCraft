from typing import List

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece


def setup_pieces(rows: int, columns: int) -> List[ChessPiece]:
    pieces: List[ChessPiece] = []
    while True:
        action = input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ")
        if action == 'add':
            piece = add_piece(max(columns, rows))
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


def add_piece(extreme_value: int) -> ChessPiece:
    name = input("Please enter the name of the piece: ")
    symbol = input("Please enter the character to represent the piece: ")
    v_move_formula = input("Please enter the formula for its vertical moves: ")
    h_move_formula = input("Please enter the formula for its horizontal moves: ")

    a_values, b_values = "", ""
    if 'a' in h_move_formula or 'a' in v_move_formula:
        a_values = input("Please enter the possible values for variable 'a' (c:c/c,c,c): ")
    if 'b' in h_move_formula or 'b' in v_move_formula:
        b_values = input("Please enter the possible values for variable 'b' (c:c/c,c,c): ")

    return ChessPiece(name, symbol, h_move_formula, v_move_formula, a_values, b_values, extreme_value)

