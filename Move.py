class Move:
    def __init__(self, x, y, moving=1, capturing=1, postcapture_moves=0, availableat_at_row=None):
        self.x = x
        self.y = y
        self.moving = moving
        self.capturing = capturing
        # self.postcapture_moves = postcapture_moves
        # self.availableat_at_row = availableat_at_row
