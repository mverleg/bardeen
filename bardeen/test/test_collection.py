
"""
	unit tests for bardeen.collection
"""

from bardeen.collection import group_by, without, make_unique_strs


def test_group_by():
	""" dividing numbers 0-100 in %N groups' """
	for N in [1, 2, 7, 12]:
		groups = group_by(range(70), lambda item: item % N)
		assert set(groups.keys()) == set(range(N))
		assert sum(len(items) for items in groups.values()) == 70
		for n, li in groups.items():
			assert all(k % N == n for k in li)
	""" grouping instances by class type """
	class A(object): pass
	class B(object): pass
	objs = [A() if (k % 2) * (k % 3) else B() for k in range(60)]
	groups = group_by(objs, lambda item: item.__class__)
	assert len(groups) == 2
	assert A in groups.keys() and B in groups.keys()
	assert len(groups[A]) == 20 and len(groups[B]) == 40
	assert all(item.__class__ is A for item in groups[A])


def test_without():
	li = list(range(5))
	assert list(without(li, (0, 2))) == [1, 3, 4]
	assert list(without(li, 3)) == [0, 1, 2, 4]
	print(without(li, 3))
	assert False


def test_make_unique_strs():
	assert make_unique_strs(['alpha', 'alpha', 'beta', 'alpha']) == ['alpha-1', 'alpha-2', 'beta', 'alpha-3']


