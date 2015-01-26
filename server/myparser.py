#! /usr/bin/python

__author__ = 'Amin'

import basictypes
from attackertank import *
from defendertank import *

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


def wm2data(wm):

	def fixNum(x):
		x *= 1000
		x = int(x)
		x = float(x)
		x /= 1000
		return x

	from tank import Tank
	from bomb import Bomb

	wmData = {}

	tank_key  = basictypes.DataNames.tank
	bomb_key  = basictypes.DataNames.bomb
	wmData[tank_key] = []
	wmData[bomb_key] = []

	allTanks = dict(wm.tanks.items() + wm.respawning_tanks.items())
	for pid in allTanks:
		tank = allTanks[pid]
		tankData = {}

		tankData[basictypes.DataNames.team] = tank.team

		if isinstance(tank, AttackerTank):
			tankData[basictypes.DataNames.tanktype]     = basictypes.TankTypes.attacker
			tankData[basictypes.DataNames.health]       = fixNum(tank.health)
			tankData[basictypes.DataNames.direction]    = fixNum(tank.launcherDirection)
			tankData[basictypes.DataNames.launcher]     = fixNum(tank.launcherLength)
			tankData[basictypes.DataNames.respawn_time] = fixNum(tank.respawn_time)
		elif isinstance(tank, DefenderTank):
			tankData[basictypes.DataNames.tanktype]  = basictypes.TankTypes.defender


		tankData[basictypes.DataNames.mana]     = fixNum(tank.mana)
		tankData[basictypes.DataNames.position] = (fixNum(tank.position.x), fixNum(tank.position.y))
		tankData[basictypes.DataNames.pid]      = pid

		wmData[tank_key].append(tankData)


	for b in wm.bombs:
		bombData = {}

		bombData[basictypes.DataNames.bid]      = b.bid
		bombData[basictypes.DataNames.position] = (fixNum(b.position.x), fixNum(b.position.y))

		wmData[bomb_key].append(bombData)

	wmData[basictypes.DataNames.score]     = {basictypes.Teams.left: wm.score_left, basictypes.Teams.right: wm.score_right}
	wmData[basictypes.DataNames.gamestate] = wm.game_state

	return wmData


if __name__ == "__main__":
	print data2str([{"1":1}, 2])
	print str2data('[{"1":1}, 2]')
