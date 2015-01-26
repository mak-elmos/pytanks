#! /usr/bin/python

from manager import Manager

m = Manager()
server_started = False
try:
	m.init()
	server_started = True
except:
	print "Starting server failed ..."

if server_started:
	m.run()
