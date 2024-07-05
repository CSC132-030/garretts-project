import pygame as py
import itertools as itools
from .constants import WOOD, CREAM, BLACK, RED, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

# Board class used to represent the board the game is played on
class Board:

    # Initialize the game board object and attributes
    def __init__(self):
        self.board = []

        # Each colors pieces remaining on board
        self.red_caps = self.blk_caps = 0

        # Each colors number of king pieces
        self.red_kings = 0
        self.blk_kings = 0

        # Init lists of each pieces colors
        self.red_pieces = []
        self.blk_pieces = []

        # Init count of row location for each color's pieces (used in evaluating board state)
        self.red_mid = self.blk_mid = 0
        self.red_far = self.blk_far = 0

        # Call function drawing pieces on board
        self.create_board()

    # Method drawing the checkered board the game will be played on
    def draw_squares(self, surface):
        surface.fill(WOOD)  # Color the entire board as wood color
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):  # Draw cream square every other square, alternating between rows
                py.draw.rect(surface, CREAM, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Method creating each colors pieces and storing them in 2-d array tracking the board state
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])  # Initialize a separate list for each row (0 to 7)
            for col in range(COLS):  # for each row's list, add the appropriate pieces for each col (0 to 7)
                # Stagger the pieces such that they are only located every other square
                if col % 2 == ((row+1) % 2):
                    if row < 3:  # Use black pieces for rows 0, 1, 2
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:  # Use red pieces for rows 5, 6, 7
                        self.board[row].append(Piece(row, col, RED))
                    else:  # Add 0 representing each empty square for rows 3 and 4
                        self.board[row].append(0)
                else:  # Add 0 representing empty square when a row's column is empty
                    self.board[row].append(0)

    # Method that draws the board according to board state stored in 2d array
    def draw(self, surface):
        self.draw_squares(surface)  # First draw the checkered board background by calling function
        # For each column in each row
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]  # store the value at curr row/col
                # if piece = 0, square @ row/col is empty. if != 0 then a piece is there so call the piece draw method
                if piece != 0:
                    piece.draw(surface)

    # Method which takes row and column parameter and returns piece object
    def get_piece(self, row, col):
        return self.board[row][col]

    # Method handling movement of piece and updating board array
    def move(self, piece, row, col):
        # Swap empty value at target index of board array (row, col) that is being moved to with the piece's index
        # so that the previously empty index location now contains Piece object and Piece's previous index now empty
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # Call piece function to update its row/col instance variables to new location
        piece.move(row, col)

        # If piece has moved into row 7 or 0 and not already a king, make it a king and update colors king counter
        if row == ROWS - 1 or row == 0:
            if not piece.king:
                piece.set_king()
                if piece.color == RED:
                    self.red_kings += 1
                else:
                    self.blk_kings += 1

    # Method checking left and right diagonal of Piece passed as arg, then returns dictionary with valid moves as keys
    # and a list of pieces to remove as the associated values for each key
    def get_valid_moves(self, piece):
        moves = {}  # initialize moves dictionary

        # Get location values of the piece to use as args for checking diagonals for valid moves
        left_col = piece.col - 1  # left column of Piece
        right_col = piece.col + 1  # right column of Piece
        curr_row = piece.row  # row of Piece

        # If color is red it moves from bottom to top, so check those diagonals.
        # If Piece is a king it can move backwards and must be checked regardless of color
        # Then update moves dictionary with any valid moves
        if piece.color == RED or piece.king:
            moves.update(self._check_left(curr_row - 1, max(curr_row - 3, -1), -1, piece.color, left_col))
            moves.update(self._check_right(curr_row - 1, max(curr_row - 3, -1), -1, piece.color, right_col))

        # If color is black it moves from top to bottom, so check diagonals
        # If Piece is a king it can move backwards and must be checked regardless of color
        # Then update moves dictionary with any valid moves
        if piece.color == BLACK or piece.king:
            moves.update(self._check_left(curr_row + 1, min(curr_row + 3, ROWS), 1, piece.color, left_col))
            moves.update(self._check_right(curr_row + 1, min(curr_row + 3, ROWS), 1, piece.color, right_col))

        return moves

    # Private function checking for valid moves including double (or more) jumps along the left diagonal
    def _check_left(self, start_row, stop_row, direction, color, col_to_left, jumped_pieces=[]):
        # init dictionary containing valid move locations as keys and pieces jumped as associated values
        moves = {}
        # init variable to store possible captured piece in the case of a possible double jump (or triple/etc)
        piece_jumped = []

        # loop checking diagonal square to left
        for row in range(start_row, stop_row, direction):
            # If left is less than 0, all possible moves this side have been checked
            if col_to_left < 0:
                break

            # get value in board array at row and col to left (will be 0 if empty or Piece if occupied)
            curr_square = self.board[row][col_to_left]

            # If curr square is empty square (ie it is valid move):
            if curr_square == 0:
                # If pieces have been jumped but the piece jumped is empty because jump was invalid:
                if jumped_pieces and not piece_jumped:
                    break  # break loop and do not add to valid move to dictionary since jump was invalid
                # otherwise, pieces were jumped and piece_jumped contains a valid piece which can be jumped
                elif jumped_pieces:
                    moves[(row, col_to_left)] = piece_jumped + jumped_pieces
                # If neither, since diagonal square is empty, add valid non-jump move to dictionary:
                else:
                    # In this case piece_jumped will be an empty list since no Piece was jumped/needs to be removed
                    moves[(row, col_to_left)] = piece_jumped

                # If a piece was jumped, check recursively if possible double jump is valid
                if piece_jumped:
                    # get position of next row to be checked:
                    if direction == -1:  # ie moving bottom to top
                        curr_row = max(row-3, -1)
                    else:  # ie moving top to bottom
                        curr_row = min(row+3, ROWS)
                    # check for double jump by checking for valid empty squares in left/right diagonal of new position
                    # via a recursive call adding any potential valid moves to the moves dictionary
                    moves.update(self._check_left(row + direction, curr_row, direction, color, col_to_left - 1, jumped_pieces=piece_jumped))
                    moves.update(self._check_right(row + direction, curr_row, direction, color, col_to_left + 1, jumped_pieces=piece_jumped))
                break

            # Otherwise curr square is a Piece, so check if its color is same as selected piece being checked for moves:
            elif curr_square.color == color:
                break  # if color is same break for loop, as no more valid moves on this side
            # If neither, piece @ curr square is opponents and could be jumped if it has empty diagonal (ie it is 0)
            else:
                # store possible jump move and use to check for valid jump (ie an empty diagonal to land in)
                piece_jumped = [curr_square]
            col_to_left -= 1  # decrement col by 1 to get the next col to left to check next diagonal

        # return dictionary of valid moves to caller
        return moves

    # Private function checking for valid moves including double (or more) jumps along the right diagonal
    def _check_right(self, start_row, stop_row, direction, color, col_to_right, jumped_pieces=[]):
        # init dictionary containing valid move locations as keys and pieces jumped as associated values
        moves = {}
        # init variable to store location of empty square in the case of a possible double jump (or triple/etc)
        piece_jumped = []

        # loop checking diagonal square to right
        for row in range(start_row, stop_row, direction):
            # If right is greater than or equal to number of cols, all possible moves have been checked
            if col_to_right >= COLS:
                break

            # get value in board array at row and col to right (will be 0 if empty or Piece if occupied)
            curr_square = self.board[row][col_to_right]

            # If curr square is empty (ie it is valid move):
            if curr_square == 0:
                # If pieces have been jumped but the piece jumped is empty because jump was invalid:
                if jumped_pieces and not piece_jumped:
                    break  # break loop and do not add to valid move dictionary since no valid move this side
                # otherwise, pieces were jumped and piece_jumped contains a valid piece which can be jumped
                elif jumped_pieces:
                    moves[(row, col_to_right)] = piece_jumped + jumped_pieces  # so add to dictionary
                # If neither, since diagonal is empty (ie curr == 0), add valid non-jump move to dictionary:
                else:
                    # In this case piece_jumped is empty list since no Piece was jumped/needs to be removed from board
                    moves[(row, col_to_right)] = piece_jumped

                # If a piece was jumped, check recursively if possible double jump is valid
                if piece_jumped:
                    # get position of next row to be checked:
                    if direction == -1:
                        curr_row = max(row - 3, -1)
                    else:
                        curr_row = min(row + 3, ROWS)
                    # check for double jump at left and right diagonal of new position if it was jumped to
                    moves.update(self._check_left(row + direction, curr_row, direction, color, col_to_right - 1, jumped_pieces=piece_jumped))
                    moves.update(self._check_right(row + direction, curr_row, direction, color, col_to_right + 1, jumped_pieces=piece_jumped))
                break

            # Otherwise curr square is Piece, so check if color is same as piece being moved:
            elif curr_square.color == color:
                break  # if color is same break loop, as no more valid moves on this side

            # If neither, piece @ curr square is opponents and could be jumped if it has empty diagonal (ie it is 0)
            else:
                # store possible jump move and use to check for valid jump
                piece_jumped = [curr_square]
            col_to_right += 1  # increment col by 1 to get the next col to right to check next diagonal

        # return dictionary of valid moves to caller
        return moves

    # Method getting list of pieces as arg then removing those pieces from 2d array tracking board state
    def remove(self, pieces):
        # For each piece in list of pieces, remove piece from board array by setting val to 0 @ that pieces index
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            # update the count of captured pieces according the color of the current piece being removed
            if piece != 0:
                if piece.color == RED:
                    self.blk_caps += 1
                else:
                    self.red_caps += 1

    # Method which returns winning color if a team has no pieces, otherwise returns false if no winner yet
    def win_game(self):
        if self.blk_caps > 11:
            return BLACK
        elif self.red_caps > 11:
            return RED
        return False

    # Partial eval of board state based on location of all pieces on the board relative to their home location
    def get_pos_score(self):
        # Set count of row location for each color's pieces (used in evaluating board state) to 0
        self.red_mid = self.blk_mid = 0
        self.red_far = self.blk_far = 0

        # set penalty for having a king hanging out on far side of board to 0
        bad_king_red = bad_king_blk = 0

        # Methods updating count tracking how many pieces each color has in their respective row areas
        def add_home(color):
            if color == RED:
                pass
            else:
                pass

        def add_mid(color):
            if color == RED:
                self.red_mid += 1
            else:
                self.blk_mid += 1

        def add_far(color):
            if color == RED:
                self.red_far += 1
            else:
                self.blk_far += 1

        # Dictionaries calling appropriate methods to update the count based on a piece's row position
        red_row_dict = {0: add_far, 1: add_far, 2: add_far, 3: add_mid, 4: add_mid, 5: add_home, 6: add_home,
                        7: add_home}
        blk_row_dict = {0: add_home, 1: add_home, 2: add_home, 3: add_mid, 4: add_mid, 5: add_far, 6: add_far,
                        7: add_far}

        # get the length/number of pieces for each colors list of pieces
        red_len = len(self.red_pieces)
        blk_len = len(self.blk_pieces)

        # create a dummy piece to use while iterating through each colors list of pieces for the shorter list once all
        # real pieces have been iterated through and scored
        if red_len > blk_len:
            dummy_piece = Piece(10, 10, BLACK)
        else:
            dummy_piece = Piece(10, 10, RED)

        # For each piece of each color...
        for red_piece, blk_piece in itools.zip_longest(self.red_pieces, self.blk_pieces, fillvalue=dummy_piece):
            # If the current red piece is in row 10, it is dummy piece so do not score its pos
            if red_piece.row != 10:
                # if red piece is a king...
                if red_piece.king:
                    # add to amount subtracted from score to discourage king just moving back and forth at end of board
                    if red_piece.row < 2 or red_piece.row > 5:
                        bad_king_red += 1
                    # otherwise, increment the king piece's pos score
                    else:
                        red_row_dict[red_piece.row](RED)
                # otherwise red piece is not a king, so score its pos normally
                else:
                    red_row_dict[red_piece.row](RED)

            # If the current blk piece is in row 10, it is dummy piece so do not score its pos
            if blk_piece.row != 10:
                # now do the same for the black piece...
                if blk_piece.king:
                    if blk_piece.row < 2 or blk_piece.row > 5:
                        bad_king_blk += 1
                    else:
                        blk_row_dict[blk_piece.row](BLACK)
                # otherwise blk piece is not a king, so score its pos normally
                else:
                    blk_row_dict[blk_piece.row](BLACK)

        # calc total pos score of each color based on board state
        red_pos_score = self.red_mid + 2*self.red_far - bad_king_red
        blk_pos_score = self.blk_mid + 2*self.blk_far - bad_king_blk

        # return those scores to caller
        return red_pos_score, blk_pos_score

    # Method to evaluate the board state of the current board
    def eval_board(self):
        blk_win = red_win = 0  # set to 0 since no color has won

        self.get_all_pieces()  # get all pieces on the curr board
        red_pos_score, blk_pos_score = self.get_pos_score()  # get pos score based on curr board

        # If black or red has captured more than 11 pieces, the game has been won
        if self.blk_caps > 11 or self.red_caps > 11:
            # Set win var to 100 based on which color has captured all pieces
            if self.blk_caps > 11:
                blk_win = 100
            elif self.red_caps > 11:
                red_win = 100

        # Calc score of board state by summing the diff between black caps and red caps (multiplied by the weight),
        # the diff of ea colors kings (times weight), diff of pos score, and if a board results in a win: add or
        # subtract 10000 to score based on who would win that board in order to heavily incentivize winning the game
        score = 5*(self.blk_caps - self.red_caps) + 4*(self.blk_kings - self.red_kings) + 2*(blk_pos_score - red_pos_score) + 1000*(blk_win - red_win)
        return score

    # update a boards list of pieces on the board for each color
    def get_all_pieces(self):
        self.red_pieces = []
        self.blk_pieces = []
        for row in self.board:
            # for each col in each row...
            for piece in row:
                if piece != 0:  # if that col is not empty, it must be a piece...
                    # so add that piece to the list of pieces based on the color of that piece
                    if piece.color == RED:
                        self.red_pieces.append(piece)
                    else:
                        self.blk_pieces.append(piece)
