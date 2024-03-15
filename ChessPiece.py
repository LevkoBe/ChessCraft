class ChessPiece:
    def __init__(self, name: str, symbol: str, h_move_formula: str, v_move_formula: str, a_values: str, b_values: str, extr: int):
        self.name = name
        self.symbol = symbol
        self.h_move_formula = h_move_formula
        self.v_move_formula = v_move_formula
        self.a_values = self.get_values(a_values, extr)
        self.b_values = self.get_values(b_values, extr)

    # "c:c/c,c,c,c" or "+-/c,c,c"
    def get_values(self, formula: str, extr: int) -> list:
        if formula == "":
            return [1]

        take, *remove = formula.split('/')
        if len(take) >= 2 and take[:2] == "+-":
            min_value, max_value = -extr, extr
        else:
            min_value, max_value = map(int, take.split(':'))

        if remove:
            rem_values = list(map(int, remove[0].split(',')))
        else:
            rem_values = []
        return [value for value in range(min_value, max_value + 1) if value not in rem_values]
