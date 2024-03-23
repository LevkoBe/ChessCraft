import re
from typing import List, Tuple
from Move import Move

class ChessPiece:
    def __init__(self, name: str, symbol: str, moves: List[str], steps: str, optional: List[str]):
        self.name = name
        self.symbol = symbol
        self.moves: List[Move] = self.get_moves(moves)
        self.max_steps: int = int(steps)
        self.ninja: bool = 'n' in optional          # can change direction during the move
        self.promotion: bool = 'p' in optional      # can promote to another piece after reaching the end of the board
        self.cloning: bool = 'c' in optional        # clones on each move
        self.unbreakable: bool = 'u' in optional    # cannot be captured
        self.invisible: bool = 'v' in optional      # invisible on the board
        self.shooter: bool = 's' in optional        # doesn't move when capturing others
        self.demon: bool = 'd' in optional          # lives in others (gets another "body" when captures)
        self.insatiable: bool = 'i' in optional     # after capture makes another move
        self.grouping: bool = 'g' in optional       # can gather on one cell in quantities more than 1
        self.fusion: bool = 'f' in optional         # combining two or more pieces into a single, more powerful entity

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
