
"""
System related utilities (e.g. filesystem)
"""

from os import symlink, makedirs
from shutil import copyfile
from errno import EEXIST
from os.path import exists, isdir


def link_else_copy(filename_from, filename_to):
	"""
	Try to create a symbolic link 'copy' of a file (almost no space use).

	If that doesn't work then really copy them (files are independent).

	:param filename_from: the existing file
	:param filename_to: the desired new file
	:return: True if linking worked, False otherwise
	:raise: OSError if copy fails

	This command was switched from hard to soft links because it's clearer and works across filesystem boundaries.
	"""
	try:
		symlink(filename_from, filename_to)
		return True
	except OSError:
		copyfile(filename_from, filename_to)
		return False


def mkdirp(dir_path, mode=None):
	"""
	Creates all the directories on dir_path if they do not exist.

	Like ``mkdir -p`` in shell.

	:param dir_path: path whose components will be created as directories
	:raise: OSError for unexpected problems and if dir_path is something other than a directory;\
	no error if directory already exists
	"""
	if exists(dir_path) and not isdir(dir_path):
		raise OSError('"%s" already exists, but is not a directory' % dir_path)
	try:
		if mode is None:
			makedirs(dir_path)
		else:
			makedirs(dir_path, mode=mode)
	except OSError as err:
		if err.errno != EEXIST:
			raise


"""
	NOTE: if you add something, write a test!
"""


