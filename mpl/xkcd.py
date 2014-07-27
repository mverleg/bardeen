
'''
	XKCD version of Matplotlib
'''

from bardeen.mpl.base import *


'''
	Singleton class that keeps track of figures
'''
class MyMPL(BaseMPL):

	def __init__(self, save_all = False, extension = 'png', directory = '.'):
		super(MyMPL, self).__init__(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.usetex'] = False
		matplotlib.pyplot.xkcd()

	def default_font_properties(self):
		return {}


def figure(*args, **kwargs):
	return MyMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
	return MyMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
	return MyMPL.instance().show(*args, **kwargs)

def close(*args, **kwargs):
	return MyMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
	MyMPL.instance().order(*args, **kwargs)