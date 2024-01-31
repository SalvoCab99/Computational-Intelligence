import random
from game import Game, Move, Player
from copy import deepcopy
from tqdm.auto import tqdm
import pickle
import os

#Random player modified to have a higer probability to make an existing move
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = random.choice(perimeter_coordinate)
        move = random.choice(all_slides)
        return from_pos, move
    
ALPHA = 0.1
DISCOUNT_FACTOR = 1

perimeter_coordinate = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0)]
all_slides = [Move.TOP, Move.RIGHT, Move.BOTTOM, Move.LEFT]

#Created to modify the array, used to search the array in the dictionary
def rotate90(arr):
    rotated = [list(r) for r in zip(*arr[::-1])]
    return rotated
def vertical_mirror(arr):
    mirrored = [row[::-1] for row in arr]
    return mirrored

#it is called when select a move from the dictionary and in the dictionary we have a rotated array
def rotate_move_to_do(posmove, n): 
    p, s = posmove
    match n:
        case 0:#no rotation and mirroring
            pos, slide = p, s

        case 1:#it has been rotated 90 degrees rotaion clockwise, we need to rotate 90 degrees counterclockwise
            y, x = p
            pos = (x, (4 - y))
            i = all_slides.index(s)
            slide = all_slides[(i+3) % 4]

        case 2:#it has been rotated 180 degrees rotaion clockwise from original
            x, y = p
            pos = ((4 - x), (4 - y))
            i = all_slides.index(s)
            slide = all_slides[(i+2) % 4]

        case 3:#it has been rotated 270 degrees rotaion clockwise from original
            y, x = p
            pos = ((4- x), y)
            i = all_slides.index(s)
            slide = all_slides[(i+1) % 4]

        case 4:#vertical mirror
            x, y = p
            pos = ((4 - x), y)
            i = all_slides.index(s)
            if (i % 2 == 1):        #if slides right or left invert the slides
                slide = all_slides[4 - i]
            else:
                slide = s
                
        case 5:#it was vertical mirrored and rotated 90 degrees rotaion clockwise
            y, x = p
            pos = ((4 - x), (4 - y))
            i = all_slides.index(s)
            if (i < 2):        #if right-->top and if left-->bottom and viceversa
                slide = all_slides[1 - i]
            else:
                slide = all_slides[5 - i]

        case 6:#it was vertical mirrored and rotated 180 degrees rotaion clockwise (it's equal a orizontal mirror)
            x, y = p
            pos = (x, (4 - y))
            i = all_slides.index(s)
            if (i % 2 == 0):        #if slides top or bottom invert the slides
                slide = all_slides[2 - i]
            else:
                slide = s

        case 7:#it was vertical mirrored and rotated 270 degrees rotaion clockwise
            y, x = p
            pos = (x, y)
            i = all_slides.index(s)
            if (i == 0 or i == 3):        #if slides top or bottom invert the slides
                slide = all_slides[3 - i]
            else:
                slide = all_slides[3 - i]

        case _:
            print("impossible case")
    return pos, slide

#it is called only in training (update_dict) to rotate the move done before
def rotate_move_done(posmove, n): #it is called only in training to rotate the move done
    p, s = posmove
    match n:
        case 0:#no rotation and mirroring
            pos, slide = p, s

        case 1:#it will rotate 90 degrees rotaion clockwise
            y, x = p
            pos = ((4 - x), y)
            i = all_slides.index(s)
            slide = all_slides[(i+1) % 4]

        case 2:#it will rotate 180 degrees rotaion clockwise from original
            x, y = p
            pos = ((4 - x), (4 - y))
            i = all_slides.index(s)
            slide = all_slides[(i+2) % 4]

        case 3:#it will rotate 270 degrees rotaion clockwise from original
            y, x = p
            pos = (x,(4 - y))
            i = all_slides.index(s)
            slide = all_slides[(i+3) % 4]

        case 4:#vertical mirror
            x, y = p
            pos = ((4 - x), y)
            i = all_slides.index(s)
            if (i % 2 == 1):        #if slides right or left invert the slides
                slide = all_slides[4 - i]
            else:
                slide = s
                
        case 5:#it will vertical mirror and rotate 90 degrees rotaion clockwise
            y, x = p
            pos = ((4 - x), (4 - y))
            i = all_slides.index(s)
            if (i < 2):        #if right-->top and if left-->bottom and viceversa
                slide = all_slides[1 - i]
            else:
                slide = all_slides[5 - i]

        case 6:#it will vertical mirror and rotate 180 degrees rotaion clockwise (it's equal a orizontal mirror)
            x, y = p
            pos = (x, (4 - y))
            i = all_slides.index(s)
            if (i % 2 == 0):        #if slides top or bottom invert the slides
                slide = all_slides[2 - i]
            else:
                slide = s

        case 7:#it will vertical mirrored and rotate 270 degrees rotaion clockwise
            y, x = p
            pos = (x, y)
            i = all_slides.index(s)
            if (i == 0 or i == 3):        #if slides top or bottom invert the slides
                slide = all_slides[3 - i]
            else:
                slide = all_slides[3 - i]

        case 8:
            pos, slide = p, s
    return pos, slide

