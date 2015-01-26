#! /usr/bin/python

__author__ = 'Amin'

from connection import *
from handler import *
from worldmodel import *
from gamemap import *
import myparser as parser
import time
import constvars

class Manager:
	def __init__(self):
		self.connection = Connection()
		self.wm         = WorldModel()
		self.cycle_time = constvars.network_cycle_time

	def init(self):
		#print "your ip:", socket.gethostname()
		host    = raw_input("enter server ip: ")
		port    = raw_input("enter server port: ")
		mapname = raw_input("enter map name: ")
		self.max_score = input("enter max score: ")

		self.connection.startServer(host, int(port))
		self.connection.startAcceptThread(mapname, self.max_score)
		self.loadMapAndFillObjects(mapname)


	def loadMapAndFillObjects(self, mapname):
		gamemap = loadMap(mapname)

		### tank
    		Tank.respawn_time_default = gamemap.tank_respawn_time_default
    		Tank.respawn_time         = 0.0


		### attacker tank
        	AttackerTank.size       = Vector(gamemap.attacker_width, gamemap.attacker_height)
		AttackerTank.shootSpeed = gamemap.attacker_shootSpeed
		AttackerTank.speed      = gamemap.attacker_speed
		AttackerTank.mu         = gamemap.attacker_mu

		AttackerTank.mana       = gamemap.attacker_manaMax
		AttackerTank.manaMax    = gamemap.attacker_manaMax
		AttackerTank.manaReg    = gamemap.attacker_manaReg
		AttackerTank.manaCost   = gamemap.attacker_manaCost

		AttackerTank.health     = gamemap.attacker_healthMax
		AttackerTank.healthMax  = gamemap.attacker_healthMax
		AttackerTank.healthReg  = gamemap.attacker_healthReg
		AttackerTank.healthCost = gamemap.attacker_healthCost

        	AttackerTank.launcherLength_min = gamemap.attacker_launcherLength_min
        	AttackerTank.launcherLength_max = gamemap.attacker_launcherLength_max
        	AttackerTank.launcherLength     = gamemap.attacker_launcherLength_max - gamemap.attacker_launcherLength_min

		AttackerTank.launcherDirection_first = gamemap.attacker_launcherDirection_first
		AttackerTank.launcherDirection_max   = gamemap.attacker_launcherDirection_max
	 	AttackerTank.launcherDirection_min   = gamemap.attacker_launcherDirection_min
	 	AttackerTank.launcherDirection_speed = gamemap.attacker_launcherDirection_speed

	 	AttackerTank.explosion_const = gamemap.attacker_explosion_const
		AttackerTank.momentum_const  = gamemap.attacker_momentum_const

	        ### defender tank
        	DefenderTank.size      = Vector(gamemap.defender_width, gamemap.defender_height)
		DefenderTank.speed     = gamemap.defender_speed
		DefenderTank.mu        = gamemap.defender_mu
		DefenderTank.mana      = gamemap.defender_manaMax
		DefenderTank.manaMax   = gamemap.defender_manaMax
		DefenderTank.manaReg   = gamemap.defender_manaReg
		DefenderTank.manaCost  = gamemap.defender_manaCost
		DefenderTank.jumpSpeed = gamemap.defender_jumpSpeed

		DefenderTank.explosion_const = gamemap.defender_explosion_const

	        ### bomb
		Bomb.radius = gamemap.bomb_radius


		### worldmodel
		WorldModel.field_width  = gamemap.field_width
		WorldModel.field_height = gamemap.field_height

		WorldModel.physics_gravity = gamemap.physics_gravity
		WorldModel.cycle_time      = gamemap.physics_cycle_time

		WorldModel.blocks          = gamemap.blocks



	def handleEvents(self, allData):
		for data in allData:
			if type(data) == dict and basictypes.DataNames.event in data:
				events = data[basictypes.DataNames.event]

				if basictypes.Events.pausegame in events:
					if self.wm.game_state == basictypes.GameStates.play:
						self.wm.game_state = basictypes.GameStates.pause
					else:
						self.wm.game_state = basictypes.GameStates.play

				del data[basictypes.DataNames.event]

	def run(self):
		#cycle_counter = 0
		#cycle_update  = int(self.wm.cycle_time / self.cycle_time)
		while True:
			start_time = time.time()

			send_data = parser.wm2data(self.wm)
			#print "-------> send data = ", send_data
			send_data = parser.compress(parser.data2str(send_data))
			self.connection.sendAll(send_data)
			#print "send_len = ", len(send_data)

			if self.wm.score_right >= self.max_score or self.wm.score_left >= self.max_score:
				time.sleep(5)
				del self.wm
				self.wm = WorldModel()


			recv_data = self.connection.recvAll()
			#print "-------> recv data = ", recv_data
			#for i in range(len(recv_data)):
			#	print "recv_len", i, "= ", len(recv_data[i])
			for i in range(len(recv_data)):
				recv_data[i] = parser.str2data(parser.decompress(recv_data[i]))

			self.handleEvents(recv_data)
			if self.wm.game_state == basictypes.GameStates.play:
				#if cycle_counter % cycle_update == 0:
				Handler.update(self.wm, recv_data)

				#cycle_counter += 1

			#print time.time() - start_time
			sleep_time = self.cycle_time - (time.time() - start_time)
			if sleep_time < 0.0:
				sleep_time = 0
			time.sleep(sleep_time)


if __name__ == "__main__":
	m = Manager()
	server_started = False
	try:
		m.init()
		server_started = True
	except:
		print "Starting server failed ..."

	if server_started:
		m.run()
