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

# Surface which will be blit onto window for the board to drawn on
BOARD_SURF = py.Surface((BOARD_WIDTH, HEIGHT))

# Constants determining the position and size of the buttons relative to screen size
BTN_WDT = 3*(X_OFFSET//4)
BTN_HT = BTN_WDT//3

R_BTN_X = WINDOW_SIZE[0] - X_OFFSET//2 - BTN_WDT//2
BTN_Y = WINDOW_SIZE[1]//8
BTN_SZE = (BTN_WDT, BTN_HT)

REV_POS = (R_BTN_X, BTN_Y)
RESET_POS = (R_BTN_X, WINDOW_SIZE[1]//2 - BTN_SZE[1]//2)
QUIT_POS = (R_BTN_X, WINDOW_SIZE[1] - BTN_Y - BTN_SZE[1])



# Set window caption
py.display.set_caption("Checkers v1.00")

BOT = True
BOT_COLOR = BLACK
DEPTH = 3


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
        bot_player = Bot(BOT_COLOR, game, DEPTH, True)

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
                tap_pos = pygame.mouse.get_pos()
                if BOARD_POS[0] <= tap_pos[0] <= BOARD_POS[0] + BOARD_WIDTH:
                    row, col = get_row_col(tap_pos)

                    if BOT:
                        if game.turn != BOT_COLOR:
                            game.select(row, col)

                    if not BOT:
                        game.select(row, col)

                if REV_POS[0] <= tap_pos[0] <= REV_POS[0] + BTN_WDT and REV_POS[1] <= tap_pos[1] <= REV_POS[1] + BTN_HT:
                    game.reverse_turn()
                if RESET_POS[0] <= tap_pos[0] <= RESET_POS[0] + BTN_WDT and RESET_POS[1] <= tap_pos[1] <= RESET_POS[1] + BTN_HT:
                    game.reset()
                if QUIT_POS[0] <= tap_pos[0] <= QUIT_POS[0] + BTN_WDT and QUIT_POS[1] <= tap_pos[1] <= QUIT_POS[1] + BTN_HT:
                    run = False

        py.draw.rect(WINDOW, RED, (REV_POS, BTN_SZE))
        py.draw.rect(WINDOW, RED, (RESET_POS, BTN_SZE))
        py.draw.rect(WINDOW, RED, (QUIT_POS, BTN_SZE))
        game.update()
        WINDOW.blit(BOARD_SURF, BOARD_POS)
    py.quit()
    sys.exit()


main()
