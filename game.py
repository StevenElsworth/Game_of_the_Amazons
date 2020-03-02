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

################################################################################
################################################################################

buffer = 0
tile_size = 60

pygame.init()
game_display = pygame.display.set_mode((2*buffer+10*tile_size,2*buffer+10*tile_size))
pygame.display.set_caption('Game of the Amazons')

board = Board()
board.create_board()

run_game = True

# Mouse positions
mx, my = pygame.mouse.get_pos()
prevx, prevy = [0,0]

selected_piece = None
turn = '1'
moves = None
shoot = None
moved = False
winner = False

while run_game: # begin running game
    for event in pygame.event.get(): # Did user press a key
        if event.type == pygame.QUIT: # If window close button, end game
            run_game = False

    else:

        if event.type == pygame.MOUSEBUTTONDOWN:


            if selected_piece == None: #(No piece selected)

                # Find index of pressed tile
                mx, my = pygame.mouse.get_pos()
                index = mouse_index(mx, my, buffer, tile_size)

                # Check if its a warrior
                if board.game_tiles[index].to_string() == turn:
                    selected_piece = index

                    # highlight legal moves
                    moves = board.game_tiles[selected_piece].find_moves(board)

            else:
                # Find index of pressed tile
                mx, my = pygame.mouse.get_pos()
                index = mouse_index(mx, my, buffer, tile_size)

                if moved: # (Ready to shoot)
                    if index in shoot and board.game_tiles[index].to_string() == '-':
                        if turn == '1':
                            pygame.display.set_caption('Game of the Amazons - Shots fired by green!')
                        else:
                            pygame.display.set_caption('Game of the Amazons - Shots fired by blue!')

                        board.game_tiles[index] = Flame(0, index)
                        shoot = None
                        selected_piece = None
                        moved = False

                else: # (Select new character or move)
                    if index in moves and board.game_tiles[index].to_string() == '-': #(Move)
                        moving_piece = board.game_tiles[selected_piece]
                        moving_piece.position = index
                        board.game_tiles[index] = moving_piece
                        board.game_tiles[selected_piece] = Null(None, None)
                        moved = True

                        # Moved character must now shoot
                        shoot = board.game_tiles[index].find_moves(board)

                        # Change turns
                        if turn == '1':
                            turn = '2'
                        else:
                            turn = '1'
                        moves = None

                    elif board.game_tiles[index].to_string() == turn: #(Select new character)
                        selected_piece = index

                        # highlight legal moves
                        moves = board.game_tiles[selected_piece].find_moves(board)

    # Draw board
    draw_board(board, tile_size, buffer, turn, moves, shoot)
    pygame.display.flip()

pygame.quit()
