from .constants import RED, REDB, BLACKB,  SQUARE_SIZE, CROWN, PADDING, OUTLINE
import pygame as py

class Piece:
    PAD = PADDING
    BORDER = OUTLINE

    # Initialize piece object's attributes
    def __init__(self, row, col, color):
        self.row = row  # row position for a piece object
        self.col = col  # column position for a piece object
        self.color = color  # color of a piece of object
        self.king = False  # boolean for whether a piece is a king

        # Initialize the x and y coordinates of where to draw each piece
        self.x = 0
        self.y = 0

        # Calculate the position of piece
        self.get_pos()

    # Method calculating the relative coordinates of piece within its square
    def get_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2

    # Method changing a normal piece to a king piece
    def set_king(self):
        self.king = True

    # Method to draw piece and its border
    def draw(self, window):
        radius = SQUARE_SIZE//2 - self.PAD  # Radius of piece is half of square minus padding
        if self.color == RED:  # If red piece, draw dark red 'border' first
            py.draw.circle(window, REDB, (self.x, self.y), radius + self.BORDER)
        else:  # Otherwise, the piece is black so draw its darker 'border' first
            py.draw.circle(window, BLACKB, (self.x, self.y), radius + self.BORDER)
        py.draw.circle(window, self.color, (self.x, self.y), radius)  # Then draw piece on top of border

        # If piece is a king, draw crown on top of piece
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.get_pos()
