
from collections import defaultdict


def group_by(collection, get_property):
	"""
	For a list of items, group them by some property and return tuples of
	that property and all items that have it.

	Similar to :func:`itertools.groupby`, but that requires the items to be ordered by that property; \
	more efficient but annoying to use.

	>>> for unique_prop, items in group_by(items, lambda item: item.name).items():
		print '%s: %d' % (unique_prop, len(items))
	"""
	grouped = defaultdict(list)
	for item in collection:
		grouped[get_property(item)].append(item)
	return grouped


def without(iterable, remove_indices):
	"""
	Returns an iterable for a collection or iterable, which returns all items except the specified indices.
	"""
	if not hasattr(remove_indices, '__iter__'):
		remove_indices = {remove_indices}
	else:
		remove_indices = set(remove_indices)
	for k, item in enumerate(iterable):
		if k in remove_indices:
			continue
		yield item


