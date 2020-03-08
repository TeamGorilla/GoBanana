from typing import Tuple

import copy
import numpy as np

from gobanana.game.tiles import Tiles
from gobanana.game.directions import Directions
from gobanana.game.helpermethods import add_tuples

class Game():
	"""
	Class to track the board for a Banana Slip game

	Args:
		board (np.ndarray): an np.ndarray object. If not specified, dims should be specified.
	"""
	
	def __init__(self, board):
		assert len(board.shape) == 2, f"The board's dimensionality should be 2. Instead it was {len(board.shape)}"
		assert board.dtype == np.int, f"The elements of the board should be integers. Instead they were {board.dtype}"
		assert board.min() >= min(Tiles), f"There are invalid tiles in the given board"
		assert board.max() <= max(Tiles), f"There are invalid tiles in the given board"
		assert all(dim>0 for dim in board.shape), f"Board dimensions must be greater than 0. Board dimensions were {self._board.shape}"
		self._board = board

	@property
	def board(self):
		"""The representation of the underlying game board"""
		return copy.deepcopy(self._board)

	@property
	def shape(self):
		"""The dimensions of the board"""
		return copy.deepcopy(self._board.shape)

	def is_on_board(self, position):
		"""Returns true if the given position is on the board"""
		assert len(self.shape) == len(position), f"Can only check to see if the newposition is on the board if newposition has the same number of dimensions as the board"
		return all(0<=position[i]<self.shape[i] for i in range(len(position)))

	def is_residable(self, position):
		"""Returns true if the given location is both on the board and not a wall tile (i.e. a valid location for the player to exist)"""
		assert len(self.shape) == len(position), f"Can only check to see if the position is on the board if position has the same number of dimensions as the board"
		#Check whether the new position is on the board and is not a wall tile
		if not self.is_on_board(position):
			return False
		if self.board[position] == Tiles.WALL:
			return False
		return True

	def is_movable_direction(self, position, direction):
		"""
		Returns true if the player can take a step in a given direction from the given position, where the position and direction are tuples,
		"""
		newposition = add_tuples(position, direction)
		return self.is_residable(newposition)

	def moved_player(self, position, direction):
		"""Returns the position to which a player would reside were they to move."""
		assert direction in Directions, f"The direction should be one of the directions in {list(Directions)}"
		assert self.is_movable_direction(position, direction), f"Player cannot move in the provided direction, {Directions(direction)}:{direction}."

		#The first step prior to banana-slipping
		newposition = add_tuples(position, direction)
		#If that step was a banana peel, or they started on a banana, keep moving the player until they hit an invalid position
		if self.board[newposition] == Tiles.BANANA_PEEL or self.board[position] == Tiles.BANANA_PEEL:
			nextposition = add_tuples(newposition, direction)
			while self.is_residable(nextposition):
				newposition = nextposition
				nextposition = add_tuples(newposition, direction)
		#Return the final valid position
		return newposition	

	def child_player_positions(self, position):
		"""Returns the possible player positions to which a player may move from the given position"""
		#Check each direction the player can move in and append the position resulting from that movement to a list
		attainable_positions = []
		for direction in Directions:
			if self.is_movable_direction(position, direction):
				newposition = self.moved_player(position, direction)
				attainable_positions.append(newposition)
		#Return the list of player positions resulting from valid movements
		return attainable_positions

	def child_games(self, position):
		"""Returns the possible games that result from a player move from the given position"""
		#Take each position resulting from valid movements and create a new corresponding game object
		available_games = []
		for child_position in self.child_player_positions(position):
			available_games.append(Game(self._board))
		#Return the list of available 
		return available_games

	def is_won(self, position):
		"""Returns true if the game has been won (the bottom-right corner has been reached)"""
		return position == add_tuples(self.shape, (-1, -1))
	
	def __str__(self):
		"""Represents the game board using ASCII characters"""
		return Board.to_string_with_player(self)

	@staticmethod
	def random_game(dims):
		"""Generates a random game with the provided dimensions"""
		assert all(1<=dim for dim in dims), f"No dimensions of the game board can be nonpositive. Dims provided: {dims}"
		assert len(dims)==2, f"The game board should only have width and height. Dims provided: {dims}."
		board = np.random.choice(a=Tiles, size=dims)
		board[(0,0)] = Tiles.FLOOR
		return Game(board)

	@staticmethod
	def from_string(string):
		"""Returns a Board/ndarray representation of the provided board-formatted-as-text"""
		lines = string.splitlines()
		numrows = len(lines)
		assert numrows>0, "Cannot read board from string with no lines in in it."
		numcols = len(lines[0])
		assert all(len(lines[i]) == numcols for i in range(numrows)), "All rows should have the same length"

		#Form characters into 2D ndarray
		char_matrix = np.array([[row[col] for col in range(numcols)] for row in lines])

		#Convert characters to integers
		vectorized_converter = np.vectorize(lambda char: Tiles.from_char(char))
		convertedboard = vectorized_converter(char_matrix)
		return Game(convertedboard)

	@staticmethod
	def to_string(game, position=None):
		"""Returns an ASCII representation of the board, possibly with a player at the provided position"""
		vectorized_converter = np.vectorize(lambda x: Tiles(x).character)
		convertedboard = vectorized_converter(game.board)
		if position is not None:
			assert game.is_on_board(position)
			convertedboard[position] = '@'
		return '\n'.join(''.join(row) for row in convertedboard)