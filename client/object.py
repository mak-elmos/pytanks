#! /usr/bin/python

__author__ = 'Milad & Amin'

from vector import *
class Object(object):
	"""
	:param position
	:param prevPositions
	:param mass
	"""

	maxPrevPosition = 100

	def __init__(self, pos):
		self.position	  = pos
		self.prevPositions = []
		

	def setPosition(self, pos):
		if not isinstance(pos, Vector):
			return

		if self.position != None:
			self.prevPositions.append(self.position)
		self.position = pos
		while len(self.prevPositions) > self.maxPrevPosition:
			del self.prevPositions[0]
