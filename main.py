
from typing import List
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import setup_pieces, setup_board
from GameRun import play_game


def main():
    while True:
        action = input('What would you like to do either "create", or "choose" game to play: ')
        if action == 'create':
            rows = int(input("Please enter the number of rows: "))
            columns = int(input("Please enter the number of columns: "))

            pieces: List[ChessPiece] = setup_pieces(rows, columns)
            board: ChessBoard = setup_board(rows, columns)
            special: str = input("Please, tell which pieces should be captured to win the game (character): ")

            play_game(board, pieces, special, rows, columns)
        elif action == 'choose':
            pass


if __name__ == "__main__":
    pieces: List[ChessPiece] = []
    main()
