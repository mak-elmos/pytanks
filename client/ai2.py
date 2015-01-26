#! /usr/bin/python

__author__ = 'Amin'

from vector import *
from tank import *
import basictypes
from pickle import *
import os.path
from math import *

def loadDataBase():
	if not os.path.exists("ai2"):
		dump({}, open("ai2", "w"))
	return load(open("ai2", "r"))

def saveDataBase(db):
	dump(db, open("ai2", "w"))


class State:
	def __init__(self):
		self.myPos   = Vector(100, 100)
		self.bombPos = Vector(100, 100)
		self.bombLastPos = Vector(100, 100)
		self.bombDir = -1

	def init(self, wm):
		if isinstance(wm.mytank, Tank):
			self.myPos   = wm.mytank.position
		else:
			self.myPos   = Vector(100, 100)

		if len(wm.tanks):
			self.bombPos = wm.tanks[wm.tanks.keys()[0]].position
			self.bombLastPos = wm.tanks[wm.tanks.keys()[0]].position
		else:
			self.bombPos = Vector(100, 100)
			self.bombLastPos = Vector(100, 100)
		self.bombDir = -1

		if len(wm.bombs):
			self.bombPos = wm.bombs[0].position

			if len(wm.bombs[0].prevPositions):
				self.bombLastPos = wm.bombs[0].prevPositions[-1]

			if len(wm.bombs[0].prevPositions):
				if len(wm.bombs[0].prevPositions) >= 25:
					dirVector = wm.bombs[0].position - wm.bombs[0].prevPositions[-25]
					self.bombDir = dirVector.getAngle()
			else:
				self.bombDir = -1


	def fixNum(self, num, digitsNum = 1, partsNum = 1):
		num = float(num)
		num *= 10.0 ** digitsNum
		num = int(num)
		num = float(num)
		num /= 10.0 ** digitsNum

		part   = 1.0 / partsNum
		sign = 1.0
		if num < 0.0:
			sign = -1.0
		newNum = abs(float(int(num)))
		if partsNum >= 1:
			while newNum + part <= abs(num):
				newNum += part

		newNum *= sign

		return newNum

	def fixDir(self, _dir, partsNum, startDegree, endDegree):
		if _dir == -1:
			return -1

		partVal = (endDegree - startDegree) / partsNum

		counter = 0
		while _dir - partVal >= startDegree:
			_dir -= partVal
			counter += 1

		return counter

	def normalizeData(self):
		self.myPos.x   = self.fixNum(self.myPos.x)
		self.myPos.y   = self.fixNum(self.myPos.y)

		self.bombPos.x = self.fixNum(self.bombPos.x)
		self.bombPos.y = self.fixNum(self.bombPos.y)

		self.bombDir   = self.fixDir(self.bombDir, 6.0, 90.0, 270.0)

	def toStr(self):
		import copy
		tmp = copy.deepcopy(self)
		tmp.normalizeData()

		result = ""

		result += str(tmp.myPos.x) + ' ' + str(tmp.myPos.y)
		result += ' '
		result += str(tmp.bombPos.x) + ' ' + str(tmp.bombPos.y)
		result += ' '
		result += str(tmp.bombDir)

		return result

	def __str__(self):
		result = ""

		result += "myPos = "   + str(self.myPos)   + "\n"
		result += "bombPos = " + str(self.bombPos) + "\n"
		result += "bombDir = " + str(self.bombDir) + "\n"

		return result


class Action:
	allowedMoves = [basictypes.Actions.goleft, basictypes.Actions.goright]

	def __init__(self):
		self.move   = basictypes.Actions.none

	def randMove(self):
		import random
		self.move = self.allowedMoves[random.randrange(len(self.allowedMoves))]


	def __str__(self):
		result = ""

		result += "move = " + self.move   + "\n"

		return result


