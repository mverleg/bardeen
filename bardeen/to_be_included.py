
"""
These functions should perhaps be included, but have not been sufficiently tested yet
"""

from numpy import prod


# from numerical_recipes/4/io
	# maybe not, perhaps realistically the grid would not be completely full and thus stored differently
def savegrid(filename, data, dims, format='%.18e', delims=['\t', '\n']):
	"""
	Save a 1D vector representing a grid to a file with given formatting and delimiters.

	The most typical example would be a 2D wavefunction stored in a 1D vector for numerical reasons.
	"""
	if len(delims) == 1:
		delims = [delims] * len(dims)
	elif len(delims) < len(dims):
		raise AssertionError('need a delimiter for each dimension! [%d]' % len(delims))
	assert len(data) == prod(dims), 'data should be a (1D) vector with a value for each grid point in dims'
	with open(filename, 'w+') as fh:
		for k, dim, delim in zip(range(len(dims)), dims, delims):
			print('dimension')
			for val in dim:
				fh.write('%s%s' % (format % val, delim))
			fh.write('\n')



