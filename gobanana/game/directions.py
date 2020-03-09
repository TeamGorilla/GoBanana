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
	UP = (-1, 0)
	DOWN = (1, 0)
	LEFT = (0, -1)
	RIGHT = (0, 1)