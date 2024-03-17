
from Gameset import Gameset
from GameRun import play_game
from UserSupervisor import string_input

def main():
    while True:
        action = string_input('What would you like to do? Either "create", or "choose" game to play: ', \
                              'select', options=['create', 'choose', 'exit'])
        if action == 'create':
            game = Gameset()
            play_game(game)
        elif action == 'choose':
            pass
        elif action == 'exit':
            return


if __name__ == "__main__":
    main()
