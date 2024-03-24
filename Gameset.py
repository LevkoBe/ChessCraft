from ast import List
import json

from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import setup_board, setup_pieces
from UserSupervisor import string_input


class Gameset:
    def __init__(self, pieces=None, board=None, special=None):
        self.pieces: List[ChessPiece] = pieces
        self.board: ChessBoard = board
        self.special: str = special

    def create_game(self):
        rows = int(string_input("Please enter the number of rows: ", "regex", options=r"^\d+$"))
        columns = int(string_input("Please enter the number of columns: ", "regex", options=r"^\d+$"))
        self.pieces: List[ChessPiece] = setup_pieces(rows, columns)
        self.board: ChessBoard = setup_board(rows, columns, [p.symbol for p in self.pieces])
        self.special: str = string_input("Please, tell which pieces should be captured to win the game (character): ", "select", [piece.symbol for piece in self.pieces])

    def save_game(self, filename):
        game_state = {
            "pieces": [piece.to_string() for piece in self.pieces],
            "board": self.board.to_json(),
            "special": self.special
        }
        with open(filename, "w") as f:
            json.dump(game_state, f)

    def load_game(self, filename):
        with open(filename, "r") as f:
            game_state = json.load(f)
            self.pieces = [ChessPiece.from_string(piece) for piece in game_state["pieces"]]
            self.board = ChessBoard.from_json(game_state["board"])
            self.special = game_state["special"]
