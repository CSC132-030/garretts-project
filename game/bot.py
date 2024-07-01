from bot.algorithm import *


class Bot:
	def __init__(self, color, game, depth, maximize):
		self.color = color
		self.game = game
		self.depth = depth
		self.max = maximize

	def take_turn(self):
		curr_board = self.game.get_board()
		score, new_board = find_move(curr_board, self.depth, self.game, self.max)
		self.game.bot_end_turn(new_board)



