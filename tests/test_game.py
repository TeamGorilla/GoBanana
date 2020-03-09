import unittest

import numpy as np

from gobanana.game.game import Game
from gobanana.game.tiles import Tiles
from gobanana.game.directions import Directions
from gobanana.game.helpermethods import add_tuples

class Test_Board_Legality(unittest.TestCase):
	"""Test methods to check on functions that have to do with board position legality"""

	def test_is_on_board(self):
		game = Game.random_game((6, 6))
		self.assertFalse(game.is_on_board((0, -1)))
		self.assertFalse(game.is_on_board((-1, 0)))
		self.assertTrue(game.is_on_board((0, 0)))
		self.assertTrue(game.is_on_board((3, 4)))
		self.assertFalse(game.is_on_board((7, 6)))
		self.assertFalse(game.is_on_board((6, 7)))
		self.assertTrue(game.is_on_board((5, 5)))

	def test_is_residable(self):
		gamestring = np.array([[Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR],\
		                       [Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR],\
		                       [Tiles.FLOOR, Tiles.FLOOR, Tiles.BANANA_PEEL]])
		game = Game(gamestring)

		badloc = (1,1)
		coordslist = []
		for i in range(game.board.shape[0]):
			for j in range(game.board.shape[1]):
				coordslist.append((i, j))
		
		for (i, j) in coordslist:
			fred = Tiles(game.board[(i, j)])
			if (i, j) != (1,1):
				self.assertTrue(game.is_residable((i, j)))
			else:
				self.assertFalse(game.is_residable((i, j)))

	def test_is_movable_direction(self):
		gamearray = np.array([[Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR],\
		                       [Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR],\
		                       [Tiles.FLOOR, Tiles.FLOOR, Tiles.BANANA_PEEL]])
		game = Game(gamearray)

		fred = game.board[(1,2)]
		self.assertFalse(game.is_movable_direction((1, 2), Directions.LEFT))
		self.assertTrue(game.is_movable_direction((1,2), Directions.UP))
		self.assertTrue(game.is_movable_direction((1,2), Directions.DOWN))
		self.assertFalse(game.is_movable_direction((1, 2), Directions.RIGHT))

		self.assertFalse(game.is_movable_direction((1, 0), Directions.LEFT))
		self.assertTrue(game.is_movable_direction((1,0), Directions.UP))
		self.assertTrue(game.is_movable_direction((1,0), Directions.DOWN))
		self.assertFalse(game.is_movable_direction((1, 0), Directions.RIGHT))

		self.assertTrue(game.is_movable_direction((2, 2), Directions.LEFT))
		self.assertTrue(game.is_movable_direction((2,2), Directions.UP))
		self.assertFalse(game.is_movable_direction((2,2), Directions.DOWN))
		self.assertFalse(game.is_movable_direction((2, 2), Directions.RIGHT))

class Test_Player_Miscellaneous(unittest.TestCase):
	"""Test methods to check miscellaneous things"""

	def test_player_won(self):
		gamearray = np.array([[Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR],\
						[Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR],\
						[Tiles.FLOOR, Tiles.FLOOR, Tiles.BANANA_PEEL]])
		game = Game(gamearray)
		self.assertTrue(game.is_won((2, 2)))
		self.assertFalse(game.is_won((2, 1)))
		self.assertFalse(game.is_won((0, 0)))

		gamearray = np.array([[Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR, Tiles.FLOOR],\
		                      [Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR, Tiles.FLOOR],\
		                      [Tiles.WALL, Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR]])
		game = Game(gamearray)
		self.assertTrue(game.is_won((2, 3)))
		self.assertFalse(game.is_won((2, 2)))
		self.assertFalse(game.is_won((0, 0)))	

