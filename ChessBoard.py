from typing import List, Dict, Tuple, Any
from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece
from PieceMapping import PieceMapping


class ChessBoard:
    def __init__(self, rows: int, columns: int, board: List[List[ChessBoardPiece]]=None):
        self.rows = rows
        self.columns = columns
        self.board: List[List[ChessBoardPiece]] = board if board else [[None for _ in range(columns)] for _ in range(rows)]

    def to_json(self):
        return {
            "rows": self.rows,
            "columns": self.columns,
            "board": [[str(piece) if piece else None for piece in row] for row in self.board]
        }
    
    @classmethod
    def from_json(cls, json_data):
        rows = json_data['rows']
        columns = json_data['columns']
        board = [[ChessBoardPiece.from_string(piece) if piece else None for piece in row] for row in json_data['board']]
        return cls(rows, columns, board)

    def get_possible_moves(self, position: Tuple[int, int], piece: ChessPiece) -> List[Tuple[int, int]]:
        
        # validation
        row, col = (position)
        if not self.is_valid_position(row, col):
            return []
        board_piece: ChessBoardPiece = self.board[row][col]
        if board_piece is None or piece is None:
            return []

        possible_moves: List[Tuple[int, int]] = []
        
        for di in piece.directions:     # in each direction
            steps_made = 0              # we can move X steps
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

    def select_piece(self, piece_mapping: PieceMapping, player_turn: str, clicked_row: int, clicked_col: int):
        
        # validation
        board_square = self.board[clicked_row][clicked_col]
        if board_square is None or board_square.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            return [], None
        
        # initialization
        piece = piece_mapping.get_piece(board_square.piece)
        position = (clicked_row, clicked_col)
        possible_moves: List[Tuple[int, int]] = self.get_possible_moves(position, piece)
        if not possible_moves:
            print(f"No possible moves from ({clicked_row}, {clicked_col})")
            return possible_moves, None

        # selection
        print(f"Possible moves: {possible_moves}")
        selected_square = (clicked_row, clicked_col)
        return possible_moves, selected_square

    def move_piece(self, selected_square: Tuple[int, int], white_pieces: List[Tuple[str, int, int]], \
                black_pieces: List[Tuple[str, int, int]], clicked_row: int, clicked_col: int, piece_mapping: PieceMapping) -> Tuple[list[Tuple[str, int, int]], Tuple[list[Tuple[str, int, int]]]]:

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

    def evaluate_position(self, white_pieces: list[tuple[str, int, int]], black_pieces: list[tuple[str, int, int]], piece_mapping: PieceMapping):
        total = 0
        for white_piece in white_pieces:
            cur_position: Tuple[int, int] = white_piece[1], white_piece[2]
            cur_piece = piece_mapping.get_piece(white_piece[0])

            mobility = len(self.get_possible_moves(cur_position, cur_piece))/cur_piece.max_cells_reachable
            added_value = mobility*cur_piece.value
            total += added_value
        for black_piece in black_pieces:
            cur_position: Tuple[int, int] = black_piece[1], black_piece[2]
            cur_piece = piece_mapping.get_piece(black_piece[0])

            mobility = len(self.get_possible_moves(cur_position, cur_piece))/cur_piece.max_cells_reachable
            added_value = mobility*cur_piece.value
            total -= added_value
        return total
