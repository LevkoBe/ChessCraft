import multiprocessing
from typing import Optional
from GameFlow import GameFlow
from GeneticAlgorithmTraining import GeneticAlgorithmTraining
from Gameset import Gameset
from UserSupervisor import string_input

def train_game(game, filename):
    training_algorithm = GeneticAlgorithmTraining(game, filename)
    training_algorithm.train()

def ask_for_saving(game: Gameset):
    # Save the game
    filename = None
    save_option = string_input('Would you like to save this game? (yes/(no)): ', 'select', options=['yes', 'no', ''])
    if save_option.lower() == 'yes':
        filename = "saved_games/" + input('Enter the filename to save the game: ') + ".json"
        game.save_game(filename)
    return filename

def ask_for_training(game: Gameset, filename: str):
    # Start training process in parallel
    train_option = string_input('Would you like to start bot training? ((yes)/no): ', 'select', options=['yes', 'no', ''])
    if train_option.lower() != 'no':
        training_process = multiprocessing.Process(target=train_game, args=(game,filename,))
        training_process.start()

def main():
    filename = None
    while True:
        action = string_input('What would you like to do? Either "create", "load", or "exit": ',
                              'select', options=['create', 'load', 'exit'])
        if action == 'create':
            # create (and save)
            game = Gameset()
            game.create_game()

            filename: Optional[str] = ask_for_saving(game)

            ask_for_training(game, filename)
        
            gamerun = GameFlow(game, False, True)
            gamerun.play_game()
        elif action == 'load':
            filename = "saved_games/" + input('Enter the filename to load the game: ') + ".json"
            game = Gameset()
            try:
                game.load_game(filename)
                
                ask_for_training(game, filename)

                gamerun = GameFlow(game, False, True)
                gamerun.play_game()
            except FileNotFoundError:
                print('Could not load the game.')

        elif action == 'exit':
            return

if __name__ == "__main__":
    main()
