from GameFlow import GameFlow
from Gameset import Gameset
from UserSupervisor import string_input

def main():
    while True:
        action = string_input('What would you like to do? Either "create", "load", or "exit": ',
                              'select', options=['create', 'load', 'exit'])
        if action == 'create':
            # create (and save)
            game = Gameset()
            game.create_game()

            # save the game
            save_option = string_input('Would you like to save this game? (yes/(no)): ', 'select', options=['yes', 'no', ''])
            if save_option.lower() == 'yes':
                filename = input('Enter the filename to save the game: ')
                game.save_game(filename)
        
            # gametrain = GameFlow(game, True, True)
            # gametrain.play_game()
            gamerun = GameFlow(game, False, True)
            gamerun.play_game()
        elif action == 'load':
            filename = input('Enter the filename to load the game: ')
            game = Gameset()
            try:
                game.load_game(filename)
                gamerun = GameFlow(game, False, False)
                gamerun.play_game()
            except FileNotFoundError:
                print('Could not load the game.')
        elif action == 'exit':
            return

if __name__ == "__main__":
    main()


# search through the code for 'todo', and 'alert'
