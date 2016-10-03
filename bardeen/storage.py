
"""
Utility methods for storing and retrieving data structures.
"""

from genericpath import getmtime
from time import time
from numpy import save, load, savetxt, loadtxt, float64
from json import dumps, loads
import gzip
from os.path import dirname
from bardeen.system import mkdirp
from collections import Mapping
from os.path import exists


"""
	General
"""


class EOAgeError(IOError):
	""" The file is older than the provided maximum age. """


def fail_if_too_old(filename, max_age = None):
	if not exists(filename):
		raise IOError('file "%s" could not be found' % filename)
	if max_age is not None:
		if time() - getmtime(filename) > max_age:
			raise EOAgeError('file "%s" could not be loaded because it is %ds old, which is more than the maximum age %ds.' % (filename, time() - getmtime(filename), max_age))


"""
	Strings
"""
#todo: unit tests for strings
#todo: unit tests for all max age


def store_str(string, filename, compressed = False):
	"""
	Store a string to a file.
	"""
	mkdirp(dirname(filename))
	if compressed:
		fh = gzip.open(filename, 'w+')
	else:
		fh = open(filename, 'w+')
	fh.write(string)
	fh.close()


def load_str(filename, max_age = None, compressed = False):
	"""
	Load a string from a file.
	"""
	fail_if_too_old(filename, max_age)
	if compressed:
		fh = gzip.open(filename, 'r')
	else:
		fh = open(filename, 'r')
	string = fh.read()
	fh.close()
	return string


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


def load_array(filename, dtype = float64, delimiter = '\t', max_age = None):
	"""
	Load a tab-delimitered array, e.g. as stored by :ref: store_array

	:param filename: (string) path to the file
	:param max_age: (None or number in seconds) if set, file will only be loaded if the file is newer than max_age

	:raises IOError: raied if file can't be opened
	:raises IOAgeError: subclass of IOError, raised if file exists but is older than max_age
	"""
	fail_if_too_old(filename, max_age)
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


def load_array_bin(filename, max_age = None):
	"""
	Load a binary, single-array numpy file

	:param filename: (string) path to the file
	:param max_age: (None or number in seconds) if set, file will only be loaded if the file is newer than max_age

	:raises IOError: raied if file can't be opened
	:raises IOAgeError: subclass of IOError, raised if file exists but is older than max_age
	"""
	fail_if_too_old(filename, max_age)
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
	assert isinstance(dicti, Mapping), 'argument is not a dictonary-like object'
	mkdirp(dirname(filename))
	with open(filename, 'w+') as fh:
		if header:
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


def load_conf(filename, max_age = None):
	"""
	Load a whitespace-delimitered config file, e.g. as stored by :ref: store_conf.

	:param filename: (string) path to the file
	:param max_age: (None or number in seconds) if set, file will only be loaded if the file is newer than max_age

	:raises IOError: raied if file can't be opened
	:raises IOAgeError: subclass of IOError, raised if file exists but is older than max_age
	"""
	fail_if_too_old(filename, max_age)
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
	assert isinstance(dicti, Mapping), 'argument is not a dictonary-like object'
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


def load_dict(filename, compressed = False, max_age = None):
	"""
	Load a json dictionary file, such as created by :ref: store_dict.

	If compressed is True and the file does not end in .gz, it is automatically appended
	(since store_dict appends it).

	:param filename: (string) path to the file
	:param max_age: (None or number in seconds) if set, file will only be loaded if the file is newer than max_age

	:raises IOError: raied by open() if file can't be opened
	:raises IOAgeError: subclass of IOError, raised if file exists but is older than max_age
	"""
	fail_if_too_old(filename, max_age)
	if compressed:
		if not filename.endswith('.gz'):
			filename = '%s.gz' % filename
		fh = gzip.open(filename, 'rb')
	else:
		fh = open(filename, 'r')
	dicti = loads(fh.read())
	fh.close()
	return dicti


