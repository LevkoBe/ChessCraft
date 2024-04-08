import json
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from GameSetup import setup_board, setup_pieces
from UserSupervisor import list_input, string_input
from PieceMapping import PieceMapping
import random

class Gameset:
    def __init__(self, pieces=None, board=None):
        self.pieces: list[ChessPiece] = pieces
        self.board: ChessBoard = board
        self.piece_mapping: PieceMapping = PieceMapping()
        # coefficients for: mobility, advancement, targeting, and special
        self.white_coefficients: tuple[int, int, int, int] = (1, 1, 1, 100)
        self.black_coefficients: tuple[int, int, int, int] = (1, 1, 1, 100)
        if pieces:
            self.piece_mapping.set_all_pieces(pieces)
    
    def randomize_coefficients(self, randomize_white=False, randomize_black=True, extent: float = 0.5):
        randomized_coefficients = []
        
        if randomize_white:
            for coef in self.white_coefficients:
                randomized_coef = coef * random.uniform(1 - extent, 1 + extent)
                randomized_coefficients.append(randomized_coef)
        
            self.white_coefficients = tuple(randomized_coefficients)
        
        randomized_coefficients = []
        
        if randomize_black:
            for coef in self.black_coefficients:
                randomized_coef = coef * random.uniform(1 - extent, 1 + extent)
                randomized_coefficients.append(randomized_coef)
        
            self.black_coefficients = tuple(randomized_coefficients)

    def create_game(self):
        rows = int(string_input("Please enter the number of rows: ", "regex", options=r"^\d+$"))
        columns = int(string_input("Please enter the number of columns: ", "regex", options=r"^\d+$"))
        self.pieces: list[ChessPiece] = setup_pieces(rows, columns)
        self.board: ChessBoard = setup_board(rows, columns, [p.symbol for p in self.pieces])
        self.piece_mapping.set_all_pieces(self.pieces)
        self.set_specials()

    def set_specials(self):
        specials = list_input("Please, tell which pieces should be captured to win the game (characters): ",
                   "select", [piece.symbol for piece in self.pieces])
        for special in specials:
            self.piece_mapping.get_piece(special).is_special = True

    def save_game(self, filename):
        game_state = {
            "pieces": [piece.to_string() for piece in self.pieces],
            "board": self.board.to_json()
        }
        with open(filename, "w") as f:
            json.dump(game_state, f)

    def load_game(self, filename):
        with open(filename, "r") as f:
            game_state = json.load(f)
            self.pieces = [ChessPiece.from_string(piece) for piece in game_state["pieces"]]
            self.board = ChessBoard.from_json(game_state["board"])
            self.piece_mapping.set_all_pieces(self.pieces)
