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

        possible_moves = []
        
        for di in piece.directions:
            steps_made = 0
            current_row = row
            current_col = col
            while steps_made < piece.max_steps:
                steps_made += 1
                new_row = current_row + (1 if board_piece.color == '+' else -1) * di[0]
                new_col = current_col + di[1]
                if not self.is_valid_position(new_row, new_col):
                    break
                possible_moves.append(self.indices_to_position(new_row, new_col))
                current_row = new_row
                current_col = new_col
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
