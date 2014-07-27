
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


def dict_round_floats(dicti, decim = 6):
	"""
		go through a dict and round all floats (in keys and values) to a
		specific number of decimal places, to make it possible to compare
		a dict that has been saved and loaded, or some math applied
	"""
	for key, value in dicti.items():
		if isinstance(key, float):
			''' this also matches for numpy.float64 etc '''
			del dicti[key]
			dicti[round(key, decim)] = value
		if isinstance(value, float):
			dicti[key] = round(value, decim)

"""
	NOTE: if you add something, write a test!
"""


