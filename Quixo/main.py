import random
from game import Game, Move, Player


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class RealPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # Leggi le coordinate da tastiera
        from_pos_input = tuple(map(int, input("Inserisci le coordinate (x y): ").split()))

        # Leggi la mossa da tastiera
        move_input_str = input("Inserisci la mossa (TOP, BOTTOM, LEFT, RIGHT): ").upper()
        move_input = Move[move_input_str]
        print(from_pos_input)

        return from_pos_input, move_input


if __name__ == '__main__':
    g = Game()
    g.print()
    player1 = RandomPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
