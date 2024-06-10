from .constants import RED, REDB, BLACKB,  SQUARE_SIZE
import pygame as py

class Piece:
    PAD = 10  # Padding between edge of squares and drawn piece
    BORDER = 2  # Thickness of the border around each piece

    def __init__(self, row, col, color):
        self.row = row  # row position for a piece object
        self.col = col  # column position for a piece object
        self.color = color  # color of a piece of object
        self.king = False  # boolean for whether a piece is a king

        if self.color == RED:  # if a red piece, the piece moves from bottom to top
            self.direction = -1
        else:  # otherwise, the piece from top to bottom (black piece)
            self.direction = 1

        # Initialize the x and y coords of piece
        self.x = 0
        self.y = 0

        # Calculate the position of piece
        self.get_pos()

    def get_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2

    def set_king(self):
        self.king = True

    def draw(self, window):
        radius = SQUARE_SIZE//2 - self.PAD
        if self.color == RED:
            py.draw.circle(window, REDB, (self.x, self.y), radius + self.BORDER)
        else:
            py.draw.circle(window, BLACKB, (self.x, self.y), radius + self.BORDER)
        py.draw.circle(window, self.color, (self.x, self.y), radius)