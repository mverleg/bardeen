
from mympl import MyMPL

__all__ = ['MyMPL', 'figure', 'subplots', 'show', 'close', 'order']


def figure(*args, **kwargs):
	return MyMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
	return MyMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
	return MyMPL.instance().show(*args, **kwargs)

def close(*args, **kwargs):
	"""
		opens and immediately closes figures; use instead of show (if already open use close_all)
	"""
	return MyMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
	MyMPL.instance().order(*args, **kwargs)


