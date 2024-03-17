from typing import List, Tuple


class ChessPiece:
    def __init__(self, name: str, symbol: str, directions: List[str], steps: str, optional: List[str]):
        self.name = name
        self.symbol = symbol
        self.directions: List[Tuple[int, int]] = self.get_directions(directions)  
        self.max_steps: int = int(steps)
        self.ninja: bool = 'n' in optional
        self.promotion: bool = 'p' in optional
        self.cloning: bool = 'c' in optional

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
