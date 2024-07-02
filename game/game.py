import pygame as py
from copy import deepcopy as dcopy
from .constants import RED, BLACK, GREEN, SQUARE_SIZE, BOARD_POS
from .board import Board


class Game:
    def __init__(self, board_surface):
        self._start()
        self.surf = board_surface
        #self.pos = BOARD_POS

    def update(self):
        self.board.draw(self.surf)
        self.draw_valid_moves(self.valid_moves)
        py.display.flip()


    # private method called to start a game
    def _start(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.turncount = 0
        self.boardlist = {}

        self.boardlist[self.turncount] = self.board

    # method to reset the game by calling start()
    def reset(self):
        self._start()

    def select(self, row, col):
        if self.selected:  # if piece already selected, try to move to given square in args
            result = self._move(row, col)  # result of whether the move occured (boolean)
            if not result:  # if given square is an invalid move and therefore no move occured
                self.selected = None  # reset the selected piece to null
                self.select(row, col)  # then recursively call select() with no selected piece (go to else statement)

        piece = self.board.get_piece(row, col)  # store piece object at given square

        # if piece is not empty (ie != 0) and it is that colors turn:
        if piece != 0 and piece.color == self.turn:
            self.selected = piece  # store the piece object as the selected piece
            self.valid_moves = self.board.get_valid_moves(piece)  # get valid moves available to selected piece
            return True

        return False  # return false if piece was empty or was not its colors turn

    def _move(self, row, col):
        # get piece at given square (either Piece object or 0)
        piece = self.board.get_piece(row, col)

        # If selection made, and piece is 0 (meaning an empty square), and given args are a valid move:
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)  # move the selected piece to square at given args
            pieces_jumped = self.valid_moves[(row, col)]
            if pieces_jumped:
                self.board.remove(pieces_jumped)
            self.end_turn()
        else:
            return False
        return True

    def end_turn(self):
        self.valid_moves = {}
        self.turncount += 1
        board_copy = dcopy(self.board)
        self.boardlist[self.turncount] = board_copy
        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED

    def reverse_turn(self):
        if self.turncount > 2:
            self.turncount -= 2
            self.board = self.boardlist[self.turncount]
            self.board.draw(self.surf)
            py.display.flip()
        else:
            self.reset()


    # Method to draw small circles once a piece is selected, indicating which squares can be moved to
    def draw_valid_moves(self, moves):
        # for each square in valid moves dictionary keys, draw a green circle indicating that square can be moved to
        for move in moves.keys():
            row, col = move  # store row and col of square it is valid to move to, then draw a circle there
            py.draw.circle(
                self.surf, GREEN,  # Draw green circles representing valid moves on the game board surface
                (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),  # x/y coords from col/row
                SQUARE_SIZE//12)  # desired diameter of circle is 1/6 of square, so radius is 1/12

    # Function which calls board win_game function and returns the returned value to caller
    def win_game(self):
        return self.board.win_game()

    def get_board(self):
        return self.board

    # Update the board after bot has taken its turn
    def bot_end_turn(self, new_board):
        self.board = new_board  # set the board to board state post the bot making its move
        self.update()  # update the game/board
        self.end_turn()  # end/pass turn to other player
