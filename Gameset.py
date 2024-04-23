import json
import random
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece
from PieceMapping import PieceMapping
from GameSetup import GameSetup
from UserSupervisor import list_input

class Gameset:
    def __init__(self, pieces=None, board=None):
        self.pieces: list[ChessPiece] = pieces
        self.board: ChessBoard = board
        self.piece_mapping: PieceMapping = PieceMapping()
        # Coefficients for: mobility, advancement, targeting, and special
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
        game_setup = GameSetup()
        game_setup.setup_board()
        self.pieces: list[ChessPiece] = game_setup.setup_pieces()
        self.board: ChessBoard = game_setup.fill_board()
        self.piece_mapping.set_all_pieces(game_setup.pieces)
        self.set_specials()

    def set_specials(self):
        specials = list_input("Please, tell which pieces should be captured to win the game (characters): ",
                   "select", [piece.symbol for piece in self.pieces])
        for special in specials:
            self.piece_mapping.get_piece(special).is_special = True

    def save_game(self, filename):
        game_state = {
            "pieces": [piece.to_string() for piece in self.pieces],
            "board": self.board.to_json(),
            "white_coefficients": self.white_coefficients,
            "black_coefficients": self.black_coefficients
        }
        with open(filename, "w") as f:
            json.dump(game_state, f)

    def load_game(self, filename):
        with open(filename, "r") as f:
            game_state = json.load(f)
            self.pieces = [ChessPiece.from_string(piece) for piece in game_state["pieces"]]
            self.board = ChessBoard.from_json(game_state["board"])
            self.piece_mapping.set_all_pieces(self.pieces)
            self.white_coefficients = tuple(game_state["white_coefficients"])
            self.black_coefficients = tuple(game_state["black_coefficients"])
