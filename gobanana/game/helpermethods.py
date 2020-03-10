from typing import Tuple

def add_tuples(tuple1: Tuple, tuple2: Tuple):
	"""Method for adding two tuples together"""
	assert len(tuple1)==len(tuple2), f"Added tuples must be of equal length. Tuple 1 was {tuple1}, Tuple 2 was {tuple2}"
	return tuple(map(sum, zip(tuple1, tuple2)))