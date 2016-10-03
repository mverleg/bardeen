
"""
N-dimensional grid.
"""

from numpy import prod
from sys import stderr


stderr.write('These grid functions are deprecated since numpy offers the same functionality using unravel_index and ravel_multi_index.')


def to_coordinate(index, dims):
	"""
	Convert from 'element N' to 'result matrix coordinate [x, y, z]'.
	"""
	assert 0 <= index < remaining_dims(dims)[0], 'The index {0:d} is out of bounds (the grid has {1:d} elements)'.format(index, remaining_dims(dims)[0])
	return tuple(index // remaining_dims(dims)[k + 1] % dim for k, dim in enumerate(dims))


def from_coordinate(coordinate, dims):
	"""
	Convert from 'result matrix coordinate [x, y, z]' to 'element N'.
	"""
	for coord, dim in zip(coordinate, dims):
		assert 0 <= coord <  dim
	return sum(tuple(coordinate[k] * remaining_dims(dims)[k + 1] for k in range(len(dims))))


def remaining_dims(dims):
	remaining_dims.CACHE = getattr(remaining_dims, 'CACHE', {})
	remaining_dims.CACHE[dims] = remaining_dims.CACHE.get(dims, tuple(prod(dims[k:], dtype = int) for k in range(len(dims) + 1)))
	return remaining_dims.CACHE[dims]


