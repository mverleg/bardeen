
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
	* to use the xkcd version of matplotlib, create mpl as MPL.xkcd() the first time (e.g. collection script)
"""

from itertools import cycle
from re import search
from os.path import join
import matplotlib
from types import MethodType, StringTypes
from collections import defaultdict
from bardeen.mpl.mpl_order import MPLorder
from bardeen.mpl.mpl_ax import boynton_colors, color_cycle_scatter, small_pad_xlabel, small_pad_ylabel, plotim
from matplotlib.pyplot import subplots as mpl_subplots, figure as mpl_figure, show as mpl_show, close as mpl_close
from numpy import array, concatenate, ndarray


class MPL(object):
	"""
		Singleton class that keeps track of figures and allows to save them automatically by label.

		Methods :method:figure can also be imported directly

		>>> from mpl import figure, subplots, show, order, close
	"""

	''' max_width, overriden by order if there is one '''
	max_width = 6.17

	def __init__(self, save_all = False, extension = 'png', directory = '.'):
		"""
			Initialize the mpl class with some settings for saving figures.

			:param save_all: (bool) if changed to True, all figures are saved
			:param extension: (str) extension or (list) of extensions which will be used for saving
			:param directory: (str) directory to save figures
		"""

		''' operation settings '''
		self.save_all = save_all
		self.directory = directory
		if isinstance(extension, StringTypes):
			self.default_extension = [extension]
		else:
			self.default_extension = extension

		''' pgf backend settings '''
		matplotlib.rcParams['text.latex.unicode'] = True
		#matplotlib.rcParams['text.usetex'] = True
		matplotlib.rcParams['pgf.texsystem'] = 'pdflatex'

		''' register single instance '''
		try:
			self.__class__.single_instance
		except AttributeError:
			''' no instance yet; good! '''
			self.__class__.single_instance = self
		else:
			''' an instance already exists! '''
			raise Exception('%s already has an instance!' % self.__class__)
		''' initial variables '''
		self.all_figures = []
		self.orders = defaultdict(list)

		""" no special font properties """
		self.__class__.default_font_properties = {}

	@classmethod
	def xkcd(cls, save_all = False, extension = 'png', directory = '.'):
		"""
			alternative constructor with xkcd display settings
		"""
		cls.default_font_properties = {}
		cls(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.usetex'] = False
		matplotlib.pyplot.xkcd()

	@classmethod
	def tex(cls, save_all = False, extension = 'png', directory = '.'):
		"""
			alternative constructor with latex display settings
		"""
		cls.default_font_properties = {
			'family': 'cmr10',
			'size': 10.0,
			'weight': 'normal',
			'style': 'normal',
		}
		cls(save_all = save_all, extension = extension, directory = directory)
		matplotlib.rcParams['text.usetex'] = True

	@classmethod
	def instance(cls, *args, **kwargs):
		"""
			Get the singleton instance.
		"""
		try:
			cls.single_instance
		except AttributeError:
			cls.single_instance = cls(*args, **kwargs)
		return cls.single_instance

	def subplots(self, ver = 1, hor = 1, label = None, figsize = (None, None), tight_layout = True, show_toolbar = False, total = None, dpi = 120, save_dpi = 300, **kwargs):
		"""
			Improved subplots function.

			Figures can be saved automatically using :ref: order before generating them.

			Changes figure size and dpi to easily such that figures can fit perfectly into LaTeX documents.

			Many default display parameters changed incl tight layout by default, supply total figures without order,
			turn toolbar off.

			:param ver: (int) number of vertical subplots (overriden if :ref: total is set)
			:param hor: (int) number of horizontal subplots (overriden if :ref: total is set)
			:param label: (str) label (name) for this image, used for title, for saving and for finding orders
			:param figsize: (tuple of two ints) dimensions of the image
			:param tight_layout: (bool) as usual, but default is True
			:param show_toolbar: (bool) if changed to True, shows toolbar
			:param total: (int/None) total number of figures, overrides hor/ver if set (will be N x N or N x N-1)
			:param dpi: (int) dpi of the figure when displaying
			:param save_dpi: (int) dpi of the figure when saving
			:param kwargs: passed directly to :ref: matplotlib.subplots
			:return: *contrary to original :ref: matplotlib.subplots*, this returns a list of *non-nested* axis objects
		"""
		''' create tiles if total set '''
		if total is not None:
			hor = ver = int(total ** 0.5)
			if hor * ver < total:
				hor += 1
			if hor * ver < total:
				ver += 1
		''' if this figure has been ordered, change a few properties '''
		if label is None:
			label = 'fig_%d' % len(self.all_figures)
		max_width = self.max_width
		font_properties = self.default_font_properties
		if label in self.orders.keys():
			for order in self.orders[label]:
				''' change font properties everywhere '''
				font_properties = order.font_properties
				max_width = order.max_width
				''' change dpi '''
				save_dpi = order.dpi
		''' change font properties everywhere '''
		matplotlib.rc('font', **font_properties)
		if figsize[0] is None:
			''' default figure size is 'maximal' '''
			figsize = (max_width, 0.75 * max_width)
		elif figsize[0] > max_width:
			''' scale down figure if too large '''
			scale = max_width / figsize[0]
			figsize = (max_width, scale * figsize[1])
		disp_dpi = dpi
		''' hide toolbar unless otherwise specified '''
		if not show_toolbar:
			matplotlib.rcParams['toolbar'] = 'None'
		''' fix a bug with minus sign not showing '''
		matplotlib.rcParams['axes.unicode_minus'] = False
		''' change the default color cycle '''
		matplotlib.rcParams['axes.color_cycle'] = boynton_colors
		''' change legend to make it smaller '''
		matplotlib.rcParams['legend.labelspacing'] = .2
		matplotlib.rcParams['legend.borderpad'] = 0.3
		''' the actual figure '''
		if hor <= 0 or ver <= 0:
			''' create empty figure if no subplots requested '''
			fig = mpl_figure(figsize = figsize, dpi = disp_dpi, **kwargs)
			axi = array([])
		else:
			''' create the requested subplots '''
			fig, axi = mpl_subplots(ver, hor, figsize = figsize, dpi = disp_dpi, **kwargs)
			''' tight layout unless otherwise specified '''
			if tight_layout:
				fig.tight_layout(rect = [.045, .03, 1., 1.], pad = .1, w_pad = 2., h_pad = 1.)
			''' merge axi into one list instead of sublists '''
			try:
				axi = concatenate(axi)
			except ValueError:
				''' axi is already one list (hor = 1 probably) '''
			except TypeError:
				''' axi is a single object (hor = ver = 1 probably) '''
			''' remove extra axi if 'total' used '''
			if total is not None and total != 1:
				for ax in axi[total:]:
					ax.axis('off')
				axi = axi[:total]
		''' store dpi for saving '''
		fig.save_dpi = save_dpi
		''' override ax.methods '''
		for ax in (axi if isinstance(axi, ndarray) else [axi]):
			''' override scatter to use color cycle '''
			ax.custom_color_cycle = cycle(boynton_colors)
			ax.mono_color_scatter = ax.scatter
			ax.scatter = MethodType(color_cycle_scatter, ax, ax.__class__)
			''' special complex number version of plot '''
			ax.plotim = MethodType(plotim, ax, ax.__class__)
			''' label distances '''
			ax.big_pad_xlabel = ax.set_xlabel
			ax.set_xlabel = MethodType(small_pad_xlabel, ax, ax.__class__)
			ax.big_pad_ylabel = ax.set_ylabel
			ax.set_ylabel = MethodType(small_pad_ylabel, ax, ax.__class__)
		''' change some things if this image was ordered '''
		fig.label = label
		for order in self.orders[label]:
			order.figure = fig
		fig.canvas.set_window_title(label)
		''' store figure reference '''
		self.all_figures.append(fig)
		''' return '''
		return (fig, axi) if axi is not None else fig

	def figure(self, *args, **kwargs):
		"""
			Improved figure function; simply calls :ref:subplots.
		"""
		return self.subplots(ver = 0, hor = 0, *args, **kwargs)[0]

	def show(self, callbacks = [], close_immediately = False, *args, **kwargs):
		"""
			Improved show function.

			You can pass callbacks to call after showing, to have sort of 'non-blocking' behaviour
			use functools.partial if you want to supply any arguments.
		"""
		for fig in self.all_figures:
			''' save the figure if it has been ordered '''
			filenames = []
			if len(self.orders[fig.label]):
				''' has this figure been ordered? '''
				for order in self.orders[fig.label]:
					if search('^(.*[^\./])\.\w+$', order.filename):
						''' already has an extension '''
						filenames.append(order.filename)
					else:
						''' no extension; add all '''
						filenames.extend('%s.%s' % (order.filename, extension) for extension in self.default_extension)
				''' order fulfilled; remove it '''
				del self.orders[fig.label]
			elif self.save_all:
				''' there is no filename (just a label), so add all extensions to that and treat it like a filename '''
				filenames.extend('%s.%s' % (fig.label, extension) for extension in self.default_extension)
			if filenames:
				print 'saving \'%s\' as %s' % (fig.label, ', '.join('\'%s\'' % filename for filename in filenames))
			for filename in filenames:
				filename = join(self.directory, filename)
				fig.savefig(filename, dpi = fig.save_dpi)
		for fig in self.all_figures:
			''' attach the on-close handles to close all other figures too '''
			fig.canvas.mpl_connect('close_event', self.close_all)
			''' close immediately if close is requested '''
			if close_immediately:
				fig.canvas.mpl_connect('draw_event', self.close_all)
			''' show the figure '''
			fig.show(*args, **kwargs)
		''' any unsaved figures? '''
		remaining_orders = sum(self.orders.values(), [])
		if len(remaining_orders):
			print 'there are %d unsaved orders! figures were not found for:' % len(remaining_orders)
			for order in remaining_orders:
				print '\'%s\' (\'%s\')' % (order.label, order.filename)
		''' show all figures to prevent error '''
		mpl_show()

	def close(self, callbacks = [], *args, **kwargs):
		self.show(callbacks = callbacks, close_immediately = True, *args, **kwargs)

	def order(self, label, filename = None, **kwargs):
		"""
			Tell MPL to save a figure if it occurs in the future.
		"""
		if filename is None:
			filename = label
		self.orders[label].append(MPLorder(label, filename, **kwargs))

	@classmethod
	def close_all(cls, event):
		for fig in cls.instance().all_figures:
			mpl_close(fig)
		cls.instance().all_figures = []


