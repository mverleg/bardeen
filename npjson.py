
"""
	Saving and loading of json data that includes numpy ndarrays.
"""

from collections import OrderedDict
from gzip import GzipFile
from numpy import ndarray, zeros, asarray
from json import dump, load, JSONEncoder


class NumpyEncoder(JSONEncoder):
	def default(self, obj):
		"""
			If input object is a ndarray it will be converted into a dict holding dtype, shape and the data base64 encoded.
		"""
		if isinstance(obj, ndarray):
			return dict(__ndarray__ = obj.tolist(), dtype = str(obj.dtype), shape = obj.shape)
		return JSONEncoder(self, obj)


def json_numpy_obj_hook(dct):
	"""
		Decodes a previously encoded numpy ndarray
		with proper shape and dtype

		:param dct: (dict) json encoded ndarray
		:return: (ndarray) if input was an encoded ndarray
	"""
	if isinstance(dct, dict) and '__ndarray__' in dct:
		return asarray(dct['__ndarray__'], dtype = dct['dtype'])#.reshape(dct['shape'])
	return dct


#todo: should now preserve order of keys; untested
def npdump(obj, filepath, compresslevel = 5, **jsonkwargs):
	with open(filepath, 'w+') as fh:
		with GzipFile(fileobj = fh, mode = 'w+', compresslevel = compresslevel) as zh:
			dump(obj = obj, fp = zh, cls = NumpyEncoder, sort_keys = False, **jsonkwargs)


#todo: should now preserve order of keys; untested
def npload(filepath, **jsonkwargs):
	with open(filepath, 'r') as fh:
		with GzipFile(fileobj = fh, mode = 'r') as zh:
			obj = load(fp = zh, object_pairs_hook = OrderedDict, object_hook = json_numpy_obj_hook, **jsonkwargs)
	return obj


if __name__ == '__main__':
	#todo: write unit tests
	z = {'data': [zeros((5, 3)), zeros(4, 2)]}
	with open('/tmp/trial.json', 'w+') as fh:
		npdump(z, fh)
	with open('/tmp/trial.json', 'r') as fh:
		z = npload(fh)



