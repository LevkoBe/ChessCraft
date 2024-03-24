from ast import List

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import setup_board, setup_pieces
from UserSupervisor import list_input, string_input


class Gameset:
    def __init__(self, pieces=None, board=None, specials=None):
        self.pieces: List[ChessPiece] = pieces
        self.board: ChessBoard = board
        self.specials: List[str] = specials
        if not pieces or not board or not specials:
            self.create_game()

    def create_game(self):
        rows = int(string_input("Please enter the number of rows: ", "regex", options=r"^\d+$"))
        columns = int(string_input("Please enter the number of columns: ", "regex", options=r"^\d+$"))
        self.pieces: List[ChessPiece] = setup_pieces()
        self.board: ChessBoard = setup_board(rows, columns, [p.symbol for p in self.pieces])
        self.specials: List[str] = list_input("Please, tell which pieces should be captured to win the game (characters): ", "select", [piece.symbol for piece in self.pieces])

