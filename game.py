import pygame
from utility.game_backend import Game, Board, Null, Flame, Warrior
from pynput.mouse import Button, Controller
import time
import random
import os


def mouse_to_index(mx, my, buffer, tile_size):
    """
    Converts a mouse click location into a board/tile index.

    Parameters:
    -----------
    mx : float
        x co-ordinate of the mouse click location.
    my : float
        y co-ordinate of the mouse click location.
    buffer : float
        Width of the buffer surrounding the game board.
    tile_size : float
        Width/height of a single tile.

    Returns:
    --------
    Board index of the tile containing the mouse click location.
    """
    s_row = (my - buffer)//tile_size # row of the board containing the mouse click location
    s_col = (mx - buffer)//tile_size # column of the board containing the mouse click location
    return s_col + s_row*10


def draw_board(game_display, buffer, tile_size, game, piece, move, move_locations, shoot_locations):
    """
    Draws the current game board.

    Parameters:
    -----------
    game_display : pygame.display
        Instance of a pygame display.
    buffer : float
        Width of the buffer surrounding the game board.
    tile_size : float
        Width/height of a single tile.
    game : Game
        Instance of the Game class from utility.game_backend
    piece: int
        Tile position on the board of selected Warrior.
    move : int
        Tile position on the board for selected Warrior to move to.
    move_locations : list
        List of tile positions on the board to which the selected warrior may move.
    shoot_locations : list
        List of tile positions on the board which the selected warrior may shoot.
    """
    # Game piece .png images.
    blue_player  = pygame.image.load('./utility/blue_player.png')   # image of blue warrior
    green_player = pygame.image.load('./utility/green_player.png')  # image of green warrior
    flame_image  = pygame.image.load('./utility/flame.png')         # image of flame

    # Pre-defined colours as RGB values.
    WHITE = (255,255,255)
    GREY  = (169,169,169)
    RED   = (255,0,0)
    BLACK = (0,0,0)

    # Draw the game board: white background.
    game_display.fill(WHITE)

    # Draw the game board: fill every other diagonal in grey.
    for x in range(0, 10):
        if x%2 == 1:
            for y in range(0, 10, 2):
                pygame.draw.rect(game_display, GREY, (buffer+x*tile_size, buffer+y*tile_size, tile_size, tile_size))
        else:
            for y in range(1, 10, 2):
                pygame.draw.rect(game_display, GREY, (buffer+x*tile_size, buffer+y*tile_size, tile_size, tile_size))

    # Draw the game board: add grey border.
    pygame.draw.line(game_display, GREY, (buffer,buffer),                           (buffer,buffer+10*tile_size), 4)                # bottom left  -> top left
    pygame.draw.line(game_display, GREY, (buffer,buffer+10*tile_size),              (buffer+10*tile_size,buffer+10*tile_size), 4)   # top left     -> top right
    pygame.draw.line(game_display, GREY, (buffer+10*tile_size,buffer+10*tile_size), (buffer+10*tile_size,buffer), 4)                # top right    -> bottom right
    pygame.draw.line(game_display, GREY, (buffer+10*tile_size,buffer),              (buffer,buffer), 4)                             # bottom right -> bottom left

    # Add pieces.
    piece_radius = int(0.4*tile_size)
    for col in range(10):
        for row in range(10):
            # Position index of (row,column) pair.
            index = row + col*10
            # Top left hand corner of the tile whose position is index.
            top_left = (int(buffer+(tile_size*(int(row)))), int(buffer+(tile_size*(int(col)))))

            if index == piece and move != None:
                pass
            elif index == move:
                if game.board.game_tiles[piece].alliance == 1:
                    game_display.blit(blue_player, top_left)
                elif game.board.game_tiles[piece].alliance == 2:
                    game_display.blit(green_player, top_left)
            else:
                if game.board.game_tiles[index].alliance == 1:
                    game_display.blit(blue_player, top_left)
                elif game.board.game_tiles[index].alliance == 2:
                    game_display.blit(green_player, top_left)
                elif game.board.game_tiles[index].alliance == 0:
                    game_display.blit(flame_image, top_left)

    # Add move locations. - TODO: Replace circle with (transparent) warrior symbols?
    if not move_locations == None:
        for move in move_locations:
            # Co-ordinates of the centre of the tile.
            location = (int(buffer+ tile_size*(move%10 + 0.5)), int(buffer+ tile_size*(move//10 + 0.5)))
            # Draw black circles to indicate possible move locations.
            pygame.draw.circle(game_display, BLACK, location, 5, 5)

    # Add shoot locations. - TODO: Replace circle with target images?
    if not shoot_locations == None:
        for s in shoot_locations:
            # Co-ordinates of the centre of the tile.
            location = (int(buffer+ tile_size*(s%10 + 0.5)), int(buffer+ tile_size*(s//10 + 0.5)))
            # Draw red circles to indicate possible shoot locations.
            pygame.draw.circle(game_display, RED, location, 5, 5)
    return


def main(testgame=True):
    """
    FUNCTION DESCRIPTION.

    Parameters:
    -----------

    Returns:
    --------
    """
    buffer    = 50  # size of border around the game board
    tile_size = 60  # size (width & height) of game tiles

    screen_x = 2*buffer+10*tile_size # width of screen
    screen_y = 2*buffer+10*tile_size # height of screen

    # Place game screen in the top left corner of the screen.
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

    # Initialize the game.
    pygame.init()

    # Set the size of the screen which displays the game board and buffer.
    game_display = pygame.display.set_mode((screen_x, screen_y))

    # Font for end of game message.
    #font = pygame.font.SysFont('arial',36)

    # Caption display at top of screen (game name).
    pygame.display.set_caption('Game of the Amazons')

    # Initialise game using class Game from game_backend.py.
    g = Game()

    # Boolean flag for game (see while loop below).
    run_game = True

    # Get x and y positions of the mouse cursor.
    mx, my = pygame.mouse.get_pos()

    # Draw initial board.
    draw_board(game_display, buffer, tile_size, g, None, None, [], [])
    pygame.display.flip()

    # Initialise play parameters.
    piece           = None
    move            = None
    move_locations  = []
    shoot_locations = []

    # If random/test game (no user).
    if testgame:
        mouse = Controller()
        time.sleep(2)

    # Game running.
    while run_game:

        # Check for available moves.
        available_plays = g.find_available_plays()

        # If no available plays, end the game and update caption.
        if available_plays == {} or g.turncount == 3: # <---- TODO: REMOVE
            if g.turn == '1':
                pygame.display.set_caption('Game of the Amazons - Green has won the game in ' + str(g.turncount-1) + ' turns! Click anywhere to close the game.')
            else:
                pygame.display.set_caption('Game of the Amazons - Blue has won the game in '  + str(g.turncount-1) + ' turns! Click anywhere to close the game.')
            """
            TODO: Have pop up message rather than caption change.
            # If game over display message to screen.
            text = font.render("Game Over", True, (0,0,0), (255,255,255))
            text_rect = text.get_rect()
            text_x = screen_x/2 - text_rect.width/2
            text_y = screen_y/2 - text_rect.height/2
            game_display.blit(text, [text_x, text_y])
            """

            draw_board(game_display, buffer, tile_size, g, piece, move, move_locations, shoot_locations)
            pygame.display.flip()

            # End game when user clicks.
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                run_game = False
                break


        # Did user press a key?
        for event in pygame.event.get():

            # If window close button is pressed, end the game.
            if event.type == pygame.QUIT:
                run_game = False

            # If a test game, complete a random play.
            # Note requires three passes through the while loop per play due to board being drawn at end.
            if testgame:
                if piece == None:
                    # Select random play.
                    r_piece = random.choice(list(available_plays))
                    r_move  = random.choice(list(available_plays[r_piece]))
                    r_shoot = random.choice(available_plays[r_piece][r_move])

                    # Select a piece.
                    x, y = int(buffer + tile_size*(r_piece%10 + 0.5)), int(buffer + tile_size*(r_piece//10 + 0.5))
                    mouse.position = (x, y)
                    mouse.click(Button.left, 1)

                elif piece != None and move == None:
                    # Select a move position.
                    x, y = int(buffer + tile_size*(r_move%10 + 0.5)), int(buffer + tile_size*(r_move//10 + 0.5))
                    mouse.position = (x, y)
                    mouse.click(Button.left, 1)

                elif piece != None and move != None:
                    # Select a shoot location.
                    x, y = int(buffer + tile_size*(r_shoot%10 + 0.5)), int(buffer + tile_size*(r_shoot//10 + 0.5))
                    mouse.position = (x, y)  ## TODO: should this be (x,y+5)?
                    mouse.click(Button.left, 1)

            # Not a random game, therefore request user input.
            #else:
            # User has pressed the mouse button to select a tile.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse cursor position.
                mx, my = pygame.mouse.get_pos()
                # Find corresponding tile index.
                index = mouse_to_index(mx, my, buffer, tile_size)

                # Warrior piece of current team selected using the mouse.
                if g.board.game_tiles[index].to_string() == g.turn and move == None:
                    # Selected tile index is the index of a Warrior.
                    piece = index
                    # Find (and highlight below) all legal moves for this Warrior.
                    move_locations = g.board.game_tiles[piece].find_moves_or_shots(g.board, piece, piece)

                # If piece has been selected, require move or shoot choice.
                elif piece != None:
                    # If piece has not yet moved and a valid move is selected.
                    if index in move_locations and move == None:
                        # Selected tile index is the index of a legal move position.
                        move = index
                        # Find (and highlight below) all legal shoot locations for this move.
                        shoot_locations = g.board.game_tiles[piece].find_moves_or_shots(g.board, move, piece, shooting=True)
                        # Reset move_locations variable.
                        move_locations = []

                    # If piece has moved but not shot, and a legal shot is selected.
                    elif index in shoot_locations and move != None:
                        # Complete valid play.
                        g.make_play(piece, move, index)
                        # Update caption to let user know whose turn it is.
                        if g.turn == '1':
                            pygame.display.set_caption('Game of the Amazons - Shot fired by Green!')
                        else:
                            pygame.display.set_caption('Game of the Amazons - Shot fired by Blue!')
                        # Reset the play parameters.
                        piece           = None
                        move            = None
                        move_locations  = []
                        shoot_locations = []


                # TODO: Change to update board.
                # Draw board
                draw_board(game_display, buffer, tile_size, g, piece, move, move_locations, shoot_locations)
                pygame.display.flip()

    # Closes the game window after the while loop condition is violated.
    pygame.quit()



if __name__ == '__main__':
    main()
