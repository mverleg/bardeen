
"""
Routines related to text input/output
"""

import sys, os


def clear_stdout(lines = 1, stream = sys.stdout, flush = True):
	"""
	Uses escape characters to move back number of lines and empty them

	To write something on the empty lines, use :func:sys.stdout.write() and :func:sys.stdout.flush()

	:param lines: the number of lines to clear
	:param stream: by default, stdout is cleared, but this can be replaced by another stream that uses these \
	escape characters (stderr comes to mind)
	:param flush: by default, uses flush after writing, but canbe overriden if you will do it yourself soon after
	"""
	stream.write('\033[F\r\x1b[K' * lines)
	if flush:
		stream.flush()


def reprint(txt, lines = 1, stream = sys.stdout):
	"""
	Removes lines from stdout and prints the requested text txt instead of them

	:param txt: the text you want to print; works best if no more than `lines` lines
	:param stream: see ``clear_stdout``
	:param lines: the number of lines you want to use; \
	this amount is cleared and if txt is shorter, the remainder is prepended

	For example for status monitoring:

	1. print N newlines
	2. do something or check something until there is news
	3. use ``reprint`` to print the as most N lines update using lines = N
	4. repeat step 2 and 3 until task is done
	5. if you want to remove the last status message, call clear_stdout using lines = N
	"""
	clear_stdout(lines = lines, flush = False)
	line_count = len(txt.splitlines())
	stream.write(
		os.linesep * (lines - line_count) +
		txt +
		os.linesep
	)
	stream.flush()


def add_linebreaks(text, max_len=80):
	"""
	Add linebreaks on whitespace such that no line is longer than `max_len`, unless it contains a single word that's longer.
	
	There are probably way faster methods, but this is simple and works.
	"""
	br_text = ''
	len_cnt = 0
	for word in text.split(' '):
		len_cnt += len(word) + 1
		if len_cnt > max_len:
			len_cnt = len(word)
			br_text += '\n' + word
		else:
			br_text += ' ' + word
	return br_text[1:]


