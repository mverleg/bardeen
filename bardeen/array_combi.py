
from numpy import array


def reduce_arrays_align0(arrays, reduce_func=lambda a, b: a + b):
	"""
	For a series of arrays, take the largest slice that fits within all arrays starting at 0,
	and then apply a reduction function (on arr1 & arr2, then the result and arr3, etc).
	
	Number of dimensions for the arrays must be the same, but shape needn't be, if they can
	be aligned at the smallest index.
	
	If `reduce_func` is not replaced, the arrays are summed.
	"""
	if len(arrays) == 0:
		return 0
	if len(arrays) == 1:
		return arrays[0]
	shapes = tuple(arr.shape for arr in arrays)
	dim_counts = set(len(shape) for shape in shapes)
	assert len(dim_counts) == 1, ('number (not size) of dimensions should be the '
		'same for all arrays in reduce_arrays_align0; got lengths {0:}').format(
		''.join(str(dim) for dim in dim_counts))
	minshape = array(shapes).min(0)
	if any(dim == 0 for dim in minshape):
		return 0
	slices = tuple(slice(0, dim, 1) for dim in minshape)
	result = arrays[0][slices]
	for arr in arrays[1:]:
		result = reduce_func(result, arr[slices])
	return result


