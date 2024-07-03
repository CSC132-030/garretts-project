from bot.algorithm import *

# class representing the bot player for single player games
class Bot:
	def __init__(self, color, game, depth, maximize):
		self.color = color  # color bot is playing as
		self.game = game  # game bot is playing in
		self.depth = depth  # recursion depth/number of moves to look ahead/difficulty
		self.max = maximize  # True = best move is max'd evaluated board score, False = best move is min'd score

	# method instructing bot how to take its turn
	def take_turn(self):
		curr_board = self.game.get_board()  # get the current board
		score, new_board = find_move(curr_board, self.depth, self.game, self.max)  # find best move and resulting board
		self.game.bot_end_turn(new_board)  # end turn by calling method & passing resulting board to game object



