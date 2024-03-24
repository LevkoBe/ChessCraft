from typing import List, Tuple


def is_valid_position(row:int, col:int, rows: int, cols: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


class ChessPiece:
    def __init__(self, name: str, symbol: str, directions: List[str], max_steps: str):
        self.name = name
        self.symbol = symbol
        self.directions: List[Tuple[int, int]] = self.get_directions(directions)  
        self.max_steps: int = int(max_steps)
        self.max_cells_reachable = None
        self.avg_cells_reachable = None

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
    def calculate_reachable_cells(self, position: Tuple[int, int], rows:int , columns: int) -> List[Tuple[int, int]] :
        row, column = position
        if not is_valid_position(row, column, rows, columns):
            return []
        # change to just counter after testing
        possible_moves: List[Tuple[int, int]] = []
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
                possible_moves.append((new_row, new_col))
                current_row = new_row
                current_col = new_col

        return possible_moves

