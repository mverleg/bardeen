
"""
	routines useful for comparison (esp. unit testing)
"""


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


