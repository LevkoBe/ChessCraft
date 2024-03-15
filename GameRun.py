

from typing import List
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece


def play_game(board: ChessBoard, pieces: List[ChessPiece]):
    player_turn = '-'
    while True:
        move = input(f"Enter the position of the {player_turn} piece you want to move (or 'quit' to end the game): ")
        if move == 'quit':
            return

        if not is_valid_input_format(move):
            print("Invalid input format. Please try again.")
            continue

        row, col = board.position_to_indices(move)

        if not board.is_valid_position(row, col):
            print("Invalid position. Please try again.")
            continue

        board_piece = board.board[row][col]

        if board_piece is None or board_piece.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            continue

        possible_moves = board.get_possible_moves(move, pieces)

        if possible_moves:
            print(f"Possible moves: {possible_moves}")
            target_move = input("Enter the position you want to move the piece to: ")
            if target_move in possible_moves:
                new_row, new_col = board.position_to_indices(target_move)
                board.board[new_row][new_col] = board_piece
                board.board[row][col] = None
                player_turn = '+' if player_turn == '-' else '-'
            else:
                print("Invalid move. Please try again.")
        else:
            print("No possible moves. Please try again.")

        board.render_board()

def is_valid_input_format(position: str) -> bool:
    if len(position) < 2:
        return False
    if not position[0].isalpha():
        return False
    if not position[1:].isdigit():
        return False
    return True
