import random
from game import Game, Move, Player
from tqdm.auto import tqdm
from qlearning import RandomPlayer, TrainedPlayer, train
from minmax import MinMaxPlayer

#Variables created for computing all exinsting position
perimeter_coordinate = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0)]
all_slides = [Move.TOP, Move.RIGHT, Move.BOTTOM, Move.LEFT]

#If you want to try some match I created a interactive Player
class RealPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # Read coordinates from keybord
        from_pos_input = tuple(map(int, input("Insert coordinates (x y): ").split()[:2]))
        while 0 > from_pos_input[0] > 4 and 0 > from_pos_input[1] > 4:
            from_pos_input = tuple(map(int, input("Coordinates have to be between 0 e 4 (Ex.:0 3): ").split()[:2]))
        # Read slide from keyboard
        legit_move =["TOP", "BOTTOM", "LEFT", "RIGHT"]
        move_input_str = input("Where do you want to move? (TOP, BOTTOM, LEFT, RIGHT): ").upper()
        while (move_input_str not in legit_move):
            move_input_str = input("Not valid, reinsert (TOP, BOTTOM, LEFT, RIGHT): ").upper()
        move_input = Move[move_input_str]
        return from_pos_input, move_input

#Funcition used when we want to see a bot match
def bot_match(play):
    match(play):
        case 1:
            player1, player2 = [TrainedPlayer(0, True), MinMaxPlayer(1)]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("Q-Learning WON!!(X)")
            else:
                print("MinMax WON!!(O)")
        case 2:
            player1, player2 = [MinMaxPlayer(0), TrainedPlayer(1, True)]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("MinMax WON!!(X)")
            else:
                print("Q-Learning WON!!(O)")
        case 3:
            player1, player2 = [TrainedPlayer(0, True), RandomPlayer()]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("Q-Learning WON!!(X)")
            else:
                print("Random WON!!(O)")
        case 4:
            player1, player2 = [RandomPlayer(), TrainedPlayer(1, True)]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("Random WON!!(X)")
            else:
                print("Q-Learning WON!!(O)")
        case 5:
            player1, player2 = [MinMaxPlayer(0), RandomPlayer()]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("MinMax WON!!(X)")
            else:
                print("Random WON!!(O)")
        case 6:
            player1, player2 = [RandomPlayer(), MinMaxPlayer(1)]
            g = Game()
            winner = g.play(player1, player2)
            g.print()
            if (winner == 0):
                print("Random WON!!(X)")
            else:
                print("MinMax WON!!(O)")


#Function created for view the performance of created players
def stats(num_episodes, play):
    match (play):
        case 1:
            player1, player2 = [TrainedPlayer(0, True), MinMaxPlayer(1)]
            print("Q-Learning vs MinMax")
        case 2:
            player1, player2 = [MinMaxPlayer(0), TrainedPlayer(1, True)]
            print("MinMax vs Q-Learning")
        case 3:
            player1, player2 = [TrainedPlayer(0, True), RandomPlayer()]
            print("Q-Learning vs Random")
        case 4:
            player1, player2 = [RandomPlayer(), TrainedPlayer(1, True)]
            print("Random vs Q-Learning")
        case 5:
            player1, player2 = [MinMaxPlayer(0), RandomPlayer()]
            print("MinMax vs Random")
        case 6:
            player1, player2 = [RandomPlayer(), MinMaxPlayer(1)]
            print("Random vs MinMax")
    p1win = 0
    p2win = 0
    for _ in tqdm(range(num_episodes)):
        g = Game()
        players = [player1, player2]
        winner = -1
        count = 0
        while winner < 0:
            g.current_player_idx += 1
            g.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[g.current_player_idx].make_move(g)
                ok = g._Game__move(from_pos, slide, g.current_player_idx)
            winner = g.check_winner()
            count +=1
            if(count > 150):
                break
        if winner == 0:
            p1win += 1
        else:
            p2win +=1
    print("player 1 won", p1win)
    print("player 2 won", p2win)
    print("draws", num_episodes - (p1win+p2win))

#menu
def show_menu():
    print("1. Play against Trained Player")
    print("2. Play against Random Player")
    print("3. Watch a bot match")
    print("4. Compute some games and view stats")
    print("q. Quit")

def welcome():
    print(r"""
 __      __          ___                                          __               _____                                  
/\ \  __/\ \        /\_ \                                        /\ \__           /\  __`\          __                 
\ \ \/\ \ \ \     __\//\ \     ___    ___     ___ ___      __    \ \ ,_\   ___    \ \ \/\ \  __  __/\_\   __  _   ___   
 \ \ \ \ \ \ \  /'__`\\ \ \   /'___\ / __`\ /' __` __`\  /'__`\   \ \ \/  / __`\   \ \ \ \ \/\ \/\ \/\ \ /\ \/'\ / __`\ 
  \ \ \_/ \_\ \/\  __/ \_\ \_/\ \__//\ \_\ \/\ \/\ \/\ \/\  __/    \ \ \_/\ \_\ \   \ \ \\'\\ \ \_\ \ \ \\/>  <//\ \_\ \
   \ `\___x___/\ \____\/\____\ \____\ \____/\ \_\ \_\ \_\ \____\    \ \__\ \____/    \ \___\_\ \____/\ \_\/\_/\_\ \____/
    '\/__//__/  \/____/\/____/\/____/\/___/  \/_/\/_/\/_/\/____/     \/__/\/___/      \/__//_/\/___/  \/_/\//\/_/\/___/                           
""")


