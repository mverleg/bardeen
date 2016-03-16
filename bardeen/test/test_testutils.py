
"""
	tests for bardeen.testutils
"""

import string
from math import pi
from re import match
from bardeen.testutils import printable_line, get_random_string, get_random_word, create_file, dict_round_floats
from os.path import isfile, abspath
from numpy import float64


def check_letters_presence(word_generator, available_letters):
	"""
		check that the allowed characters actually occur; since the generation is random, there is always a chance that
		it didn't occur for the words finite amount of words generated; try N times such that the chance for any
		false positive is < 0.001 (0.1%)

		average letters generated: ``L = N * (16 + 2) / 2.``
		number of possible letters m: ``m = len(available_letters)``
		probability of a specific letter to not occur p: ``p = ((m - 1.) / m) ** L``
		therefore, minimum N such that m * p < 0.001:
		((m - 1.) / m) ** L = 0.001 / m
		L * ln ((m - 1.) / m) = ln (0.001 / m)
		N = (2. / 18) * ln (0.001 / m) / ln ((m - 1.) / m)
		which for m 10 up to 100k is m < N < ~2m
	"""
	for check in available_letters:
		for k in range(2 * len(available_letters)):
		#for k in range(1):
			if check in word_generator():
				break
		else:
			m = len(available_letters)
			prob_false_neg = m * (((m - 1.) / m) ** (18 * m))
			raise AssertionError('didn\'t find "%s" in %d words (could be random, but p = %.6f)' % (check, 2 * m, prob_false_neg))


def test_get_random_word():
	"""
		test if get_random_word is within the limits and generated the allowed characters
	"""
	for k in range(50):
		word = get_random_word()
		assert match(r'[\w\d]{2,16}', word)
	check_letters_presence(get_random_word, string.letters + string.digits)


def test_get_random_string():
	"""
		test if get_random_string is within the limits and generated the allowed characters
	"""
	for k in range(50):
		word = get_random_string()
		assert match(r'[\w\d\s!"#$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]^_`\{|\}~]{2,16}', word)
	check_letters_presence(get_random_string, printable_line)


def test_create_file(tmpdir):
	file_path = create_file(unicode(tmpdir))
	assert isfile(file_path)
	assert abspath(file_path).startswith(abspath(unicode(tmpdir))), 'check correct directory'


def test_dict_round_floats():
	test_dict = {
		pi: float64(pi),
		'3.1415': None,
	}
	validate_dict = {
		3.14: float64(3.14),
		'3.1415': None,
	}
	dict_round_floats(test_dict, 2)
	assert test_dict == validate_dict


