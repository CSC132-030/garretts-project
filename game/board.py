import pygame as py
from .constants import WOOD, CREAM, BLACK, RED, ROWS, COLS, SQUARE_SIZE
from .piece import Piece


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
        surface.fill(WOOD)  # Color the entire board as wood
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):  # Draw cream square every other square and alternate between rows
                py.draw.rect(surface, CREAM, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Method drawing each colors pieces and storing their initial location in 2-dimensional array
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])  # Initialize a separate list for each row (0 to 7)
            for col in range(COLS):
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

    # Method that draws the board according to board state
    def draw(self, surface):
        self.draw_squares(surface)  # First draw the checkered board
        # For each column in each row, draw the piece at that location if the square is not empty
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface)

    # Method which takes row and column parameter and returns piece object
    def get_piece(self, row, col):
        return self.board[row][col]

    # Method handling movement of piece and updating board array
    def move(self, piece, row, col):
        # Swap empty value at target index of board array (row, col) that is being moved to with the piece's index
        # so that the previously empty index now contains Piece object and previous Piece index now empty
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # If piece has moved into row 7 or 0, make it a king and update colors king count
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
        if piece.color == RED or piece.king:
            moves.update(self._check_left(curr_row - 1, max(curr_row - 3, -1), -1, piece.color, left_col))
            moves.update(self._check_right(curr_row - 1, max(curr_row - 3, -1), -1, piece.color, right_col))

        # If color is black it moves from top to bottom, so check diagonals
        # If Piece is a king it can move backwards and must be checked regardless of color
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

            # get piece at row and col to left (will be 0 if empty or Piece if occupied)
            curr_square = self.board[row][col_to_left]

            # If curr is an empty square (ie it is valid move):
            if curr_square == 0:
                # If jump was possibility but was invalid because same color as piece:
                if jumped_pieces and not piece_jumped:
                    break  # break loop and do not add to valid move to dictionary since jump was invalid
                # if jump was possibility and valid, add the jump move to dictionary:
                elif jumped_pieces:
                    moves[(row, col_to_left)] = piece_jumped + jumped_pieces
                # If neither, since diagonal is empty (ie curr == 0), add valid non-jump move to dictionary:
                else:
                    # In this case last will be an empty list since no Piece was jumped/needs to be removed from board
                    moves[(row, col_to_left)] = piece_jumped

                # If last var exists, check recursively for possible jump
                if piece_jumped:
                    # get position of next row to be checked:
                    if direction == -1:
                        curr_row = max(row-3, -1)
                    else:
                        curr_row = min(row+3, ROWS)
                    # check for double jump by checking for valid empty squares in left/right diagonal of new position
                    moves.update(self._check_left(row + direction, curr_row, direction, color, col_to_left - 1, jumped_pieces=piece_jumped))
                    moves.update(self._check_right(row + direction, curr_row, direction, color, col_to_left + 1, jumped_pieces=piece_jumped))
                break

            # Otherwise curr is a Piece, so check if its color is same as selected piece:
            elif curr_square.color == color:
                break  # if color is same break for loop, as no more valid moves on this side
            # If neither, piece @ curr square is opponents and could be jumped if it has empty diagonal (ie it is 0)
            else:
                # store possible jump move and use to check for valid jump
                piece_jumped = [curr_square]
            col_to_left -= 1  # decrement left var by 1 to get the next col to left to check next diagonal

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

            # get piece at row=r and col=left (will be 0 if empty or Piece if occupied)
            curr_square = self.board[row][col_to_right]

            # If curr is an empty square (ie it is valid move):
            if curr_square == 0:
                # If jump was possibility but was invalid because same color as piece:
                if jumped_pieces and not piece_jumped:
                    break  # break loop and do not add to valid move dictionary since no valid move this side
                # if jump was possibility and was valid, add jump move to dictionary:
                elif jumped_pieces:
                    moves[(row, col_to_right)] = piece_jumped + jumped_pieces
                # If neither, since diagonal is empty (ie curr == 0), add valid non-jump move to dictionary:
                else:
                    # In this case last will be an empty list since no Piece was jumped/needs to be removed from board
                    moves[(row, col_to_right)] = piece_jumped

                # If last var exists, check recursively for possible jump
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

            # Otherwise curr is a Piece, so check if its color is same as piece being moved:
            elif curr_square.color == color:
                break  # if color is same break loop, as no more valid moves on this side

            # If neither, piece @ curr square is opponents and could be jumped if it has empty diagonal (ie it is 0)
            else:
                # store possible jump move and use to check for valid jump
                piece_jumped = [curr_square]
            col_to_right += 1  # increment right var by 1 to get the next col to right to check next diagonal

        # return dictionary of valid moves to caller
        return moves

    # Method removing a piece from board after it has been jumped
    def remove(self, pieces):
        # For each piece in list of removed pieces, remove piece from board by setting val to 0
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.blk_caps += 1
                else:
                    self.red_caps += 1

    # Method which returns winning color if a team has no pieces, otherwise returns false if there is no winner
    def win_game(self):
        if self.blk_caps > 11:
            return BLACK
        elif self.red_caps > 11:
            return RED
        return False

    def get_pos_score(self):
        # Set count of row location for each color's pieces (used in evaluating board state) to 0
        self.red_mid = self.blk_mid = 0
        self.red_far = self.blk_far = 0

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

        for red_piece, blk_piece in zip(self.red_pieces, self.blk_pieces):
            if red_piece.king:
                if red_piece.row < 2 or red_piece.row > 5:
                    bad_king_red += 1
                else:
                    red_row_dict[red_piece.row](RED)

            if blk_piece.king:
                if blk_piece.row < 2 or blk_piece.row > 5:
                    bad_king_blk += 1
                else:
                    blk_row_dict[blk_piece.row](BLACK)

            if not red_piece.king:
                red_row_dict[red_piece.row](RED)
            if not blk_piece.king:
                blk_row_dict[blk_piece.row](BLACK)

        red_pos_score = self.red_mid + 2*self.red_far - 2*bad_king_red
        blk_pos_score = self.blk_mid + 2*self.blk_far - 2*bad_king_blk

        return red_pos_score, blk_pos_score

    def eval_board(self):
        blk_win = red_win = 0

        self.get_all_pieces()
        red_pos_score, blk_pos_score = self.get_pos_score()

        if self.blk_caps > 11 or self.red_caps > 11:
            if self.blk_caps > 11:
                blk_win = 1
            elif self.red_caps > 11:
                red_win = 1

        score = 5*(self.blk_caps - self.red_caps) + 3*(self.blk_kings - self.red_kings) + (blk_pos_score - red_pos_score) + 1000*(blk_win - red_win)
        return score

    def get_all_pieces(self):
        self.red_pieces = []
        self.blk_pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == RED:
                        self.red_pieces.append(piece)
                    else:
                        self.blk_pieces.append(piece)
