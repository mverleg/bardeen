
from json import dumps, loads, encoder
import gzip


'''
	store a python dictionary with simple int, float, unicode elements
	as a easily readable config file
	dict keys (config optinos) are not allowed to contain whitespace
	- note that string '0123' will be loaded as integer 123
'''
def store_conf(dicti, filename, header = None):
	with open(filename, 'w+') as fh:
		for line in header.split('\n'):
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

'''
	load a whitespace-delimitered config file, e.g. as stored by store_conf
'''
def load_conf(filename):
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

'''
	store a dictionary as json
	if compress then the file is gzipped and .gz is appended to the filename
	- None is allowed for values but not keys
	- note that floats will be slightly different when loaded
'''
def store_dict(dicti, filename, compressed = False):
	''' http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module '''
	if compressed:
		filename = '%s.gz' % filename
		fh = gzip.open(filename, 'wb+')
		jsn = dumps(dicti, indent = None)
	else:
		fh = open(filename, 'w+')
		jsn = dumps(dicti, indent = 4)
	fh.write(jsn)
	fh.close()

'''
	load a binary, single-array numpy file
'''
def load_dict(filename, compressed = False):
	if compressed:
		if not filename.endswith('.gz'):
			filename = '%s.gz' % filename
		fh = gzip.open(filename, 'rb')
	else:
		fh = open(filename, 'r')
	dicti = loads(fh.read())
	fh.close()
	return dicti