class SarsaAI:
	alpha = 0.5
	gamma = 0.8
	defaultReward = 0.0

	def __init__(self):
		self.q_data = {}
		self.q_data = loadDataBase()
		#print self.q_data

	def init(self, wm):
		self.map_field_width  = wm.map.field_width
		self.map_field_height = wm.map.field_height

		self.map_physics_gravity = wm.map.physics_gravity
		self.map_cycle_time      = wm.map.physics_cycle_time

		self.map_attacker_width  = wm.map.attacker_width
		self.map_attacker_height = wm.map.attacker_height

		self.map_bomb_radius = wm.map.bomb_radius

		self.currentState  = self.getWorldModelState(wm)
		if not self.currentState.toStr() in self.q_data:
			self.addState(self.currentState)
		self.currentAction = self.getWeightedAction(self.currentState)

	def addState(self, state):
		data = {}
		for move in Action.allowedMoves:
			data[move] = self.defaultReward

		"""if int(state.myPos.x) == -self.map_field_width / 2.0 + 2:
			del data[basictypes.Actions.goleft]
		if int(state.myPos.x) == -1:
			del data[basictypes.Actions.goright]"""

		#print state
		#print state.toStr()
		self.q_data[state.toStr()] = data

	def getWorldModelState(self, wm):
		import copy
		state = copy.deepcopy(State())
		state.init(copy.deepcopy(wm))
		#state.normalizeData()
		#print state
		return state

	def getRandomAction(self):
		act = Action()
		act.randMove()
		return act

	def getWeightedAction(self, state):
		import random
		import copy

		act = Action()
		choices = copy.deepcopy(self.q_data[state.toStr()])

		min_choices = min(choices[c] for c in choices)
		max_choices = max(choices[c] for c in choices)
		if min_choices == 0.0 or max_choices == 0.0:
			for c in choices:
				choices[c] = 1

		if min_choices < 0.0 and max_choices < 0.0:
			for c in choices:
				choices[c] *= -1.0
			keys = choices.keys()
			choices[keys[0]], choices[keys[1]] = choices[keys[1]], choices[keys[0]]
		elif min_choices < 0.0 and max_choices > 0.0:
			for c in choices:
				choices[c] += 1 - min_choices

		total = sum(choices[c] for c in choices)
		r = random.uniform(0, total)

		upto = 0
		for c in choices:
			w = choices[c]
			if upto + w >= r:
				act.move = c
				break
			upto += w

		return act

	"""def calculateFitness(self, state):
		fitness = 0

		vel = state.bombPos - state.bombLastPos
		vel.x /= self.map_cycle_time
		vel.y /= self.map_cycle_time
		if state.bombPos.y > self.map_attacker_height:
			h = state.bombPos.y - self.map_attacker_height / 2.0
		else:
			h = state.bombPos.y

		endVel_y = (2.0 * (-1.0 * self.map_physics_gravity) * h + vel.y ** 2.0) ** 0.5 * -1.0
		dtime = (vel.y - endVel_y) / (-1.0 * self.map_physics_gravity)
		endX = state.bombPos.x + vel.x * dtime
		#print "bomb pos real       = ", state.bombPos.x
		#print "bomb pos end        = ", endX

		fitness += 20.0 * abs(state.myPos.x - endX)
		if abs(state.myPos.x - endX) < self.map_attacker_width / 2.0 + 0.3:
			print "------------------------------------------------------------------------------------"
			fitness -= 1000
		#if abs(state.myPos.x - state.bombPos.x) < self.map_attacker_width / 2.0 + 0.1 and abs(state.myPos.y - state.bombPos.y) < self.map_attacker_height / 2.0 + 0.1:
		#	print "------------------------------------------------------------------------------------"
		#	fitness -= 1000

		return fitness"""

	def calculateFitness(self, state):
		fitness = 0

		if state.bombPos.y < 2.5:
			fitness += 20.0 * abs(state.myPos.x - state.bombPos.x)
		if abs(state.myPos.x - state.bombPos.x) < self.map_attacker_width / 2.0 + self.map_bomb_radius and abs(state.myPos.y - state.bombPos.y) < self.map_attacker_height / 2.0 + self.map_bomb_radius:
			print "------------------------------------------------------------------------------------"
			fitness -= 1000

		return fitness


	def getMaxRewardOfState(self, state):
		maxReward = -9999999999999999999999999999999999999.0

		if not state.toStr() in self.q_data:
			return 0.0

		for act_move in self.q_data[state.toStr()]:
			r = self.q_data[state.toStr()][act_move] 
			if r > maxReward:
				maxReward = r

		return maxReward

	def process(self, wm):
		if self.currentState == None:## or len(wm.bombs) == 0:
			return
		#print "---->  ", wm.mytank, wm.bombs[0], self.calculateFitness(self.currentState)

		currentState  = self.currentState
		currentAction = self.currentAction
		nextState     = self.getWorldModelState(wm)
		if not nextState.toStr() in self.q_data:
			self.addState(nextState)

		if nextState.toStr() == self.currentState.toStr():
			return self.currentAction.move

		nextAction = self.getWeightedAction(nextState)

		if not currentState.toStr() in self.q_data:
			return

		if currentState.toStr() == nextState.toStr():
			return

		if not currentAction.move in self.q_data[currentState.toStr()]:
			return

		print self.q_data[currentState.toStr()]

		self.q_data[currentState.toStr()][currentAction.move] += self.alpha * (self.calculateFitness(currentState) + self.gamma * self.q_data[nextState.toStr()][nextAction.move] - self.q_data[currentState.toStr()][currentAction.move])
		saveDataBase(self.q_data)
		self.currentState  = nextState
		self.currentAction = nextAction
		#print self.q_data
		print len(self.q_data)
		return self.currentAction.move

	def getBestMove(self, wm):
		self.currentState = self.getWorldModelState(wm)
		state = self.currentState
		print state
		if not state.toStr() in self.q_data:
			print "NOOOOOOTHING"
			return basictypes.Actions.none
			#return self.currentAction.move

		maxReward = -9999999999999999999999999999999999999.0
		bestMove = None

		for act_move in self.q_data[state.toStr()]:
			r = self.q_data[state.toStr()][act_move] 
			if r > maxReward:
				maxReward = r
				bestMove  = act_move

		self.currentAction.move = bestMove

		print self.calculateFitness(state)
		print self.q_data[state.toStr()]
		return bestMove


	def __str__(self):
		return str(self.q_data)

