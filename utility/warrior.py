class Warrior(object):

    alliance = None
    position = None

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return "1" if self.alliance==1 else "2"

    def find_moves(self, board):
        # List of all one step moves (directions)
        possible_steps = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
        moves = []
        for step in possible_steps:
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
