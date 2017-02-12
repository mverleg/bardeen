
"""
	unit tests for bardeen.storage
	tmpdir is automatically an empty temporary directory
	http://stackoverflow.com/questions/4199700/python-how-do-i-make-temporary-files-in-my-test-suite
"""

from os.path import join
from random import random
from bardeen.testutils import dict_round_floats
from bardeen.storage import store_array, load_array, store_array_bin, \
	load_array_bin, store_conf, load_conf, store_dict, load_dict
from numpy import array_equal, float64, exp, complex128
from numpy.random import rand, randint
from bardeen.testutils import get_random_word as rword, get_random_string as rstr


"""
	numpy arrays
"""


def store_load_array(tmpdir, original, header = '', load_dtype = float64):
	filename = join(unicode(tmpdir), '%s_%s.txt' % (unicode(original.dtype), 'x'.join(str(d) for d in original.shape)))
	store_array(original, filename, header = header)
	loaded = load_array(filename, dtype = load_dtype)
	assert array_equal(original, loaded)


def store_load_array_bin(tmpdir, original):
	filename = join(unicode(tmpdir), '%s_%s.npy' % (unicode(original.dtype), 'x'.join(str(d) for d in original.shape)))
	store_array_bin(original, filename)
	loaded = load_array_bin(filename)
	assert array_equal(original, loaded)


def test_float_array(tmpdir):
	original = rand(10, 15)
	store_load_array(tmpdir, original, header = 'random data columns')
	store_load_array_bin(tmpdir, original)


def test_int_array(tmpdir):
	original = randint(low = -4, high = 17, size = (10, 15))
	store_load_array(tmpdir, original, load_dtype = original.dtype)
	store_load_array_bin(tmpdir, original)


def test_complex_array(tmpdir):
	original = 100 * rand(10, 15) * exp(1j * rand(10, 15))
	store_load_array(tmpdir, original, header = '#complex numbers!!', load_dtype = complex128)
	store_load_array_bin(tmpdir, original)


"""
	dictionaries
"""

FLOAT_PREC = 8


def store_load_conf(tmpdir, original, header = ''):
	filename = join(unicode(tmpdir), 'test.conf')
	store_conf(original, filename, header = header)
	loaded = load_conf(filename)
	assert dict_round_floats(original, FLOAT_PREC) == dict_round_floats(loaded, FLOAT_PREC)


def store_load_dict(tmpdir, original):
	filename = join(unicode(tmpdir), 'test.conf')
	store_dict(original, filename)
	loaded = load_dict(filename)
	assert dict_round_floats(original, FLOAT_PREC) == dict_round_floats(loaded, FLOAT_PREC)


def store_load_dict_compressed(tmpdir, original):
	filename = join(unicode(tmpdir), 'test.conf')
	store_dict(original, filename, compressed = True)
	loaded = load_dict(filename, compressed = True)
	assert dict_round_floats(original, FLOAT_PREC) == dict_round_floats(loaded, FLOAT_PREC)


def test_mixed_dict(tmpdir):
	for N in range(50):
		dicti = {
			rstr(): rstr(),
			randint(-1e7, 1e7): randint(-1e7, 1e7),
			1e8 * random(): 1e8 * random(),
			rstr(): 1e8 * random(),
			randint(-1e7, 1e7): rstr(),
			1e8 * random(): randint(-1e7, 1e7),
			rstr(): None,
		}
		store_load_dict(tmpdir, dicti)
		store_load_dict_compressed(tmpdir, dicti)


def test_conf_dict(tmpdir):
	for N in range(50):
		dicti = {
			rword(): rstr(),
			randint(-1e7, 1e7): randint(-1e7, 1e7),
			1e8 * random(): 1e8 * random(),
			rword(): rstr(),
			rword(): randint(-1e7, 1e7),
			rword(): 1e8 * random(),
		}
		store_load_conf(tmpdir, dicti, header = '#test')
		dicti['hello world'] = 7
		try:
			store_load_conf(tmpdir, dicti, header = '#test')
		except KeyError:
			''' a key error should be thrown, as a space in a key would lead to inconsistent loading '''
		else:
			raise AssertionError('a key error should be thrown, as a space in a key would lead to inconsistent loading, but no error was thrown')
		del dicti['hello world']
		dicti['hello_world'] = '7\n'
		try:
			store_load_conf(tmpdir, dicti, header = '#test')
		except ValueError:
			''' a value error should be thrown, as a newline in a value would lead to inconsistent loading '''
		else:
			raise AssertionError('a value error should be thrown, as a newline in a value would lead to inconsistent loading, but no error was thrown')


