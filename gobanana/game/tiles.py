from enum import IntEnum, unique

@unique
class Tiles(IntEnum):
	"""Enumerated constants for holding information about tiles"""
	FLOOR 		= 0, 'floor', '.'
	WALL		= 1, 'wall', '#'
	BANANA_PEEL	= 2, 'banana', '^'

	def __new__(cls, keycode, spritename=None, character = None):
		obj = int.__new__(cls, keycode)
		obj._value_ = keycode
		obj.spritename = spritename or 'unknown'
		obj.character = character or '?'
		return obj	
	
	def values():
		"""Returns a list of the enumerated constants' underlying values"""
		return [key.value for key in Tiles]