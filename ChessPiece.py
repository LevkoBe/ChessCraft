from typing import List, Tuple


class ChessPiece:
    def __init__(self, name: str, symbol: str, directions: List[str], max_steps: str):
        self.name = name
        self.symbol = symbol
        self.directions: List[Tuple[int, int]] = self.get_directions(directions)  
        self.max_steps: int = int(max_steps)

    def to_string(self) -> str:
        directions_str = ' '.join([f"{('+' if d[0] >= 0 else '')}{d[0]},{('+' if d[1] >= 0 else '')}{d[1]}" for d in self.directions])
        return f"{self.name};{self.symbol};{directions_str};{self.max_steps}"

    @classmethod
    def from_string(cls, piece_string: str):
        name, symbol, directions_str, max_steps = piece_string.split(';')
        directions = [dir_str for dir_str in directions_str.split(' ')]
        return cls(name, symbol, directions, max_steps)

    def get_directions(self, directions_list: List[str]) -> List[Tuple[int, int]]:
        directions: List[Tuple[int, int]] = []
        for directions_string in directions_list:
            if len(directions_string) == 2:
                # format: ".." with '+', '-', or '0' representing (vertical, horizontal) moves 'forward', 'backward', and 'none'
                x = 1 if directions_string[0] == '+' else -1 if directions_string[0] == '-' else 0
                y = 1 if directions_string[1] == '+' else -1 if directions_string[1] == '-' else 0
                directions.append((x, y))
            else:
                # format: ".n,.n", where '.' is '+', or '-', and 'n' is a number of (vertical, horizontal) moves
                directions.append(tuple(map(int, directions_string.split(','))))
        return directions
