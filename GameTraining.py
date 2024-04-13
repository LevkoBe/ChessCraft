import copy
import multiprocessing
from GameFlow import GameFlow
from Gameset import Gameset

class GeneticAlgorithm:
    def __init__(self, initial_gameset: Gameset, num_games_in_generation: int = 10, num_best_children: int = 5, mutation_rate: float = 110.2):
        self.initial_gameset = initial_gameset
        self.num_games_in_generation = num_games_in_generation
        self.num_best_children = num_best_children
        self.mutation_rate = mutation_rate
        self.best_coeffs_for_generation = [initial_gameset.white_coefficients]
        self.evaluation_scores = []

    def update_coefficients(self, coeffs):
        self.best_coeffs_for_generation.append(coeffs)
        self.initial_gameset.white_coefficients = self.best_coeffs_for_generation[-1]
        self.initial_gameset.black_coefficients = self.best_coeffs_for_generation[-1]
        print(f"New coefficients: {self.best_coeffs_for_generation[-1]}")

    def train(self, num_moves):
        current_generation: list[GameFlow] = [GameFlow(copy.deepcopy(self.initial_gameset), True, True)]
        while True:
            self.play_a_game(num_moves, current_generation)
            some_condition = True
            if not some_condition:
                break

    def play_a_game(self, num_moves, current_generation: list[GameFlow]):
        while True:
            # Define a multiprocessing pool
            pool = multiprocessing.Pool()

            # Play moves for each game flow in the current generation in parallel
            results = pool.map(self.play_moves, [(game, num_moves) for game in current_generation])
            pool.close()
            pool.join()

            # Process the results
            games_to_remove = []
            self.evaluation_scores.clear()
            for game, winner, score in results:
                self.evaluation_scores.append((game, score))
                if winner == 2:  # black won
                    self.update_coefficients(game.game.black_coefficients)
                    return
                elif not winner:  # game is still ongoing
                    continue
                else:  # white won
                    games_to_remove.append(game)

            # Remove game flows that need to be removed
            for game in games_to_remove:
                print(f"Removing game: {game}")
                current_generation.remove(game)

            # if we lose in every game flow, start again
            if not current_generation:
                return

            # Select the best gamesets to retain, based on evaluation with original coefficients, and update the original coefficients
            best_gamesets = sorted(self.evaluation_scores, key=lambda x: x[1])[:self.num_best_children]
            print(f"Best results: {[score for _, score in best_gamesets]}")
            print(f"Best coefficients: {[game.game.black_coefficients for game, _ in best_gamesets]}")
            self.update_coefficients(best_gamesets[0][0].game.black_coefficients)

            children = []
            # Generate children from the best-performing gamesets
            for x in range(self.num_games_in_generation - self.num_best_children):
                parent = best_gamesets[x // self.num_best_children][0]
                child_gameset = copy.deepcopy(parent.game)
                child_gameset.randomize_coefficients(self.mutation_rate)
                children.append(GameFlow(child_gameset, True, True))

            # Update current generation with the best gamesets and children
            current_generation = [game for game, _ in best_gamesets] + children

    def play_moves(self, args):
        game, num_moves = args
        game.play_game(num_moves)
        winner = game.game_finished()
        score = game.game.board.evaluate_position(game.white_pieces, game.black_pieces, game.game.piece_mapping, self.initial_gameset.white_coefficients)
        return game, winner, score
