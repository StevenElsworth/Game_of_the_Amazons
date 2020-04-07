# Game of the Amazons

## Rules of the game
The 'Game of the Amazons' is a two player abstract strategy game invented by Walter Zamkauskas from Argentina in 1988. The game is usually played on a 10x10 grid where each player has four amazons.
A turn consists of two parts. First the player moves one of their amazons to an empty square in a straight line (like a Queen in a game of chess). Secondly, after moving, the amazon fires a flaming arrow to another square using a queenlike move. The square where the arrow lands is burning for the remainder of the game. The amazon warrior movement as well as arrow shots may not travel through or lang on a square which is occupied by an amazon warrior or burning.

## Implementation
The core of the game is implemented in the file utility/game_backend.py which contains 5 classes.

Game - The main class within this python script controls all attributes of the game. When initialised it constructs an initial board and sets the player turn to player 1. This class has 4 functions, the main ones being make_play, check_play_is_legal and find_available_plays. The function find_available_plays runs through a players warriors and provides a dictionary of all available plays. A play consists of selecting a piece, a move location and a shoot location. The nested dictionary is structured as follows:

available_plays[warrior_location][move_location] = [shoot_locations]

The function check_play_is_legal just checks if a specific play belongs to the available_plays dictionary and finally the make_play function takes a board, piece, move, shoot, then checks the play is legal and makes the play by editing the board.

The function play provides an awful interface to play the game directly in the terminal. The game can also be played using the pygame GUI.

Board - Stores all information about the current board. The main attribute is the game_tiles which is a list of length 100 where each entry is either a Flame, Null or Warrior object. The 100 entries correspond to the 10x10 board. The layout of the board is as follows:

 0  1  2  3  4  5  6  7  8  9
10 11 12 13 14 15 16 17 18 19
20 21 22 23 24 25 26 27 28 29
30 31 32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47 48 49
50 51 52 53 54 55 56 57 58 59
60 61 62 63 64 65 66 67 68 69
70 71 72 73 74 75 76 77 78 79
80 81 82 83 84 85 86 87 88 89
90 91 92 93 94 95 96 97 98 99

Flame - This piece has no alliance and prints the string '0' when called

Null - This piece has no alliance and prints the string '-' when called

Warrior - This piece has either alliance '1' or '2' dependent on which player it belongs. This class also has two extremely important functions, find_moves and find_shoots. find_moves looks for all available move locations for the particular piece given the board. It does this by looking exhaustively in each of the 9 directions. find_shoots looks at all the possible shoot locations given a specific move. There is quite a bit of overlap in the functions which could probably be simplified.

The game can be played on the command line using the game.play() function or using the python script game which has a GUI built using pygame.

## AlphaZero Reinforcement Learning

1) Deep convolutional neural net with residual blocks.

2) Monet Carlo Tree Search Algorithm.

3) Network discarding.

## TODO
- GUI very inefficient, the whole board is drawn each time.
- Add AI
- Check if a player has won
- Allow user specify board size and number of warriors in each tribe
