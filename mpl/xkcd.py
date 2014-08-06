
'''
	XKCD version of Matplotlib
'''

from bardeen.mpl.base import *


'''
	Singleton class that keeps track of figures
'''
class xkcdMPL(BaseMPL):

	def __init__(self, save_all = False, extension = 'png', directory = '.'):
		super(xkcdMPL, self).__init__(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.usetex'] = False
		matplotlib.pyplot.xkcd()

	def default_font_properties(self):
		return {}


def figure(*args, **kwargs):
	return xkcdMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
	return xkcdMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
	return xkcdMPL.instance().show(*args, **kwargs)

def close(*args, **kwargs):
	return xkcdMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
	xkcdMPL.instance().order(*args, **kwargs)