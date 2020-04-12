import random # used for randomly selecting moves in test games.


class Game:
    """
    Controls all attributes of the game, with functions to find all available
    plays, request a play command from the user, check an input play is legal
    and enact a legal play. Initialised with a board instance, turn counter and
    turn indicator.
    """
    def __init__(self, testgame=False):
        self.board = Board()        # initialise a game board
        self.turn = '1'             # set turn indicator to (player) 1
        self.turncount = 1          # initialise turn counter to 1
        self.testgame = testgame    # indicate whether user game or random/test game

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
        # Move.
        moving_piece = self.board.game_tiles[piece]     # get Warrior object
        moving_piece.position = move                    # assign (new) position attribute to index of Warrior
        self.board.game_tiles[move] = moving_piece      # assign Warrior object on game board to proposed location using index
        self.board.game_tiles[piece] = Null(None, None) # generate empty tile for where Warrior was before moving

        # Shoot.
        self.board.game_tiles[shoot] = Flame(0, shoot)  # assign Flame object to location which has been shot

        # Change turn of player.
        if self.turn == '1':
            self.turn = '2'
        else:
            self.turn = '1'

        # Increment the turn counter.
        self.turncount += 1

    def find_available_plays(self):
        """
        Find all available plays for a player.

        Returns:
        --------
        available_plays : dictionary
            Nested dictionary of the form available_plays[warrior_location][move_location] = [shoot_locations],
            containing all available moves and corresponding shoot locations for each piece.
        """
        # Initialise dictionary to store available plays.
        available_plays = {}

        # Search through board tiles.
        for i, tile in enumerate(self.board.game_tiles):
            # Found a warrior belonging to current player.
            if tile.to_string() == self.turn:
                # Find all available moves.
                moves = tile.find_moves_or_shots(self.board, tile.position, tile.position)
                # Find all available shots for each possible move.
                for move in moves:
                    shoot_locations = tile.find_moves_or_shots(self.board, move, tile.position, shooting=True)
                    if shoot_locations != []:
                        if i not in available_plays:
                            available_plays[i] = {}                 # create nested dictionary if doesn't already exist
                        available_plays[i][move] = shoot_locations  # store possible move locations and corresponding possible shoot locations for piece i
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
        is not a legal move, ask again. Otherwise the play is completed. The
        game is ended when no available plays remain.
        """
        while True:
            # Print the board to screen.
            self.board.print_board()

            # If the game has ended (ie, no available plays), output message to screen.
            available_plays = self.find_available_plays()
            if available_plays == {}:
                if self.turn == '1':
                    print('Player 2 has won the game in ' + str(self.turncount) + ' turns!')
                else:
                    print('Player 1 has won the game in ' + str(self.turncount) + ' turns!')
                break

            while True:
                # If game is being played by user, request user input a play.
                if not self.testgame:
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
    Stores all information about the current board. The tiles attribute
    indicates which positions are empty (Null class), which are occupied by
    warriors (Warrior class) and which are on fire (Flame class).
    """
    def __init__(self):
        # Possible directions of travel for pieces and arrows.
        self.possible_steps = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]

        # Initialise the board with nulls.
        self.game_tiles = []
        for tile in range(100):
            self.game_tiles.append(Null(None, None))

        # Add Warriors of tribe/player 1.
        self.game_tiles[3]  = Warrior(1, 3)
        self.game_tiles[6]  = Warrior(1, 6)
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
                print('|')

        print('\n') # create space between boards in test games


class Warrior:
    """
    Represents the players' pieces, each piece has alliance '1' or '2' to
    indicate which player it belongs to. Contains function to find all available
    moves and shots for that piece.
    """
    def __init__(self, alliance, position):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        """
        Return a string indicating to which player the warrior belongs.
        """
        return '1' if self.alliance==1 else '2'

    def find_moves_or_shots(self, board, current_pos, old_pos, shooting=False):
        """
        Find all possible positions to which the piece can move or shoot.

        Parameters:
        -----------
        board : class
            Current board.
        current_pos : int
            Current position of Warrior.
        old_pos : int
            Position of warrior before moving (equal to current position if not shooting).
        shooting : Boolean
            Indicate whether shooting or moving.

        Returns:
        -----------
        targets : list of potential move or shoot positions.
        """
        # Initialise storage for possible targets.
        targets = []

        # Explore each of the 8 directions in turn.
        for step in board.possible_steps:
            # Current position of the warrior.
            pos = current_pos

            # Convert integer representation of current position to Cartesian co-ordinates.
            x = pos%10
            y = pos//10

            # Explore in current step direction to the edge of the board.
            while (0 <= x <= 9) and (0 <= y <= 9):
                x += step[0]
                y += step[1]
                if (0 <= x <= 9) and (0 <= y <= 9):
                    # Convert Cartesian co-ordinates of target positition to integer representation.
                    target = x + 10*y

                    # If new position is unoccupied, add it to possible target locations.
                    if (board.game_tiles[target].to_string() == '-') or (shooting and target == old_pos):
                        targets.append(target)
                    else:
                        break
                else:
                    break
        return targets


class Flame:
    """
    Flame object which occupies a single board position. Has no allegiance to
    either team and is represented by the string "0".
    """
    def __init__(self, alliance=None, position=None):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return '0'


class Null:
    """
    Null object which represents an empty board position. Has no allegiance to
    either team and is represented by the string "-".
    """
    def __init__(self, alliance=None, position=None):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return '-'
