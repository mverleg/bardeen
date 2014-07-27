
'''
	change matplotlib plotting functions a little to make saving
	images easier and fix minor nuicances
	- subplots returns one list of axis objects rather than a list of lists
	- closing one figure will close all the figures
	- make tight layout the default
	!! saving stuff
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


