from tilemapping import Tiles
from enum import Enum, auto
import copy
import numpy as np

class Directions(Enum):
	UP = auto(), (0, -1)
	DOWN = auto(), (0, 1)
	LEFT = auto(), (-1, 0)
	RIGHT = auto(), (1, 0)
	def __new__(cls, keycode, coords=None):
		obj = object.__new__(cls)
		obj._value_ = keycode
		obj.coords = np.array(coords)
		return obj

def addtuples(tuple1, tuple2):
	tuple1 = tuple(tuple1)
	tuple2 = tuple(tuple2)
	return tuple(map(sum, zip(tuple1, tuple2)))

class Game():
	def __init__(self, dims, board=None, player=None):
		self._board = board if board is not None else np.random.randint(low = 0, high = len(Tiles), size = dims)
		self._player = player if player is not None else (0, 0)
		self._dims = dims

	@property
	def board(self):
		return self._board.copy()
	@property
	def player(self):
		return copy.deepcopy(self._player)
	@property
	def dims(self):
		return copy.deepcopy(self._dims)

	def deepcopy(self):
		dc = Game(self.dims, self.board, self.player)
		return dc

	def __str__(self):
		vectorized_converter = np.vectorize(lambda x: Tiles(x).character)
		convertedboard = vectorized_converter(self.board)
		convertedboard[self.player] = '@'
		return '\n'.join(''.join(row) for row in convertedboard)

	def canmoveinto(self, newposition):
		if any(np.less(newposition, (0, 0))):
			return False
		if any(np.greater_equal(newposition, self.dims)):
			return False
		if self.board[newposition] == Tiles.WALL:
			return False
		return True

	def canmovealong(self, direction):
		newposition = addtuples(self.player, direction.coords)
		return self.canmoveinto(newposition)

	def moved_in_direction(self, direction):
		newposition = addtuples(self.player, direction.coords)
		if self.board[newposition] == Tiles.BANANA_PEEL:
			while self.canmoveinto(addtuples(newposition, direction.coords)):
				newposition = addtuples(newposition, direction.coords)
		
		return Game(self.dims, self.board, newposition)


	def getmoves(self):
		availablemoves = []
		for direction in Directions:
			if self.canmovealong(direction):
				availablemoves.append(self.moved_in_direction(direction))
		return availablemoves
