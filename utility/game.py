import pygame
import time
from utility.board import Board
from utility.null import Null
from utility.flame import Flame

def mouse_index(mx, my, buffer, tile_size):
    s_row = (my - buffer)//tile_size
    s_col = (mx - buffer)//tile_size
    return s_col + s_row*10

def draw_board(board, tile_size, buffer, turn, moves, shoot):
    flame_image = pygame.image.load('./utility/flame.png')
    blue_player = pygame.image.load('./utility/blue_player.png')
    green_player = pygame.image.load('./utility/green_player.png')

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

    # Add pieces
    piece_radius = int(0.4*tile_size)
    for col in range(10):
        for row in range(10):
            index = row + (col)*10
            if not board.game_tiles[index].to_string() == '-':
                #center = (int(buffer+(tile_size*(int(row)+0.5))), int(buffer+(tile_size*(int(col)+0.5))))
                top_left = (int(buffer+(tile_size*(int(row)))), int(buffer+(tile_size*(int(col)))))
                if board.game_tiles[index].alliance == 1:
                    game_display.blit(blue_player, top_left)
                    #pygame.draw.circle(game_display, (0,0,255), center, piece_radius, piece_radius)
                elif board.game_tiles[index].alliance == 2:
                    game_display.blit(green_player, top_left)
                    #pygame.draw.circle(game_display, (0,255,0), center, piece_radius, piece_radius)
                elif board.game_tiles[index].alliance == 0:
                    game_display.blit(flame_image, top_left)
                    #pygame.draw.circle(game_display, (255,0,0), center, piece_radius, piece_radius)
                else:
                    pass

    # Add moves
    if not moves == None:
        for move in moves:
            location = (int(buffer+ tile_size*(move%10 + 0.5)), int(buffer+ tile_size*(move//10 + 0.5)))
            pygame.draw.circle(game_display, (0,0,0), location, 5, 5)

    # Add shoot
    if not shoot == None:
        for s in shoot:
            location = (int(buffer+ tile_size*(s%10 + 0.5)), int(buffer+ tile_size*(s//10 + 0.5)))
            pygame.draw.circle(game_display, (255,0,0), location, 5, 5)



# play game

buffer = 0     # border size from game board
tile_size = 60 # size of game tiles

pygame.init() # initialize the game
game_display = pygame.display.set_mode((2*buffer+10*tile_size,2*buffer+10*tile_size))
# sets the size of the screen which displays the game board and buffer
pygame.display.set_caption('Game of the Amazons')
# caption display at top of screen (game name)

board = Board() # generate Board object
board.create_board() # generate initial game board

run_game = True # boolean flag for game (see while loop below)

mx, my = pygame.mouse.get_pos() # get x and y coordinates of mouse click
prevx, prevy = [0,0]

selected_piece = None
turn           = '1'
moves          = None
shoot          = None
moved          = False
winner         = False


while run_game: # begin running game
    for event in pygame.event.get(): # Did user press a key
        if event.type == pygame.QUIT: # If window close button, end game
            run_game = False

    else:

        if event.type == pygame.MOUSEBUTTONDOWN:


            if selected_piece == None: # No piece selected

                mx, my = pygame.mouse.get_pos() # find index of pressed tile
                index = mouse_index(mx, my, buffer, tile_size) # find tile index

                # Check if its a Warrior
                if board.game_tiles[index].to_string() == turn:
                    selected_piece = index
                    # selected_piece is now the index of a Warrior

                    moves = board.game_tiles[selected_piece].find_moves(board)
                    # highlight legal moves

            else:
                mx, my = pygame.mouse.get_pos() # find index of pressed tile
                index = mouse_index(mx, my, buffer, tile_size) # find tile index

                # Tile index now found, we move onto moving and shooting


                if moved: # move has now happened so lets assign fire to shoot location (Ready to shoot)
                    if index in shoot and board.game_tiles[index].to_string() == '-':

                        board.game_tiles[index] = Flame(0, index)
                        # assign Flame object to location which has been shot
                        shoot = None
                        # recycle shoot for next turn
                        selected_piece = None
                        # recycle selected_piece for next turn
                        moved = False
                        # recycle moved for next turn
                        if turn == '1': # update caption to let user know whos turn it is
                            pygame.display.set_caption('Game of the Amazons - Shots fired by green!')
                        else:
                            pygame.display.set_caption('Game of the Amazons - Shots fired by blue!')

                else: # move has not been completed, else statement either select new character or moves

                    if index in moves and board.game_tiles[index].to_string() == '-': # both conditions ensure valid move
                        moving_piece          = board.game_tiles[selected_piece]
                        # get Warrior object
                        moving_piece.position = index
                        # assign position attribute to index of Warrior
                        board.game_tiles[index] = moving_piece
                        # assign Warrior object on game board to proposed location
                        # using index
                        board.game_tiles[selected_piece] = Null(None, None)
                        # generate empty tile for where Warrior was before moving
                        moved = True
                        # move is now complete. Onto shooting from move...

                        shoot = board.game_tiles[index].find_moves(board)
                        # finds possible moves from new Warrior location

                        # Change turns
                        if turn == '1':
                            turn = '2'
                        else:
                            turn = '1'
                        moves = None

                    elif board.game_tiles[index].to_string() == turn:
                        # if user doesn't presses another Warrior on same team
                        selected_piece = index
                        # selected_piece is the index of other Warrior
                        moves = board.game_tiles[selected_piece].find_moves(board)
                        # give possible moves from different Warrior
    # Draw board
    draw_board(board, tile_size, buffer, turn, moves, shoot)
    pygame.display.flip()

pygame.quit()
# closes window after while loop condition is violated
