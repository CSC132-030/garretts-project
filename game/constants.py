import pygame as py

## BOARD DIMENSIONS ##
BOARD_WIDTH, HEIGHT = 600, 600  # Board size
ROWS, COLS = 8, 8  # Checkers board is 8x8 grid
SQUARE_SIZE = BOARD_WIDTH // COLS  # Size of individual cells on board

# Boolean controlling window size and other changes needed when running on the rPi/Potato
RPI = False

## WINDOW DIMENSIONS ##
if RPI:
	WINDOW_WIDTH = 1024  # Window width used when ran in fullscreen on rPi
else:
	WINDOW_WIDTH = BOARD_WIDTH + 400  # Window width based on board width plus side bar padding

WINDOW_SIZE = (WINDOW_WIDTH, HEIGHT)  # tuple of width, height of window

BOARD_POS = (WINDOW_WIDTH // 2 - BOARD_WIDTH // 2, 0)  # Pos to draw the board based on window width and board width

X_OFFSET = (WINDOW_WIDTH - BOARD_WIDTH)//2  # offset in x direction of (0, 0) and pos where board starts

## PIECE DIMENSIONS ##
PADDING = 10  # Padding between edge of squares and drawn piece
OUTLINE = 2  # Thickness of the border around each piece

## RGB COLOR VALUES ##
RED = (255, 0, 0)  # Color of player's pieces
REDB = (171, 5, 5)  # Outline of player's pieces
CREAM = (255, 248, 220)  # Board color of squares
WOOD = (139, 105, 20)  # Board color of squares
BLACK = (64, 61, 61)  # Color of bot's pieces
BLACKB = (0, 0, 0)  # Outline of bot's pieces
GREEN = (82, 196, 16)  # Color indicating valid spaces a piece can be moved

piece_diameter = (SQUARE_SIZE//2 - PADDING)*2  # Diameter of one game piece
x_scale = 2*piece_diameter//3  # Set width of crown to 2/3 the diameter of a piece
y_scale = 256*x_scale//445  # Calculate height while maintaining images original aspect ratio

# crown image scaled to fit on a piece to indicate it is a king
CROWN = py.transform.scale(py.image.load('assets/crown.png'), (x_scale, y_scale))
