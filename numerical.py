

from numpy import eye, float64


def laplacian(N, dtype = float64):
	'''
		create a del2 laplacian matrix of dimension N
		e.g. for N = 4
		 2 -1  0  0
		-1  2 -1  0
		 0 -1  2 -1
		 0  0  -1 2
		used for numerical differentiation
		in many cases, scipy.ndimage.filters.laplace is faster
		  (might be slightly different at boundaries)
		(not the graph theory laplacian matrix)
	'''
	return 2 * eye(N, k = 0, dtype = dtype) + \
			 - eye(N, k = -1, dtype = dtype) + \
			 - eye(N, k = 1, dtype = dtype)


