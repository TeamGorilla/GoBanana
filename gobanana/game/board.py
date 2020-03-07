import numpy as np


class Board(object):
    ROAD = 0
    WALL = 1
    BANANA = 2

    def __init__(self, mat: np.ndarray):
        self._mat = mat
        assert len(self._mat.shape) == 2

    @property
    def mat(self):
        return self._mat

    @property
    def shape(self):
        return self._mat.shape

    @classmethod
    def encode_tile(cls, tile):
        assert tile in (Board.ROAD, Board.WALL, Board.BANANA)
        vector = np.zeros(3, dtype=np.int)
        vector[tile] = 1
        return vector

    @classmethod
    def decode_tile(cls, vector):
        tile = vector.argmax()
        assert tile in (Board.ROAD, Board.WALL, Board.BANANA)
        return tile

    def to_list(self):
        return self._mat.tolist()

    @classmethod
    def from_list(cls, list_board):
        assert list_board
        num_rows = len(list_board)
        num_cols = len(list_board[0])
        mat = np.zeros((num_rows, num_cols), dtype=np.int)
        for row_idx, row in enumerate(list_board):
            assert len(row) == num_cols
            for col_idx, tile in enumerate(row):
                assert tile in (Board.ROAD, Board.WALL, Board.BANANA)
                mat[row_idx, col_idx] = tile
        return Board(mat)

    def to_one_hot(self):
        one_hot_mat = self._mat[:, :, np.newaxis]
        return np.apply_along_axis(self.encode_tile, -1, one_hot_mat)

    @classmethod
    def from_one_hot(cls, one_hot_board):
        mat = np.apply_along_axis(cls.decode_tile, -1, one_hot_board).squeeze()
        return Board(mat)

    def __eq__(self, other):
        assert isinstance(other, Board)
        return (self._mat == other.mat).all()
