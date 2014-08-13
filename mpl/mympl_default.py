
'''
	defines a special LaTeX version of mpl
'''

from bardeen.mpl.base import *


class MyMPL(BaseMPL):
	"""
		Version of mpl class, which sets some properties for LaTeX compatibility
	"""

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


