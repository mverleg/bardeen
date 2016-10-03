
from threading import Thread
import urllib2


def async_forget_thread(func, *args, **kwargs):
	"""
	Very simply async decorator, intended for writing things while continuing the program. No output is sent back.

	* Uses non-daemon mode, which causes the program to keep running until this thread exits.
	* Using threading, so runs on the same code due to Python global interpreter lock.
	"""
	#Thread(target = func, args = args, kwargs = kwargs, daemon = False).start()
	Thread(target = func, args = args, kwargs = kwargs).start()
	#todo: tested only superficially


def fetch_urls(urls):
	"""
	Fetch urls in parllel, then wait until they're all done.

	@return: content specified by the urls in the same order as the urls

	http://stackoverflow.com/questions/16181121/python-very-simple-multithreading-parallel-url-fetching-without-queue
	"""
	results = [None] * len(urls)
	def fetch_url(nr, url):
		results[nr] = urllib2.urlopen(url).read()
	threads = [Thread(target = fetch_url, args = (nr, url)) for nr, url in enumerate(urls)]
	for thread in threads: thread.start()
	for thread in threads: thread.join()
	return results


