from typing import List

from ChessPiece import ChessPiece
from GameRun import play_game
from GameSetup import setup_pieces, setup_board


def main():
    rows = int(input("Please enter the number of rows: "))
    columns = int(input("Please enter the number of columns: "))

    pieces = setup_pieces(rows, columns)

    board = setup_board(rows, columns)

    board.render_board()

    play_game(board, pieces)

if __name__ == "__main__":
    pieces: List[ChessPiece] = []
    main()
