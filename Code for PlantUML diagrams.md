Class diagram:
```
@startuml
!theme crt-amber
!define RECTANGLE class

RECTANGLE main {
Main: Manage cycle create/load -> save -> train -> play

  +main(): Entry point for the application
  +ask_for_saving(): Ask the player to save the game
  +ask_for_training(): Ask the player to train the bots
  +train_game(): Initiate bot training process
}

RECTANGLE Helpers.UserSupervisor {
    UserSupervisor: Ensure proper inputs from the user

  +string_input(): Supervise string input
  +list_input(): Supervise list input
}

RECTANGLE GeneticAlgorithmTraining {
GeneticAlgorithmTraining: Training featuring genetic algorithm

  -initial_gameset: Gameset
  -num_games_in_generation: int
  -num_best_children: int
  -mutation_rate: float
  -evaluation_scores: List(Tuple)
  -generation_count: int
  -filename: Optional(str)
  +update_coefficients(): Update initial game's coefficients
  +train(): Train game strategies using genetic algorithm
  +log_black_win(): Log black winning occurrence
  +log_generation_info(): Log generation information
  +play_n_moves(): Play N moves for the given game
  +play_game(): Concurrent play by multiple bots
}

RECTANGLE TrainingFlow {
TrainingFlow: Flow of the running game

  -game: Gameset
  -running: bool
  -white_pieces: List(Tuple)
  -black_pieces: List(Tuple)
  +play_game(): Run game loop
  +game_finished(): Check game termination condition
}

RECTANGLE GameFlow {
GameFlow: Flow of the running game with UI

  -game: Gameset
  -white_bot: bool
  -black_bot: bool
  -running: bool
  -white_pieces: List(Tuple)
  -black_pieces: List(Tuple)
  +play_game(): Run game loop
  +player_select_and_move(): Manage player's turn
  +cheat(): Handle cheat codes
  +game_finished(): Check game termination condition
}

RECTANGLE Gameset {
Gameset: Class responsible for the game components and their state

  -pieces: List(ChessPiece): unique pieces of the game
  -board: ChessBoard: current board state
  -piece_mapping: PieceMapping
  -white_coefficients: Tuple
  -black_coefficients: Tuple
  +randomize_coefficients(): Randomize coefficients for evaluation
  +create_game(): Set up board and pieces
  +set_specials(): Specify most important pieces
  +save_game(): Save game state to a file
  +load_game(): Load game state from a file
}

RECTANGLE GameUI {
GameUI: UI based on Pygame

  -square_size: int
  -screen: pygame.Surface
  -clock: pygame.Clock
  +render_board(): Render ChessBoard and pieces
  +process_events(): Process Pygame events
  +get_mouse_click(): Get mouse click coordinates
  +set_color_palette(): Set color palette
  +set_window_dimensions(): Adjust window size
}

RECTANGLE GameSetup {
GameSetup: Helper for setting up the game components

  -rows: int
  -columns: int
  -pieces: List(ChessPiece)
  -board: ChessBoard
  +setup_pieces(): Add pieces to the game
  +setup_board(): Initialize game board
  +white_black_division(): Divide pieces into factions
}

RECTANGLE ChessBoard {
ChessBoard: Current board state

  -rows: int
  -columns: int
  -board: List(List(ChessBoardPiece))
  +to_json(): Serialize board state to JSON
  +from_json(): Deserialize board state from JSON
  +get_possible_moves(): All possible moves for a piece
  +ninja_moves(): All possible moves for a ninja piece
  +select_piece(): Select a piece for movement
  +move_piece(): Move a piece on the board
  +is_valid_position(): Whether position on the board is valid
  +evaluate_position(): Evaluate current board position
  +calculate_evaluation(): Evaluation for one side
  +minimax(): Minimax algorithm + alpha-beta pruning
  +find_best_move(): Find best move using minimax
}

RECTANGLE PieceMapping {
PieceMapping: Mapping (symbol -> ChessPiece)

  -mapping: Dict(str, ChessPiece)
  +add_piece(): Add a piece to the mapping
  +get_piece(): Get a piece from the mapping
  +get_all_pieces(): Get the mapping
  +set_all_pieces(): Map the list of ChessPieces
}

RECTANGLE ChessPiece {
ChessPiece: Represents a distinct piece to be used in a game

  -name: str
  -symbol: str
  -moves: List(Move)
  -max_steps: int
  -max_cells_reachable: int
  -value: int
  -special_properties: List(bool)
  +to_string(): Encode into a string
  +from_string(): Initialize instance from a string
  +get_moves(): String input into list of possible moves
  +is_valid_position(): Check if position is valid
  +calculate_reachable_cells(): Reachable cells in the position
  +calculate_reachable_cells_stats(): Get max and avg of reachable cells
}

RECTANGLE ChessBoardPiece {
ChessBoardPiece: Entity on the board

  -piece: ChessPiece
  -color: str
  +__str__(): Convert into a string
  +from_string(): Initialize from a string
}

RECTANGLE Move {
Move: A rule for piece's move

  -x: int
  -y: int
  -moving: bool
  -capturing: bool
}

main --> GeneticAlgorithmTraining
main --> TrainingFlow
main --> GameFlow
GeneticAlgorithmTraining --> Gameset
GeneticAlgorithmTraining --> GameFlow
GeneticAlgorithmTraining --> TrainingFlow
TrainingFlow --> Gameset
TrainingFlow --> GameSetup
GameFlow --> GameSetup
GameFlow --> Gameset
GameFlow --> GameUI
Gameset --> ChessBoard
Gameset --> PieceMapping
Gameset --> ChessPiece
Gameset --> GameSetup
GameUI --> ChessBoard
GameSetup --> ChessBoard
GameSetup --> ChessPiece
GameSetup --> ChessBoardPiece
ChessBoard --> PieceMapping
ChessBoard --> ChessBoardPiece
ChessBoard --> ChessPiece
PieceMapping --> ChessPiece
ChessPiece --> Move
@enduml
```

