
'''
	Order for a MPL figure
'''


class MPLorder(object):
	"""
		Tells MyMPL to save a figure with matching label using these details
	"""

	max_width = 6.17    # inch
	dpi = 400
	font_name = 'crm10'
	font_size = 10.0    # pt
	font_weight = 'normal'
	font_style =  'italic'

	''' the kwargs should be a subset of the properties defined above '''
	def __init__(self, label, filename, **kwargs):
		self.label = label
		self.filename = filename
		self.figure = None
		for kwkey, kwvalue in kwargs.items():
			setattr(self, kwkey, kwvalue)

	font_properties = {
		'family': font_name,
		'size':   font_size,
		'weight': font_weight,
		'style':  font_style,
	}


