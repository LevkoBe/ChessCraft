from typing import List, Tuple


class ChessPiece:
    def __init__(self, name: str, symbol: str, directions: List[str], steps: str):
        self.name = name
        self.symbol = symbol
        self.directions: List[Tuple[int, int]] = self.get_directions(directions)  
        self.max_steps: int = int(steps)

    def get_directions(self, directions_list: List[str]) -> List[Tuple[int, int]]:
        directions: List[Tuple[int, int]] = []
        for directions_string in directions_list:
            if len(directions_string) == 2:
                x = 1 if directions_string[0] == '+' else -1 if directions_string[0] == '-' else 0
                y = 1 if directions_string[1] == '+' else -1 if directions_string[1] == '-' else 0
                directions.append((x, y))
            else:
                directions.append(tuple(map(int, directions_string.split(','))))
        return directions
