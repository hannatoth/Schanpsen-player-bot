"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
from api import util

class Bot:

	def __init__(self):
		self.ml = util.load_player("ml")
		self.rdeep = util.load_player("rdeep")
		self.minimax = util.load_player("alphabeta")

	def get_move(self, state):
		# type: (State) -> tuple[int, int]
		"""
		Function that gets called every turn. This is where to implement the strategies.
		Be sure to make a legal move. Illegal moves, like giving an index of a card you
		don't own or proposing an illegal mariage, will lose you the game.

		This bot redirects this request depending on the ranking of the current turn:

		* Turn 1, 2, and 3 use the ML bot
		* Turn 4 and 5 use rdeep
		* After that minimax is used


		:param State state: An object representing the gamestate. This includes a link to
			the states of all the cards, the trick and the points.
		:return: A tuple of integers or a tuple of an integer and None,
			indicating a move; the first indicates the card played in the trick, the second a
			potential spouse.
		"""
		#We use the stock size to derive which turn it is
		size = state.get_stock_size()
		if size in [10, 8, 6]:
			delegate = self.ml
		elif size in [4, 2]:
			delegate = self.rdeep
		elif size == 0:
			delegate = self.minimax
		else:
			raise Exception("Stock size not in valid range")
		print (delegate)
		return delegate.get_move(state)