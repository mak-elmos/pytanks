#! /usr/bin/python

__author__ = 'Amin'

def data2str(_data):
	return str(_data)

def str2data(_str):
	result = ""
	if len(_str) >= 1 and _str[0] == '{':
		result = eval(_str)

	return result


def compress(x):
	import zlib
	return zlib.compress(x)

def decompress(x):
	if type(x) != str or len(x) == 0:
		return ""

	import zlib
	return zlib.decompress(x)


if __name__ == "__main__":
	print data2str([{"1":1}, 2])
	print str2data('[{"1":1}, 2]')
