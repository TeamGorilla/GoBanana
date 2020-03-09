class _ConstantList(type):
	"""Metaclass to allow iterating over a list of class members"""
	def __iter__(self):
		for attr in vars(self).keys():
			if not attr.startswith("__"):
				returnattr = self.__dict__[attr]
				if not callable(returnattr):
					yield self.__dict__[attr]

class Directions(metaclass=_ConstantList):
	"""Tuples representing Up, Down, Left and Right"""
	UP = (0, -1)
	DOWN = (0, 1)
	LEFT = (-1, 0)
	RIGHT = (1, 0)