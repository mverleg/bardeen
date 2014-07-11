
from os.path import join
from numpy import array_equal, float64, exp, complex128
from numpy.random import rand, randint
from storage.array import store_array, load_array, \
	store_array_bin, load_array_bin


'''
	tmpdir is automatically an empty temporary directory
	http://stackoverflow.com/questions/4199700/python-how-do-i-make-temporary-files-in-my-test-suite
'''
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


