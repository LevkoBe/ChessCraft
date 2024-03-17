
from typing import List
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import setup_pieces, setup_board
from GameRun import play_game
from UserSupervisor import string_input, list_input


def main():
    while True:
        action = string_input('What would you like to do? Either "create", or "choose" game to play: ', 'select', options=['create', 'choose', 'exit'])
        if action == 'create':
            rows = int(string_input("Please enter the number of rows: ", "regex", options=r"^\d+$"))
            columns = int(string_input("Please enter the number of columns: ", "regex", options=r"^\d+$"))

            pieces: List[ChessPiece] = setup_pieces(rows, columns)
            board: ChessBoard = setup_board(rows, columns, [p.symbol for p in pieces])
            special: str = string_input("Please, tell which pieces should be captured to win the game (character): ", "select", [piece.symbol for piece in pieces])

            play_game(board, pieces, special, rows, columns)
        elif action == 'choose':
            pass
        elif action == 'exit':
            return


if __name__ == "__main__":
    pieces: List[ChessPiece] = []
    main()
