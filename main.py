from typing import List


class ChessPiece:
    def __init__(self, name, symbol, h_move_formula, v_move_formula, a_values, b_values, extr):
        self.name = name
        self.symbol = symbol
        self.h_move_formula = h_move_formula
        self.v_move_formula = v_move_formula
        self.a_values = self.get_values(a_values, extr)
        self.b_values = self.get_values(b_values, extr)

    # "c:c/c,c,c,c" or "+-/c,c,c"
    def get_values(self, formula, extr):
        if formula == "":
            return [1]

        take, remove = formula.split('/')
        if len(take) >= 2 and take[:2] == "+-":
            min_value, max_value = -extr, extr
        else:
            min_value, max_value = map(int, take.split(':'))

        rem_values = list(map(int, remove.split(',')))
        return [value for value in range(min_value, max_value + 1) if value not in rem_values]


class ChessBoardPiece:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color
    
    def __str__(self):
        return self.piece + self.color

class ChessBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]

    def place_piece(self, row, col, piece, color):
        self.board[row][col] = ChessBoardPiece(piece, color)

    def render_board(self):
        print("     " + "    ".join(str(i + 1) for i in range(self.columns)))
        print("   " + "+".join(["----"] * self.columns))
        for i, row in enumerate(self.board):
            print(chr(ord('a') + i) + " | " + " | ".join(self.render_piece(cell) for cell in row) + " |")
            print("   " + "+".join(["----"] * self.columns))
    
    def render_piece(self, figure):
        if figure is None:
            return '  '
        else:
            return str(figure)

    def get_possible_moves(self, position):
        row, col = self.position_to_indices(position)
        if not self.is_valid_position(row, col):
            return []

        board_piece = self.board[row][col]
        if board_piece is None:
            return []

        piece_symbol = board_piece.piece
        piece = None
        for p in pieces:
            if p.symbol == piece_symbol:
                piece = p
                break

        if piece is None:
            return []

        v_formula, h_formula = piece.v_move_formula, piece.h_move_formula
        a_values, b_values = piece.a_values, piece.b_values

        possible_moves = []

        for a in a_values:
            for b in b_values:
                v_steps = eval(v_formula.replace('a', str(a)).replace('b', str(b)))
                h_steps = eval(h_formula.replace('a', str(a)).replace('b', str(b)))
                new_row = row + (1 if board_piece.color == '+' else -1) * v_steps
                new_col = col + h_steps
                if self.is_valid_position(new_row, new_col):
                    possible_moves.append(self.indices_to_position(new_row, new_col))
        return possible_moves


    def position_to_indices(self, position):
        row = ord(position[0].lower()) - ord('a')
        col = int(position[1:]) - 1
        return row, col

    def indices_to_position(self, row, col):
        position = chr(ord('a') + row) + str(col + 1)
        return position

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.columns


def add_piece(extreme_value):
    name = input("Please enter the name of the piece: ")
    symbol = input("Please enter the character to represent the piece: ")
    v_move_formula = input("Please enter the formula for its vertical moves: ")
    h_move_formula = input("Please enter the formula for its horizontal moves: ")

    a_values, b_values = "", ""
    if 'a' in h_move_formula or 'a' in v_move_formula:
        a_values = input("Please enter the possible values for variable 'a' (c:c/c,c,c): ")
    if 'b' in h_move_formula or 'b' in v_move_formula:
        b_values = input("Please enter the possible values for variable 'b' (c:c/c,c,c): ")

    return ChessPiece(name, symbol, h_move_formula, v_move_formula, a_values, b_values, extreme_value)

def main():
    rows = int(input("Please enter the number of rows: "))
    columns = int(input("Please enter the number of columns: "))
    board = ChessBoard(rows, columns)
    extreme_value = max(columns, rows)

    while True:
        action = input("Enter 'add' to add a piece, 'next' to continue, or 'quit' to end the game: ")
        if action == 'add':
            piece = add_piece(extreme_value)
            pieces.append(piece)
            print(f"{piece.name} added successfully.")
        elif action == 'next':
            break
        elif action == 'quit':
            return
        else:
            print("Invalid command. Please try again.")

    print("Please fill the board with the figures:")
    for i in range(rows):
        row_input = input().split()
        color = "+" if i <= rows // 2 else "-"
        for j in range(columns):
            if j < len(row_input):
                board.place_piece(i, j, row_input[j], color)
            else:
                board.board[i][j] = None

    board.render_board()

    player_turn = '-'
    while True:
        move = input(f"Enter the position of the {player_turn} piece you want to move (or 'quit' to end the game): ")
        if move == 'quit':
            return

        row, col = board.position_to_indices(move)

        if not board.is_valid_position(row, col):
            print("Invalid position. Please try again.")
            continue

        board_piece = board.board[row][col]

        if board_piece is None or board_piece.color != player_turn:
            print(f"No {player_turn} piece at the specified position. Please try again.")
            continue

        possible_moves = board.get_possible_moves(move)
        print(f"Possible moves: {possible_moves}")

        if possible_moves:
            target_move = input("Enter the position you want to move the piece to: ")
            if target_move in possible_moves:
                new_row, new_col = board.position_to_indices(target_move)
                board.board[new_row][new_col] = board_piece
                board.board[row][col] = None
                player_turn = '+' if player_turn == '-' else '-'  # Switch player's turn
            else:
                print("Invalid move. Please try again.")
        else:
            print("No possible moves. Please try again.")

        board.render_board()

if __name__ == "__main__":
    pieces: List[ChessPiece] = []
    main()
