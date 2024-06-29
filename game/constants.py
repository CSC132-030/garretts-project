import pygame as py

## BOARD DIMENSIONS ##
WIDTH, HEIGHT = 600, 600  # Window size
ROWS, COLS = 8, 8  # Checkers board is 8x8 grid
SQUARE_SIZE = WIDTH//COLS  # Size of individual cells on board

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
x_scale = piece_diameter * 2/3  # Set width of crown to 2/3 the diameter of a piece
y_scale = x_scale*(256/445)  # Calculate height while maintaining images original aspect ratio
CROWN = py.transform.scale(py.image.load('assets/crown.png'), (x_scale, y_scale))
