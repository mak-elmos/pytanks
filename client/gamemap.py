#! /usr/bin/python

__author__ = 'Amin'

from basictypes import TankColors

class GraphicData:
	def decodeLoadedImages(self):

		def decode(data):
			import pygame
			import bz2

			img = pygame.image.fromstring(bz2.decompress(data[0]), data[1], 'RGBA')
			return img

		self.background   = decode(self.background)
		self.pause_screen = decode(self.pause_screen)

		self.tank_attacker = decode(self.tank_attacker)
		self.tank_defender = decode(self.tank_defender)

		self.launcher = decode(self.launcher)

		for i in range(len(self.bombs)):
			self.bombs[i] = decode(self.bombs[i])

		self.block = decode(self.block)

		for i in range(len(self.digits)):
			self.digits[i] = decode(self.digits[i])

		self.winner_left  = decode(self.winner_left)
		self.winner_right = decode(self.winner_right)


class Map:
	pass


def loadMap(name):
	import pickle
	return pickle.load(open("maps/" + name + '.ptm', "r"))
