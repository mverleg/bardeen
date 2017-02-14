# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst', 'r') as fh:
	readme = fh.read()

setup(
	name='bardeen',
	description='Collection of scientific utilities.',
	long_description=readme,
	url='https://github.com/mverleg/bardeen',
	author='Mark V',
	maintainer='(the author)',
	author_email='mdilligaf@gmail.com',
	license='Revised BSD License (LICENSE.txt)',
	keywords=[],
	version='1.4.2',
	packages=['bardeen'],
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	install_requires=[
		'numpy',
	],
)
