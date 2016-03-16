
"""
	Some not necessarily coherent helper functions.
"""

from numpy import array
from os import fork
from bardeen.mpl.mpl import MPL


def qplot(X = None, *Ys):
	"""
		Make a quick plot without options, just for testing; you still need to call show()
	"""
	X = None if X is None else array(X)
	if X is None and Ys is None:
		raise Exception('quickplot needs something to plot')
	if not Ys:
		Ys = array([X])
		X = None
	if X is None:
		X = array(range(len(Ys[0])))
	fig, ax = MPL.instance().subplots()
	for k, Y in enumerate(Ys):
		ax.plot(X, Y, label = '#%d' % k)
	ax.legend(loc = 'lower right')


def splot(X = None, *Ys):
	"""
		Make a simple plot without options, just for testing, and show it immediately in the background
		(without blocking the program flow, but not closing when program exits).

		quickplot(y)
		quickplot(x, y)
		quickplot(x, y, z)
		quickplot(None, y, z)
	"""
	procnr = fork()
	if procnr == 0:
		qplot(X, *Ys)
		MPL.instance().show()
		exit()


