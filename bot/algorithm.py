## IMPORTS ##

# allow boards to be copied to simulate moves without altering original board state
from copy import deepcopy as dcopy
import pygame as py
from game.constants import RED, BLACK


def find_move(curr_board, depth, curr_game, maximize):
	if depth == 0 or curr_board.win_game() is not False:
		return curr_board.eval_board(), curr_board

	if maximize:
		hi_score = float('-inf')
		best_board = None

		possible_moves = get_all_moves(curr_board, BLACK, curr_game)

		for pot_board in possible_moves:
			# recursively return only score and not resulting board state until all possible moves checked
			curr_score = find_move(pot_board, depth-1, curr_game, False)[0]
			hi_score = max(hi_score, curr_score)

			if hi_score == curr_score:
				best_board = pot_board

		return hi_score, best_board

	else:
		lo_score = float('inf')
		best_board = None

		possible_moves = get_all_moves(curr_board, RED, curr_game)

		for pot_board in possible_moves:
			# recursively return only score and not resulting board state until all possible moves checked
			curr_score = find_move(pot_board, depth - 1, curr_game, True)[0]
			lo_score = min(lo_score, curr_score)

			if lo_score == curr_score:
				best_board = pot_board

		return lo_score, best_board


def try_move(piece, move, board, game, jumped):
	board.move(piece, row=move[0], col=move[1])

	if jumped:
		#jumped_pcs = len(jumped)  # TODO: Add additional scoring for number of jumped pieces here?
		board.remove(jumped)

	return board


def get_all_moves(board, player_color, game):
	possible_moves = []

	board.get_all_pieces()
	piece_dict = {RED: board.red_pieces, BLACK: board.blk_pieces}  # TODO: gotta be a better way to do this...

	for piece in piece_dict[player_color]:
		valid_moves = board.get_valid_moves(piece)

		for move, jumped in valid_moves.items():
			board_copy = dcopy(board)  # copy of current board state to be altered to test potential moves/outcomes
			test_piece = board_copy.get_piece(piece.row, piece.col)
			new_board = try_move(test_piece, move, board_copy, game, jumped)
			possible_moves.append(new_board)

	return possible_moves




