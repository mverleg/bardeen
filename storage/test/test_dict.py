
import string
from os.path import join
from random import sample, randint, random
from storage.dict import store_conf, load_conf, store_dict, load_dict
from testing.comparison import dict_round_floats


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
	def get_word():
		return unicode(''.join(sample(string.printable, randint(2, 32))))
	dicti = {
		get_word(): get_word(),
		randint(-1e7, 1e7): randint(-1e7, 1e7),
		1e8 * random(): 1e8 * random(),
		get_word(): 1e8 * random(),
		randint(-1e7, 1e7): get_word(),
		1e8 * random(): randint(-1e7, 1e7),
		get_word(): None,
	}
	store_load_dict(tmpdir, dicti)
	store_load_dict_compressed(tmpdir, dicti)

def test_conf_dict(tmpdir):
	def get_word():
		return unicode(''.join(sample(string.letters + string.digits, randint(2, 32))))	
	dicti = {
		get_word(): get_word(),
		randint(-1e7, 1e7): randint(-1e7, 1e7),
		1e8 * random(): 1e8 * random(),
		get_word(): get_word(),
		get_word(): randint(-1e7, 1e7),
		get_word(): 1e8 * random(),
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


