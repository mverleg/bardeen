
"""
	utility methods for storing and retrieving data structures
"""

from numpy import save, load, savetxt, loadtxt, float64
from json import dumps, loads
import gzip
from os.path import dirname
from bardeen.system import mkdirp


"""
	numpy arrays
"""


def store_array(arr, filename, header = ''):
	"""
		Store a numpy array in a format readable by many programs
		(whitespace delimitered plain text with # header)

		:param arr: numpy array
		:param filename: (string) path to store the file; directory is created if it does not exist
	"""
	mkdirp(dirname(filename))
	if 'int' in unicode(arr.dtype):
		fmt = '%18d'
	else:
		fmt = '%.18e'
	savetxt(filename, arr, fmt = fmt, delimiter = '\t', newline = '\n', header = header)


def load_array(filename, dtype = float64, delimiter = '\t'):
	"""
		Load a tab-delimitered array, e.g. as stored by :ref: store_array
	"""
	return loadtxt(filename, dtype = dtype, delimiter = delimiter)


def store_array_bin(arr, filename):
	"""
		Store as binary, single-array numpy file

		:param arr: numpy array
		:param filename: (string) path to store the file; directory is created if it does not exist

		extension .npy is strongly recommended
	"""
	#todo: maybe gzip later
	mkdirp(dirname(filename))
	save(filename, arr)


def load_array_bin(filename):
	"""
		Load a binary, single-array numpy file
	"""
	return load(filename)


"""
	dictionaries
"""


def store_conf(dicti, filename, header = None):
	"""
		Store a python dictionary with simple int, float, unicode elements
		as a easily readable config file.

		:param dicti: (dict) dictionary to store; keys (config options) are not allowed to contain whitespace
		:param filename: (string) path to store the file; directory is created if it does not exist
		:param header: (string/None) if string, added at the beginning of the file

		* ``None`` is allowed for values but not keys
		* Note that floats will be slightly different when loaded
		* Note that string '0123' will be loaded as integer 123
	"""
	mkdirp(dirname(filename))
	with open(filename, 'w+') as fh:
		for line in header.splitlines():
			fh.write('# %s\n' % line)
		for key, value in dicti.items():
			if isinstance(key, basestring):
				if ' ' in key or '\t' in key or '\n' in key or '\r' in key:
					raise KeyError('config dict can not be stored if keys contain whitespace')
			else:
				try:
					float(key)
				except:
					raise KeyError('key %s is not a string or number' % key)
			if isinstance(value, basestring):
				if '\n' in value or '\r' in value:
					raise ValueError('config dict can not be stored if values contain newlines')
			else:
				try:
					float(value)
				except:
					raise KeyError('value %s is not a string or number' % value)
			fh.write('%s\t%s\n' % (
				key,
				value,
			))


def load_conf(filename):
	"""
		Load a whitespace-delimitered config file, e.g. as stored by :ref: store_conf.
	"""
	with open(filename, 'r') as fh:
		dicti = {}
		''' http://stackoverflow.com/questions/15233340/getting-rid-of-n-when-using-readlines '''
		for nr, line in enumerate(fh.read().splitlines()):
			if not line.startswith('#'):
				try:
					raw_key, raw_value = line.split(None, 1)
				except ValueError:
					raise ValueError('config file %s inproperly configured in line %d: no delimiter whitespace (make sure comments start with #)' % (filename, nr))
				try:
					key = int(raw_key)
				except ValueError:
					try:
						key = float(raw_key)
					except ValueError:
						key = unicode(raw_key)
				try:
					value = int(raw_value)
				except ValueError:
					try:
						value = float(raw_value)
					except ValueError:
						value = unicode(raw_value)
				dicti[key] = value
	return dicti


def store_dict(dicti, filename, compressed = False):
	"""
		Store a dictionary as json.

		:param dicti: (dict) dictionary to store
		:param filename: (string) path to store the file; .gz is appended if compressed; directory is created if it does not exist
		:param compressed: if True, the file is gzipped and .gz is appended to the filename

		* Contrary to :ref: store_conf, whitespace in keys is allowed
		* See notes at :ref: store_conf
	"""
	mkdirp(dirname(filename))
	# todo: questionable whether the appending of .gz is a good idea; expect `filename` to be the actual filename
	""" http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module """
	if compressed:
		filename = '%s.gz' % filename
		fh = gzip.open(filename, 'wb+')
		jsn = dumps(dicti, indent = None)
	else:
		fh = open(filename, 'w+')
		jsn = dumps(dicti, indent = 4)
	fh.write(jsn)
	fh.close()


def load_dict(filename, compressed = False):
	"""
		Load a json dictionary file, such as created by :ref: store_dict.

		If compressed is True and the file does not end in .gz, it is automatically appended
		(since store_dict appends it).
	"""
	if compressed:
		if not filename.endswith('.gz'):
			filename = '%s.gz' % filename
		fh = gzip.open(filename, 'rb')
	else:
		fh = open(filename, 'r')
	dicti = loads(fh.read())
	fh.close()
	return dicti


