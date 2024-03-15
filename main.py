from typing import List

from ChessPiece import ChessPiece
from ChessBoard import ChessBoard


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


def main():
    rows = int(input("Please enter the number of rows: "))
    columns = int(input("Please enter the number of columns: "))
    board = ChessBoard(rows, columns)
    extreme_value = max(columns, rows)

    while True:
        action = input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ")
        if action == 'add':
            piece = add_piece(extreme_value)
            pieces.append(piece)
            print(f"{piece.name} added successfully.")
        elif action == 'next':
            break
        elif action == 'quit':
            return
        else:
            print("Invalid command. Please try again.")

    print("Please fill the board with the figures:")
    for i in range(rows):
        row_input = input().split()
        color = "+" if i <= rows // 2 else "-"
        for j in range(columns):
            if j < len(row_input):
                board.place_piece(i, j, row_input[j], color)
            else:
                board.board[i][j] = None

    board.render_board()

    player_turn = '-'
    while True:
        move = input(f"Enter the position of the {player_turn} piece you want to move (or 'quit' to end the game): ")
        if move == 'quit':
            return

        row, col = board.position_to_indices(move)

        if not board.is_valid_position(row, col):
            print("Invalid position. Please try again.")
            continue

        board_piece = board.board[row][col]

        if board_piece is None or board_piece.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            continue

        possible_moves = board.get_possible_moves(move, pieces)
        print(f"Possible moves: {possible_moves}")

        if possible_moves:
            target_move = input("Enter the position you want to move the piece to: ")
            if target_move in possible_moves:
                new_row, new_col = board.position_to_indices(target_move)
                board.board[new_row][new_col] = board_piece
                board.board[row][col] = None
                player_turn = '+' if player_turn == '-' else '-'  # Switch player's turn
            else:
                print("Invalid move. Please try again.")
        else:
            print("No possible moves. Please try again.")

        board.render_board()

if __name__ == "__main__":
    pieces: List[ChessPiece] = []
    main()
