
import copy
import multiprocessing
from GameFlow import GameFlow
from Gameset import Gameset

# using genetic algorithm, we will follow similar steps to these:
# 1. original gameset -> 2. mutations => children -> 3. play -> 4. selecting best -> repeat 2-4 until game-over
# result is a set of coefficients for each generation

# 1. Initialize the initial gameset with coefficients.
# 2. Create a generation of game flows, each with a randomized copy of the initial gameset.
# 3. Repeat until one game flow ends with black winning, or all end with white winning:
#    a. Play a fixed number of moves in each game flow.
#    b. Evaluate the fitness (game board evaluation with current coefficients) for each game flow.
#    c. Select the best-performing game flows (fitness function is game.board.evaluate_position(original_white_coeffs))
#    d. Generate children from the best-performing game flows with randomized coefficients.
#    e. Update the current generation with the best-performing game flows and their children.
#    f. Save the coefficients for the generation
# 4. Select the winning/best coefficients from the final generation.
# 5. Start again with the initial gameset using the winning/best coefficients.


# fitness function is game.board.evaluate_position() with initial coefficients


class GeneticAlgorithm:
    def __init__(self, initial_gameset: Gameset, num_games_in_generation: int = 10, num_best_children: int = 5, mutation_rate: float = 0.2):
        self.initial_gameset = initial_gameset
        self.num_games_in_generation = num_games_in_generation
        self.num_best_children = num_best_children
        self.mutation_rate = mutation_rate
        self.best_coeffs_for_generation = [initial_gameset.white_coefficients]

    def update_coefficients(self, coeffs):
        self.best_coeffs_for_generation.append(coeffs)
        self.initial_gameset.white_coefficients = self.best_coeffs_for_generation[-1]
        self.initial_gameset.black_coefficients = self.best_coeffs_for_generation[-1]
        print(f"New coefficients: {self.best_coeffs_for_generation[-1]}")
    
    def train(self, num_moves):
        current_generation: list[GameFlow] = [GameFlow(copy.deepcopy(self.initial_gameset), True, True)]
        while True:
            self.play_a_game(num_moves, current_generation)
            if not self.current_generation:
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
            for game, winner in results:
                if winner == 2:  # black won
                    self.update_coefficients(game.game.black_coefficients)
                    return
                elif not winner:  # game is still ongoing
                    continue
                else:  # white won
                    games_to_remove.append(game)

            for game in games_to_remove:
                current_generation.remove(game)
            
            # if we lose in every game flow, start again
            if not current_generation:
                return
            
            # Select the best gamesets to retain, based on evaluation with original coefficients, and update the original coefficients
            sorted_generation = sorted(current_generation, key=lambda x: x.game.board.evaluate_position(x.white_pieces, x.black_pieces, x.game.piece_mapping, self.initial_gameset.white_coefficients))
            best_gamesets = sorted_generation[:self.num_best_children]
            print(f"Best results: {[game.game.board.evaluate_position(game.white_pieces, game.black_pieces, game.game.piece_mapping, self.initial_gameset.white_coefficients) for game in sorted_generation]}")
            print(f"Best coefficients: {[game.game.black_coefficients for game in sorted_generation]}")
            self.update_coefficients(best_gamesets[0].game.black_coefficients)
            
            children = []
            # Generate children from the best-performing gamesets
            for x in range(self.num_games_in_generation - self.num_best_children):
                parent = best_gamesets[x // self.num_best_children]
                child_gameset = copy.deepcopy(parent.game)
                child_gameset.randomize_coefficients(self.mutation_rate)
                children.append(GameFlow(child_gameset, True, True))
        
            # Update current generation with the best gamesets and children
            current_generation = best_gamesets + children
    
    def play_moves(self, args):
        game, num_moves = args
        game.play_game(num_moves)
        winner = game.game_finished()
        return game, winner
    