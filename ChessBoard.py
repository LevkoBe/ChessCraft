import logging
import copy
from typing import Optional
from ChessBoardPiece import ChessBoardPiece
from ChessPiece import ChessPiece
from PieceMapping import PieceMapping
import copy
from UserSupervisor import string_input


class ChessBoard:
    def __init__(self, rows: int, columns: int, board: list[list[ChessBoardPiece]] = None):
        self.rows = rows
        self.columns = columns
        self.board: list[list[ChessBoardPiece]] = board if board else [[None for _ in range(columns)] for _ in range(rows)]

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

    def get_possible_moves(self, row, col, piece: ChessPiece, color: str, piece_mapping: PieceMapping) -> list[tuple[int, int, str]]:

        # validation
        if not self.is_valid_position(row, col):
            return []
        board_piece: ChessBoardPiece = self.board[row][col]
        if board_piece is None or piece is None:
            return []
        
        if piece.ninja:
            return self.ninja_moves(piece, row, col, piece_mapping)

        possible_moves: list[tuple[int, int, str]] = []

        for di in piece.moves:      # in each direction
            steps_made = 0          # we can move X steps
            current_row = row
            current_col = col
            while steps_made < piece.max_steps:
                steps_made += 1
                new_row = current_row + (1 if board_piece.color == 'b' else -1) * di.x
                new_col = current_col + di.y
                if not self.is_valid_position(new_row, new_col):
                    break
                target_square = self.board[new_row][new_col]
                if target_square is None:
                    current_row = new_row
                    current_col = new_col
                    if piece.promotion and ((color == 'w' and new_row == 0) or (color == 'b' and new_row == self.rows - 1)):
                        for promotion_piece in piece_mapping.mapping.keys():
                            possible_moves.append((new_row, new_col, promotion_piece))
                    else:
                        possible_moves.append((new_row, new_col, ""))
                    continue
                if target_square.color == board_piece.color:
                    # fusion piece check
                    break
                if target_square.color != board_piece.color:
                    # unbreakable piece check
                    # shooter piece check
                    # insatiable piece check
                    if piece.promotion and ((color == 'w' and new_row == 0) or (color == 'b' and new_row == self.rows - 1)):
                        for promotion_piece in piece_mapping.mapping.keys():
                            possible_moves.append((new_row, new_col, promotion_piece))
                    else:
                        possible_moves.append((new_row, new_col, ""))
                    break
        return possible_moves

    def ninja_moves(self, piece: ChessPiece, row: int, col: int, piece_mapping: PieceMapping):
        possible_moves: list[tuple[int, int]] = []
        board_piece: ChessBoardPiece = self.board[row][col]

        def next_moves(row: int, col: int, steps_left: int): # alert: may be very costy
            if steps_left == 0:
                return
            for di in piece.moves:
                # validation
                new_row = row + (1 if board_piece.color == 'b' else -1) * di.x
                new_col = col + di.y
                if not self.is_valid_position(new_row, new_col) or (new_row, new_col) in possible_moves:
                    continue

                # recursion
                target_square = self.board[new_row][new_col]
                if target_square is None:
                    if piece.promotion and ((board_piece.color == 'w' and new_row == 0) or (board_piece.color == 'b' and new_row == self.rows - 1)):
                        for promotion_piece in piece_mapping.mapping.keys():
                            possible_moves.append((new_row, new_col, promotion_piece))
                    else:
                        possible_moves.append((new_row, new_col, ""))
                    next_moves(new_row, new_col, steps_left - 1)
                    continue

                # stop traversal
                if target_square.color == board_piece.color:
                    continue
                if target_square.color != board_piece.color:
                    if piece.promotion and ((board_piece.color == 'w' and new_row == 0) or (board_piece.color == 'b' and new_row == self.rows - 1)):
                        for promotion_piece in piece_mapping.mapping.keys():
                            possible_moves.append((new_row, new_col, promotion_piece))
                    else:
                        possible_moves.append((new_row, new_col, ""))
                    continue

        next_moves(row, col, piece.max_steps)

        return possible_moves             

    def select_piece(self, piece_mapping: PieceMapping, player_turn: str, clicked_row: int, clicked_col: int):

        # validation
        board_square = self.board[clicked_row][clicked_col]
        if board_square is None or board_square.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            return [], None

        # initialization
        piece = piece_mapping.get_piece(board_square.piece)
        possible_moves: list[tuple[int, int, str]] = self.get_possible_moves(clicked_row, clicked_col, piece, player_turn, piece_mapping)
        if not possible_moves:
            print(f"No possible moves from ({clicked_row}, {clicked_col})")
            return possible_moves, None

        # selection
        selected_square = (clicked_row, clicked_col)
        return possible_moves, selected_square

    def move_piece(self, current_row: int, current_col: int, clicked_row: int, clicked_col: int, promo_char: Optional[str], piece_characters: str,
                   white_pieces: list[tuple[str, int, int]], black_pieces: list[tuple[str, int, int]], piece_mapping: PieceMapping) -> tuple[list[tuple[str, int, int]], tuple[list[tuple[str, int, int]]]]:
        target_cell = self.board[clicked_row][clicked_col]
        cur_board_piece: ChessBoardPiece = self.board[current_row][current_col]
        cur_chess_piece = piece_mapping.get_piece(cur_board_piece.piece)

        # change the position of the piece
        if cur_board_piece.color == 'w':
            white_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == current_row and piece[2] == current_col
                            else piece for piece in white_pieces]
        else:
            black_pieces = [(piece[0], clicked_row, clicked_col) if piece[1] == current_row and piece[2] == current_col
                            else piece for piece in black_pieces]
        # special
        if not cur_chess_piece.cloning:
            self.board[current_row][current_col] = None
        if cur_chess_piece.promotion and \
            ((cur_board_piece.color == 'w' and clicked_row == 0) or (cur_board_piece.color == 'b' and clicked_row == self.rows - 1)):
            cur_board_piece = ChessBoardPiece(promo_char, cur_board_piece.color)
            if cur_board_piece.color == 'w':
                white_pieces = [(promo_char, clicked_row, clicked_col) if piece[1] == clicked_row and piece[2] == clicked_col
                                else piece for piece in white_pieces]
            else:
                black_pieces = [(promo_char, clicked_row, clicked_col) if piece[1] == clicked_row and piece[2] == clicked_col
                                else piece for piece in black_pieces]
        
        self.board[clicked_row][clicked_col] = cur_board_piece
        # remove the piece standing on the target cell
        if target_cell is not None:
            if target_cell.color == 'b':
                black_pieces = [piece for piece in black_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
            else:
                white_pieces = [piece for piece in white_pieces if piece[1] != clicked_row or piece[2] != clicked_col]
            # special
            if cur_chess_piece.demon: ### todo: maybe, adjust?
                self.board[current_row][current_col] = copy.deepcopy(cur_board_piece)
                cur_board_piece.piece = target_cell.piece
        return white_pieces, black_pieces

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.columns

    def evaluate_position(self, white_pieces: list[tuple[str, int, int]], black_pieces: list[tuple[str, int, int]],
                          piece_mapping: PieceMapping, coefficients: tuple[int, int, int, int]) -> float:
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
        # todo:
        # Nevertheless, coefficients can be added, as well as other criterias
        if not white_pieces:
            return float('-inf')
        if not black_pieces:
            return float('inf')
        total_for_white = self._calculate_evaluation(white_pieces, piece_mapping, True, coefficients)
        total_for_black = self._calculate_evaluation(black_pieces, piece_mapping, False, coefficients)
        # finding ratio looks more normalized than finding difference
        if total_for_white > total_for_black:
            return total_for_white / total_for_black
        return -total_for_black / total_for_white

    def _calculate_evaluation(self, pieces: list[tuple[str, int, int]], piece_mapping: PieceMapping,
                              is_white: bool, coefficients: tuple[int, int, int, int]) -> float:
        total = 0
        max_row = self.rows - 1

        for piece_data in pieces:
            piece_symbol, cur_row, cur_col = piece_data
            cur_piece = piece_mapping.get_piece(piece_symbol)
            board_piece = self.board[cur_row][cur_col]
            if board_piece is None or cur_piece is None:
                logging.warning(
                    f"Inconsistent data for piece at row {cur_row}, column {cur_col}")  # Not supposed to happen
                continue

            mobility = 0
            advanced = (max_row - cur_row) / max_row if is_white else cur_row / max_row
            # if cur_piece.promotion: # may be unjust, evaluating promoted pieces higher
            #     advanced *= 10
            targeting = 0

            for move in cur_piece.moves:
                steps_made = 0
                current_row = cur_row
                current_col = cur_col
                while steps_made < cur_piece.max_steps:
                    steps_made += 1
                    new_row = current_row + (1 if board_piece.color == 'b' else -1) * move.x
                    new_col = current_col + move.y
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
                        targeting += piece_mapping.get_piece(
                            target_square.piece).value * 100 if piece_mapping.get_piece(
                            target_square.piece).is_special else piece_mapping.get_piece(target_square.piece).value
                        break
            current_value = 0
            current_value += coefficients[0] * (mobility / piece_mapping.get_piece(piece_symbol).max_cells_reachable) * cur_piece.value
            current_value += coefficients[1] * advanced * cur_piece.value
            current_value += coefficients[2] * targeting / cur_piece.value
            current_value = current_value if not piece_mapping.get_piece(
                piece_symbol).is_special else coefficients[3] + current_value
            total += current_value

        return total

    def minimax(self, white_pieces, black_pieces, coefficients: tuple[int, int, int, int], cur_pos: tuple[int, int], cur_move: tuple[int, int, str], max_depth: int,
                maximazing_player, piece_mapping: PieceMapping, positions_analyzed, alpha, beta, curdepth=0):
        positions_analyzed += 1
        # make local copies of everything
        local_board = copy.deepcopy(self)
        white_pieces_local = copy.deepcopy(white_pieces)
        black_pieces_local = copy.deepcopy(black_pieces)
        maximazing_player_local = copy.deepcopy(maximazing_player)

        # move piece, increase depth, change player turn
        white_pieces_local, black_pieces_local = local_board.move_piece(cur_pos[0], cur_pos[1], cur_move[0], cur_move[1], cur_move[2],
                                                 piece_mapping.mapping.values(), white_pieces_local, black_pieces_local,
                                                                         piece_mapping)
        curdepth += 1
        player_turn_local = ("b" if maximazing_player_local else "w")
        maximazing_player_local = not maximazing_player_local

        # check depth
        if curdepth == max_depth:
            return local_board.evaluate_position(white_pieces_local, black_pieces_local,
                                                 piece_mapping, coefficients), positions_analyzed
        break_outer_loop = False

        if maximazing_player_local:
            max_val = -float("inf")
            for piece in white_pieces_local:
                if break_outer_loop:
                    break
                symbol, row, col = piece
                cur_pos = (row, col)
                cur_piece = piece_mapping.get_piece(symbol)
                possible_moves: list[tuple[int, int]] = local_board.get_possible_moves(row, col, cur_piece, player_turn_local, piece_mapping)

                for cur_move in possible_moves:
                    cur_move_value, positions_analyzed = local_board.minimax(white_pieces_local, black_pieces_local, coefficients,
                                                                             cur_pos, cur_move,
                                                                             max_depth, maximazing_player_local, piece_mapping,
                                                                             positions_analyzed, alpha, beta, curdepth)
                    max_val = max(max_val, cur_move_value)
                    alpha = max(alpha, cur_move_value)
                    if beta <= alpha:
                        break_outer_loop = True
                        break

            return max_val, positions_analyzed

        else:
            min_val = float("inf")
            for piece in black_pieces_local:
                if break_outer_loop:
                    break
                symbol, row, col = piece
                cur_pos = (row, col)
                cur_piece = piece_mapping.get_piece(symbol)
                possible_moves: list[tuple[int, int]] = local_board.get_possible_moves(row, col, cur_piece, player_turn_local, piece_mapping)

                for cur_move in possible_moves:
                    cur_move_value, positions_analyzed = local_board.minimax(white_pieces_local, black_pieces_local, coefficients,
                                                                             cur_pos, cur_move,
                                                                             max_depth, maximazing_player_local, piece_mapping,
                                                                             positions_analyzed, alpha, beta, curdepth)
                    min_val = min(min_val, cur_move_value)
                    beta = min(beta, cur_move_value)
                    if beta <= alpha:
                        break_outer_loop = True
                        break

            return min_val, positions_analyzed

    def find_best_move(self, white_pieces: list[tuple[str, int, int]], black_pieces: list[tuple[str, int, int]],
                       piece_mapping: PieceMapping, player_turn: str, coefficients: tuple[int, int, int, int]) -> tuple[tuple[int, int], str, int, int]:
        move_to_value: dict[tuple[tuple[int, int, str], str, int, int], float] = {}
        maximal_depth = 2
        positions_analyzed = 0
        maximazing_player = True if player_turn == "w" else False

        for piece in (white_pieces if player_turn == 'w' else black_pieces):
            symbol, row, col = piece
            cur_pos = (row, col)
            cur_piece = piece_mapping.get_piece(symbol)
            possible_moves: list[tuple[int, int]] = self.get_possible_moves(row, col, cur_piece, player_turn, piece_mapping)

            for cur_move in possible_moves:
                cur_move_value, positions_analyzed = self.minimax(white_pieces, black_pieces, coefficients, cur_pos, cur_move,
                                                                  maximal_depth, maximazing_player, piece_mapping,
                                                                  positions_analyzed, alpha=-float("inf"), beta=float("inf"))
                move_to_value[cur_move, symbol, row, col] = cur_move_value

        best_move = (max(move_to_value, key=move_to_value.get) if player_turn == 'w' else min(move_to_value,
                                                                                              key=move_to_value.get))
        print(f"number of positions analyzed: {positions_analyzed}, depth: {maximal_depth}")
        return best_move
