
import copy
import multiprocessing
from GameFlow import GameFlow
from Gameset import Gameset


class GameTraining(multiprocessing.Process):
    def __init__(self, main_game: Gameset, lock: multiprocessing.Lock):
        super().__init__()
        self.main_game = main_game
        self.game_copy = copy.deepcopy(main_game)
        self.game_copy.randomize_coefficients(False, True, 0.5)
        self.good_coefficients = [self.main_game.white_coefficients]
        self.lock = lock

    def run(self):
        while True: # create new game
            game = copy.deepcopy(self.game_copy)
            gametrain = GameFlow(game, True, True)
            previous_pos_eval = game.board.evaluate_position(gametrain.white_pieces, gametrain.black_pieces, game.piece_mapping, game.white_coefficients)
            while not gametrain.game_finished(): # play N moves
                print(previous_pos_eval)
                game.randomize_coefficients()
                moves_to_make = 10
                current_pos_eval = gametrain.play_game(moves_to_make)
                if current_pos_eval < previous_pos_eval: # better for black
                    self.good_coefficients.append(game.black_coefficients)
                    self.update_coefficients()
                previous_pos_eval = current_pos_eval

    def update_coefficients(self):
        avg_coefficients = [sum(x) / len(self.good_coefficients) for x in zip(*self.good_coefficients)]
        print(avg_coefficients)
        with self.lock:
            self.main_game.black_coefficients = tuple(avg_coefficients)
            self.game_copy.black_coefficients = tuple(avg_coefficients)
