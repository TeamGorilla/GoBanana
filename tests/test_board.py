import pytest
import numpy as np

from gobanana import game


def test_tile_encode_decode():
    for tile in (game.Board.WALL, game.Board.ROAD, game.Board.BANANA):
        encoded = game.Board.encode_tile(tile)
        decoded = game.Board.decode_tile(encoded)
        assert decoded == tile


def test_board_conversions():
    list_representation_board = [
        [1, 1, 1],
        [1, 0, 0],
        [0, 2, 1]
    ]
    board_from_list = game.Board.from_list(list_representation_board)

    assert board_from_list.to_list() == list_representation_board

    one_hot_representation_board = board_from_list.to_one_hot()
    board_from_one_hot = game.Board.from_one_hot(one_hot_representation_board)

    assert board_from_one_hot == board_from_list


def test_assert_valid_board():
    with pytest.raises(AssertionError):
        game.Board.from_list([[4]])

    with pytest.raises(AssertionError):
        game.Board(np.array([-1, 3]))

    with pytest.raises(AssertionError):
        game.Board(np.array([1, 0], dtype=np.float))
