
'''
	defines a special LaTeX version of mpl
'''

from bardeen.mpl.base import *


class NoTexMPL(BaseMPL):
	"""
		Version of mpl class, which sets some properties for LaTeX compatibility
	"""

	def __init__(self, save_all = False, extension = 'png', directory = '.'):
		super(NoTexMPL, self).__init__(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.latex.unicode'] = False
		matplotlib.rcParams['text.usetex'] = False
		matplotlib.rcParams['pgf.texsystem'] = 'pdflatex'

	def default_font_properties(self):
		return {
			'family': 'cmr10',
			'size': 10.0,
			'weight': 'normal',
			'style': 'normal',
		}


def figure(*args, **kwargs):
	return NoTexMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
	return NoTexMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
	return NoTexMPL.instance().show(*args, **kwargs)

def close(*args, **kwargs):
	return NoTexMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
	NoTexMPL.instance().order(*args, **kwargs)


