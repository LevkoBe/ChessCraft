class ChessPiece:
    def __init__(self, name, symbol, h_move_formula, v_move_formula, possible_values):
        self.name = name
        self.symbol = symbol
        self.h_move_formula = h_move_formula
        self.v_move_formula = v_move_formula
        self.possible_values = possible_values

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
        print("    " + "   ".join(str(i + 1) for i in range(self.columns)))
        print("   " + "+".join(["----"] * self.columns))
        for i, row in enumerate(self.board):
            print(chr(ord('a') + i) + " | " + " | ".join(self.render_piece(cell) for cell in row) + " |")
            print("   " + "+".join(["----"] * self.columns))
    
    def render_piece(self, figure):
        if figure is None:
            return '  '
        else:
            return str(figure)

def add_piece():
    name = input("Please enter the name of the piece: ")
    symbol = input("Please enter the character to represent the piece: ")
    h_move_formula = input("Please enter the formula for its horizontal moves: ")
    v_move_formula = input("Please enter the formula for its vertical moves: ")
    possible_values = input("Please enter the possible values for the variables (comma-separated): ").split(',')
    return ChessPiece(name, symbol, h_move_formula, v_move_formula, possible_values)

def main():
    rows = int(input("Please enter the number of rows: "))
    columns = int(input("Please enter the number of columns: "))
    board = ChessBoard(rows, columns)

    pieces = []
    while True:
        action = input("Enter 'add' to add a piece, 'next' to continue: ")
        if action == 'add':
            piece = add_piece()
            pieces.append(piece)
            print(f"{piece.name} added successfully.")
        elif action == 'next':
            break
        else:
            print("Invalid command. Please try again.")

    print("Please fill the board with the figures:")
    for i in range(rows):
        row_input = input().split()
        color = "b" if i <= rows // 2 else "w"
        for j in range(columns):
            if j < len(row_input):
                board.place_piece(i, j, row_input[j], color)
            else:
                board.board[i][j] = None

    board.render_board()

if __name__ == "__main__":
    main()
