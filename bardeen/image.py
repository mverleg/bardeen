
from numpy import roll


def translate(arr, shifts, fill_value = 0):
	"""
	For a numpy array (e.g. image), translate all values by an integer vector.

	:arg arr: The ndarray to shift (remains unaffected).
	:arg shifts: The sequence of shift distances (integers).
	:return: shifted array

	Compare roll and pad.
	"""
	#todo: unit tests
	Ns = arr.shape
	assert len(Ns) == len(shifts), 'Provide a shift distance for each axis'
	for k, shift in enumerate(shifts):
		if shift != 0:
			arr = roll(arr, shift = shift, axis = k)
			s = [slice(None)] * len(shifts)
			s[k] = slice(0, shift) if shift > 0 else slice(shift, Ns[k])
			arr[s] = fill_value
	return arr


