
from numpy import hstack, vstack, arange, newaxis, allclose
from bardeen.array_combi import reduce_arrays_align0


def test_reduce_arrays_align0():
	basearr = hstack(arange(5)[:, newaxis] for k in range(5)) + vstack(arange(5) for k in range(5))
	arrays = [
		basearr[:5, :3],
		basearr[:3, :5],
		basearr[:4, :4],
	]
	res = reduce_arrays_align0(arrays)
	assert allclose(res, 3 * basearr[:3, :3])