#Trained  player it's a classical Q-Lerning player with the addition of move_to_win that allows it to win if it only needs one move
class TrainedPlayer(Player):
    def __init__(self, player:int, use_file_dict: bool) -> None:
        super().__init__()
        self.player = player
        self.dictionary_x = {}
        self.state_dictionary_x = []
        self.dictionary_o = {}
        self.state_dictionary_o = []
        self.alpha = ALPHA
        self.epsilon = 1.0      #in the beginnig epsilon is set to 1 and each move it decreases exponetially
        self.dis_factor = DISCOUNT_FACTOR
        
        if(use_file_dict): #use file dict is used in training to update or recreate the dictionary
            if(player == 0):
                with open("Quixo/dict_x", 'rb') as file:
                    self.dictionary_x = pickle.load(file)
                with open("Quixo/state_dict_x", 'rb') as file:
                   self.state_dictionary_x = pickle.load(file)

            if(player == 1):
                with open("Quixo/dict_o", 'rb') as file:
                    self.dictionary_o = pickle.load(file)
                with open("Quixo/state_dict_o", 'rb') as file:
                    self.state_dictionary_o = pickle.load(file)

    #this function make all rotation and speculation to find a state that cuold be in the dictionary
    def find_in_dict(self, arr):
        i = 0
        if self.player == 0:
            dictionary = self.state_dictionary_x
        else:
            dictionary = self.state_dictionary_o
        while arr not in dictionary and i < 8:
            arr = rotate90(arr)
            if (i == 3 or i == 7):
                arr = vertical_mirror(arr)
            i +=1
        return i, arr

    #if it is a new move (n == 8) make a random move or if is it possible make a move to win
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        if self.epsilon != 0 and random.random() < self.epsilon:
            from_pos = random.choice(perimeter_coordinate)
            move = random.choice(all_slides)
        else:
            copy_g = deepcopy(game.get_board())
        #player X
            n_rotation, copy_g = self.find_in_dict(copy_g.tolist())
            if n_rotation == 8:      #if the state is not in the dictionary play a random move
                moves_to_win = []
                moves = []
                for pos in perimeter_coordinate:
                    for slide in all_slides:
                        fake_g = deepcopy(game)
                        valid = fake_g._Game__move(pos,slide, fake_g.current_player_idx)
                        if valid:
                            moves.append((pos,slide))
                            if self.state_value(fake_g) == 1:
                                moves_to_win.append((pos,slide))
                if (moves_to_win):
                    from_pos, move = random.choice(moves_to_win)
                else:
                    from_pos, move = random.choice(moves)
            else:
                move_values =[]
                possible_moves =[]
                possible_moves_in_dict = []
                if (self.player == 0):
                    for pos in perimeter_coordinate:
                        for slide in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]:
                            fake_g = deepcopy(game)
                            valid = fake_g._Game__move(pos,slide, fake_g.current_player_idx)
                            if valid:
                                choose = (tuple(map(tuple, copy_g)), pos, slide)
                                possible_moves.append(choose)
                                if choose in self.dictionary_x :
                                    possible_moves_in_dict.append(choose)
                                    move_values.append(self.dictionary_x[choose])
                    max_v = max(move_values, default=0.0)
                    if max_v > 0:
                        best_moves = [m for m in possible_moves_in_dict if self.dictionary_x[m] == max_v]
                    else:
                        best_moves= possible_moves
                    from_pos, move = rotate_move_to_do(random.choice(best_moves)[1:], n_rotation)
                
                #player O
                else:           
                    for pos in perimeter_coordinate:
                        for slide in all_slides:
                            fake_g = deepcopy(game)
                            valid = fake_g._Game__move(pos,slide, fake_g.current_player_idx)
                            if valid:
                                choose = (tuple(map(tuple, copy_g)), pos, slide)
                                possible_moves.append(choose)
                                if choose in self.dictionary_o :
                                    possible_moves_in_dict.append(choose)
                                    move_values.append(self.dictionary_o[choose])
                    max_v = max(move_values, default=0.0)
                    if max_v > 0:
                        best_moves = [m for m in possible_moves_in_dict if self.dictionary_o[m] == max_v]
                    else:
                        best_moves= possible_moves
                    from_pos, move = rotate_move_to_do(random.choice(best_moves)[1:], n_rotation)
        
        self.epsilon = self.epsilon*0.75 #function to decreases the epsilon
        if self.epsilon < 0.01:
            self.epsilon = 0
        return from_pos, move
    
    #function to update the dictionary (X or O), the dicionary is updated with the classical formula
    def update_dict(self, state, action, reward, g):
        if (self.player == 0):
            n, prev_state = self.find_in_dict(state.tolist())
            pos_dict, slide_dict = rotate_move_done(action, n)
            next_dict_values = []
            for pos in perimeter_coordinate:
                for slide in all_slides:
                    fake_g = deepcopy(g)
                    valid = fake_g._Game__move(pos,slide, fake_g.current_player_idx)
                    if valid:
                        choose = (tuple(map(tuple,fake_g.get_board())), pos, slide)
                        if choose in self.dictionary_x :
                            next_dict_values.append(self.dictionary_x[choose])
            if next_dict_values : 
                max_next_value = max(next_dict_values)
            else:
                max_next_value = 0
            current_v = 0 if (tuple(map(tuple, prev_state)), pos_dict, slide_dict) not in self.dictionary_x else self.dictionary_x[tuple(map(tuple, prev_state)), pos_dict, slide_dict]
            result = (1 - self.alpha)*current_v + self.alpha*(reward + self.dis_factor * max_next_value)
            self.dictionary_x[tuple(map(tuple, prev_state)), pos_dict, slide_dict] = result
            if n == 8:
                self.state_dictionary_x.append(prev_state)
        else:
            n, prev_state = self.find_in_dict(state.tolist())
            pos_dict, slide_dict = rotate_move_done(action, n)
            next_dict_values = []
            for pos in perimeter_coordinate:
                for slide in all_slides:
                    fake_g = deepcopy(g)
                    valid = fake_g._Game__move(pos,slide, fake_g.current_player_idx)
                    if valid:
                        choose = (tuple(map(tuple,fake_g.get_board())), pos, slide)
                        if choose in self.dictionary_o :
                            next_dict_values.append(self.dictionary_o[choose])
            if next_dict_values : 
                max_next_value = max(next_dict_values)
            else:
                max_next_value = 0
            current_v = 0 if (tuple(map(tuple, prev_state)), pos_dict, slide_dict) not in self.dictionary_o else self.dictionary_o[tuple(map(tuple, prev_state)), pos_dict, slide_dict]
            result = (1 - self.alpha)*current_v + self.alpha*(reward + self.dis_factor * max_next_value)
            self.dictionary_o[tuple(map(tuple, prev_state)), pos_dict, slide_dict] = result
            if n == 8:
                self.state_dictionary_o.append(prev_state)

    #function to give the player the reward of its state
    def state_value(self, g) -> float:
        """Evaluate state:  +1 if our player wins
                            -1 if our player loses
                            -0.01 if a player move"""
        if g.check_winner() == -1:
            return -0.01
        if g.check_winner() == 0:
            return 1 if self.player == 0 else -1
        return 1 if self.player == 1 else -1

