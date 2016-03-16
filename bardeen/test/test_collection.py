
"""
	unit tests for bardeen.collection
"""

from bardeen.collection import group_by


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


