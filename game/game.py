import pygame as py
from copy import deepcopy as dcopy
from .constants import RED, BLACK, GREEN, SQUARE_SIZE
from .board import Board

# game class handling game logic
class Game:
    def __init__(self, board_surface):
        self._start()  # calls private method to set inst vars @ start so game can be reset w/o creating new object
        self.surf = board_surface  # surface to draw the board on

    # updates the game by drawing board, valid moves, then updating the display
    def update(self):
        self.board.draw(self.surf)
        self.draw_valid_moves(self.valid_moves)
        py.display.flip()

    # private method called to set/return inst vars to their default state at start of game
    def _start(self):
        self.selected = None  # stores piece that has been selected
        self.board = Board()  # stores the board object game is played on
        self.turn = RED  # red takes first turn
        self.valid_moves = {}  # dictionary of valid moves associated to jumped pieces
        self.turncount = 0  # number of turns taken (used when undoing a previous move)
        self.boardlist = {}  # dict of board objects with turncount as key

        self.boardlist[self.turncount] = self.board

    # method to reset the game by calling start() since start is private
    def reset(self):
        self._start()

    # method selecting piece at row/col passed at args if a piece is there and it is same color as the turn color
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
            pieces_jumped = self.valid_moves[(row, col)]  # store piece objects which were jumped and must be removed
            if pieces_jumped:  # if pieces jumped is not null
                self.board.remove(pieces_jumped)  # call the boards remove function to remove those pieces
            self.end_turn()  # end the turn
        # Otherwise the move was not made so result is false
        else:
            return False
        return True

    # called when move has been made to pass turn to other player
    def end_turn(self):
        self.valid_moves = {}  # clear the dict of previously valid moves
        self.turncount += 1  # increment the turncount
        board_copy = dcopy(self.board)  # store a deep copy of the board to revert to if undo move button used
        self.boardlist[self.turncount] = board_copy  # store the board in dict with the turn # as its key
        # if it is currently red's turn, pass the turn to black
        if self.turn == RED:
            self.turn = BLACK
        # otherwise it is currently black's turn, so pass turn to red
        else:
            self.turn = RED

    # called when undo move button clicked, which reverts board to a previous board state stored in the dict
    def reverse_turn(self):
        # if enough turns taken that reversing turn not same as resetting the board
        if self.turncount > 2:
            self.turncount -= 2 # decrement turncount by 2 so it is still the same color's turn
            self.board = self.boardlist[self.turncount]  # board everts by becoming board associated with that turncount
            self.board.draw(self.surf)  # draw new (or previous I guess?) board onto the board surface
            py.display.flip()  # update the display window
        # otherwise just reset the board
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

    # returns the board object to caller (used in algorithm to find best move)
    def get_board(self):
        return self.board

    # called when bot is playing to update the board after bot has taken its turn
    def bot_end_turn(self, new_board):
        self.board = new_board  # set the board to board state post the bot making its move
        self.update()  # update the game/board
        self.end_turn()  # end/pass turn to other player
