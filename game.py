import pygame
from utility.game_backend import Game, Board, Null, Flame, Warrior
from pynput.mouse import Button, Controller
import time
import random
import os


def mouse_index(mx, my, buffer, tile_size):
    """
    FUNCTION DESCRIPTION.

    Parameters:
    -----------

    Returns:
    --------
    """
    s_row = (my - buffer)//tile_size
    s_col = (mx - buffer)//tile_size
    return s_col + s_row*10


def draw_board(game_display, buffer, tile_size, game, piece, move, move_locations, shoot_locations):
    """
    FUNCTION DESCRIPTION.

    Parameters:
    -----------

    Returns:
    --------
    """
    flame_image = pygame.image.load('./utility/flame.png')          # image of flame
    blue_player = pygame.image.load('./utility/blue_player.png')    # image of blue warrior
    green_player = pygame.image.load('./utility/green_player.png')  # image of green warrior

    game_display.fill((255,255,255))

    # Draw board
    for x in range(0, 10):
        if x%2 == 1:
            for y in range(0, 10, 2):
                pygame.draw.rect(game_display, (169,169,169), (buffer+x*tile_size, buffer+y*tile_size, tile_size, tile_size))
        else:
            for y in range(1, 10, 2):
                pygame.draw.rect(game_display, (169,169,169), (buffer+x*tile_size, buffer+y*tile_size, tile_size, tile_size))
    pygame.draw.line(game_display, (169,169,169), (buffer,buffer), (buffer,buffer+10*tile_size), 4)
    pygame.draw.line(game_display, (169,169,169), (buffer,buffer+10*tile_size), (buffer+10*tile_size,buffer+10*tile_size), 4)
    pygame.draw.line(game_display, (169,169,169), (buffer+10*tile_size,buffer+10*tile_size), (buffer+10*tile_size,buffer), 4)
    pygame.draw.line(game_display, (169,169,169), (buffer+10*tile_size,buffer), (buffer,buffer), 4)

    # Add pieces, move_locations and shoot_locations
    piece_radius = int(0.4*tile_size)
    for col in range(10):
        for row in range(10):
            index = row + (col)*10
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

    # Add moves
    if not move_locations == None:
        for move in move_locations:
            location = (int(buffer+ tile_size*(move%10 + 0.5)), int(buffer+ tile_size*(move//10 + 0.5)))
            pygame.draw.circle(game_display, (0,0,0), location, 5, 5)

    # Add shoot
    if not shoot_locations == None:
        for s in shoot_locations:
            location = (int(buffer+ tile_size*(s%10 + 0.5)), int(buffer+ tile_size*(s//10 + 0.5)))
            pygame.draw.circle(game_display, (255,0,0), location, 5, 5)
    return


def main(testgame=False):
    """
    FUNCTION DESCRIPTION.

    Parameters:
    -----------

    Returns:
    --------
    """
    buffer    = 50  # border size from game board
    tile_size = 60  # size of game tiles

    # Place game screen in te top left corner of the screen.
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

    # Initialize the game.
    pygame.init()
    game_display = pygame.display.set_mode((2*buffer+10*tile_size,2*buffer+ \
    10*tile_size))
    # Sets the size of the screen which displays the game board and buffer

    # Caption display at top of screen (game name).
    pygame.display.set_caption('Game of the Amazons')

    # Initialise game using class Game from backend.
    g = Game()

    # Boolean flag for game (see while loop below).
    run_game = True

    # Get x and y positions of the mouse cursor.
    mx, my = pygame.mouse.get_pos()

    # Draw initial board.
    draw_board(game_display, buffer, tile_size, g, None, None, [], [])
    pygame.display.flip()

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
        # Did user press a key?
        for event in pygame.event.get():

            # If window close button is pressed, end the game.
            if event.type == pygame.QUIT:
                run_game = False

            # If a test game, complete a random play.
            if testgame:
                if piece == None:
                    # Select random play.
                    available_plays = g.find_available_plays()
                    r_piece = random.choice(list(available_plays))
                    r_move  = random.choice(list(available_plays[r_piece]))
                    r_shoot = random.choice(available_plays[r_piece][r_move])

                    # Select a piece.
                    x, y = int(buffer + tile_size*(r_piece%10 + 0.5)), int(buffer + tile_size*(r_piece//10 + 0.5))
                    mouse.position = (x, y+5)
                    mouse.click(Button.left, 1)

                elif piece != None and move == None:
                    # Select a move position.
                    x, y = int(buffer + tile_size*(r_move%10 + 0.5)), int(buffer + tile_size*(r_move//10 + 0.5))
                    mouse.position = (x, y+5)
                    mouse.click(Button.left, 1)

                elif piece != None and move != None:
                    # Select a shoot location.
                    x, y = int(buffer + tile_size*(r_shoot%10 + 0.5)), int(buffer + tile_size*(r_shoot//10 + 0.5))
                    mouse.position = (x, y)
                    mouse.click(Button.left, 1)

            # Not a random game, request user input.
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos() # find index of pressed tile
                    index = mouse_index(mx, my, buffer, tile_size) # find tile index


                    if g.board.game_tiles[index].to_string() == g.turn and move == None:
                        piece = index # selected_piece is now the index of a Warrior
                        move_locations = g.board.game_tiles[piece].find_moves(g.board) # highlight legal moves

                    elif piece != None:
                        if index in move_locations and move == None: # Piece not moved
                            move = index
                            shoot_locations = g.board.game_tiles[piece].find_shoots(g.board, move)
                            move_locations = []

                        elif index in shoot_locations and move != None: # Piece not shot
                            g.make_play(piece, move, index)
                            if g.turn == '1': # update caption to let user know whos turn it is
                                pygame.display.set_caption('Game of the Amazons - Shots fired by green!')
                            else:
                                pygame.display.set_caption('Game of the Amazons - Shots fired by blue!')
                            piece           = None
                            move            = None
                            move_locations  = []
                            shoot_locations = []


                ### **CHANGE TO UPDATE BOARD**

                # Draw board
                draw_board(game_display, buffer, tile_size, g, piece, move, move_locations, shoot_locations)
                pygame.display.flip()

    pygame.quit() # closes window after while loop condition is violated



if __name__ == '__main__':
    main()
