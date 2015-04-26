
"""
	Replacements or addictions for matplotlib axis methods (labels, colours)
"""

from numpy import abs, real, imag


''' default color cycle for scatter '''
boynton_colors = [
	(0., 0., 1., 1.),    # Blue
	(1., 0., 0., 1.),    # Red
	(0., 1., 0., 1.),    # Green
	(1., 1., 0., 1.),    # Yellow
	(1., 0., 1., 1.),    # Magenta
	(1., .5, .5, 1.),    # Pink
	(.5, .5, .5, 1.),    # Gray
	(.5, 0., 0., 1.),    # Brown
	(1., .5, 0., 1.),    # Orange
]


def color_cycle_scatter(ax, *args, **kwargs):
	"""
		New :ref: ax.scatter method that cycles through colours if none are provided
	"""
	if 'color' in kwargs.keys():
		return ax.mono_color_scatter(*args, **kwargs)
	return ax.mono_color_scatter(*args, color = next(ax.custom_color_cycle), **kwargs)


def small_pad_xlabel(ax, *args, **kwargs):
	"""
		New :ref: ax.xlabel with smaller default padding (not a rcParam apparently)
	"""
	if 'labelpad' in kwargs.keys():
		return ax.big_pad_xlabel(*args, **kwargs)
	return ax.big_pad_xlabel(*args, labelpad = 0., **kwargs)


def small_pad_ylabel(ax, *args, **kwargs):
	if 'labelpad' in kwargs.keys():
		return ax.big_pad_ylabel(*args, **kwargs)
	return ax.big_pad_ylabel(*args, labelpad = 2., **kwargs)


def plotim(ax, *args, **kwargs):
	"""
		Plot the real, imaginary and absolute of a (supposedly complex) function
	"""
	if 'label' in kwargs.keys():
		label = '%s ' % kwargs.pop('label')
	else:
		label = '$\Psi$'
	if len(args) >= 2:
		x, y = args[0], args[1]
		args = args[2:]
	else:
		x, y = range(len(args[0])), args[0]
		args = args[1:]
	plots = []
	plots.append(ax.plot(x,  abs(y), *args, label = '$|$%s$|$' % label, **kwargs))
	plots.append(ax.plot(x, real(y), *args, label = '$\Re$ %s' % label, **kwargs))
	plots.append(ax.plot(x, imag(y), *args, label = '$\Im$ %s' % label, **kwargs))
	return plots


def field():
	"""
		Plot a 2D matrix as a grayscale intensity map, optionally with gradient vectors
	"""
	#todo: implement
	#todo: check if name unique
	#todo: normal x- and y-axis for imshow
	#todo: default black-and-white colormap
	#todo: numpy.gradient has unexpected directions compared to pyplot.quiver
	#todo: gradient vectors should be toggleable
	#todo: pass-on arguments, including interpolation
	#todo: intensity map optional (just quiver)
	#todo: be able to reduce number of arrows (skip or interpolate)
	#todo: add this to MPL axes objects
	pass


