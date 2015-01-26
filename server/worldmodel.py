#! /usr/bin/python

__author__ = 'Milad'

import basictypes

class WorldModel:
	def __init__(self):
		self.game_state   = basictypes.GameStates.play
		self.score_left   = 0
		self.score_right  = 0 
		self.tanks = {}
		self.respawning_tanks = {}
		self.disconnected_tanks = {}
		self.tanks_lastSeen = {}
		self.bombs = []
		self.bombs_counter = 0
		self.destroyingScore = 1
		#self.zaribeTakaneyeBomb = .07 ## in nabayad inja bashe bara test injast
