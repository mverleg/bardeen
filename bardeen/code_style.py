
"""
Functions for switching between code styles.
"""

from sys import argv, stderr
from re import sub, search, findall


def docstrings(code, to_double = True):
	"""
	Converts between 3x' and 3x" as long as only one of them occurs in the file.
	"""
	single, double = "'''", '"""'
	if single in code and double in code:
		print('skipping docstrings because both %s and %s appear' % (single, double))
		return code
	if to_double:
		code = code.replace(single, double)
	else:
		code = code.replace(double, single)
	return code


def indentation(code, to_tabs = True):
	"""
	Switch between indentation with tabs or 4 spaces
	"""
	lines = code.splitlines()
	for nr, line in enumerate(lines):
		if to_tabs:
			indent = len(findall(r'^((?:    )*)', line)[0])
			lines[nr] = '\t' * indent + line.lstrip('    ')
		else:
			indent = len(findall(r'^(\t*)', line)[0])
			lines[nr] = '    ' * indent + line.lstrip('\t')
	return '\n'.join(lines)


str = '''
from collections import defaultdict
def group_by(collection, get_property):
	"""
		For a list of items, group them by some property and return tuples of
		that property and all items that have it.

		Similar to :func:`itertools.groupby`, but that requires the items to be ordered by that property;
		more efficient but annoying to use.

		>>> for unique_prop, items in group_by(items, lambda item: item.name).items():
			print '%s: %d' % (unique_prop, len(items))
	"""
	grouped = defaultdict(list)
	for item in collection:
		grouped[get_property(item)].append(item)
	return grouped
"""
	NOTE: if you add something, write a test!
"""'''
print(indentation(str, to_tabs = True))
print(indentation(indentation(str, to_tabs = True), to_tabs = False))
exit()


def first_lines(code, goal_empty_count = 1):
	"""
	Makes sure first lines are empty, after a possible #-prefix.
	"""
	lines = code.splitlines()
	if not lines:
		return code
	""" extract prefix """
	prefix = []
	if lines[0].startswith('#'):
		prefix = [lines.pop(0)]
	""" fix empty lines """
	lines = _prefix_empty_lines(lines, goal_empty_count = goal_empty_count)
	""" construct result """
	return '\n'.join(prefix + lines)


def last_lines(code, goal_empty_count = 3):
	lines = code.splitlines()
	""" fix empty lines """
	lines = _prefix_empty_lines(lines[::-1], goal_empty_count = goal_empty_count + 2)[::-1]
	""" construct result """
	return '\n'.join(lines)


def argument_assignment(code, arg_space = True):
	"""
	Whitespace around = and the like.
	"""
	stderr.write('argument_assignment is not very precise; it will match some constructs such as (a,b)=(1,2) ' + \
		'as well as any strings or comments; it won\'t break code but may create weird formatting\n')
	lines = code.splitlines()
	for nr, line in enumerate(lines):
		copyline = None
		while not copyline == line:
			copyline = line
			if arg_space:
				line = sub(r'\((.*[^ ])=\s*([^ ].*)\)', r'(\1 = \2)', line)
				line = sub(r'\((.*[^ ])\s*=([^ ].*)\)', r'(\1 = \2)', line)
			else:
				line = sub(r'\((.*[^ ])\s+=\s*([^ ].*)\)', r'(\1=\2)', line)
				line = sub(r'\((.*[^ ])\s*=\s+([^ ].*)\)', r'(\1=\2)', line)
		lines[nr] = line
	return '\n'.join(lines)


def imports_together(code):
	"""
	Remove empty lines between imports (like IDE's like to create).
	"""
	lines = code.splitlines()
	import_lines = _find_import_lines(lines)
	if not import_lines:
		return code
	empty_lines = set(range(min(import_lines), max(import_lines) + 1)) - set(import_lines)
	for empty_nr in reversed(sorted(list(empty_lines))):
		lines.pop(empty_nr)
	return '\n'.join(lines)


def _find_import_lines(lines):
	"""
	Internal function that returns the line numbers of the top part import block.

	Any code in the import section will stop the search at that point.
	"""
	in_imports, import_lines = False, []
	for nr, line in enumerate(lines):
		if search(r'import\s+[\w\._]+', line) or search(r'from\s+[\w\._]+\s+import\s+[\w\._]+', line):
			in_imports = True
			import_lines.append(nr)
		elif not line.strip():
			continue
		else:
			if in_imports:
				break
	return import_lines


def _prefix_empty_lines(lines, goal_empty_count):
	"""
	Internal function to prepend empty lines (no prefix considerations).
	"""
	""" find current empty line count """
	current_empty_count = 0
	for line in lines:
		if line.strip():
			break
		current_empty_count += 1
	""" insert newlines if too few """
	lines = [''] * (goal_empty_count - current_empty_count) + lines
	""" remove newlines if too many """
	if current_empty_count > goal_empty_count:
		lines = lines[current_empty_count - goal_empty_count:]
	""" done! """
	return lines


def _print_code(code):
	print('+' * 20)
	for nr, line in enumerate(code.splitlines()):
		print('%3d\t%s' % (nr + 1, line.replace('\t', '~   ')))
	print('+' * 20)


def change_settings(code, to_tabs = None, to_double = None, start_empty = None, end_empty = None, arg_space = None):
	"""
	Apply various settings to a code string.
	"""
	if to_tabs is not None:
		code = indentation(code, to_tabs = to_tabs)
	if to_double is not None:
		code = docstrings(code, to_double = to_double)
	if start_empty is not None:
		code = first_lines(code, goal_empty_count = start_empty)
	if end_empty is not None:
		code = last_lines(code, goal_empty_count = end_empty)
	if arg_space is not None:
		code = argument_assignment(code, arg_space = arg_space)
	code = imports_together(code)
	return code


def change_file(filepath, change = False, to_tabs = None, to_double = None, start_empty = None, end_empty = None,
		arg_space = None):
	"""
	Apply various settings to a file if change = True (otherwise prints only).
	"""
	with open(filepath, 'r') as fh:
		code = fh.read()
		_print_code(code)
	code = change_settings(code, to_tabs = to_tabs, to_double = to_double, start_empty = start_empty,
		end_empty = end_empty, arg_space = arg_space)
	if change:
		with open(filepath, 'w') as fh:
			fh.write(code)
	else:
		_print_code(code)


def pep_files(filepaths, change = False):
	"""
	Convert somewhat to pep-compliant format for all the files in list filepaths.
	"""
	for filepath in filepaths:
		change_file(filepath, change = change, to_double = False, arg_space = False)


def mark_style_files(filepaths, change = False):
	"""
	Convert somewhat to pep-compliant format for all the files in list filepaths.
	"""
	for filepath in filepaths:
		change_file(filepath, change = change, to_double = True, arg_space = True, start_empty = 1, end_empty = 3)


if __name__ == '__main__':
	if len(argv) < 3:
		print('first argument should be the style; "pep" or "mark"')
		print('provide at least one file path of a python file (no directories)')
	filepaths = argv[2:]
	if argv[1] == 'pep':
		pep_files(filepaths)
	elif argv[1] == 'mark':
		mark_style_files(filepaths)
	else:
		print('first argument should be the style; "pep" or "mark" (got %s)' % argv[1])

