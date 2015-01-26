#! /usr/bin/python

__author__ = 'Amin & Milad'

import basictypes

class GraphicData:
	def __init__(self):
		### names
		self.fname_background   = 'background'
		self.fname_pause_screen = 'pause'

		self.fname_tank_attacker = 'attacker'
		self.fname_tank_defender = 'defender'

		self.fname_launcher = 'launcher'

		self.fname_bomb = 'bomb'
		self.bombsNum   = 5

		self.fname_block = 'block'

		self.fname_digits = 'digits/'

		self.fname_winner_left  = 'winner/left'
		self.fname_winner_right = 'winner/right'


		### team colors
		self.tank_colors_health = basictypes.TankColors()
		self.tank_colors_mana   = basictypes.TankColors()

		self.tank_colors_health.me    = (0, 0, 0)
		self.tank_colors_health.left  = (0, 0, 0)
		self.tank_colors_health.right = (0, 0, 0)


	def loadResources(self, mapname):

		def loadImage(imgName):
			import pygame
			import bz2

			img  = pygame.image.load('maps_resources/' + mapname + '/' + imgName + '.png')
			size = (img.get_width(), img.get_height())
			img  = bz2.compress(pygame.image.tostring(img, 'RGBA'))

			return (img, size)


		self.background   = loadImage(self.fname_background)
		self.pause_screen = loadImage(self.fname_pause_screen)

		self.tank_attacker = loadImage(self.fname_tank_attacker)
		self.tank_defender = loadImage(self.fname_tank_defender)

		self.launcher = loadImage(self.fname_launcher)

		self.bombs = []
		for i in range(0, self.bombsNum):
			self.bombs.append(loadImage(self.fname_bomb + str(i)))

		self.block = loadImage(self.fname_block)

		self.digits = []
		for i in range(10):
			self.digits.append(loadImage(self.fname_digits + str(i)))

		self.winner_left  = loadImage(self.fname_winner_left)
		self.winner_right = loadImage(self.fname_winner_right)


class Map:

	def __init__(self):

		###   general
		self.name = 'empty_room'

		###   field
		self.field_width  = 20.0 # meter
		self.field_height = 8.0  # meter

		self.physics_gravity    = -10.0
		self.physics_cycle_time = 0.02


		###   tank
		self.tank_respawn_time_default = 5

		###   attacker tank
		self.attacker_width  = 2.0
		self.attacker_height = 1.0

		self.attacker_mu         = 5
		self.attacker_speed      = 2
		self.attacker_shootSpeed = 10.0

		self.attacker_launcherLength_min = 0.5
		self.attacker_launcherLength_max = 1

		self.attacker_launcherDirection_first = 45.0 #degree
		self.attacker_launcherDirection_max   = 70.0 #degree
		self.attacker_launcherDirection_min   = 20.0 #degree
		self.attacker_launcherDirection_speed = 40   #degree per second

		self.attacker_manaMax  = 100 #percent
		self.attacker_manaReg  = 25  #percent per second
		self.attacker_manaCost = 25  #percent 

		self.attacker_explosion_const = 0.1
		self.attacker_momentum_const  = 0.18

		self.attacker_healthMax  = 100
		self.attacker_healthReg  = 5 #percent
		self.attacker_healthCost = 40

		###   defender tank
		self.defender_width  = 1.0
		self.defender_height = 1.0

		self.defender_mu        = 5
		self.defender_speed     = 4
		self.defender_jumpSpeed = 10.0

		self.defender_manaMax  = 100 #percent
		self.defender_manaReg  = 25  #percent per second
		self.defender_manaCost = 55  #percent

		self.defender_explosion_const = 0.4


		###   bomb
		self.bomb_radius = .2


		### graphic
		self.guiData = GraphicData()


		### blocks
		self.blocks = []


	def fillBlocks(self):
		### blocks
		import vector
		import block

		self.blocks.append(block.Block(vector.Vector(0.0, 1.75), 1.0, 3.5))
		self.blocks.append(block.Block(vector.Vector(self.field_width / 2.0  + 0.25, self.field_height / 2.0 - 0.5), 0.5, self.field_height + 1.0))
		self.blocks.append(block.Block(vector.Vector(-self.field_width / 2.0 - 0.25, self.field_height / 2.0 - 0.5), 0.5, self.field_height + 1.0))
		self.blocks.append(block.Block(vector.Vector(0.0, -0.5), self.field_width, 1.0))
		self.blocks.append(block.Block(vector.Vector(0.0, self.field_height - 0.25), self.field_width, 0.5))



	def loadResources(self):
		self.guiData.loadResources(self.name)


	def convertForServer(self):
		import copy
		server_map = copy.deepcopy(self)

		del server_map.guiData

		return server_map

	def convertForClient(self):
		import copy
		client_map = copy.deepcopy(self)

		del client_map.attacker_mu
		del client_map.attacker_speed
		del client_map.attacker_shootSpeed
		del client_map.attacker_launcherDirection_first
		del client_map.attacker_launcherDirection_speed

		del client_map.attacker_momentum_const
		del client_map.attacker_explosion_const

		del client_map.defender_mu
		del client_map.defender_speed
		del client_map.defender_jumpSpeed

		del client_map.defender_explosion_const


		## gui
		del client_map.guiData.fname_background
		del client_map.guiData.fname_pause_screen
		del client_map.guiData.fname_tank_attacker
		del client_map.guiData.fname_tank_defender
		del client_map.guiData.fname_launcher
		del client_map.guiData.fname_bomb
		del client_map.guiData.bombsNum

		return client_map



def saveMap(_map):
	import pickle

	pickle.dump(_map, open("maps/" + _map.name + '.ptm', "w"))

	pickle.dump(_map.convertForServer(), open("maps_server/" + _map.name + '.ptm', "w"))
	pickle.dump(_map.convertForServer(), open("../server/maps/" + _map.name + '.ptm', "w"))

	pickle.dump(_map.convertForClient(), open("maps_client/" + _map.name + '.ptm', "w"))
	pickle.dump(_map.convertForClient(), open("../client/maps/" + _map.name + '.ptm', "w"))

def loadMap(name):
	import pickle
	return pickle.load(open("maps/" + name + '.ptm', "r"))
