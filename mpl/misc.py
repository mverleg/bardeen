
"""
	Some not necessarily coherent helper functions.
"""

from os import fork
from bardeen.mpl.mpl import MPL


def qplot(X = None, Ys = None):
	"""
		Make a quick plot without options, just for testing; you still need to call show()
	"""
	if X is None and not len(Ys):
		raise Exception('quickplot needs something to plot')
	if not Ys:
		Ys = [X]
		X = None
	if X is None:
		X = range(len(Ys[0]))
	fig, ax = MPL.instance().subplots()
	for k, Y in enumerate(Ys):
		ax.plot(X, Y, label = '#%d' % k)
	ax.legend(loc = 'lower right')


def plotshow(X = None, Ys = None):
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
		qplot(X = X, Ys = Ys)
		MPL.instance().show()
		exit()