class Test_Player_Movement(unittest.TestCase):
	"""Test methods to check on the player movement functions"""

	def test_moved_player(self):
		gamearray = np.array([[Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR, Tiles.FLOOR],\
		                      [Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR, Tiles.FLOOR],\
		                      [Tiles.WALL, Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR]])
		game = Game(gamearray)

		self.assertEqual(game.moved_player((2, 3), Directions.LEFT), (2, 1))
		self.assertEqual(game.moved_player((2, 2), Directions.LEFT), (2, 1))
		self.assertEqual(game.moved_player((2, 2), Directions.UP), (0, 2))
		self.assertEqual(game.moved_player((0, 1), Directions.RIGHT), (0, 3))
		self.assertEqual(game.moved_player((0, 1), Directions.LEFT), (0, 0))

	def test_child_position(self):
		gamearray = np.array([[Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR, Tiles.FLOOR],\
		                     [Tiles.FLOOR, Tiles.WALL, Tiles.FLOOR, Tiles.FLOOR],\
		                     [Tiles.WALL, Tiles.FLOOR, Tiles.BANANA_PEEL, Tiles.FLOOR]])
		game = Game(gamearray)

		self.assertTrue( sorted(game.child_player_positions((2, 3))) == sorted([(2, 1), (1, 3)]))
		self.assertTrue( sorted(game.child_player_positions((2, 2))) == sorted([(2, 1), (2, 3), (0, 2)]))

class Test_Game_String_Conversions(unittest.TestCase):
	"""Test methods that have to do with string conversions"""


	def test_from_string(self):
		game = Game.from_string(\
f"""\
{Tiles.WALL.character*2}{Tiles.BANANA_PEEL.character*3}
{Tiles.BANANA_PEEL.character*5}
{Tiles.FLOOR.character*5}
{Tiles.WALL.character*2}{Tiles.BANANA_PEEL.character*1}{Tiles.FLOOR.character*2}
{Tiles.BANANA_PEEL.character*2}{Tiles.WALL.character*3}
""")
		wall_locs = [(0,0), (0, 1), (3, 0), (3, 1), (4, 2), (4, 3), (4, 4)]
		floor_locs = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
		banana_locs = [(0, 2), (0, 3), (0, 4), (3, 2), (4, 0), (4,1)]
		for wall_loc in wall_locs:
			self.assertEqual(Tiles.WALL, game.board[wall_loc])
		for floor_loc in floor_locs:
			self.assertEqual(Tiles.FLOOR, game.board[floor_loc])
		for banana_loc in banana_locs:
			self.assertEqual(Tiles.BANANA_PEEL, game.board[banana_loc])

		print(game.board)

	def test_to_string(self):
		board =np.array(\
		            [[Tiles.WALL, Tiles.WALL, Tiles.BANANA_PEEL, Tiles.BANANA_PEEL, Tiles.BANANA_PEEL],\
		        	 [Tiles.BANANA_PEEL, Tiles.BANANA_PEEL, Tiles.BANANA_PEEL, Tiles.BANANA_PEEL, Tiles.BANANA_PEEL],\
		        	 [Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR, Tiles.FLOOR],\
		        	 [Tiles.WALL, Tiles.WALL, Tiles.BANANA_PEEL, Tiles.FLOOR, Tiles.FLOOR],\
		        	 [Tiles.BANANA_PEEL, Tiles.BANANA_PEEL, Tiles.WALL, Tiles.WALL, Tiles.WALL]])
		
		game = Game(board)

		gamestring1 = Game.to_string(game)
		gamestring2 =\
f"""\
{Tiles.WALL.character*2}{Tiles.BANANA_PEEL.character*3}
{Tiles.BANANA_PEEL.character*5}
{Tiles.FLOOR.character*5}
{Tiles.WALL.character*2}{Tiles.BANANA_PEEL.character*1}{Tiles.FLOOR.character*2}
{Tiles.BANANA_PEEL.character*2}{Tiles.WALL.character*3}"""

		self.assertEqual(gamestring1, gamestring2, f"To-string failed. \ngamestring1:\n{gamestring1}. \ngamestring2:\n{gamestring2}")
	

	

if __name__ == '__main__':
    unittest.main()