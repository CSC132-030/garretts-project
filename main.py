import sys

import pygame as py
import pygame.mouse

from game.constants import (BOARD_WIDTH, HEIGHT, RED, BLACK, SQUARE_SIZE, WINDOW_SIZE,
							BOARD_POS, X_OFFSET, REDB, BLACKB, WOOD, CREAM)
from game.game import Game
from game.bot import Bot

# Initialize fonts in pygame
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
BTN_FONT = py.font.Font(None, 22)
BTN_FONT.underline = True

# Set window caption
py.display.set_caption("Checkers v1.10")

# Bot constants for color the bot plays and recursion depth/difficulty
BOT_COLOR = BLACK
DEPTH = 3


# Takes position of mouse in window and returns the row and column for location of piece in board array
def get_row_col(pos):
	x, y = pos
	x -= X_OFFSET
	row = y // SQUARE_SIZE
	col = x // SQUARE_SIZE
	return row, col


# Main game loop, takes boolean arg 'bot' from caller specifying whether the game will be 1 player or 2
def main(bot):
	WINDOW.fill(BLACKB)
	bot = bot
	run = True
	clock = py.time.Clock()
	game = Game(BOARD_SURF)

	disp_sze = (BTN_SZE[0], 3*BTN_SZE[1])
	disp_font = py.font.Font(None, 38)
	team_font = py.font.Font(None, 28)
	scr_font = py.font.Font(None, 38)

	disp_font.bold = True
	disp_font.italic = True
	team_font.underline = True
	scr_font.bold = True

	# Set x,y tuples for position of buttons/display based on window size
	rev_pos = (R_BTN_X, BTN_Y)
	reset_pos = (R_BTN_X, WINDOW_SIZE[1] // 2 - BTN_SZE[1] // 2)
	quit_pos = (R_BTN_X, WINDOW_SIZE[1] - BTN_Y - BTN_SZE[1])
	menu_pos = (X_OFFSET // 2 - BTN_SZE[0] // 2, WINDOW_SIZE[1] - WINDOW_SIZE[1] // 4 - BTN_SZE[1])
	caps_pos = (X_OFFSET // 2 - disp_sze[0] // 2, WINDOW_SIZE[1] // 4 - disp_sze[1] // 6)

	# Create surfaces for the buttons/display
	rev_surf = py.Surface(BTN_SZE)
	reset_surf = py.Surface(BTN_SZE)
	quit_surf = py.Surface(BTN_SZE)
	menu_surf = py.Surface(BTN_SZE)
	caps_surf = py.Surface(disp_sze)

	# Create text to overlay onto the buttons/display
	rev_txt = BTN_FONT.render('Undo Last Move', True, (255, 255, 255))
	reset_txt = BTN_FONT.render('Reset Game', True, (255, 255, 255))
	quit_txt = BTN_FONT.render('Quit', True, (255, 255, 255))
	menu_txt = BTN_FONT.render('Main Menu', True, (255, 255, 255))
	caps_txt_top = disp_font.render("Captures", True, WOOD)
	caps_txt_rteam = team_font.render("Red:", True, RED)
	caps_txt_bteam = team_font.render("Black:", True, BLACK)

	# Create rectangles for the text to be rendered onto
	rev_txt_rect = rev_txt.get_rect(center=(rev_surf.get_width() // 2, rev_surf.get_height() // 2))
	reset_txt_rect = reset_txt.get_rect(center=(reset_surf.get_width() // 2, reset_surf.get_height() // 2))
	quit_txt_rect = quit_txt.get_rect(center=(quit_surf.get_width() // 2, quit_surf.get_height() // 2))
	menu_txt_rect = menu_txt.get_rect(center=(menu_surf.get_width() // 2, menu_surf.get_height() // 2))
	caps_txt_top_rect = caps_txt_top.get_rect(center=(caps_surf.get_width()//2, caps_surf.get_height()//6))
	caps_txt_rteam_rect = caps_txt_rteam.get_rect(center=(caps_surf.get_width()//4, caps_surf.get_height()//2))
	caps_txt_bteam_rect = caps_txt_bteam.get_rect(center=(3*(caps_surf.get_width()//4), caps_surf.get_height()//2))

	# Rectangle used for determining if menu button is clicked on (discovered this way after other buttons were done...)
	menu_btn_rect = py.Rect(menu_pos, BTN_SZE)

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

		caps_txt_red = scr_font.render(f"{game.board.red_caps}", True, RED)
		caps_txt_blk = scr_font.render(f"{game.board.blk_caps}", True, BLACK)

		caps_txt_red_rect = caps_txt_red.get_rect(center=(caps_surf.get_width() // 4, caps_surf.get_height() - caps_surf.get_height()//4))
		caps_txt_blk_rect = caps_txt_blk.get_rect(center=(3 * (caps_surf.get_width() // 4), caps_surf.get_height() - caps_surf.get_height()//4))

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

				if rev_pos[0] <= tap_pos[0] <= rev_pos[0] + BTN_WDT and rev_pos[1] <= tap_pos[1] <= rev_pos[1] + BTN_HT:
					rev_btn_clk = py.draw.rect(WINDOW, REDB, (rev_pos, BTN_SZE))
					py.display.update(rev_btn_clk)
					game.reverse_turn()
					game.update()
				if reset_pos[0] <= tap_pos[0] <= reset_pos[0] + BTN_WDT and reset_pos[1] <= tap_pos[1] <= reset_pos[
					1] + BTN_HT:
					reset_btn_clk = py.draw.rect(WINDOW, REDB, (reset_pos, BTN_SZE))
					py.display.update(reset_btn_clk)
					game.reset()
				if quit_pos[0] <= tap_pos[0] <= quit_pos[0] + BTN_WDT and quit_pos[1] <= tap_pos[1] <= quit_pos[
					1] + BTN_HT:
					quit_btn_clk = py.draw.rect(WINDOW, REDB, (quit_pos, BTN_SZE))
					py.display.update(quit_btn_clk)
					run = False
				if menu_btn_rect.collidepoint(event.pos):
					menu_btn_clk = py.draw.rect(WINDOW, REDB, (menu_pos, BTN_SZE))
					py.display.update(menu_btn_clk)
					welcome()
				py.time.delay(75)

		# draw rectangles of respective size for each button on their surface and color them red
		py.draw.rect(rev_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(reset_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(quit_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(menu_surf, RED, ((0, 0), BTN_SZE))
		py.draw.rect(caps_surf, CREAM, ((0, 0), disp_sze))

		# blit the appropriate text on the correct surf at each of the drawn rectangles
		rev_surf.blit(rev_txt, rev_txt_rect)
		reset_surf.blit(reset_txt, reset_txt_rect)
		quit_surf.blit(quit_txt, quit_txt_rect)
		menu_surf.blit(menu_txt, menu_txt_rect)
		caps_surf.blit(caps_txt_top, caps_txt_top_rect)
		caps_surf.blit(caps_txt_rteam, caps_txt_rteam_rect)
		caps_surf.blit(caps_txt_bteam, caps_txt_bteam_rect)
		caps_surf.blit(caps_txt_red, caps_txt_red_rect)
		caps_surf.blit(caps_txt_blk, caps_txt_blk_rect)

		# blit each of the surfaces onto the window at the correct positions
		WINDOW.blit(rev_surf, rev_pos)
		WINDOW.blit(reset_surf, reset_pos)
		WINDOW.blit(quit_surf, quit_pos)
		WINDOW.blit(menu_surf, menu_pos)
		WINDOW.blit(caps_surf, caps_pos)

		game.update()

		WINDOW.blit(BOARD_SURF, BOARD_POS)

		py.display.update()
	py.quit()
	sys.exit()


# Main menu/welcome screen. Allows selection of 1 or 2 players and calls main() with bot arg based on button clicked
def welcome():
	WINDOW.fill(BLACKB)
	run = True
	clock = py.time.Clock()

	ypad = WINDOW_SIZE[1] // 16
	wbtn_sze = (2 * BTN_SZE[0], BTN_SZE[1])
	banner_sze = (WINDOW_SIZE[0] - WINDOW_SIZE[0] // 14, (WINDOW_SIZE[1] - 2 * (WINDOW_SIZE[1] // 3)))

	banner_font = py.font.Font(None, 84)
	banner_font.italic = banner_font.bold = True

	wbtn_font = py.font.Font(None, 36)
	wbtn_font.underline = True

	banner_surf = py.Surface(banner_sze)
	sngl_surf = py.Surface(wbtn_sze)
	two_surf = py.Surface(wbtn_sze)
	quit_surf = py.Surface(BTN_SZE)

	banner_txt = banner_font.render('Checkers Game For Cool People', True, CREAM)
	sngl_txt = wbtn_font.render('1 Player', True, (255, 255, 255))
	two_txt = wbtn_font.render('2 Player', True, (255, 255, 255))
	quit_txt = BTN_FONT.render('Quit', True, (255, 255, 255))

	banner_txt_rect = banner_txt.get_rect(center=(banner_surf.get_width() // 2, banner_surf.get_height() // 2))
	sngl_txt_rect = sngl_txt.get_rect(center=(sngl_surf.get_width() // 2, sngl_surf.get_height() // 2))
	two_txt_rect = two_txt.get_rect(center=(two_surf.get_width() // 2, two_surf.get_height() // 2))
	quit_txt_rect = quit_txt.get_rect(center=(quit_surf.get_width() // 2, quit_surf.get_height() // 2))

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


# Win screen called by main() once game has been won, buttons allow user to return to main menu or quit
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


welcome()  # Calls welcome screen when file is ran
