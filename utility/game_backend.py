from utility.board import Board
from utility.null import Null
from utility.flame import Flame

class Game(object):

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
