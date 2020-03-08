from typing import Tuple

import copy
import numpy as np

from tiles import Tiles
from directions import Directions
from helpermethods import addtuples

class Game():
	"""
	Class to track the board and player position for a Banana Slip game

	Args:
		board (Board): a Board object. If not specified, dims should be specified.
		player (Tuple<int>): The player's coordinates within the board (i.e., (0,0) is the upper-left corner; (0,1) is one spot right.)
	"""
	
	def __init__(self, board, player:Tuple = (0,0)):
		assert len(board.shape) == 2, f"The board's dimsensionality should be 2. Instead it was {len(board.shape)}"
		assert board.dtype == np.int, f"The elements of the board should be integers. Instead they were {board.dtype}"
		assert board.min() >= min(Tiles), f"There are invalid tiles in the given board"
		assert board.max() <= max(Tiles), f"There are invalid tiles in the given board"
		assert all(dim>0 for dim in board.shape), f"Board dimensions must be greater than 0. Board dimensions were {self._board.shape}"
		assert board[player] is not Tiles.WALL, f"Player cannot start in a wall. Player position was {self._player}"
		self._board = board
		self._player = player

	@property
	def board(self):
		"""The representation of the underlying game board, sans the player"""
		return copy.deepcopy(self._board)

	@property
	def player(self):
		"""The player position atop the board"""
		return copy.deepcopy(self._player)

	@property
	def shape(self):
		"""The dimensions of the board"""
		return copy.deepcopy(self._board.shape)

	def is_on_board(self, newposition):
		"""Returns true if the given position is on the board"""
		assert len(self.shape) == len(newposition), f"Can only check to see if the newposition is on the board if newposition has the same number of dimensions as the board"
		return all(0<=newposition[i]<self.shape[i] for i in range(len(newposition)))

	def is_residable(self, newposition):
		"""Returns true if the given location is both on the board and not a wall tile"""
		assert len(self.shape) == len(newposition), f"Can only check to see if the newposition is on the board if newposition has the same number of dimensions as the board"
		#Check whether the new position is on the board and is not a wall tile
		if not self.is_on_board(newposition):
			return False
		if self.board[newposition] == Tiles.WALL:
			return False
		return True

	def is_movable_direction(self, direction):
		"""
		Returns true if the player can take a step in a given direction, where the direction is a tuple
		representing the change in coofrom board import Boarddinates from the current position
		"""
		newposition = addtuples(self._player, direction)
		return self.is_residable(newposition)

	def moved_player(self, direction):
		"""Returns the position to which a player would reside were they to move."""
		assert direction in Directions, f"The direction should be one of the directions in {list(Directions)}"
		assert self.is_movable_direction(direction), f"Player cannot move in the provided direction, {Directions(direction)}:{direction}."
		#The first step prior to banana-slipping
		newposition = addtuples(self._player, direction)
		#If that step was a banana peel, keep  moving the player until they hit an invalid position
		if self.board[newposition] == Tiles.BANANA_PEEL:
			nextposition = addtuples(newposition, direction)
			while self.is_residable(nextposition):
				newposition = nextposition
				nextposition = addtuples(newposition, direction)
		#Return the final valid position
		return newposition

	def child_player_positions(self):
		"""Returns the possible player positions to which a player may move from this point"""
		#Check each direction the player can move in and append the position resulting from that movement to a list
		attainable_positions = []
		for direction in Directions:
			if self.is_movable_direction(direction):
				newposition = self.moved_player(direction)
				attainable_positions.append(newposition)
		#Return the list of player positions resulting from valid movements
		return attainable_positions

	def child_games(self):
		"""Returns the possible games that result from a player move from this point"""
		#Take each position resulting from valid movements and create a new corresponding game object
		available_games = []
		for child_position in self.child_player_positions():
			available_games.append(Game(self._board, child_position))
		#Return the list of available 
		return available_games
	
	def __str__(self):
		"""Represents the game using ascii characters"""
		vectorized_converter = np.vectorize(lambda x: Tiles(x).character)
		convertedboard = vectorized_converter(self._board)
		convertedboard[self._player] = '@'
		return '\n'.join(''.join(row) for row in convertedboard)

	@staticmethod
	def random_game(dims):
		"""Generates a random game with the provided dimensions"""
		assert all(1<=dim for dim in dims), f"No dimensions of the game board can be nonpositive. Dims provided: {dims}"
		assert len(dims)==2, f"The game board should only have width and height. Dims provided: {dims}."
		board = np.random.choice(a=Tiles, size=dims)
		board[(0,0)] = Tiles.FLOOR
		return Game(board, (0,0))


