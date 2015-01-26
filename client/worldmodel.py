#! /usr/bin/python

__author__ = 'Amin'

from tank import *
from bomb import *
from gamemap import *
import basictypes
import constvars


class WorldModel:
	def __init__(self):
		self.cycle_time  = constvars.cycle_time

		self.game_state  = basictypes.GameStates.play
		self.score_left  = 0
		self.score_right = 0
		self.mytank      = None
		self.tanks       = {}
		self.bombs       = []

	def init(self, pid, mapname):
		self.pid = pid
		self.map = loadMap(mapname)
		self.map.guiData.decodeLoadedImages()


	def parseData(self, data):
		if type(data) != dict:
			return

		self.game_state  = data[basictypes.DataNames.gamestate]
		self.score_left  = data[basictypes.DataNames.score][basictypes.Teams.left]
		self.score_right = data[basictypes.DataNames.score][basictypes.Teams.right]

		tanks = data[basictypes.DataNames.tank]
		bombs = data[basictypes.DataNames.bomb]

		# tank
		updatedTanks = []
		for tankData in tanks:
			self.updateTanks(tankData)
			updatedTanks.append(tankData[basictypes.DataNames.pid])
		for pid in self.tanks.keys():
			if not pid in updatedTanks:
				del self.tanks[pid]

		# bomb
		updatedBombs = []
		for bombData in bombs:
			self.updateBomb(bombData)
			updatedBombs.append(bombData[basictypes.DataNames.bid])
		for b in self.bombs:
			if not b.bid in updatedBombs:
				self.bombs.remove(b)


	def updateTanks(self, tankData):
		tank = Tank()
		if tankData[basictypes.DataNames.pid] == self.pid and isinstance(self.mytank, Tank):
			tank = self.mytank
		elif  tankData[basictypes.DataNames.pid] in self.tanks:
			tank = self.tanks[tankData[basictypes.DataNames.pid]]

		tank.team     = tankData[basictypes.DataNames.team]
		tank.tanktype = tankData[basictypes.DataNames.tanktype]

		if tank.tanktype == basictypes.TankTypes.attacker:
			tank.health            = tankData[basictypes.DataNames.health]
			tank.launcherDirection = tankData[basictypes.DataNames.direction]
			tank.launcherLength    = tankData[basictypes.DataNames.launcher]
			tank.respawn_time      = tankData[basictypes.DataNames.respawn_time]

		tank.mana     = tankData[basictypes.DataNames.mana]
		if tank.tanktype == basictypes.TankTypes.attacker:
			tank.size = Vector(self.map.attacker_width, self.map.attacker_height)
			tank.manaCost = self.map.attacker_manaCost
		elif tank.tanktype == basictypes.TankTypes.defender:
			tank.size = Vector(self.map.defender_width, self.map.defender_height)
			tank.manaCost = self.map.defender_manaCost

		tank.prevPositions.append(tank.position)
		tank.setPosition(Vector(tankData[basictypes.DataNames.position][0], tankData[basictypes.DataNames.position][1]))

		if tankData[basictypes.DataNames.pid] == self.pid:
			self.mytank = tank
		elif  not tankData[basictypes.DataNames.pid] in self.tanks:
			self.tanks[tankData[basictypes.DataNames.pid]] = tank

	def updateBomb(self, bombData):
		bomb = Bomb()

		bomb.bid      = bombData[basictypes.DataNames.bid]
		bomb.setPosition(Vector(bombData[basictypes.DataNames.position][0], bombData[basictypes.DataNames.position][1]))

		for b in self.bombs:
			if bomb.bid == b.bid:
				b.prevPositions.append(b.position)
				b.position = bomb.position
				return

		bomb.radius = self.map.bomb_radius
		self.bombs.append(bomb)


	def update(self, data):
		self.parseData(data)


	def __str__(self):
		result = "********************************************************\n"

		result += "--------------PID--------------\n"
		result += str(self.pid) + "\n"

		result += "------------GameState------------\n"
		result += str(self.game_state) + "\n"

		result += "--------------SCORE--------------\n"
		result += str(self.score_left)  + "\n"
		result += str(self.score_right) + "\n"

		result += "--------------MY TANK--------------\n"
		if isinstance(self.mytank, Tank):
			result += "position = " + str(self.mytank.position) + "\n"
			##for pos in self.mytank.prevPositions:
			##	result += "prev position = " + str(pos) + "\n"
			result += "size     = " + str(self.mytank.size) + "\n"
			result += self.mytank.team      + "\n"
			result += self.mytank.tanktype  + "\n"
			result += str(self.mytank.mana) + "\n"
			result += str(self.mytank.manaCost)  + "\n"
			if self.mytank.tanktype == basictypes.TankTypes.attacker:
				result += str(self.mytank.health)            + "\n"
				result += str(self.mytank.launcherDirection) + "\n"
				result += str(self.mytank.launcherLength)    + "\n"
				result += str(self.mytank.respawn_time)      + "\n"

		result += "-------------------\n"

		result += "--------------OTHER TANKS--------------\n"
		for pid in self.tanks:
			tank = self.tanks[pid]
			result += "position = "    + str(tank.position) + "\n"
			result += "size     = "    + str(tank.size) + "\n"
			result += tank.team        + "\n"
			result += tank.tanktype    + "\n"
			result += str(tank.mana)   + "\n"
			result += str(tank.manaCost)  + "\n"
			if tank.tanktype == basictypes.TankTypes.attacker:
				result += str(tank.health)            + "\n"
				result += str(tank.launcherDirection) + "\n"
				result += str(tank.launcherLength)    + "\n"
				result += str(tank.respawn_time)      + "\n"
			result += "-------------------\n"

		result += "--------------BOMBS--------------\n"
		for b in self.bombs:
			result += "----------------------- bid = " + str(b.bid) + " -----------------------" + "\n"
			result += "position = "                    + str(b.position)                         + "\n"
			result += "radius = "                      + str(b.radius)                           + "\n"
			##for pos in b.prevPositions:
			##	result += "prev position = " + str(pos) + "\n"
			result += "-------------------\n"

		result += "********************************************************\n"

		return result
