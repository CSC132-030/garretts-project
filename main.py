import sys

import pygame as py
import pygame.mouse

from game.constants import BOARD_WIDTH, HEIGHT, RED, BLACK, SQUARE_SIZE, WINDOW_SIZE, BOARD_POS, X_OFFSET, REDB, BLACKB
from game.game import Game
from game.bot import Bot

py.font.init()

# Frame rate constant for clock.tick()
FPS = 60

# Create window according to dimensions set by WIDTH and HEIGHT
WINDOW = py.display.set_mode(WINDOW_SIZE)

# Surface which will be blit onto window for the board to drawn on
BOARD_SURF = py.Surface((BOARD_WIDTH, HEIGHT))

# Button constants for their position/size/font/etc.
BTN_WDT = 3 * (X_OFFSET // 4)
BTN_HT = BTN_WDT // 3

R_BTN_X = WINDOW_SIZE[0] - X_OFFSET // 2 - BTN_WDT // 2
BTN_Y = WINDOW_SIZE[1] // 8
BTN_SZE = (BTN_WDT, BTN_HT)

REV_POS = (R_BTN_X, BTN_Y)
RESET_POS = (R_BTN_X, WINDOW_SIZE[1] // 2 - BTN_SZE[1] // 2)
QUIT_POS = (R_BTN_X, WINDOW_SIZE[1] - BTN_Y - BTN_SZE[1])

BTN_FONT = py.font.Font(None, 22)
BTN_FONT.underline = True

rev_surf = py.Surface(BTN_SZE)
reset_surf = py.Surface(BTN_SZE)
quit_surf = py.Surface(BTN_SZE)

rev_txt = BTN_FONT.render('Undo Last Move', True, (255, 255, 255))
reset_txt = BTN_FONT.render('Reset Game', True, (255, 255, 255))
quit_txt = BTN_FONT.render('Quit', True, (255, 255, 255))

rev_txt_rect = rev_txt.get_rect(center=(rev_surf.get_width() // 2, rev_surf.get_height() // 2))
reset_txt_rect = reset_txt.get_rect(center=(reset_surf.get_width() // 2, reset_surf.get_height() // 2))
quit_txt_rect = quit_txt.get_rect(center=(quit_surf.get_width() // 2, quit_surf.get_height() // 2))

# Set window caption
py.display.set_caption("Checkers v1.05")

BOT_COLOR = BLACK
DEPTH = 3


# Takes position of mouse in window and returns the row and column for location of piece in board array
def get_row_col(pos):
	x, y = pos
	x -= X_OFFSET
	row = y // SQUARE_SIZE
	col = x // SQUARE_SIZE
	return row, col


def main(bot):
	WINDOW.fill(BLACKB)
	bot = bot
	run = True
	clock = py.time.Clock()
	game = Game(BOARD_SURF)

	if bot:
		bot_player = Bot(BOT_COLOR, game, DEPTH, True)

	# Main game loop
	while run:
		clock.tick(FPS)

		if bot and game.turn == BLACK:
			game.update()
			bot_player.take_turn()

		winner = game.win_game()

		if winner:
			game_won(winner)

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

					if bot:
						if game.turn != BOT_COLOR:
							game.select(row, col)

					if not bot:
						game.select(row, col)

				if REV_POS[0] <= tap_pos[0] <= REV_POS[0] + BTN_WDT and REV_POS[1] <= tap_pos[1] <= REV_POS[1] + BTN_HT:
					rev_btn_clk = py.draw.rect(WINDOW, REDB, (REV_POS, BTN_SZE))
					py.display.update(rev_btn_clk)
					game.reverse_turn()
					game.update()
				if RESET_POS[0] <= tap_pos[0] <= RESET_POS[0] + BTN_WDT and RESET_POS[1] <= tap_pos[1] <= RESET_POS[
					1] + BTN_HT:
					reset_btn_clk = py.draw.rect(WINDOW, REDB, (RESET_POS, BTN_SZE))
					py.display.update(reset_btn_clk)
					game.reset()
				if QUIT_POS[0] <= tap_pos[0] <= QUIT_POS[0] + BTN_WDT and QUIT_POS[1] <= tap_pos[1] <= QUIT_POS[
					1] + BTN_HT:
					quit_btn_clk = py.draw.rect(WINDOW, REDB, (QUIT_POS, BTN_SZE))
					py.display.update(quit_btn_clk)
					run = False
				py.time.delay(75)

		py.draw.rect(rev_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(reset_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(quit_surf, RED, ((0, 0), BTN_SZE))

		rev_surf.blit(rev_txt, rev_txt_rect)
		reset_surf.blit(reset_txt, reset_txt_rect)
		quit_surf.blit(quit_txt, quit_txt_rect)

		WINDOW.blit(rev_surf, REV_POS)
		WINDOW.blit(reset_surf, RESET_POS)
		WINDOW.blit(quit_surf, QUIT_POS)

		game.update()

		WINDOW.blit(BOARD_SURF, BOARD_POS)

		py.display.update()
	py.quit()
	sys.exit()


def welcome():
	WINDOW.fill(BLACKB)
	run = True
	clock = py.time.Clock()

	ypad = WINDOW_SIZE[1] // 16
	wbtn_sze = (2 * BTN_SZE[0], BTN_SZE[1])
	banner_sze = (WINDOW_SIZE[0] - WINDOW_SIZE[0] // 14, (WINDOW_SIZE[1] - 2 * (WINDOW_SIZE[1] // 3)))

	banner_font = py.font.Font(None, 84)
	banner_font.italic = True

	wbtn_font = py.font.Font(None, 36)
	wbtn_font.underline = True

	banner_surf = py.Surface(banner_sze)
	sngl_surf = py.Surface(wbtn_sze)
	two_surf = py.Surface(wbtn_sze)

	banner_txt = banner_font.render('Checkers Game For Cool People', True, REDB)
	sngl_txt = wbtn_font.render('1 Player', True, (255, 255, 255))
	two_txt = wbtn_font.render('2 Player', True, (255, 255, 255))

	banner_txt_rect = banner_txt.get_rect(center=(banner_surf.get_width() // 2, banner_surf.get_height() // 2))
	sngl_txt_rect = sngl_txt.get_rect(center=(sngl_surf.get_width() // 2, sngl_surf.get_height() // 2))
	two_txt_rect = two_txt.get_rect(center=(two_surf.get_width() // 2, two_surf.get_height() // 2))

	sngl_pos = (WINDOW_SIZE[0] // 2 - sngl_surf.get_width() // 2, WINDOW_SIZE[1] // 2 - ypad)
	two_pos = (WINDOW_SIZE[0] // 2 - two_surf.get_width() // 2, sngl_pos[1] + sngl_surf.get_height() + ypad)
	wquit_pos = (WINDOW_SIZE[0] // 2 - quit_surf.get_width() // 2, two_pos[1] + two_surf.get_height() + ypad)

	sngl_btn_rect = py.Rect((sngl_pos, wbtn_sze))
	two_btn_rect = py.Rect((two_pos, wbtn_sze))
	wquit_btn_rect = py.Rect((wquit_pos, BTN_SZE))

	while run:
		clock.tick(FPS)

		for event in py.event.get():
			if event.type == py.QUIT:
				run = False
			if event.type == py.MOUSEBUTTONDOWN:
				if sngl_btn_rect.collidepoint(event.pos):
					sngl_btn_clk = py.draw.rect(WINDOW, REDB, (sngl_pos, wbtn_sze))
					py.display.update(sngl_btn_clk)
					main(True)
				if two_btn_rect.collidepoint(event.pos):
					two_btn_clk = py.draw.rect(WINDOW, REDB, (two_pos, wbtn_sze))
					py.display.update(two_btn_clk)
					main(False)
				if wquit_btn_rect.collidepoint(event.pos):
					wquit_btn_clk = py.draw.rect(WINDOW, REDB, (wquit_pos, BTN_SZE))
					py.display.update(wquit_btn_clk)
					run = False
				py.time.delay(75)

		py.draw.rect(sngl_surf, RED, ((0, 0), wbtn_sze))
		py.draw.rect(two_surf, RED, ((0, 0), wbtn_sze))
		py.draw.rect(quit_surf, RED, ((0, 0), BTN_SZE))

		banner_surf.blit(banner_txt, banner_txt_rect)
		sngl_surf.blit(sngl_txt, sngl_txt_rect)
		two_surf.blit(two_txt, two_txt_rect)
		quit_surf.blit(quit_txt, quit_txt_rect)

		WINDOW.blit(banner_surf, ((WINDOW_SIZE[0] - banner_surf.get_width()) // 2,
								  WINDOW_SIZE[1] // 4 - banner_surf.get_height() // 2))
		WINDOW.blit(sngl_surf, sngl_pos)
		WINDOW.blit(two_surf, two_pos)
		WINDOW.blit(quit_surf, wquit_pos)

		py.display.update()

	py.quit()
	sys.exit()


def game_won(color_won):
	if color_won == RED:
		winner = "RED"
		color = REDB
	else:
		winner = "BLACK"
		color = BLACKB

	WINDOW.fill(color)

	run = True
	clock = py.time.Clock()

	xpad = WINDOW_SIZE[0] // 8
	gwbtn_sze = (2 * BTN_SZE[0], BTN_SZE[1])
	banner_sze = (WINDOW_SIZE[0] - WINDOW_SIZE[0] // 14, (WINDOW_SIZE[1] - 2 * (WINDOW_SIZE[1] // 3)))

	banner_font = py.font.Font(None, 108)
	banner_font.italic = True
	banner_font.underline = True

	banner_surf = py.Surface(banner_sze)
	banner_surf.fill(color)
	menu_surf = py.Surface(gwbtn_sze)
	gwquit_surf = py.Surface(gwbtn_sze)

	banner_txt = banner_font.render(f"{winner} WINS!", True, (255, 255, 255))
	menu_txt = BTN_FONT.render("Main Menu", True, color_won)
	gwquit_txt = BTN_FONT.render("Quit", True, color_won)

	banner_txt_rect = banner_txt.get_rect(center=(banner_surf.get_width() // 2, banner_surf.get_height() // 2))
	menu_txt_rect = menu_txt.get_rect(center=(menu_surf.get_width() // 2, menu_surf.get_height() // 2))
	gwquit_txt_rect = gwquit_txt.get_rect(center=(gwquit_surf.get_width() // 2, gwquit_surf.get_height() // 2))

	menu_pos = (WINDOW_SIZE[0]//2 - xpad - gwbtn_sze[0], WINDOW_SIZE[1] - WINDOW_SIZE[1]//3 - BTN_SZE[1])
	gwquit_pos = (WINDOW_SIZE[0]//2 + xpad, WINDOW_SIZE[1] - WINDOW_SIZE[1]//3 - BTN_SZE[1])

	menu_btn_rect = py.Rect((menu_pos, gwbtn_sze))
	gwquit_btn_rect = py.Rect((gwquit_pos, gwbtn_sze))

	while run:
		clock.tick(FPS)

		for event in py.event.get():
			if event.type == py.QUIT:
				run = False
			if event.type == py.MOUSEBUTTONDOWN:
				if menu_btn_rect.collidepoint(event.pos):
					menu_btn_clk = py.draw.rect(WINDOW, (182, 182, 182), (menu_pos, gwbtn_sze))
					py.display.update(menu_btn_clk)
					welcome()
				if gwquit_btn_rect.collidepoint(event.pos):
					gwquit_btn_clk = py.draw.rect(WINDOW, (182, 182, 182), (gwquit_pos, gwbtn_sze))
					py.display.update(gwquit_btn_clk)
					run = False
				py.time.delay(75)

		py.draw.rect(menu_surf, (255, 255, 255), ((0, 0), gwbtn_sze))
		py.draw.rect(gwquit_surf, (255, 255, 255), ((0, 0), gwbtn_sze))

		banner_surf.blit(banner_txt, banner_txt_rect)
		menu_surf.blit(menu_txt, menu_txt_rect)
		gwquit_surf.blit(gwquit_txt, gwquit_txt_rect)

		WINDOW.blit(banner_surf, ((WINDOW_SIZE[0] - banner_surf.get_width()) // 2, WINDOW_SIZE[1] // 4 - banner_surf.get_height() // 2))
		WINDOW.blit(menu_surf, menu_pos)
		WINDOW.blit(gwquit_surf, gwquit_pos)

		py.display.update()

	py.quit()
	sys.exit()


welcome()