#function created to train the player in a lot of match, the dictionaries will be saved in a file 
def train(num_episodes, player, use_file_dict):
    if player == 0:
        players = [TrainedPlayer(0, use_file_dict), RandomPlayer()]
        print(len(players[0].state_dictionary_x), "states in X")
        print(len(players[0].dictionary_x), "states + actions in X")
    elif player == 1:
        players = [RandomPlayer(), TrainedPlayer(1, use_file_dict)]
        print(len(players[1].state_dictionary_o), "states in O")
        print(len(players[1].dictionary_o), "states + actions in O")
    for _ in tqdm(range(num_episodes)):
        g = Game()
        num = 0
        players[player].epsilon = 1.0
        winner = -1
        while winner < 0 and num < 150:
            g.current_player_idx += 1
            g.current_player_idx %= len(players)
            ok = False
            state = g.get_board()
            while not ok:
                from_pos, slide = players[g.current_player_idx].make_move(g)
                ok = g._Game__move(from_pos, slide, g.current_player_idx)
            num +=1
            action = from_pos, slide
            reward = players[player].state_value(g)
            players[player].update_dict(state, action, reward, g)
            winner = g.check_winner()
            
    if (player == 0):
        if os.path.exists("Quixo/dict_x"):
            os.remove("Quixo/dict_x")
        if os.path.exists("Quixo/state_dict_x"):
            os.remove("Quixo/state_dict_x")

        with open("Quixo/dict_x", 'wb') as file:
            pickle.dump(players[0].dictionary_x, file)
        with open("Quixo/state_dict_x", 'wb') as file:
            pickle.dump(players[0].state_dictionary_x, file)
        print(len(players[0].state_dictionary_x), "states in X")
        print(len(players[0].dictionary_x), "states + actions in X")
    elif (player == 1):
        if os.path.exists("Quixo/dict_o"):
            os.remove("Quixo/dict_o")
        if os.path.exists("Quixo/state_dict_o"):
            os.remove("Quixo/state_dict_o")
        with open("Quixo/dict_o", 'wb') as file:
            pickle.dump(players[1].dictionary_o, file)
        with open("Quixo/state_dict_o", 'wb') as file:
            pickle.dump(players[1].state_dictionary_o, file)
        print(len(players[1].state_dictionary_o), "states in O")
        print(len(players[1].dictionary_o), "states + actions in O")