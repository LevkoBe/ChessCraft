import pygame
from GameSetup import white_black_division
from GameUI import GameUI
from Gameset import Gameset
from UserSupervisor import string_input


class GameFlow:
    def __init__(self, game: Gameset, white_bot: bool, black_bot: bool):
        self.game = game
        self.white_bot = white_bot
        self.black_bot = black_bot
        self.running = True
        self.white_pieces, self.black_pieces = white_black_division(self.game.board)
    
    def play_game(self):
        ui = GameUI(self.game.board)
        moves_played = 0
        players = "wb"
        bots = (self.white_bot, self.black_bot)

        while self.running: # while game lasts: (make one move)
            ui.process_events()
            ui.render_board(self.game.board, self.game.board.rows, self.game.board.columns, [], None, self.game.piece_mapping)
            current_player = players[moves_played % 2]
            current_bot = bots[moves_played % 2]
            if current_bot:
                # bot's move
                print(current_player, "is thinking...")
                best_move, _, current_row, current_col = self.game.board.find_best_move(self.white_pieces, self.black_pieces, self.game.piece_mapping, current_player)
                self.white_pieces, self.black_pieces = self.game.board.move_piece(current_row, current_col, best_move[0], best_move[1], best_move[2],
                                           self.game.piece_mapping.mapping.values(), self.white_pieces, self.black_pieces, self.game.piece_mapping)
            else:
                # player's manual move
                self.player_select_and_move(ui, current_player)
                
            # check winners
            if self.game_finished():
                break

            moves_played += 1
            
        pygame.quit()
    
    def player_select_and_move(self, ui, current_player):

        def player_select_piece():
            while True:
                row, col, cheat = ui.get_mouse_click()
                self.cheat(cheat, current_player)
                possible_moves, selected_square = self.game.board.select_piece(self.game.piece_mapping, current_player, row, col)
                if possible_moves:
                    return (possible_moves, selected_square)
        
        def player_move_piece(possible_moves, cur_row, cur_col):
            row, col, cheat = ui.get_mouse_click()
            self.cheat(cheat, current_player)
            piece = self.game.piece_mapping.get_piece(self.game.board.board[cur_row][cur_col].piece)
            promotion_char = "" if not (piece.promotion and ((current_player == 'w' and row == 0) or (current_player == 'b' and row == self.rows - 1))) \
                                else string_input("Into which piece would you like to promote: ", "select", options=self.game.piece_mapping.mapping.keys())
            if (row, col, promotion_char) in possible_moves:
                self.white_pieces, self.black_pieces = self.game.board.move_piece(cur_row, cur_col, row, col, promotion_char,
                    self.game.piece_mapping.mapping.values(), self.white_pieces, self.black_pieces, self.game.piece_mapping)
                return True
            return False
        
        while True:
            possible_moves, selected_square = player_select_piece()
            ui.render_board(self.game.board, self.game.board.rows, self.game.board.columns, possible_moves, selected_square, self.game.piece_mapping)
            move_made = player_move_piece(possible_moves, selected_square[0], selected_square[1])
            if move_made:
                return
            possible_moves, selected_square = [], None
            ui.render_board(self.game.board, self.game.board.rows, self.game.board.columns, possible_moves, selected_square, self.game.piece_mapping)
    
    def cheat(self, cheatcode, player_turn):
        if cheatcode == "hint":
            target_square, piece, cur_row, cur_col = self.game.board.find_best_move(self.white_pieces, self.black_pieces, self.game.piece_mapping, player_turn)
            print(f"best move is by {piece} from ({cur_row}, {cur_col}) to {target_square}")
        elif cheatcode == "reset":
            print("Resetting...")
            print("unsuccessful.")
            pass
        elif cheatcode == "quit":
            self.running = False
            pass
        elif cheatcode == "eval":
            value_of_position = self.game.board.evaluate_position(self.white_pieces, self.black_pieces, self.game.piece_mapping)
            print(f"Position is evaluated as {value_of_position}")
        elif cheatcode == "help":
            print("Available cheats:")
            print("hint - show the best move")
            print("reset - reset the game")
            print("quit - quit the game")
            print("help - show this message")
            print("save - save the game")
            print("eval - evaluate the position")
        elif cheatcode == "save":
            print("Saving...")
            print("unsuccessful.")
            pass

    def game_finished(self):
        if not any(self.game.piece_mapping.get_piece(p[0]).is_special for p in self.white_pieces):
            print("Second player won!")
            return True
        if not any(self.game.piece_mapping.get_piece(p[0]).is_special for p in self.black_pieces):
            print("First player won!")
            return True
        return False
