#! /usr/bin/python

__author__ = 'Amin'

class DataNames:
	# enums
	event     = 'E_EVENT'
	action    = 'E_ACTION'
	team      = 'E_TEAM'
	tanktype  = 'E_TANKTYPE'
	gamestate = 'E_GAMESTATE'

	# types
	tank      = 'T_TANK'
	bomb      = 'T_BOMB'
	block     = 'T_BLOCK'

	# attributes
	pid          = 'A_PID'
	bid          = 'A_BID'
	position     = 'A_POSITION'
	direction    = 'A_DIR'
	launcher     = 'A_LAUNCHER'
	health       = 'A_HEALTH'
	mana         = 'A_MANA'
	respawn_time = 'A_SPWN'
	score        = 'A_SCORE'


class Events:
	quitgame  = 'EVENT_QUIT'
	pausegame = 'EVENT_PAUSE'
	showgui   = 'EVENT_CANSHOW'
	training  = 'EVENT_TRAINING'
	changebot = 'EVENT_CHANGEBOT'


class Actions:
	goleft        = 'ACT_GOLEFT'
	goright       = 'ACT_GORIGHT'
	increaseangle = 'ACT_INCREASE_ANGLE'
	decreaseangle = 'ACT_DECREASE_ANGLE'
	jump          = 'ACT_JUMP'
	shoot         = 'ACT_SHOOT'
	none          = 'ACT_NONE'

	def _toList(self):
		result = []
		attrs = filter(lambda aname: not aname.startswith('_'), dir(self))
		for i in attrs:
			result.append(getattr(self, i))
		return result
		

class Teams:
	left  = 'TEAM_LEFT'
	right = 'TEAM_RIGHT'
	none  = 'TEAM_NONE'


class TankTypes:
	attacker = 'TANK_ATTACKER'
	defender = 'TANK_DEFENDER'

class GameStates:
	play  = 'STATE_PLAY'
	pause = 'STATE_PAUSE'

class TankColors:
	pass
