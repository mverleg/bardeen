
"""
Routines related to changing text, e.g. substitution or escape for some format
"""

from re import escape as re_escape, compile


#todo: unit test
def tex_escape(text):
	"""
	:param text: a plain text message
	:return: the message escaped to appear correctly in LaTeX
	"""
	conv = {
		'&': r'\&',
		'%': r'\%',
		'$': r'\$',
		'#': r'\#',
		'_': r'\_',
		'{': r'\{',
		'}': r'\}',
		'~': r'\textasciitilde{}',
		'^': r'\^{}',
		'\\': r'\textbackslash{}',
		'<': r'\textless',
		'>': r'\textgreater',
	}
	return sub_dict(text, conv)


def sub_dict(text, subst):
	"""
	Replace all instances of multiple words in a string. Prevents problems with overlapping keys and substitutions.

	:param subst: something that behaves like a dictionary, where each key is converted to it's value
	"""
	regex = compile('|'.join(re_escape(unicode(key)) for key in sorted(subst.keys(), key = lambda item: - len(item))))
	return regex.sub(lambda match: subst[match.group()], unicode(text))


