from typing import List, Tuple

from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece


class ChessBoard:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.board: List[List[ChessBoardPiece]] = [[None for _ in range(columns)] for _ in range(rows)]

    def get_possible_moves(self, position: Tuple[int, int], piece: ChessPiece) -> List[str]:
        row, col = (position)
        if not self.is_valid_position(row, col):
            return []

        board_piece: ChessPiece = self.board[row][col]
        if board_piece is None or piece is None:
            return []

        possible_moves: List[Tuple[int, int]] = []
        
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
                target_square = self.board[new_row][new_col]
                if target_square is None:
                    possible_moves.append((new_row, new_col))
                    current_row = new_row
                    current_col = new_col
                    continue
                if target_square.color == board_piece.color:
                    break
                if target_square.color != board_piece.color:
                    possible_moves.append((new_row, new_col))
                    break
        return possible_moves

    def select_piece(self, pieces: List[ChessPiece], player_turn: str, clicked_row: int, clicked_col: int):
        board_square = self.board[clicked_row][clicked_col]
        if board_square is None or board_square.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            return [], None
        piece = None
        for p in pieces:
            if p.symbol == board_square.piece:
                piece = p
                break
        position = (clicked_row, clicked_col)
        possible_moves: List[Tuple[int, int]] = self.get_possible_moves(position, piece)
        if not possible_moves:
            print(f"No possible moves from ({clicked_row}, {clicked_col})")
            return possible_moves, None
        selected_square = (clicked_row, clicked_col)
        print(f"Possible moves: {possible_moves}")

        return possible_moves, selected_square

    def move_piece(self, selected_square: Tuple[int, int], white_pieces: List[Tuple[str, int, int]], \
                black_pieces: List[Tuple[str, int, int]], clicked_row: int, clicked_col: int) -> Tuple[List[Tuple[int, int]], str, Tuple[int, int]]:

        print(f"Move from {selected_square} to ({clicked_row}, {clicked_col})")
        target_cell = self.board[clicked_row][clicked_col]
        current_piece = self.board[selected_square[0]][selected_square[1]]

        # change the position of the piece
        if current_piece.color == '-':
            white_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in white_pieces]
        else:
            black_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in black_pieces]
        self.board[selected_square[0]][selected_square[1]] = None
        self.board[clicked_row][clicked_col] = current_piece

        # remove the piece standing on the target cell
        if target_cell is not None:
            if target_cell.color == '+':
                black_pieces = [piece for piece in black_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
            else:
                white_pieces = [piece for piece in white_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
        
        return white_pieces, black_pieces

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.columns
