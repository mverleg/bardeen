
"""
	unit tests for bardeen.system
"""

from os.path import join, isdir, isfile, islink
from bardeen.system import mkdirp, link_else_copy
from bardeen.testutils import create_file, get_random_word
from shutil import Error


def test_link_else_copy(tmpdir):
	old_path = create_file(unicode(tmpdir))
	new_path = join(unicode(tmpdir), get_random_word()) + '.txt'
	link_else_copy(old_path, new_path)
	assert isfile(new_path) or islink(new_path)
	assert open(old_path, 'r').read() == open(new_path, 'r').read(), 'check if files the same'
	try:
		link_else_copy(old_path, new_path)
	except Error:
		""" link already created """
	except OSError:
		""" file already copied """
	else:
		raise AssertionError('link_else_copy does not raise an error if the destination file already exists')
	try:
		link_else_copy(old_path + '.DoesNotExist', new_path)
	except IOError:
		""" as expected """
	else:
		raise AssertionError('link_else_copy does not raise an error if the source file doesn\'t exist')


def test_mkdirp(tmpdir):
	dir_pth = join(unicode(tmpdir), get_random_word(), get_random_word(), get_random_word())
	mkdirp(dir_pth)
	assert isdir(dir_pth)
	file_pth = join(dir_pth, get_random_word())
	fh = open(file_pth, 'w+')
	fh.write('testfile')
	fh.close()
	assert isfile(file_pth)
	try:
		mkdirp(file_pth)
	except OSError:
		""" expected error """
	else:
		raise AssertionError('did not throw an exception, even though the path was a file and as such, \
			no directory was created')


