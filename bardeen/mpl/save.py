
"""
	Order and generate images specified as command line parameters.
"""

from collections import defaultdict
from os.path import splitext
from sys import argv, stderr
from bardeen.mpl import MPL


def order_imgs(filenames, img_map, mpl = None, properties = None):
	"""
		Order a specified set of images (e.g. from argv) using a mapping from image to generation method.

		:param filenames: iterable of filenames whose non-extension name is in img_map
		:param img_map: a map of non-extension filenames to the way to generate them, where the keys are tuples of \
		basenames generated by the script and the values are tuples (label, pypath, function, kwargs) \
		where function can be either the name of the function in the module, or any python function:

		>>> {('test', 'test2'): ('demo_image', 'demos', lambda **kwargs: demos.generate_demos(**kwargs), {}, properties),	...}

		:param mpl: optionally, an mpl instance
		:param properties: deprecated

		Exits with status code 1 if not all images were found; some stdout and stderr messages.
	"""

	if properties or len(img_map.values()[0]) == 4:
		raise NotImplementedError('you are using an old format; img_map values should now be (label, module, func, \
			kwargs, properties), see docstring')

	if not filenames:
		stderr.write('no images provided to order_imgs\n')
	if mpl is None:
		mpl = MPL.instance(directory = '.', save_all = False)

	bases = defaultdict(set)
	for img in filenames:
		bases[splitext(img)[0]].add(img)
	for files, (label, pypath, func, kwargs, properties) in img_map.items():
		""" find and order keys that were ordered """
		matches = set(bases.keys()) & set(files)
		if matches:
			for match in matches:
				for filename in bases[match]:
					mpl.order(label = label, filename = filename, **properties)
				del bases[match]
			""" generate the images using provided method """
			if not callable(func):
				# <-- why fromlist? (it imports A instead of B for import A.B without fromlist, but why?)
				module = __import__(pypath, fromlist = [pypath])
			if isinstance(func, basestring):
				func = getattr(module, func)
			''' callable that generated images, possibly given kwargs '''
			if func is not None:
				func(**kwargs if kwargs else {})

	mpl.close()

	if bases:
		stderr.write('no way found to build these images: %s\n' % ', '.join(', '.join(imgnames) for imgnames in bases.values()))
		exit(1)


def from_argv(img_map, mpl = None, properties = None):
	return order_imgs(argv[1:], img_map, mpl = mpl)


