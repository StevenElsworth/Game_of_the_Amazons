class Warrior(object):

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
