import random

class Game:
    """
    Description of Game class.
    """
    def __init__(self, testgame=0):
        self.board = Board()
        self.turn = '1'
        self.testgame = testgame

    def make_play(self, piece, move, shoot):
        """
        Select warrior at location 'piece', move it to location 'move' and fire
        arrow at location 'shoot.'

        Parameters:
        -----------
        piece : int
            Location of warrior to be played.
        move  : int
            Location to move warrior to.
        shoot : int
            Location for arrow to be fired.

        Notes:
        ------
        This function assumes the move and shoot actions are legal.
        """
        # --------
        #   MOVE
        # --------
        moving_piece = self.board.game_tiles[piece]     # get Warrior object
        moving_piece.position = move                    # assign (new) position attribute to index of Warrior
        self.board.game_tiles[move] = moving_piece      # assign Warrior object on game board to proposed location using index
        self.board.game_tiles[piece] = Null(None, None) # generate empty tile for where Warrior was before moving

        # --------
        #  SHOOT
        # --------
        self.board.game_tiles[shoot] = Flame(0, shoot) # assign Flame object to location which has been shot

        # Change turn of player.
        if self.turn == '1':
            self.turn = '2'
        else:
            self.turn = '1'

    def find_available_plays(self):
        """
        Find all available plays for a player.

        Returns:
        --------
        available_plays : dictionary
            Nested dictionary of the form available_plays[warrior_location][move_location] = [shoot_locations],
            containing all available moves and corresponding shoot locations for each piece.
        """
        available_plays = {} # dictionary for efficiency
        for i, tile in enumerate(self.board.game_tiles): # search entire board
            if tile.to_string() == self.turn: # found a warrior belonging to current player
                moves = tile.find_moves(self.board) # find all available moves
                for move in moves:
                    shoot_locations = tile.find_shoots(self.board, move) # find all shoot locations
                    if shoot_locations != []:
                        if i not in available_plays:
                            available_plays[i] = {} # create nested dictionary if doesn't already exist
                        available_plays[i][move] = shoot_locations # store possible move locations and corresponding possible shoot locations for piece i
        return available_plays

    def check_play_is_legal(self, available_plays, piece, move, shoot):
        """
        Check proposed play is legal.

        Parameters:
        -----------
        available_plays : dictionary
            Nested dictionary of the form available_plays[warrior_location][move_location] = [shoot_locations],
            containing all available moves and corresponding shoot locations for each piece.
        piece : int
            Location of warrior to be played.
        move  : int
            Location to move warrior to.
        shoot : int
            Location for arrow to be fired.

        Returns:
        --------
        boolean
        True if play legal, False otherwise.
        """
        try:
            if shoot in available_plays[piece][move]:
                return True # play is contained in available_plays
            else:
                return False # shoot option is not in available_plays
        except:
            return False # no applicable entry in available_plays to check

    def play(self):
        """
        Requests user to provide piece, move and shoot values. If the combination
        is not a legal move, ask again. Otherwise the play is completed.
        """
        while True:
            # Print the board to screen.
            self.board.print_board()

            # Check if the game has ended (ie, no available plays).
            available_plays = self.find_available_plays()
            if available_plays == {}: # Q: Is this a sufficient condition for the game to end?
                if self.turn == '1':
                    print('Player 2 has won the game!')
                else:
                    print('Player 1 has won the game!')
                break

            while True:
                # If game is being played by user, request user input.
                if self.testgame == 0:
                    piece = int(input('Player ' + self.turn + ', select a piece:'))
                    move  = int(input('Now choose a move location:'))
                    shoot = int(input('Now choose a shoot location:'))
                    if self.check_play_is_legal(available_plays, piece, move, shoot):
                        break
                    else:
                        print('Invalid play selection, please choose a different piece, move & shoot combination.')
                        self.board.print_board()
                # If test game, choose from available plays at random.
                else:
                    piece = random.choice(list(available_plays))
                    move  = random.choice(list(available_plays[piece]))
                    shoot = random.choice(available_plays[piece][move])
                    break

            # Complete a valid play.
            self.make_play(piece, move, shoot)

class Board:
    """
    Description of Board class.
    """
    def __init__(self, ):
        # Possible directions of travel for pieces and arrows.
        self.possible_steps = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]

        # Initialise the board with nulls.
        self.game_tiles = []
        for tile in range(100):
            self.game_tiles.append(Null(None, None))

        # Add Warriors of tribe/player 1.
        self.game_tiles[3] = Warrior(1, 3)
        self.game_tiles[6] = Warrior(1, 6)
        self.game_tiles[30] = Warrior(1, 30)
        self.game_tiles[39] = Warrior(1, 39)

        # Add Warriors or tribe/player 2.
        self.game_tiles[60] = Warrior(2, 60)
        self.game_tiles[69] = Warrior(2, 69)
        self.game_tiles[93] = Warrior(2, 93)
        self.game_tiles[96] = Warrior(2, 96)


    def print_board(self):
        """
        Display the game board to screen.
        """
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
