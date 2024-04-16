import multiprocessing
from GameFlow import GameFlow
from GameTraining import GeneticAlgorithm
from Gameset import Gameset
from UserSupervisor import string_input

def train_game(game, filename):
    training_algorithm = GeneticAlgorithm(game, filename)
    training_algorithm.train()

def main():
    filename = None
    while True:
        action = string_input('What would you like to do? Either "create", "load", or "exit": ',
                              'select', options=['create', 'load', 'exit'])
        if action == 'create':
            # create (and save)
            game = Gameset()
            game.create_game()

            # Save the game
            save_option = string_input('Would you like to save this game? (yes/(no)): ', 'select', options=['yes', 'no', ''])
            if save_option.lower() == 'yes':
                filename = "saved_games/" + input('Enter the filename to save the game: ') + ".json"
                game.save_game(filename)

            # Start training process in parallel
            training_process = multiprocessing.Process(target=train_game, args=(game,filename,))
            training_process.start()
        
            gamerun = GameFlow(game, False, True)
            gamerun.play_game()
        elif action == 'load':
            filename = "saved_games/" + input('Enter the filename to load the game: ') + ".json"
            game = Gameset()
            try:
                game.load_game(filename)
                
                # Start training process in parallel
                training_process = multiprocessing.Process(target=train_game, args=(game,filename,))
                training_process.start()

                gamerun = GameFlow(game, False, True)
                gamerun.play_game()
            except FileNotFoundError:
                print('Could not load the game.')

        elif action == 'exit':
            return

if __name__ == "__main__":
    main()
