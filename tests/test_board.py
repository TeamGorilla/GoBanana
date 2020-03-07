from gobanana import game


def test_board():
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

