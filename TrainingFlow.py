from GameSetup import white_black_division
from Gameset import Gameset


class TrainingFlow:
    def __init__(self, game: Gameset):
        self.game = game
        self.running = True
        self.white_pieces, self.black_pieces = white_black_division(self.game.board)
    
    def play_game(self, maximum_moves=-1):
        moves_played = 0
        players = "wb"
        coefficients_sets = (self.game.white_coefficients, self.game.black_coefficients)

        while self.running and moves_played != maximum_moves:
            current_player = players[moves_played % 2]
            coefficients = coefficients_sets[moves_played % 2]

            # bot's move
            best_move, _, current_row, current_col = self.game.board.find_best_move(self.white_pieces, self.black_pieces, self.game.piece_mapping, current_player, coefficients)
            self.white_pieces, self.black_pieces = self.game.board.move_piece(current_row, current_col, best_move[0], best_move[1], best_move[2],
                                           self.game.piece_mapping.mapping.values(), self.white_pieces, self.black_pieces, self.game.piece_mapping)
            
            # check winners
            if self.game_finished():
                break

            moves_played += 1
            
        return self.game.board.evaluate_position(self.white_pieces, self.black_pieces, self.game.piece_mapping, self.game.white_coefficients)

    def game_finished(self):
        if not any(self.game.piece_mapping.get_piece(p[0]).is_special for p in self.white_pieces):
            return 2
        if not any(self.game.piece_mapping.get_piece(p[0]).is_special for p in self.black_pieces):
            return 1
        return 0

