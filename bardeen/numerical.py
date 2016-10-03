

from numpy import eye, float64


def laplacian(N, dtype = float64):
	"""
	Create a del2 laplacian matrix of dimension N.

	E.g. for N = 4:

	.. math::

		\begin{matrix}
		 2 & -1 &  0 &  0 \\\\
		-1 &  2 & -1 &  0 \\\\
		 0 & -1 &  2 & -1 \\\\
		 0 &  0 & -1 &  2 \\\\
		\end{matrix}

	Used for numerical differentiation.

	In many cases, :ref: scipy.ndimage.filters.laplace, which calculates the derivative of a vector,
	is faster (but might be slightly different at boundaries).

	Note that this is not the graph theory laplacian matrix.
	"""
	return 2 * eye(N, k = 0, dtype = dtype) + \
			 - eye(N, k = -1, dtype = dtype) + \
			 - eye(N, k = 1, dtype = dtype)

"""
	NOTE: if you add something, write a test!
"""
