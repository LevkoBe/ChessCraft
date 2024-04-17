import json
import re
from typing import List, Tuple
from Move import Move

def is_valid_position(row:int, col:int, rows: int, cols: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


class ChessPiece:
    def __init__(self, name: str, symbol: str, moves: List[str], max_steps: str, optional: List[str], max_cells_reachable: int = 0, value: int = 0):
        self.name = name
        self.symbol = symbol
        self.moves: List[Move] = self.get_moves(moves)
        self.max_steps: int = int(max_steps)
        self.max_cells_reachable = max_cells_reachable
        self.value: int = value
        self.is_special: bool = False               # most important piece of the game          # '!' in special
        self.trap: bool = 'x' in optional           # when captured, kills the opponent's piece
        self.ninja: bool = 'n' in optional          # can change direction during the move
        self.scary: bool = 'y' in optional          # moves other pieces when making a move (as though they flee)
        self.demon: bool = 'd' in optional          # lives in others (gets another "body" when captures)
        self.leader: bool = 'l' in optional         # moves other pieces when making a move (as though they follow him)
        self.fusion: bool = 'f' in optional         # combining two or more pieces into a single, more powerful entity
        self.shooter: bool = 's' in optional        # doesn't move when capturing others
        self.cloning: bool = 'c' in optional        # clones on each move
        self.grouping: bool = 'g' in optional       # can gather on one cell in quantities more than 1
        self.fortress: bool = '+' in optional       # can spawn other pieces
        self.promotion: bool = 'p' in optional      # can promote to another piece after reaching the end of the board
        self.invisible: bool = 'v' in optional      # invisible on the board
        self.explosive: bool = 'e' in optional      # explodes when captured
        self.insatiable: bool = 'i' in optional     # after capture makes another move
        self.unbreakable: bool = 'u' in optional    # cannot be captured
        self.random_self: bool = '?' in optional    # can change itself into another piece during the move
        self.radioactive: bool = 'r' in optional    # kills other pieces when approaches them
        self.random_others: bool = 'o' in optional  # can change other pieces into another piece during the move
        self.time_traveler: bool = 't' in optional  # undoes opponent's moves in the area where he goes
        self.active_learner: bool = 'a' in optional # learns new moves from others (my favourite)

    def to_string(self) -> str:
        moves_list = [[move.x, move.y, move.moving, move.capturing] for move in self.moves]
        optional_str = ''.join([
            'x' if self.trap else '',
            'n' if self.ninja else '',
            'y' if self.scary else '',
            'd' if self.demon else '',
            'l' if self.leader else '',
            'f' if self.fusion else '',
            's' if self.shooter else '',
            'c' if self.cloning else '',
            'g' if self.grouping else '',
            '+' if self.fortress else '',
            'p' if self.promotion else '',
            'v' if self.invisible else '',
            'e' if self.explosive else '',
            'i' if self.insatiable else '',
            'u' if self.unbreakable else '',
            '?' if self.random_self else '',
            'r' if self.radioactive else '',
            'o' if self.random_others else '',
            't' if self.time_traveler else '',
            'a' if self.active_learner else '',
            '!' if self.is_special else ''
        ])
        piece_dict = {
            "name": self.name,
            "symbol": self.symbol,
            "moves": moves_list,
            "max_steps": self.max_steps,
            "value": self.value,
            "max_cells_reachable": self.max_cells_reachable,
            "optional": optional_str
        }
        return json.dumps(piece_dict)
    
    @classmethod
    def from_string(cls, piece_string: str):
        piece_dict = json.loads(piece_string)
        moves_list = [Move(move[0], move[1], move[2], move[3]) for move in piece_dict["moves"]]
        optional_str = piece_dict["optional"]
        optional_str = optional_str.ljust(20, '0')  # Pad with zeros if necessary
        piece = cls(
            piece_dict["name"],
            piece_dict["symbol"],
            [],
            piece_dict["max_steps"],
            optional_str,
            piece_dict["max_cells_reachable"],
            piece_dict["value"]
        )
        piece.moves = moves_list
        (
            piece.trap, piece.ninja, piece.scary, piece.demon, piece.leader,
            piece.fusion, piece.shooter, piece.cloning, piece.grouping, piece.fortress,
            piece.promotion, piece.invisible, piece.explosive, piece.insatiable,
            piece.unbreakable, piece.random_self, piece.radioactive, piece.random_others,
            piece.time_traveler, piece.active_learner, piece.is_special
        ) = (optional_str.find(c) != -1 for c in 'xnydlfscg+pveiu?rort!')
        return piece

    def get_moves(self, moves_list: List[str]) -> List[Tuple[int, int]]:
        moves: List[Move] = []
        for moves_string in moves_list:
            if len(moves_string) == 2:
                # format: ".." with '+', '-', or '0' representing (vertical, horizontal) moves 'forward', 'backward', and 'none'
                x = 1 if moves_string[0] == '+' else -1 if moves_string[0] == '-' else 0
                y = 1 if moves_string[1] == '+' else -1 if moves_string[1] == '-' else 0
                moves.append(Move(x, y))
            else:
                moving, capturing = 1, 1
                if not bool(re.match(r"^[+-0][+-0]$|^[+-]\d+,[+-]\d+$", moves_string)):
                    # extract booleans 'moving' and 'capturing' from the string. Format: "**.n,.n", where * is 0 or 1
                    moving = not not moves_string[0]
                    capturing = not not moves_string[1]
                    moves_string = moves_string[2:]
                # format: ".n,.n", where '.' is '+', or '-', and 'n' is a number of (vertical, horizontal) moves
                move_tuple = tuple(map(int, moves_string.split(',')))
                moves.append(Move(move_tuple[0], move_tuple[1], moving, capturing))
        return moves

    def calculate_reachable_cells(self, position: Tuple[int, int], rows:int , columns: int) -> int :
        row, column = position
        if not is_valid_position(row, column, rows, columns):
            return 0
        possible_moves = 0
        for move in self.moves:     # in each direction
            steps_made = 0              # we can move X steps
            current_row = row
            current_col = column
            while steps_made < self.max_steps:
                steps_made += 1
                new_row = current_row + move.x
                new_col = current_col + move.y
                if not is_valid_position(new_row, new_col, rows, columns):
                    break
                possible_moves += 1
                current_row = new_row
                current_col = new_col

        return possible_moves

    def calculate_reachable_cells_stats(self, rows:int, columns: int):
        nums_reachable_cells = []
        for r in range(0, rows):
            for c in range(0, columns):
                nums_reachable_cells.append(self.calculate_reachable_cells((r, c),rows, columns))
        self.max_cells_reachable = max(nums_reachable_cells)
        self.value = sum(nums_reachable_cells)/len(nums_reachable_cells)
        return