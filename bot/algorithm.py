## IMPORTS ##

# allow boards to be copied to simulate moves without altering original board state
from copy import deepcopy as dcopy
from game.constants import RED, BLACK

# Find best move based on the curr board state, num of moves to look ahead (depth), game (in case later want to run
# multiple game simultaneously, and bool whether to maximize score (True = Black since it wants to maximize the score
# returned by eval function, False = Red since it wants to minimize score returned by eval function)
def find_move(curr_board, depth, curr_game, maximize):
	# if at max depth or the board would win game, return the score and board state
	if depth == 0 or curr_board.win_game() is not False:
		return curr_board.eval_board(), curr_board

	# If score is being max'd...
	if maximize:
		hi_score = float('-inf')  # initial hi_score is -inf so any returned board state score > initial score
		best_board = None

		# get all possible board states that would result from all possible moves black pieces could make based on the
		# curr board state and game
		possible_moves = get_all_moves(curr_board, BLACK, curr_game)

		# for each potential board state in the resulting possible board states
		for pot_board in possible_moves:
			# recursively check next depth level which would be a prediction of the move red would make and then
			# return only the score and not resulting board state until all possible moves checked
			curr_score = find_move(pot_board, depth-1, curr_game, False)[0]
			hi_score = max(hi_score, curr_score)  # set hi score to the highest of previous hi score and current score

			# if the hi score is the curr score that was just returned, save that board stat as best board possible
			if hi_score == curr_score:
				best_board = pot_board

		return hi_score, best_board  # return the best board state and best score found, indicating the optimal move

	# get all possible board states that would result from all possible moves red pieces could make based on the
	# curr board state and game (same as black except best score is lowest rather than highest)
	else:
		lo_score = float('inf')
		best_board = None

		possible_moves = get_all_moves(curr_board, RED, curr_game)

		for pot_board in possible_moves:
			curr_score = find_move(pot_board, depth - 1, curr_game, True)[0]
			lo_score = min(lo_score, curr_score)

			if lo_score == curr_score:
				best_board = pot_board

		return lo_score, best_board


def try_move(piece, move, board, game, jumped):
	board.move(piece, row=move[0], col=move[1])

	if jumped:
		board.remove(jumped)

	return board

# function returning all possible moves for a given colors pieces based on a given board state
def get_all_moves(board, player_color, game):
	possible_moves = []

	board.get_all_pieces()  # update the list of pieces for each color on the given board
	piece_dict = {RED: board.red_pieces, BLACK: board.blk_pieces}

	# for each piece in the list of pieces for given color...
	for piece in piece_dict[player_color]:
		valid_moves = board.get_valid_moves(piece)  # get valid moves of each piece of that color

		# for each move, simulate the board state after that move and evaluate the resulting board's score
		for move, jumped in valid_moves.items():
			board_copy = dcopy(board)  # copy of current board state to be altered to test potential moves/outcomes
			test_piece = board_copy.get_piece(piece.row, piece.col)
			new_board = try_move(test_piece, move, board_copy, game, jumped)
			possible_moves.append(new_board)

	return possible_moves




