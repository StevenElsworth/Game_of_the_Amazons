class Game:

    def __init__(self):
        self.board = Board()
        self.turn = '1'

    def make_play(self, piece, move, shoot):
        """
        This function assumes the move and shoot actions are legal.
        """
        # --------
        # MOVE
        # --------
        moving_piece = self.board.game_tiles[piece] # get Warrior object
        moving_piece.position = move # assign position attribute to index of Warrior
        self.board.game_tiles[move] = moving_piece # assign Warrior object on game board to proposed location using index
        self.board.game_tiles[piece] = Null(None, None) # generate empty tile for where Warrior was before moving

        # --------
        # SHOOT
        # --------
        self.board.game_tiles[shoot] = Flame(0, shoot) # assign Flame object to location which has been shot

        # Change turn of player
        if self.turn == '1':
            self.turn = '2'
        else:
            self.turn = '1'

    def find_available_plays(self):
        """
        Find all available plays for a player.
        """
        available_plays = {} # dictionary for efficiency
        for i, tile in enumerate(self.board.game_tiles):
            if tile.to_string() == self.turn: # found a warrior
                moves = tile.find_moves(self.board) # find all available moves
                for move in moves:
                    shoot_locations = tile.find_shoots(self.board, move) # find all shoot locations
                    if shoot_locations != []:
                        if i not in available_plays:
                            available_plays[i] = {}
                        available_plays[i][move] = shoot_locations
        return available_plays

    def check_play_is_legal(self, available_plays, piece, move, shoot):
        """
        Check move is legal
        """
        try:
            if shoot in available_plays[piece][move]:
                return True
            else:
                return False
        except:
            return False

    def play(self):
        while True:
            self.board.print_board()

            available_plays = self.find_available_plays()
            #if available_plays == {}:
            #    print('Someone has won')
            #    break

            while True:
                p = int(input('Player '+self.turn+', select a piece:'))
                m = int(input('Make a move:'))
                s = int(input('And shoot:'))
                if self.check_play_is_legal(available_plays, p, m, s):
                    break
                else:
                    print('Invalid')
                    self.board.print_board()

            self.make_play(p, m, s)

class Board:
    def __init__(self):
        self.possible_steps = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
        self.game_tiles = []

        # Fill board with nulls
        for tile in range(100):
            self.game_tiles.append(Null(None, None))

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

class Null:

    def __init__(self, alliance=None, position=None):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return "-"

class Flame:

    def __init__(self, alliance=None, position=None):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return '0'

class Warrior:

    def __init__(self, alliance, position):
        self.alliance       = alliance
        self.position       = position

    def to_string(self):
        return "1" if self.alliance==1 else "2"

    def find_moves(self, board):
        """
        Find possible move locations
        """
        moves = []
        for step in board.possible_steps:
            pos = self.position
            # Convert to cartesian
            x = pos%10
            y = pos//10
            while (0 <= x <= 9) and (0 <= y <= 9):
                x += step[0]
                y += step[1]
                if (0 <= x <= 9) and (0 <= y <= 9):
                    pos2 = x + 10*y
                    if board.game_tiles[pos2].to_string() == '-':
                        moves.append(pos2)
                    else:
                        break
                else:
                    break
        return moves

    def find_shoots(self, board, move):
        """
        Find possible shoot locations from the position move.
        """
        old_position = self.position
        moves = []
        for step in board.possible_steps:
            pos = move
            # Convert to cartesian
            x = pos%10
            y = pos//10
            while (0 <= x <= 9) and (0 <= y <= 9):
                x += step[0]
                y += step[1]
                if (0 <= x <= 9) and (0 <= y <= 9):
                    pos2 = x + 10*y
                    if board.game_tiles[pos2].to_string() == '-' or pos2 == old_position:
                        moves.append(pos2)
                    else:
                        break
                else:
                    break
        return moves
