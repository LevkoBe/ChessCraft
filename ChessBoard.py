from typing import List

from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece


class ChessBoard:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]

    def place_piece(self, row: int, col: int, piece: str, color: str):
        self.board[row][col] = ChessBoardPiece(piece, color)

    def render_board(self):
        print("     " + "    ".join(str(i + 1) for i in range(self.columns)))
        print("   " + "+".join(["----"] * self.columns))
        for i, row in enumerate(self.board):
            print(chr(ord('a') + i) + " | " + " | ".join(self.render_piece(cell) for cell in row) + " |")
            print("   " + "+".join(["----"] * self.columns))
    
    def render_piece(self, figure: str) -> str:
        if figure is None:
            return '  '
        else:
            return str(figure)

    def get_possible_moves(self, position: str, pieces: List[ChessPiece]) -> List[str]:
        row, col = self.position_to_indices(position)
        if not self.is_valid_position(row, col):
            return []

        board_piece = self.board[row][col]
        if board_piece is None:
            return []

        piece_symbol = board_piece.piece
        piece = None
        for p in pieces:
            if p.symbol == piece_symbol:
                piece = p
                break

        if piece is None:
            return []

        v_formula, h_formula = piece.v_move_formula, piece.h_move_formula
        a_values, b_values = piece.a_values, piece.b_values

        possible_moves = []

        for a in a_values:
            for b in b_values:
                v_steps = eval(v_formula.replace('a', str(a)).replace('b', str(b)))
                h_steps = eval(h_formula.replace('a', str(a)).replace('b', str(b)))
                new_row = row + (1 if board_piece.color == '+' else -1) * v_steps
                new_col = col + h_steps
                if self.is_valid_position(new_row, new_col):
                    possible_moves.append(self.indices_to_position(new_row, new_col))
        return possible_moves

    def position_to_indices(self, position: str) -> tuple:
        row = ord(position[0].lower()) - ord('a')
        col = int(position[1:]) - 1
        return row, col

    def indices_to_position(self, row: int, col: int) -> str:
        position = chr(ord('a') + row) + str(col + 1)
        return position

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.columns
