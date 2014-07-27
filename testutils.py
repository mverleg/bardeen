
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
		creates a small random file, for testing

		:param dir_path: (temporary) dir to create the file
		:return: full path to the file
	"""
	file_path = join(dir_path, get_random_word()).rstrip('/') + '.' + get_random_word()[:3]
	fh = open(file_path, 'w+')
	fh.write('\n'.join(get_random_string() for line in range(100)))
	fh.close()
	return file_path

"""
	NOTE: if you add something, write a test!
"""

