### File: game.py
In the class `Game` have been done two changes:
*   one is in the function `print(self)`, beacuse I print the table in a different way (`-1`->`_|`,`0`->`X`,`1`->`O`) and in some cases I print the move done of the players
*   I added a counter, this counter count the number of moves that are done, if the counter go over 150 the game will return a winner = -1, in this way is impossible to do infinite match 

### File: main.py
##### Classes:
*   `RealPlayer(Player)`: It's a class that allows us to play vs the other Players.
#### Funcitons:

*   `bot_match(play)`: Start a match of two Players (qlearnig,minmax,random) that are not humans, the players are selected by the user.
*   `stats(num_episodes, play)`: Compute matches and show results of two Players (qlearnig,minmax,random), the players are selected by the user.
*   `__name__ == '__main__'`: In the main section will will be shown a menu when the user can decide what to do(play vs other Players, watch results of different matches, whatch a match and also traning the qlearning player(`train` secret word in the menu, here you can decide if retrain the Player or update the dictionary with some match).

## Players

### RandomPlayer:
A class of players that makes random moves.
### Q-learning (qlearning.py):

**TrainedPlayer**: A class of players implementing Q-learning. It learns by playing against itself or other players and updates its Q-table accordingly.

*   `find_in_dict`: Finds a state in the dictionary by rotating and mirroring the board state.
*   `make_move`: Chooses the best move based on the current state, considering the trade-off between exploration and exploitation. In this function that is a "cheat", when it checks all possible actions and the next move is a win it will do that move. The reason of taking this decision is to train the player to find quicly the move that allows it to win, but i know that it will require a lot of training that my pc doesn't support :(
*   `update_dict`: Updates the Q-table based on the received reward.
*   `state_value`: Evaluates the state based on the game board.

**train**: Trains the Q-learning player by playing many episodes against random players and saves the learned Q-table to a file.

### Minimax (minmax.py):

**MinMaxPlayer**:  A class of players implementing the Minimax algorithm with alpha-beta pruning.
*   `make_move`: Chooses the best move based on the Minimax algorithm up to a certain depth (in my case `depth` = 2, it is editable from the code, but I really think this number is a good balance between performance and efficiency).
*   `minmax`: Implements the Minimax algorithm recursively with alpha-beta pruning. It starts with `alpha`= -100 and  `beta` = 100 and then compute recursively the algorithm unless it reaches the depth, in the `leaves` there is the value given from state_value.
*   `state_value`: Evaluates the state based on the game state. The evaluation is 20 if `X` wins, -20 if `O` wins, 2*(max(linex)-max(lineo)) in the other cases where linex= maximum number of X in the same line(rows, columns or 2 diagonal) lineo= linex but `O` insted of `X`