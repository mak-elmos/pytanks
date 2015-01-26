#! /usr/bin/python

__author__ = 'Amin'

class Map:
	pass


def loadMap(name):
	import pickle
	return pickle.load(open("maps/" + name + '.ptm', "r"))
