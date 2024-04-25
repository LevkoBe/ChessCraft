from ChessBoard import ChessBoard
from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece
from UserSupervisor import string_input, list_input

class GameSetup:
    def __init__(self):
        self.rows: int = None
        self.columns: int = None
        self.pieces: list[ChessPiece] = []
        self.board: ChessBoard = None

    def setup_pieces(self) -> list[ChessPiece]:
        while True:
            action = string_input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ", input_type="select", options=["add", "next", "quit"])
            if action == 'add':
                piece = self.add_piece([p.symbol for p in self.pieces])
                self.pieces.append(piece)
                print(f"{piece.name} added successfully.")
            elif action == 'next':
                break
            elif action == 'quit':
                return self.pieces
            else:
                print("Invalid command. Please try again.")
        return self.pieces

    def setup_board(self) -> ChessBoard:
        self.rows = int(string_input("Please enter the number of rows: ", "regex", options=r"^\d+$"))
        self.columns = int(string_input("Please enter the number of columns: ", "regex", options=r"^\d+$"))
        self.board = ChessBoard(self.rows, self.columns)
        
    def fill_board(self) -> ChessBoard:
        print("Please fill the board with the figures:")
        for i in range(self.rows):
            row_input = list_input(f"Row {i} |", "select", options=[p.symbol for p in self.pieces] + [''])
            color = "b" if i <= self.rows // 2 else "w"
            for j in range(self.columns):
                if j < len(row_input) and row_input[j]:
                    self.board.board[i][j] = ChessBoardPiece(row_input[j], color)
                else:
                    self.board.board[i][j] = None
        return self.board

    def add_piece(self, pieces: list[str]) -> ChessPiece:
        name = input("Please, enter the name of the piece: ")
        symbol = string_input("Please, enter the character to represent the piece: ", "regex", options=r"^.$", prohibited=pieces)
        directions = list_input("Please, enter the possible directions of moves (++, or +2,-3 format): ", "regex", options=r"^[+-0][+-0]$|^[+-]\d+,[+-]\d+$")
        steps = int(string_input("Please, enter the maximum number of steps in any direction: ", "regex", options=r"^\d+$"))
        optional = list_input("Optional parameters: ", "select", options=['n', 'p', 'c', 's', 'v', 'u', 'd', 'i', 'g', 'f', ''])
        piece = ChessPiece(name, symbol, directions, steps, optional)
        piece.calculate_reachable_cells_stats(self.rows, self.columns)
        return piece

    @staticmethod
    def white_black_division(board: ChessBoard):
        white_pieces: list[tuple[str, int, int]] = []
        black_pieces: list[tuple[str, int, int]] = []
        for row in range(board.rows):
            for col in range(board.columns):
                piece = board.board[row][col]
                if piece is not None:
                    if piece.color == 'w':
                        white_pieces.append((piece.piece, row, col))
                    else:
                        black_pieces.append((piece.piece, row, col))
        return white_pieces, black_pieces
