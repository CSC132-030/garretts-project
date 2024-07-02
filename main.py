import sys

import pygame as py
import pygame.mouse

from game.constants import BOARD_WIDTH, HEIGHT, RED, BLACK, SQUARE_SIZE, WINDOW_SIZE, BOARD_POS, X_OFFSET
from game.game import Game
from game.bot import Bot

# Frame rate constant for clock.tick()
FPS = 60

# Create window according to dimensions set by WIDTH and HEIGHT
WINDOW = py.display.set_mode(WINDOW_SIZE)

BOARD_SURF = py.Surface((BOARD_WIDTH, HEIGHT))


# Set window caption
py.display.set_caption('Checkers v1.00')

BOT = True
DEPTH = 4


# Takes position of mouse in window and returns the row and column for location of piece in board array
def get_row_col(pos):
    x, y = pos
    x -= X_OFFSET
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = py.time.Clock()
    game = Game(BOARD_SURF)

    if BOT:
        bot_player = Bot(BLACK, game, DEPTH, True)

    # Main game loop
    while run:
        clock.tick(FPS)

        if BOT and game.turn == BLACK:
            game.update()
            bot_player.take_turn()

        game_won = game.win_game()

        if game_won:
            if game_won == RED:
                winner = 'Red'
            else:
                winner = 'Black'
            print(f'{winner} has won the game!')
            run = False


        # Event handler
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

            # TODO: Change for touchscreen after testing, ie py.FINGERDOWN or FINGERUP (TEST WHICH)
                # Other event is py.FINGERMOTION
            if event.type == py.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if BOARD_POS[0] <= pos[0] <= BOARD_POS[0] + BOARD_WIDTH:
                    row, col = get_row_col(pos)

                    if BOT:
                        if game.turn == RED:
                            game.select(row, col)

                    else:
                        game.select(row, col)

        game.update()
        WINDOW.blit(BOARD_SURF, BOARD_POS)
    py.quit()
    sys.exit()


main()
