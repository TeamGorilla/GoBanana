from enum import IntEnum, unique, EnumMeta
from collections import defaultdict

class TilesMeta(EnumMeta):
	reverse_spritename_lookup = defaultdict(lambda: -1)
	reverse_character_lookup = defaultdict(lambda: -1)

@unique
class Tiles(IntEnum, metaclass=TilesMeta):
	"""Enumerated constants for holding information about tiles"""
	FLOOR 		= 0, 'floor', '.'
	WALL		= 1, 'wall', '#'
	BANANA_PEEL	= 2, 'banana', '^'

	def __new__(cls, keycode, spritename=None, character = None):
		obj = int.__new__(cls, keycode)
		obj._value_ = keycode

		if spritename is not None:
			obj.spritename = spritename
			cls.reverse_spritename_lookup[spritename] = obj
		else:
			obj.spritename = 'unknown'

		if character is not None:
			obj.character = character
			cls.reverse_character_lookup[character] = obj
		else:
			obj.character = '?'		
		return obj	

	@classmethod
	def from_sprite(cls, sprite):
		"""Returns the tile associated with this sprite name"""
		return cls.reverse_spritename_lookup[sprite]
	
	@classmethod
	def from_char(cls, char):
		"""Returns the tile associated with this character"""
		return cls.reverse_character_lookup[char]

	@classmethod
	def values(cls):
		"""Returns a list of the enumerated constants' underlying values"""
		return [key.value for key in cls]