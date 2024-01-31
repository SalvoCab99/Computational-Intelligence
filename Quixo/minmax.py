from game import Game, Move, Player
import numpy as np
from copy import deepcopy

perimeter_coordinate = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0)]
all_slides = [Move.TOP, Move.RIGHT, Move.BOTTOM, Move.LEFT]

class MinMaxPlayer(Player):
    def __init__(self, player) -> None:
        super().__init__()
        self.player = player


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        fake_g = deepcopy(game)
        best_move, _ = self.minmax(fake_g, 2, self.player, -100, 100)       #at the beginning the depth is set to 2, alpha -100 and beta 100
        from_pos, move = best_move
        return from_pos, move
    
    def minmax(self, game, depth, fake_p, alpha, beta):
        val = self.state_value(game)
        if (val == -20 or val == 20):
            return None, val
        if (depth > 0):
            if(fake_p == 0):
                for pos in perimeter_coordinate:
                    for slide in all_slides:
                        fake_g = deepcopy(game)
                        valid = fake_g._Game__move(pos,slide, 0)
                        if valid:
                            _, leaf = self.minmax(fake_g, depth-1, (1-fake_p), alpha, beta)
                            if(leaf > alpha):
                                alpha = leaf
                                best_move = pos, slide
                            
                            if(alpha >= beta):
                                break
                return best_move, alpha
            else:
                for pos in perimeter_coordinate:
                    for slide in all_slides:
                        fake_g = deepcopy(game)
                        valid = fake_g._Game__move(pos,slide, 1)
                        if valid:
                            _,leaf = self.minmax(fake_g, depth-1, 1-fake_p, alpha, beta)
                            if(leaf < beta):
                                beta = leaf
                                best_move = pos, slide
                            
                            if(alpha >= beta):
                                break
                return best_move, beta

        return None, val
    
    #Evaluation state, the result will be depend on X or O in each row and column and also on the two orizontal lines
    def state_value(self, g) -> float:
        """Evaluate state:  +20 if X player wins
                            -20 if O player wins
                            range(8,-8) if nobody wins, it depends to the state of the game"""
        win = g.check_winner()
        if win == -1:
            state = g.get_board()
            max_x = max(np.max(np.sum(state == 0, axis=1)), np.max(np.sum(state == 0, axis=0)))
            max_o = max(np.max(np.sum(state == 1, axis=1)), np.max(np.sum(state == 1, axis=0)))
            max_x_orizontal = max(sum(1  for i in range(5) if state[i][i]==0),sum(1  for i in range(5) if state[4-i][i]==0))
            max_o_orizontal = max(sum(1  for i in range(5) if state[i][i]==1),sum(1  for i in range(5) if state[4-i][i]==1))
            result = 2*(max(max_x,max_x_orizontal)-max(max_o,max_o_orizontal))
            return result
        
        if win == 0:
            return 20
        return -20