
"""
	unit tests for bardeen.inout
"""

from time import sleep
from bardeen.inout import clear_stdout, reprint


"""
	clear_stdout and reprint and difficult to test automatically;
	optionally you can run the below code manually in a shell
"""


def manual_test_clear_stdout():
	"""
		Prints "before going back", then creates lines, removes them and prints numbers
	"""
	for k in range(5):
		print 'this line should be removed; if you see it, it went wrong'
	clear_stdout(lines = 5)
	for k in range(5):
		print 'item #%d' % (k + 1)


def manual_test_reprint():
	"""
		Simple status monitoring example, showing count and stars (takes 3 lines but uses 2)
	"""
	print '\n' * 2
	for k in range(1, 11):
		reprint('item #%.2d/10: %s \n^ that is the status!' % (k, '*' * k), lines = 3)
		sleep(0.15)


if __name__ == '__main__':
	print 'manual_test_clear_stdout: you should see item#1-5'
	manual_test_clear_stdout()
	print 'manual_test_reprint: you should see an updating status'
	manual_test_reprint()


