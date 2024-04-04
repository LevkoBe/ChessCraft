import re
from typing import List, Tuple
from Move import Move

def is_valid_position(row:int, col:int, rows: int, cols: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


class ChessPiece:
    def __init__(self, name: str, symbol: str, moves: List[str], max_steps: str, optional: List[str]):
        self.name = name
        self.symbol = symbol
        self.moves: List[Move] = self.get_moves(moves)
        self.max_steps: int = int(max_steps)
        self.max_cells_reachable = None
        self.value = None
        self.is_special: bool = False               # most important piece of the game
        self.ninja: bool = 'n' in optional          # can change direction during the move
        self.demon: bool = 'd' in optional          # lives in others (gets another "body" when captures)
        self.fusion: bool = 'f' in optional         # combining two or more pieces into a single, more powerful entity
        self.shooter: bool = 's' in optional        # doesn't move when capturing others
        self.cloning: bool = 'c' in optional        # clones on each move
        self.grouping: bool = 'g' in optional       # can gather on one cell in quantities more than 1
        self.promotion: bool = 'p' in optional      # can promote to another piece after reaching the end of the board
        self.invisible: bool = 'v' in optional      # invisible on the board
        self.insatiable: bool = 'i' in optional     # after capture makes another move
        self.unbreakable: bool = 'u' in optional    # cannot be captured

    def to_string(self) -> str:
        directions_str = ' '.join([f"{('+' if d[0] >= 0 else '')}{d[0]},{('+' if d[1] >= 0 else '')}{d[1]}" for d in self.directions])
        return f"{self.name};{self.symbol};{directions_str};{self.max_steps}"

    @classmethod
    def from_string(cls, piece_string: str):
        name, symbol, directions_str, max_steps = piece_string.split(';')
        directions = [dir_str for dir_str in directions_str.split(' ')]
        return cls(name, symbol, directions, max_steps)

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
        for di in self.directions:     # in each direction
            steps_made = 0              # we can move X steps
            current_row = row
            current_col = column
            while steps_made < self.max_steps:
                steps_made += 1
                new_row = current_row + di[0]
                new_col = current_col + di[1]
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