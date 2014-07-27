
from collections import defaultdict


def group_by(collection, get_property):
	"""
		for a list of items, group them by some property and return tuples of
		that property and all items that have it

		itertools.groupby requires the items to be sorted by property;
		more efficient but annoying to use

			for unique_prop, items in group_by(items, lambda item: item.name).items():
	"""
	grouped = defaultdict(list)
	for item in collection:
		grouped[get_property(item)].append(item)
	return grouped


"""
	NOTE: if you add something, write a test!
"""


