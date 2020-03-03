from utility.null import Null
from utility.warrior import Warrior

class Board:

    game_tiles = {}

    def __init__(self):
        self.possible_steps = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]

    def create_board(self):
        # Fill board with nulls
        for tile in range(100):
            self.game_tiles[tile] = Null(None, None)

        # Add tribe 1
        self.game_tiles[3] = Warrior(1, 3)
        self.game_tiles[6] = Warrior(1, 6)
        self.game_tiles[30] = Warrior(1, 30)
        self.game_tiles[39] = Warrior(1, 39)

        # Add tribe 2
        self.game_tiles[60] = Warrior(2, 60)
        self.game_tiles[69] = Warrior(2, 69)
        self.game_tiles[93] = Warrior(2, 93)
        self.game_tiles[96] = Warrior(2, 96)

    def print_board(self):
        for tiles in range(100):
            print('|', end=self.game_tiles[tiles].to_string())

            if (tiles+1)%10 == 0:
                print('|', end='\n')
