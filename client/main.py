#! /usr/bin/python

from manager import Manager

m = Manager()
if m.init():
	m.run()
