
"""
	An extension for matplotlib which adds many miscellaneous pieces of functionality. The main purpose is to
	integrate well with LaTeX, allowing figures to be exported with the correct fonts, display settings and
	dimensions to fit into LaTeX documents perfectly.

	>>> from mpl import subplots, show

	Functionality includes:

	* use :ref: order to mark a figure to be saved automatically as it's shown
	* provide only the total number of subplots, and get a list result
	* change some default settings, e.g. turn tight_layout on and toolbar off
	* closing one figure will close all figures automatically
	* ``ax.plotim`` plots the real, imaginary and absolute of a complex function
	* callbacks for show(), to have non-blocking behaviour
	* automatically cycles through high-contrast colors when plotting multiple lines
	* various positioning and axis parameters

	Please note that:

	* some function signatures are changed for this version.
#	* the xkcd version of matplotlib is available by creating the mpl class from the .xkcd module.
#
#	>>> from mpl.xkcd import subplots, show
"""

#todo: import mpl.xkcd gives an xkcd instance

from mpl import MPL


__all__ = ['MyMPL', 'figure', 'subplots', 'show', 'close', 'order']


def figure(*args, **kwargs):
	return MPL.instance().figure(*args, **kwargs)


def subplots(*args, **kwargs):
	return MPL.instance().subplots(*args, **kwargs)


def show(*args, **kwargs):
	return MPL.instance().show(*args, **kwargs)


def close(*args, **kwargs):
	return MPL.instance().close(*args, **kwargs)


def order(*args, **kwargs):
	MPL.instance().order(*args, **kwargs)
