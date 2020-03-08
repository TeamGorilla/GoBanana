from copy import deepcopy
import numpy as np
from gobanana.game.tiles import Tiles

class Board(np.ndarray):
    """
    Class to convert and track game boards. Extends ndarray.

    Args:
        input_array (np.ndarray): The input array/matrix the instantiated object of this class will be the value of.
    """

	##Methods for inheriting from ndarray

	def __new__(cls, input_array):
		obj = np.asarray(input_array).view(cls)
		return obj

	def __array_finalize__(self, obj):
		if obj is None:
			return


	##Instance methods

	def to_one_hot(self):
		"""Converts a 2D board of tile values into a 3D board of one-hot vectors"""
		return Board.to_one_hot(self)

	def __str__(self):
		"""Represents the board using ASCII characters"""
		return Board.to_string(self)


	##Static Methods

	@staticmethod
	def encode_tile(tile):
		"""Takes in a tile value and returns a one-hot vector encoding of that tile"""
		assert tile in Tiles.values()
		vector = np.zeros(3, dtype=np.int)
		vector[tile] = 1
		return vector

	@staticmethod
	def decode_tile(vector):
		"""Takes in a one-hot vector representing a tile on the board and returns the tile"""
		tile = vector.argmax()
		assert tile in Tiles.values()
		return tile

	@staticmethod
	def fromlist(cls, list_board):
		"""Converts a list of lists to a board (with sanity checks)"""
		num_rows = len(list_board)
		num_cols = len(list_board[0])
		mat = np.zeros((num_rows, num_cols), dtype=np.int)
		for row_idx, row in enumerate(list_board):
			assert len(row) == num_cols
			for col_idx, tile in enumerate(row):
				assert tile in Tiles.values
				mat[row_idx, col_idx] = tile
		return Board(mat)

	@staticmethod
	def to_one_hot(board: np.ndarray):
		"""Converts a 2D board of tile values into a 3D board of one-hot vectors"""
		one_hot_mat = board[:, :, np.newaxis]
		return np.apply_along_axis(Board.encode_tile, -1, one_hot_mat)

	@staticmethod
	def from_one_hot(one_hot_board):
		"""Converts a 3D board of one-hot vectors representing tiles into a 2D board of tile values"""
		mat = np.apply_along_axis(Board.decode_tile, -1, one_hot_board).squeeze()
		return Board(mat)
    	
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
		return Board(convertedboard)

	@staticmethod
	def to_string(board):
		"""Returns an ASCII representation of the board"""
		vectorized_converter = np.vectorize(lambda x: Tiles(x).character)
		convertedboard = vectorized_converter(game.board)
		return '\n'.join(''.join(row) for row in convertedboard)
