
from numpy import save, load, savetxt, loadtxt, float64


'''
	store a numpy array in a format readable by many programs 
	(whitespace delimitered plain text with # header)
'''
def store_array(arr, filename, header = ''):
	if 'int' in unicode(arr.dtype):
		fmt = '%18d'
	else:
		fmt = '%.18e'
	savetxt(filename, arr, fmt = fmt, delimiter = '\t', newline = '\n', header = header)

'''
	load a tab-delimitered array, e.g. as stored by store_array
'''
def load_array(filename, dtype = float64):
	return loadtxt(filename, dtype = dtype, delimiter = '\t')

'''
	store as binary, single-array numpy file
	extension .npy is strongly recommended
'''
def store_array_bin(arr, filename):
	#todo: maybe gzip later
	save(filename, arr)

'''
	load a binary, single-array numpy file
'''
def load_array_bin(filename):
	return load(filename)


