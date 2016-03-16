
"""
	unit tests for bardeen.numerical
"""

from bardeen.numerical import laplacian


def test_laplacian():
	for N in [1, 2, 3, 7]:
		M = laplacian(N)
		assert M.shape == (N, N)
		for k in range(N):
			for m in range(N):
				if k == m:
					assert M[k, m] == 2
				elif abs(k - m) == 1:
					assert M[k, m] == -1
				else:
					assert M[k, m] == 0


