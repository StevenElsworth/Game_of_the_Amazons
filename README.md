# Game of the Amazons

## Rules of the game
The 'Game of the Amazons' is a two player abstract strategy game invented by Walter Zamkauskas from Argentina in 1988. The game is usually played on a 10x10 grid where each player has four amazons.
A turn consists of two parts. First the player moves one of their amazons to an empty square in a straight line (like a Queen in a game of chess). Secondly, after moving, the amazon fires a flaming arrow to another square using a queenlike move. The square where the arrow lands is burning for the remainder of the game. The amazon warrior movement as well as arrow shots may not travel through or lang on a square which is occupied by an amazon warrior or burning.

## Implementation
The majority of the game is implemented in the class `Game` in utility/game_backend.py. The board is represented by a list of length 100 where each entry contains either a null/flame/warrior class. Making a move involves passing a piece, move and shoot position to the game class via the function make_move.

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
