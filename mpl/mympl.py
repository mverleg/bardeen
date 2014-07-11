
'''
	change matplotlib plotting functions a little to make saving 
	images easier and fix minor nuicances
	- subplots returns one list of axis objects rather than a list of lists
	- closing one figure will close all the figures
	- make tight layout the default
	!! saving stuff
'''

from mpl.base import *


'''
	Singleton class that keeps track of figures
'''
class MyMPL(BaseMPL):
	
	def __init__(self, save_all = False, extension = 'png', directory = '.'):
		super(MyMPL, self).__init__(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.usetex'] = True
	
	def default_font_properties(self):
		return {
			'family': 'cmr10',
			'size': 10.0,
			'weight': 'normal',
			'style': 'normal',
		}


''' non-class version like the normal MPL '''
def figure(*args, **kwargs):
	return MyMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
	return MyMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
	return MyMPL.instance().show(*args, **kwargs)

''' opens and immediately closes figures; use instead of show (if already open use close_all) '''
def close(*args, **kwargs):
	return MyMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
	MyMPL.instance().order(*args, **kwargs)


