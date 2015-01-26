#! /usr/bin/python

__author__ = 'Amin'

from connection import *
from worldmodel import *
from menu import *
from gui import *
from menuinfo import *

from ai import QLearningAI
from ai2 import SarsaAI

import myparser as parser
import basictypes
import time
import copy


class Manager:
	def __init__(self):
		self.connection = Connection()
		self.wm         = WorldModel()
		self.menu       = Menu()
		self.gui        = GUI()
		self.info       = MenuInfo()

		self.ai_q     = QLearningAI()
		self.ai_sarsa = SarsaAI()

		self.command  = {}
		self.showgui  = True
		self.training = False


	def init(self):
		while True:
			self.menu.start()
			if not self.menu.donePressed():
				return False

			self.info  = self.menu.getMenuInfo()
			first_data = self.connection.connect(self.info.host, self.info.port)
			if first_data != None:
				first_data = first_data.split(' ')
				break

			self.menu.showMsg("host not found ...", "connection error")


		self.connection.startRecvThread()
		# first time connected
		##pid = self.connection.recv()
		self.info.pid = int(first_data[0])

		self.fillCommand(True)
		if not self.connection.send(parser.compress(parser.data2str(self.command))):
			return False

		self.wm.init(self.info.pid, first_data[1], int(first_data[2]))
		self.ai_q.init(copy.deepcopy(self.wm))
		self.ai_sarsa.init(copy.deepcopy(self.wm))
		self.gui.init(self.wm, self.info.monitor_width, self.info.monitor_height)

		if self.info.isAI:
			self.training = True

		return True


	def fillCommand(self, firstTime=False):
		self.command = {}
		self.command[basictypes.DataNames.pid]      = self.info.pid
		self.command[basictypes.DataNames.team]     = self.info.team
		self.command[basictypes.DataNames.tanktype] = self.info.tanktype

		if not firstTime:
			if self.info.isAI:
				self.command[basictypes.DataNames.action] = self.getActionsAI_QLearning()
				#self.command[basictypes.DataNames.action] = self.getActionsAI_SARSA()
			else:
				self.command[basictypes.DataNames.action] = self.gui.getActions()
				if self.training:
					if len(self.wm.bombs) == 0:
						self.command[basictypes.DataNames.action].append(basictypes.Actions.shoot)

			events = self.gui.getEvents()
			if basictypes.Events.pausegame in events:
				events = [basictypes.Events.pausegame]
			self.command[basictypes.DataNames.event] = events


	def handleEvents(self):
		events = self.gui.getEvents()

		if basictypes.Events.quitgame in events:
			self.connection.disconnect()

		if basictypes.Events.showgui in events:
			self.showgui = not self.showgui

		if basictypes.Events.training in events:
			self.training = not self.training

		if basictypes.Events.changebot in events:
			self.info.isAI = not self.info.isAI

	def getActionsAI_QLearning(self):
		if not self.training:
			self.ai_q.process(self.wm)
			return [self.ai_q.getBestMove(self.wm)]

		self.ai_q.process(self.wm)
		return [self.ai_q.pre_process(self.wm)]


	def getActionsAI_SARSA(self):
		if not self.training:
			return [self.ai_sarsa.getBestMove(self.wm)]

		return [self.ai_sarsa.process(self.wm)]

	def run(self):
		while self.connection.connected:
			start_time = time.time()

			recv_data = parser.str2data(parser.decompress(self.connection.recv()))
			#print "recv data = ", recv_data

			self.wm.update(recv_data)

			#print self.wm

			if self.showgui:
				winner = basictypes.Teams.none
				if self.wm.score_left >= self.wm.max_score:
					winner = basictypes.Teams.left
				elif self.wm.score_right >= self.wm.max_score:
					winner = basictypes.Teams.right

				self.gui.show(self.wm, winner)

			self.gui.fillActionsAndEvents()

			if self.showgui:
				self.gui.playSound(self.wm)

			self.fillCommand()

			send_data = parser.compress(parser.data2str(self.command))
			if not self.connection.send(send_data):
				break

			self.handleEvents()

			#print time.time() - start_time
			sleep_time = self.wm.cycle_time - (time.time() - start_time)
			if sleep_time < 0.0:
				sleep_time = 0
			time.sleep(sleep_time)


if __name__ == "__main__":
	m = Manager()
	if m.init():
		m.run()
