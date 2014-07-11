
'''
    order for a MPL figure
'''


'''
    Tells MyMPL to save a figure with matching label using these details
'''
class MPLorder(object):
    
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
    
    def font_properties(self):
        return {
            'family': self.font_name,
            'size'  : self.font_size,
            'weight': self.font_weight,
            'style' : self.font_style,
        }


