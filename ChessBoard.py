import logging
from typing import List, Dict, Tuple, Any
from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece
from PieceMapping import PieceMapping
import copy


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

    def get_possible_moves(self, row, col, piece: ChessPiece) -> List[Tuple[int, int]]:
        
        # validation
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
                new_row = current_row + (1 if board_piece.color == 'b' else -1) * di[0]
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
        possible_moves: List[Tuple[int, int]] = self.get_possible_moves(clicked_row, clicked_col, piece)
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
        if current_piece.color == 'w':
            white_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in white_pieces]
        else:
            black_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == selected_square[0] and piece[2] == selected_square[1]
                            else piece for piece in black_pieces]
        self.board[selected_square[0]][selected_square[1]] = None
        self.board[clicked_row][clicked_col] = current_piece

        # remove the piece standing on the target cell
        if target_cell is not None:
            if target_cell.color == 'b':
                black_pieces = [piece for piece in black_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
            else:
                white_pieces = [piece for piece in white_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
        return white_pieces, black_pieces

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.columns  
    
    def evaluate_position(self, white_pieces: List[Tuple[str, int, int]], black_pieces: List[Tuple[str, int, int]], piece_mapping: PieceMapping) -> float:
        # LevkoBe: current position evaluation:
            # value: piece value
            # mobility: possible_moves / by max_cells_reachable
            # attacked - attacking (targeting): sum(other_piece.value / self.value) (* 100 if other_piece.special)
                # -- the bigger proportion is the better (imagine 'pawn takes queen' and vice versa)
            # protected - defending (targeting): sum(other_piece.value / self.value)
                # -- again, big proportion is good, as pricey pieces are better to be moving on the board, 
                # while "pawns" can stay when they are, defending others
            # advanced: (cur_row / max_row) * self.value (* 10 if self.promotion)
        # therefore, formula is:
            # ((mobility + advanced) * value) + (targeting / value)
        # estimated ranges for each property:
            # mobility: 0 - 1
            # advanced: 0 - 1
            # targeting: 0 - ?
        # Nevertheless, coefficients can be added, as well as other criterias
        total_for_white = self._calculate_evaluation(white_pieces, piece_mapping, True)
        total_for_black = self._calculate_evaluation(black_pieces, piece_mapping, False)
        print(f"white: {total_for_white}")
        print(f"black: {total_for_black}")
        return total_for_white - total_for_black

    def _calculate_evaluation(self, pieces: List[Tuple[str, int, int]], piece_mapping: PieceMapping, is_white: bool) -> float:
        total = 0
        max_row = self.rows - 1

        for piece_data in pieces:
            piece_symbol, cur_row, cur_col = piece_data
            cur_piece = piece_mapping.get_piece(piece_symbol)
            board_piece = self.board[cur_row][cur_col]
            if board_piece is None or cur_piece is None:
                logging.warning(f"Inconsistent data for piece at row {cur_row}, column {cur_col}") # Not supposed to happen
                continue

            mobility = 0
            advanced = (max_row - cur_row) / max_row if is_white else cur_row / max_row
            # if self.promotion: advanced *= 10
            targeting = 0

            for di in cur_piece.directions:
                steps_made = 0
                current_row = cur_row
                current_col = cur_col
                while steps_made < cur_piece.max_steps:
                    steps_made += 1
                    new_row = current_row + (1 if board_piece.color == 'b' else -1) * di[0]
                    new_col = current_col + di[1]
                    if not self.is_valid_position(new_row, new_col):
                        break
                    target_square = self.board[new_row][new_col]
                    if target_square is None:
                        mobility += 1
                        current_row = new_row
                        current_col = new_col
                        continue
                    if target_square.color == board_piece.color:
                        targeting += piece_mapping.get_piece(target_square.piece).value
                        break
                    if target_square.color != board_piece.color:
                        mobility += 1
                        targeting += piece_mapping.get_piece(target_square.piece).value * 100 if piece_mapping.get_piece(target_square.piece).is_special else piece_mapping.get_piece(target_square.piece).value
                        break
            
            current_value = ((mobility / piece_mapping.get_piece(piece_symbol).max_cells_reachable + advanced) * cur_piece.value) + (targeting / cur_piece.value)
            total += current_value

        return total
    

    def minimax(self, white_pieces, black_pieces, cur_pos:Tuple[int, int], cur_move:Tuple[int, int], max_depth:int, player_turn, piece_mapping, curdepth=0):
        # make local copies of everything
        local_board = copy.deepcopy(self)
        white_pieces_local = copy.deepcopy(white_pieces)
        black_pieces_local = copy.deepcopy(black_pieces)
        player_turn_local = player_turn

        # move piece, increase depth, change player turn
        white_pieces_local, black_pieces_local = local_board.move_piece(cur_pos, white_pieces_local, black_pieces_local,cur_move[0], cur_move[1], piece_mapping)
        curdepth += 1
        player_turn_local = ("b" if player_turn_local == "w" else "w")

        # change if it is an edge case
        if not any(piece_mapping.get_piece(p[0]).is_special for p in white_pieces_local):
            return -100000
        if not any(piece_mapping.get_piece(p[0]).is_special for p in black_pieces_local):
            return 100000
        if curdepth == max_depth:
            return local_board.evaluate_position(white_pieces_local, black_pieces_local, piece_mapping)
        
        # find all values in children positions
        possible_positions_vals = []
        for piece in (white_pieces_local if player_turn_local == 'w' else black_pieces_local):
            symbol, row, col = piece
            cur_pos = (row, col)
            cur_piece = piece_mapping.get_piece(symbol)
            possible_moves: List[Tuple[int, int]] = local_board.get_possible_moves(row, col, cur_piece)

            for cur_move in possible_moves:
                cur_move_value = local_board.minimax(white_pieces_local, black_pieces_local, cur_pos, cur_move, max_depth, player_turn_local,piece_mapping, curdepth)
                possible_positions_vals.append(cur_move_value)
        # select max or min of children positions values (based on player's turn)
        value = (max(possible_positions_vals) if player_turn_local == "w" else min(possible_positions_vals))
        return value

    def find_best_move(self, white_pieces: List[Tuple[str, int, int]], black_pieces: List[Tuple[str, int, int]], piece_mapping: PieceMapping, player_turn):
        move_to_value = {}
        maximal_depth = 2

        for piece in (white_pieces if player_turn == 'w' else black_pieces):
            symbol, row, col = piece
            cur_pos = (row, col)
            cur_piece = piece_mapping.get_piece(symbol)
            possible_moves: List[Tuple[int, int]] = self.get_possible_moves(row, col, cur_piece)

            for cur_move in possible_moves:
                cur_move_value = self.minimax(white_pieces, black_pieces,cur_pos, cur_move, maximal_depth, player_turn,piece_mapping)
                move_to_value[cur_move, symbol, row, col] = cur_move_value

        best_move = (max(move_to_value, key=move_to_value.get) if player_turn == 'w' else min(move_to_value, key=move_to_value.get))
        return best_move