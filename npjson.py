
"""
	From: http://stackoverflow.com/questions/3488934/simplejson-and-numpy-array/24375113#24375113
"""

from functools import partial
from numpy import ndarray, frombuffer, zeros
from json import dump, load, JSONEncoder
from base64 import b64encode, b64decode


class NumpyEncoder(JSONEncoder):
	def default(self, obj):
		"""
			If input object is a ndarray it will be converted into a dict holding dtype, shape and the data base64 encoded.
		"""
		if isinstance(obj, ndarray):
			data_b64 = b64encode(obj.data)
			return dict(__ndarray__ = data_b64, dtype = str(obj.dtype), shape = obj.shape)
		return JSONEncoder(self, obj)


def json_numpy_obj_hook(dct):
	"""
		Decodes a previously encoded numpy ndarray
		with proper shape and dtype
		:param dct: (dict) json encoded ndarray
		:return: (ndarray) if input was an encoded ndarray
	"""
	if isinstance(dct, dict) and '__ndarray__' in dct:
		data = b64decode(dct['__ndarray__'])
		return frombuffer(data, dct['dtype']).reshape(dct['shape'])
	return dct


npdump = partial(dump, cls = NumpyEncoder)
mpload = partial(load, object_hook = json_numpy_obj_hook)


if __name__ == '__main__':
	#todo: write unit tests
	z = {'data': [zeros((5, 3)), zeros(4, 2)]}
	with open('/tmp/trial.json', 'w+') as fh:
		dump(z, fh, cls = NumpyEncoder)
	with open('/tmp/trial.json', 'r') as fh:
		z = load(fh, object_hook = json_numpy_obj_hook)


