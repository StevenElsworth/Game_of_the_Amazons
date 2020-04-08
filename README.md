# Game of the Amazons

## Rules of the game
The 'Game of the Amazons' is a two player abstract strategy game invented by Walter Zamkauskas from Argentina in 1988. The game is usually played on a 10x10 grid where each player has four 'Amazon warriors' (or 'pieces').
A turn consists of two parts. First, the player moves one of their warriors in a straight line (like a queen in a game of chess) to an empty square. Secondly, after moving, the Amazon fires a flaming arrow to another empty square using a queen-like move. The square where the arrow lands is then burning for the remainder of the game. Neither warriors nor arrows may travel through a square which is burning or occupied by another Amazon. To complete their turn, a player must be able to successfully move one of their warriors **_and_** fire an arrow. The game is won when the opponent cannot complete a legal move.

## Implementation

The game can be played using a GUI built using PyGame or directly in the terminal with a basic interface.

The core of the game is implemented in the file utility/game_backend.py which contains five classes:

1. Game

  The main class within this python script which controls all attributes of the game. When initialised it constructs an initial board and sets the player turn to Player 1. This class has 4 functions, make_play, check_play_is_legal, find_available_plays and play.
  * find_available_plays: Runs through a players warriors and provides a dictionary of all available plays. A play consists of selecting a piece, a move location and a shoot location. The nested dictionary is structured as follows
    
    ```python
    available_plays[warrior_location][move_location] = [shoot_locations]
    ```
    
  * check_play_is_legal: Checks if a specific play belongs to the available_plays dictionary
  * make_play: Takes a board, piece, move, shoot combination and checks the play is legal. If the play is legal it makes the play by editing the board.
  * play: Used to play the game in terminal. Requests a play selection from the user and calls make_play.

2. Board

  This class stores all information about the current board. The main attribute is game_tiles which is a list of length 100 where each entry is either a Flame, Null or Warrior object. The 100 entries correspond to the 10x10 board. The layout of the board is as follows:

  |     |       |       |       |       |       |       |       |       |       |     |
  | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
  |     |    0  |    1  |    2  |    3  |    4  |    5  |    6  |    7  |    8  |    9  |
  |     |   10  |   11  |   12  |   13  |   14  |   15  |   16  |   17  |   18  |   19  |
  |     |   20  |   21  |   22  |   23  |   24  |   25  |   26  |   27  |   28  |   29  |
  |     |   30  |   31  |   32  |   33  |   34  |   35  |   36  |   37  |   38  |   39  |
  |     |   40  |   41  |   42  |   43  |   44  |   45  |   46  |   47  |   48  |   49  |
  |     |   50  |   51  |   52  |   53  |   54  |   55  |   56  |   57  |   58  |   59  |
  |     |   60  |   61  |   62  |   63  |   64  |   65  |   66  |   67  |   68  |   69  |
  |     |   70  |   71  |   72  |   73  |   74  |   75  |   76  |   77  |   78  |   79  |
  |     |   80  |   81  |   82  |   83  |   84  |   85  |   86  |   87  |   88  |   89  |
  |     |   90  |   91  |   92  |   93  |   94  |   95  |   96  |   97  |   98  |   99  |


  3. Warrior

    This piece has either alliance '1' or '2' dependent on which player it belongs. This class also has two extremely important functions, find_moves and find_shoots. find_moves looks for all available move locations for the particular piece given the board. It does this by looking exhaustively in each of the 9 directions. find_shoots looks at all the possible shoot locations given a specific move. There is quite a bit of overlap in the functions which could probably be simplified.

4. Flame

  This piece has no alliance and prints the string '0' when called

5. Null

  This piece has no alliance and prints the string '-' when called




## AlphaZero Reinforcement Learning

1) Deep convolutional neural net with residual blocks.

2) Monte Carlo Tree Search Algorithm.

3) Network discarding.

## TODO
- GUI very inefficient, the whole board is drawn each time.
- Add AI
- Check if a player has won
- Allow user specify board size and number of warriors in each tribe
