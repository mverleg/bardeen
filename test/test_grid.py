
from pytest import raises
from numpy import prod
from grid import to_coordinate, from_coordinate


def test_grid_inversion():
	dims = (2, 3, 2, 4)
	for k in range(prod(dims)):
		assert from_coordinate(to_coordinate(k, dims), dims) == k


def test_grid_examples():
	dims = (2, 3, 2, 4)
	assert to_coordinate(0, dims)  == (0, 0, 0, 0)
	assert to_coordinate(17, dims) == (0, 2, 0, 1)
	assert to_coordinate(39, dims) == (1, 1, 1, 3)


def test_changing_dims():
	dims = (2, 3, 2, 4)
	assert to_coordinate(17, dims) == (0, 2, 0, 1)
	dims = (1, 2, 1, 1)
	assert to_coordinate(1, dims) == (0, 1, 0, 0)


def test_one_dimensional():
	dims = (7,)
	for k in range(dims[0]):
		assert to_coordinate(k, dims)  == (k,)
		assert from_coordinate(to_coordinate(k, dims), dims) == k


def test_out_of_bounds():
	dims = (2, 3, 2, 4)
	with raises(AssertionError):
		to_coordinate(-1, dims)
	with raises(AssertionError):
		print(to_coordinate(prod(dims), dims))
	with raises(AssertionError):
		from_coordinate((0, 0, 0, -1), dims)
	with raises(AssertionError):
		from_coordinate((0, 0, 0, 7), dims)


