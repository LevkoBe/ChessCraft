# ChessCraft

### **Table of Contents**

1. [Introduction](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#introduction)
2. [Project Structure and Core Components](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#project-structure-and-core-components)
3. [Game Concept](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#game-concept)
4. [Installation](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#installation)
5. [Usage](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#usage)
6. [Contribution Guidelines](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#contribution-guidelines)
7. [Next Steps](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#next-steps)
8. [About the Authors](https://github.com/LevkoBe/ChessCraft/blob/graphics/README.md#about-the-authors)

## **Introduction**

Welcome to the comprehensive documentation for ChessCraft, an innovative and dynamic game that pushes the boundaries of traditional chess gameplay. ChessCraft offers players a platform to unleash their creativity by allowing them to customize every aspect of the game, from board dimensions to piece types, rules, special features, initial setup, and victory conditions. Whether you're a seasoned chess enthusiast or a newcomer to the world of strategic gameplay, ChessCraft offers a unique and engaging experience that caters to players of all skill levels.

## **Project Structure and Core Components**

ChessCraft is structured around a modular architecture consisting of several core components, each responsible for distinct aspects of the game's functionality. These components include:

1. **Main Control Hub (`main.py`)**: This module serves as the entry point for the application, orchestrating game creation, loading, and training processes based on user input. It manages the game's main logic and user interactions, ensuring a seamless gameplay experience.
2. **Game Customization (`Gameset.py`)**: The `Gameset` class manages the game state, including pieces, board, and coefficients for evaluation. It provides functionality for setting up custom games, loading/saving game states, and adjusting coefficients for bot training.
3. **Game Board Management (`ChessBoard.py`)**: The `ChessBoard` class handles the game board and related operations, such as calculating possible moves, evaluating positions, and facilitating AI decision-making using algorithms like minimax and alpha-beta pruning.
4. **AI Bot Strategies (`GameTraining.py`)**: ChessCraft features advanced AI bots with multi-layered intelligence. These bots understand game rules, evaluate board positions, and determine optimal moves using sophisticated algorithms. The `GeneticAlgorithm` class orchestrates the training process, optimizing bot strategies through genetic algorithms and coefficient adjustments.
5. **User Interface (`GameUI.py`)**: The `GameUI` module manages the graphical user interface of the game, rendering the chessboard, pieces, and game-related information using the Pygame library. It provides an interactive interface for players to view and interact with the game elements seamlessly.

You can see more details on the class diagram below (click to upscale):

https://github.com/LevkoBe/ChessCraft/assets/118983753/496f2f24-7667-44b1-b999-30d21b908e79

## **Game Concept**

ChessCraft redefines traditional chess gameplay by offering players unparalleled freedom and customization options. Players can:

- Define board dimensions, piece types, rules, and special features like invisibility or cloning.
- Customize initial piece setup, including the number and positions of pieces for black and white factions.
- Specify game-end conditions, such as selecting key pieces to be captured for victory.
- Engage in various gameplay modes, including player-vs-player, player-vs-bot, or bot-vs-bot matches.
- Utilize cheat codes for hints, evaluation of position, and other options.
- Set color palettes for a personalized gaming experience. This includes predefined palettes as well as random ones, with the possibility to save them and reuse later.
- Train AI bots to improve their strategies and challenge themselves with increasingly formidable opponents.

ChessCraft empowers players to explore their strategic prowess, experiment with new gameplay mechanics, and engage in thrilling chess battles like never before. Whether you're a casual player looking for a fun challenge or a competitive enthusiast seeking to hone your skills, ChessCraft offers endless possibilities for enjoyment and strategic growth. Are you ready to embark on your chess adventure with ChessCraft? Let the game begin!

To understand the program even better, see the diagrams below (click on the image to zoom in):

Use-case diagram:

https://github.com/LevkoBe/ChessCraft/assets/118983753/fd007d43-f13b-4739-8953-c9b529dcd561

State diagram:

https://github.com/LevkoBe/ChessCraft/assets/118983753/acf89432-762f-42e7-8059-cde1ef10e243

You can also review the [presentation](https://www.canva.com/design/DAGCfR5YdRo/_uuWHMq1nkiyPIJXt8NGwA/edit?utm_content=DAGCfR5YdRo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) about the game.

## **Installation**

To install ChessCraft, follow these steps:

1. Clone the repository from GitHub:
    
    ```
    git clone <https://github.com/LevkoBe/ChessCraft>
    
    ```
    
2. Navigate to the project directory:
    
    ```
    cd ChessCraft
    
    ```
    
3. Install the required dependencies using pip:
    
    ```
    pip install pygame
    
    ```
    
4. Once the dependencies are installed, you're ready to start using ChessCraft!

## **Usage**

To use ChessCraft, follow these guidelines:

1. Run the `main.py` script to start the application:
    
    ```
    python main.py
    
    ```
    
2. Follow the on-screen prompts to create a new game, load a saved game, or exit the application.
You can also use predefined inputs for games, saved in the file `inputs.ipynb` — just copy-paste the contents of any cell into the terminal (use combinations `Ctrl`+`A`, `Ctrl`+`C`, and `Ctrl`+`V`).
Or to load some of the existing games, enter `load`, and then type some name of the game from the folder `saved_games`, for example `chess`.
3. While creating a new game, you can customize the game settings, including board dimensions, piece types, rules, and special features. Afterwards, you can save the game, entering `yes` when asked.
4. Play against another player, challenge the AI bot, or watch bot-vs-bot matches to observe different strategies in action. If you want, you can change the mode in the `main.cpp` file before the game.
5. Utilize cheat codes for hints, save/load games, and set color palettes for a personalized gaming experience. Palettes can be set with pressing any number from `0` to `9`, or with `?` you can get some random one. Some cheatcodes can be `hint`, `eval`, or `quit`.
6. Experiment with different game setups, train AI bots to improve their strategies, and enjoy the endless possibilities offered by ChessCraft!

## **Contribution Guidelines**

We welcome contributions from the community to help improve ChessCraft. Here are some guidelines for contributing:

1. Fork the repository and create a new branch for your contributions.
2. Make your changes or enhancements to the codebase.
3. Ensure that your code follows the project's coding style and conventions.
4. Write clear and concise commit messages explaining the purpose of your changes.
5. Test your changes thoroughly to ensure they do not introduce any regressions.
6. Submit a pull request detailing the changes you've made and the rationale behind them.
7. Your pull request will be reviewed by the project maintainers, and any necessary feedback will be provided.
8. Once your changes are approved, they will be merged into the main codebase.

## **Next Steps**

As we continue to develop ChessCraft, here are some next steps and potential areas for improvement:

1. Code Efficiency Optimization: Optimize code for better performance and resource utilization.
2. Minimax Heuristics: Implement heuristics to speed up move analysis and allow bots to analyze with greater depth.
3. GUI and User-Friendliness: Develop a graphical user interface for game setup and level selection to enhance user experience.
4. Minimax Time-Limiting: Implement time-limiting for minimax to prevent excessive computation and improve responsiveness.
5. Endless Games Resolution: Address issues with games getting stuck in endless loops by implementing safeguards or alternate victory conditions.
6. More Game Sets: Add more predefined game setups and saved games to provide players with diverse options.
7. Less Rules Limitations: Allow for more flexibility in defining game rules and constraints to encourage creativity.
8. Levels Differentiation: Introduce adjustable difficulty levels and create a map with varying challenges and rule sets.
9. Handling Other Cheat Codes: Expand cheat code functionality to include features like saving, resetting games, and reversing moves.

## **About the Authors**

ChessCraft is the collaborative effort of Levko Beniakh and Varvara Chornomorets, two dedicated software engineers with a shared passion for strategic gaming and innovative development.

Levko Beniakh took the lead in developing fundamental game classes such as piece, board, and gameset, along with handling game setup, visuals, move mechanics, finding possible moves, implementing the genetic algorithm, and enhancing the static evaluation function. Levko's proactive approach and wealth of ideas played a pivotal role in shaping the project's direction.

Varvara Chornomorets contributed significantly to the implementation of advanced AI algorithms, including minimax and alpha-beta pruning, as well as crafting the basic static evaluation function. Varvara also played a crucial role in the project's presentation and overall refinement.

Throughout the development process, Levko and Varvara engaged in open discussions, collaborated on reviews, and offered valuable suggestions for improvements and fixes. While Levko demonstrated more initiative and generated additional ideas, both authors played integral roles in bringing ChessCraft to fruition.

For more information about **[Levko Beniakh](https://www.linkedin.com/in/levko-beniakh-91a2422b4/)** and their projects, check out their [GitHub profile](https://github.com/LevkoBe). Stay updated on **[Varvara Chornomorets](https://www.linkedin.com/in/varvara-chornomorets-005a262a2/)**' contributions and future endeavors by following them on social media.

> You may also like: TanksGame
>
