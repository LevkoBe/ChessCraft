
import copy
import multiprocessing
from GameFlow import GameFlow
from Gameset import Gameset


class GameTraining(multiprocessing.Process):
    def __init__(self, main_game: Gameset, lock: multiprocessing.Lock):
        super().__init__()
        self.main_game = main_game
        self.game = copy.deepcopy(main_game)
        self.game.randomize_coefficients(0.5)
        self.good_coefficients = [self.main_game.coefficients]
        self.lock = lock

    def run(self):
        while True:
            self.game.randomize_coefficients()
            gametrain = GameFlow(self.game, True, True)
            winner = gametrain.play_game()
            if winner == 2:
                self.good_coefficients.append(self.game.coefficients)
                self.update_coefficients()

    def update_coefficients(self):
        avg_coefficients = [sum(x) / len(self.good_coefficients) for x in zip(*self.good_coefficients)]
        with self.lock:
            self.main_game.coefficients = tuple(avg_coefficients)
            self.game.coefficients = tuple(avg_coefficients)
