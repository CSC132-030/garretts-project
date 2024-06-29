import sys

import pygame as py
import pygame.mouse

from game.constants import WIDTH, HEIGHT, RED, BLACK, SQUARE_SIZE
from game.game import Game
from game.bot import Bot

# Frame rate constant for clock.tick()
FPS = 60

# Create window according to dimensions set by WIDTH and HEIGHT
WINDOW = py.display.set_mode((WIDTH, HEIGHT))

# Set window caption
py.display.set_caption('Checkers v0.10')

BOT = True


# Takes position of mouse in window and returns the row and column for location of piece in board array
def get_row_col(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = py.time.Clock()
    game = Game(WINDOW)

    if BOT:
        bot_player = Bot(BLACK, game, 2, True)

    # Main game loop
    while run:
        clock.tick(FPS)

        if BOT and game.turn == BLACK:
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
                row, col = get_row_col(pos)

                if BOT:
                    if game.turn == RED:
                        game.select(row, col)

                else:
                    game.select(row, col)

        game.update()
    py.quit()
    sys.exit()


main()