if __name__ == '__main__':
    welcome()
    while True:
        show_menu()
        option = input("Write what you want to do: ")
        print()
        match option:
            case "1":   #Match against Trained player
                print("You will play against Trained Player")
                print("1. Play against Q_Learning Player")
                print("2. Play against MinMax Player (maybe unbeatable)")
                p = input("Select the opponent: ")
                while p != "1" and p != "2":
                    p = input("Not valid opponent -> 1 or 2: ")
                print(p)
                select = input("Select your side (X or O): ").upper()
                while select != "O" and select != "X":
                    select = input("Not valid select X or O: ").upper()
                print(select)
                if (select == "X"):
                    g = Game()
                    player1 = RealPlayer()
                    player2 = TrainedPlayer(1, True) if p == "1" else MinMaxPlayer(1)
                    winner = g.play(player1, player2)
                    g.print()
                    if (winner == 0):
                        print("YOU WON!!")
                    else:
                        print("YOU LOSE :(")
                else:
                    g = Game()
                    player1 = TrainedPlayer(0, True) if p == "1" else MinMaxPlayer(0)
                    player2 = RealPlayer()
                    winner = g.play(player1, player2)
                    g.print()
                    if (winner == 1):
                        print("YOU WON!!")
                    else:
                        print("YOU LOST :(")
            case "2":
                print("You will play against Random Player")
                select = input("Select your side (X or O): ").upper()
                while select != "O" and select != "X":
                    select = input("Not valid select X or O: ").upper()
                if (select == "X"):
                    g = Game()
                    player1 = RealPlayer()
                    player2 = RandomPlayer()
                    winner = g.play(player1, player2)
                    g.print()
                    if (winner == 0):
                        print("YOU WON!!")
                    else:
                        print("YOU LOSE :(")
                else:
                    g = Game()
                    player1 = RandomPlayer()
                    player2 = RealPlayer()
                    winner = g.play(player1, player2)
                    g.print()
                    if (winner == 1):
                        print("YOU WON!!")
                    else:
                        print("YOU LOST :(")
            case "3":
                print("What do you want to see?")
                print("1. Q_Learning Player vs MinMax Player")
                print("2. MinMax Player vs Q_Learning Player")
                print("3. Q_Learning Player vs Random Player")
                print("4. Random Player vs Q_Learning Player")
                print("5. MinMax Player vs Random Player")
                print("6. Random Player vs MinMax Player")
                while True:
                    play = input("Enter your choice (1-6): ")
                    if play.isdigit():  # Verify if it is a number
                        play = int(play)
                        if 1 <= play <= 6:  # Verify if it is between 1 and 6
                            break
                    print("Please enter a valid choice (1-6)")
                bot_match(play)
            case "4":
                print("Let's see some results")
                print("What do you want to see? Results of ")
                print("1. Q_Learning Player vs MinMax Player")
                print("2. MinMax Player vs Q_Learning Player")
                print("3. Q_Learning Player vs Random Player")
                print("4. Random Player vs Q_Learning Player")
                print("5. MinMax Player vs Random Player")
                print("6. Random Player vs MinMax Player")
                while True:
                    play = input("Enter your choice (1-6): ")
                    if play.isdigit():  # Verify if it is a number
                        play = int(play)
                        if 1 <= play <= 6:  # Verify if it is between 1 and 6
                            break
                    print("Please enter a valid choice (1-6)")
                while True:
                    ep = input("how many matches? (from 1 to 100) ")
                    if ep.isdigit():  # Verify if it is a number
                        ep = int(ep)
                        if 1 <= ep <= 100:  # Verify if it is between 1 and 100
                            break
                    print("Please enter a valid choice (1-6)")
                stats(ep, play)
            case "train":
                select = input("Do you want to train X or O: ").upper()
                while select != "O" and select != "X":
                    select = input("Not valid, select X or O: ").upper()
                print("Do you want to update or recreate the dictionary? (1000 episodes)")
                print("(u)update        (r)recreate (UNRACCOMANDED)")
                p = input("").lower()
                while p != "u" and p != "r":
                    p = input("Not valid - u or r: ").lower()
                if(select == "X"):
                    train(500, 0, True if p=="u" else False)
                if(select == "O"):
                    train(500, 1, True if p=="u" else False)
            case "q":
                print("Good bye!")
                break
            case _:
                print("It is not valid")
