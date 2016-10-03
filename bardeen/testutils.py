
import string
from random import sample, randint
from os.path import join


printable_line = string.printable.replace('\n', '').replace('\r', '')


def get_random_word():
	"""
	:return: random alphanumeric word of 2-16 characters
	"""
	return unicode(''.join(sample(string.letters + string.digits, randint(2, 16))))


def get_random_string():
	"""
	:return: random string of 2-16 printable characters, without newlines
	"""
	return unicode(''.join(sample(printable_line, randint(2, 16))))


def create_file(dir_path):
	"""
	Creates a small random file, for testing.

	:param dir_path: (temporary) dir to create the file
	:return: full path to the file
	"""
	file_path = join(dir_path, get_random_word()).rstrip('/') + '.' + get_random_word()[:3]
	fh = open(file_path, 'w+')
	fh.write('\n'.join(get_random_string() for line in range(100)))
	fh.close()
	return file_path


def dict_round_floats(dicti, decim = 6):
	"""
	Go through a dict and round all floats (in keys and values) to a specific number of decimal places, to make it
	possible to compare a dict that has been saved and loaded, or some math applied.

	:return: no return value; **substitution happens in-place**!
	"""
	for key, value in dicti.items():
		if isinstance(key, float):
			''' this also matches for numpy.float64 etc '''
			del dicti[key]
			key = round(key, decim)
			dicti[key] = value
		if isinstance(value, float):
			dicti[key] = round(value, decim)


