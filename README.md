# Game of the Amazons


## Rules of the Game
The 'Game of the Amazons' (see [here](https://www.chessvariants.com/other.dir/amazons.html) or [here](http://www.solitairelaboratory.com/amazons.html)) is a two player abstract strategy game invented by Walter Zamkauskas from Argentina in 1988. The game is usually played on a 10x10 grid where each player has four 'Amazon warriors' (or 'pieces').
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

This class represents the players' pieces. Each piece has alliance '1' or '2' indicating which player it belongs to. This class has an extremely important function:
  * find_moves or shots: Given the board, current warrior position and old warrior poistion, returns all available locations to which the piece can move or shoot. It does this by looking exhaustively in each of the 8 directions.


4. Flame

This class represents the locations hit by a fire arrow. This object has no alliance and prints the string '0' when called.


5. Null

  This class represents locations which have neither a warrior object nor a fire object on them. This object has no alliance and prints the string '-' when called.

## Testing

Run:
'''bash
py.test
'''

## To Do
- Add AI to play against user. Train using AlphaZero reinforcement learning (see below)
- Generalise the size of the board and the number of warriors
- Improve the efficiency of the GUI: e.g., currently the whole board is drawn each turn
- Improve the appearance of the GUI: e.g., better player icons, better fire icon (GIF?), grey-out warriors when they have zero available moves, more information in text
- Improve the features of the GUI: e.g., add undo button
- Autocomplete function to end game?


## AlphaZero Reinforcement Learning

Train an AI to play the game using the approach detailed in the paper [[1]](https://www.nature.com/articles/nature24270).

1. Deep convolutional neural net with residual blocks.

2. Monte Carlo Tree Search (MCTS) Algorithm.

3. Network discarding.

[[1] Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A. and Chen, Y., 2017. Mastering the game of go without human knowledge. Nature, 550(7676), pp.354-359](https://www.nature.com/articles/nature24270).
