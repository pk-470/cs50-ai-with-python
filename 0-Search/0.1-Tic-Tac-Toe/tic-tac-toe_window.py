import pygame
import sys
from time import sleep

from board import *
from minimax import *

KEY = {1: "X", -1: "O"}

pygame.init()
size = width, height = 820, 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("fonts/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("fonts/OpenSans-Regular.ttf", 36)
moveFont = pygame.font.Font("fonts/OpenSans-Regular.ttf", 80)

user = None
board = Board()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                sleep(0.2)
                user = X
            elif playOButton.collidepoint(mouse):
                sleep(0.2)
                user = O

    else:

        # Draw game board
        tile_size = 120
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size,
                    tile_size,
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board.state[i, j] != 0:
                    move = moveFont.render(KEY[board.state[i, j]], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        winner = board.winner()
        player = board.player_turn

        # Show title
        if winner is not None:
            if winner == 0:
                title = "Naturally, you cannot beat a master like myself..."
            else:
                title = "Kneel before my superior intellect, loser..."
        elif user == player:
            title = f"Play as {KEY[user]}"
        else:
            title = "..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and winner is None:
            if ai_turn:
                sleep(0.5)
                board.play_move(optimal_move(board))
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and winner is None:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board.state[i, j] == 0 and tiles[i][j].collidepoint(mouse):
                        board.play_move((i, j))

        if winner is not None:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    sleep(0.2)
                    user = None
                    board = Board(state=np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
                    ai_turn = False

    pygame.display.flip()
