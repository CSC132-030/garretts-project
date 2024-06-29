from .piece import Piece
from .board import Board
from .constants import BLACK
from bot.algorithm import *

class Bot:
	def __init__(self, color, game, depth, max):
		self.color = color
		self.game = game
		self.depth = depth
		self.max = max

	def take_turn(self):
		curr_board = self.game.get_board()
		score, new_board = find_move(curr_board, self.depth, self.game, self.max)
		#print(f'type {type(new_board)}')
		self.game.bot_end_turn(new_board)



