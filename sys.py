
"""
	system related utilities (e.g. filesystem)
"""

from os import link, makedirs
from shutil import copyfile
from errno import EEXIST


def link_else_copy(filename_from, filename_to):
	"""
		try to create a hard-link 'copy' of a file (almost no space use)
		if that doesn't work then really copy them (files are independent)

		:param filename_from: the existing file
		:param filename_to: the desired new file
		:return: True if linking worked, False otherwise
		:raise: OSError if copy fails
	"""
	try:
		link(filename_from, filename_to)
		return True
	except OSError:
		copyfile(filename_from, filename_to)
		return False


def mkdirp(dir_path):
	"""
		creates all the directories on dir_path if they do not exist
		like mkdir -p in shell

		:param dir_path: path whose components will be created as directories
		:raise: OSError for unexpected problems; no error if directory already exists
	"""
	try:
		makedirs(dir_path)
	except OSError as err:
		if err.errno != EEXIST:
			raise



