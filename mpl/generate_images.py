
'''
    use MyMPL class to save figures for use in reports
    function should:
    - import subplots & show from mympl
    - preferably use 'label' argument to subplots that are to be saved
        (otherwise numbers can be used, but that is sensitive to change)
    - call show() in __main__ (so it's not used when imported)
'''

import sys
from sys import argv
from plot.mympl import MyMPL
#from settings import temp_dir, image_dir
from coordinates.raw_data import conv_raw_data
from fitting.visualize_results import bar_error_minima
from jobs.settings_fann import settings_fann
from tempfile import mkstemp

''' initialize '''
directory = argv[1] if len(argv) > 1 else '.' #image_dir
mympl = MyMPL.instance(extension = 'pgf', directory = directory, save_all = True)
properties =  {
    'max_width': 6.17,
    'dpi': 600,
    'font_name': 'cmr10',
    'font_size': 10.0,
    'font_weight': 'normal',
    'font_style': 'normal',
}

'''  stdout reirected to /tmp; (to print, use print >> old_stdout, 'your message') '''
fh, name = mkstemp(suffix='.out')
print 'redirected stdout to %s/img_gen.out; please wait patiently' % name
old_stdout, sys.stdout = sys.stdout, fh

''' order the images and call the functions that generate them '''
mympl.order(label = 'EvsR_filtered_data', **properties)
conv_raw_data(display = True)

mympl.order(label = 'fann_settings_compare', **properties)
queue = settings_fann()
jobs, results = queue.get_jobs(), queue.result().values()
bar_error_minima(jobs, results, label = 'fann_settings_compare')


''' restore output  '''
sys.stdout = old_stdout

print 'all the figures will be opened and immediately closed; please ignore these'
mympl.close()



""" #todo: old, remove
    mympl.order(label = 'modulopolate_3', filename = 'modulopolate', **properties)
    show_modulopolate(*calc_modulopolate())
    
    mympl.order(label = 'boundary_problem', **properties)
    mympl.order(label = 'boundary_fix_attempt', **properties)
    raise Exception('below data and network needs to be updated')
    pes_continuity(label = 'boundary_problem', pes_file = '../data/filtered_random.dnet')
    pes_continuity(label = 'boundary_fix_attempt', pes_file = '../data/modulo.dnet')
    
    mympl.order(label = 'settings_fann_bar', **properties)
    bar_error_minima(jobs = settings_fann().get_jobs(), label = 'settings_fann_bar')
    
    mympl.order(label = 'gradient_map_yz', filename = 'show_gradient', **properties)
    show_gradient_frame()
    
    mympl.order(label = 'dih_degeneracy_bad', **properties)
    special_angles()
    
    mympl.order(label = 'pes_EvsR', **properties)
    mympl.order(label = 'pes_ang_surf', **properties)
    inter_pes_EvsR()
    inter_pes_ang_surf()
"""


