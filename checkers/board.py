import pygame as py
from .constants import WOOD, CREAM, BLACK, RED, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_remain = 12
        self.wht_remain = 12
        self.red_kings = 0
        self.wht_kings = 0
        self.create_board()

    def draw_squares(self, window):
        window.fill(WOOD)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                py.draw.rect(window, CREAM, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

