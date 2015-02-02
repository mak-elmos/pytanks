#! /usr/bin/python

__author__ = 'Milad & Amin'

from attackertank import *
from defendertank import *
from block import *
from bomb import *

import constvars
import basictypes
import random
import math
import copy


class Handler(object):
	def __init__(self):
		pass
		
	@staticmethod
	def randomStartPosition(wm, tank_team):
		tank_height = AttackerTank.size.y
		tank_width  = AttackerTank.size.x
		if tank_team == basictypes.Teams.right:
			return Vector(random.uniform(tank_width, wm.field_width / 2.0 - tank_width), wm.field_height / 2.0)
		else:
			return Vector(random.uniform(- (wm.field_width / 2.0 - tank_width), - tank_width), wm.field_height / 2.0)

	@staticmethod
	def sign(var):
		if var == 0:
			return 0
		elif var > 0:
			return 1
		else:
			return -1		

	@staticmethod			
	def addTank(wm, data):
		position = Handler.randomStartPosition(wm, data[basictypes.DataNames.team])
		if data[basictypes.DataNames.tanktype] == basictypes.TankTypes.attacker:
			wm.tanks[data[basictypes.DataNames.pid]] = AttackerTank(team=data[basictypes.DataNames.team], pos=position)
			wm.tanks[data[basictypes.DataNames.pid]].launcherDirection = AttackerTank.launcherDirection_first
			if data[basictypes.DataNames.team] == basictypes.Teams.right:
				wm.tanks[data[basictypes.DataNames.pid]].launcherDirection = 180 - AttackerTank.launcherDirection_first
			wm.tanks_lastSeen[data[basictypes.DataNames.pid]] = 0
		elif data[basictypes.DataNames.tanktype] == basictypes.TankTypes.defender:
			wm.tanks[data[basictypes.DataNames.pid]] = DefenderTank(team=data[basictypes.DataNames.team], pos=position)
			wm.tanks_lastSeen[data[basictypes.DataNames.pid]] = 0
		else: 
			raise Exception("types of tank must be <attacker> or <defender>")

	@staticmethod			
	def resetTank(wm, tank):
		"""reset a tank after destroyed"""
		
		tank.health = tank.healthMax
		tank.mana = tank.manaMax
		tank.position = Handler.randomStartPosition(wm, tank.team)
		tank.velocity = Vector(0, 0)
		tank.acceleration = Vector(0, 0)
		if tank.team == basictypes.Teams.right:
			tank.launcherDirection = 180.0 - tank.launcherDirection_first
		else:
			tank.launcherDirection = tank.launcherDirection_first
		tank.respawn_time = 0
		Handler.deleteRespawningTank(wm, tank)

	@staticmethod		
	def deleteDestroyedTank(wm, tank):
		for pid in wm.tanks.keys():
			if wm.tanks[pid] == tank:
				wm.respawning_tanks[pid] = copy.deepcopy(wm.tanks[pid])
				del wm.tanks[pid]

	@staticmethod
	def deleteRespawningTank(wm, tank):
		for pid in wm.respawning_tanks.keys():
			if wm.respawning_tanks[pid] == tank:
				wm.tanks[pid] = copy.deepcopy(wm.respawning_tanks[pid])
				del wm.respawning_tanks[pid]
				#del wm.tanks_lastSeen[pid]

	@staticmethod			
	def destroyTank(wm, tank):
		if tank.team == basictypes.Teams.right:
			wm.score_left  += wm.destroyingScore
		else:
			wm.score_right += wm.destroyingScore	

		tank.position = Vector(0, 0)
		tank.velocity = Vector(0, 0)
		tank.acceleration = Vector(0, 0)
		tank.respawn_time = tank.respawn_time_default
		Handler.deleteDestroyedTank(wm, tank)	

	@staticmethod				
	def isOnAir(obj):
		"""return true if object isn't on a <block> """
		if obj.velocity.y == 0 and obj.acceleration.y == 0:
			if obj.last_velocity_y_sign == 1:   
				return True
			return False
		return True

	@staticmethod	
	def tank_jump(tank):
		if not isinstance (tank, DefenderTank):
			return
		if tank.mana < tank.manaCost:
			return
		tank.mana -= tank.manaCost
		tank.velocity.y = tank.jumpSpeed
	
	@staticmethod	
	def tank_goRight(tank):
		if Handler.isOnAir(tank):
			return
		if isinstance(tank, AttackerTank):
			tank.velocity.x = +tank.speed * tank.health / tank.healthMax
		else:
			tank.velocity.x = +tank.speed 

	@staticmethod	
	def tank_goLeft(tank):
		if Handler.isOnAir(tank):
			return
		if isinstance(tank, AttackerTank):
			tank.velocity.x = -tank.speed * tank.health / tank.healthMax
		else:
			tank.velocity.x = -tank.speed 

	@staticmethod
	def tank_increaseAngle(wm, tank):
		if not isinstance(tank, AttackerTank):
			return
		if tank.team == basictypes.Teams.right:
			if tank.launcherDirection - tank.launcherDirection_speed * wm.cycle_time >= 180 - tank.launcherDirection_max:
				tank.launcherDirection -= tank.launcherDirection_speed * wm.cycle_time
		else:
			if tank.launcherDirection + tank.launcherDirection_speed * wm.cycle_time <= tank.launcherDirection_max:
				tank.launcherDirection += tank.launcherDirection_speed * wm.cycle_time

	@staticmethod
	def tank_decreaseAngle(wm, tank):
		"""decrease angle of an <attackerTank> object """
		if not isinstance(tank, AttackerTank):
			return
			
		if tank.team == basictypes.Teams.right:
			if tank.launcherDirection + tank.launcherDirection_speed * wm.cycle_time <= 180 - tank.launcherDirection_min:
				tank.launcherDirection += tank.launcherDirection_speed * wm.cycle_time
		else:
			if tank.launcherDirection - tank.launcherDirection_speed * wm.cycle_time >= tank.launcherDirection_min:
				tank.launcherDirection -= tank.launcherDirection_speed * wm.cycle_time

	@staticmethod
	def tank_shoot(wm, tank):
		if not isinstance(tank, AttackerTank):
			return
		if tank.mana < tank.manaCost:
			return

		cos = math.cos(math.radians(tank.launcherDirection))
		sin = math.sin(math.radians(tank.launcherDirection))
		tank.mana -= tank.manaCost
		wm.bombs.append(Bomb(wm.bombs_counter, Vector(tank.position.x - Handler.sign(cos) * tank.size.x /2.0 + tank.launcherLength * cos, tank.position.y + tank.size.y /2.0 + tank.launcherLength * sin),
							Vector(tank.shootSpeed * cos + tank.velocity.x, tank.shootSpeed * sin + tank.velocity.y), Vector(0, wm.physics_gravity)))	
		tank.velocity -= Vector(tank.shootSpeed * cos, tank.shootSpeed * sin) * tank.momentum_const
		wm.bombs_counter += 1

	@staticmethod	
	def remove_bomb(wm, bomb):
		"""remove a bomb from worldModel """
		if bomb in wm.bombs: 
			wm.bombs.remove(bomb)

	@staticmethod		
	def bomb_explosion(wm, bomb, obj):
		if isinstance(obj, Tank):
			if isinstance(obj, AttackerTank):
				obj.health -= obj.healthCost
				if obj.health <= 0:
					Handler.destroyTank(wm, obj)
			obj.velocity += bomb.velocity * obj.explosion_const
		Handler.remove_bomb(wm, bomb)

	@staticmethod	
	def checkCollision(wm, obj):  
		if not isinstance(obj, DynamicObject):
			return 
		#check collision for bomb
		if isinstance(obj, Bomb):
			
			before_x = obj.position.x + Handler.sign(obj.velocity.x) * obj.radius
			after_x  = obj.position.x + Handler.sign(obj.velocity.x) * obj.radius + wm.cycle_time * obj.velocity.x + .5 *  (wm.cycle_time ** 2) * obj.acceleration.x
			before_y = obj.position.y + Handler.sign(obj.velocity.y) * obj.radius
			after_y  = obj.position.y + Handler.sign(obj.velocity.y) * obj.radius + wm.cycle_time * obj.velocity.y + .5 *  (wm.cycle_time ** 2) * obj.acceleration.y
			for block in wm.blocks:
				condition_x = cmp(before_x, block.position.x - Handler.sign(obj.velocity.x) * block.width / 2.0) * cmp(after_x, block.position.x - Handler.sign(obj.velocity.x) * block.width / 2.0) <= 0 and abs(obj.position.y - block.position.y) < obj.radius + block.height / 2.0          
				condition_y = cmp(before_y, block.position.y - Handler.sign(obj.velocity.y) * block.height / 2.0) * cmp(after_y, block.position.y - Handler.sign(obj.velocity.y) * block.height / 2.0) <= 0 and abs(obj.position.x - block.position.x) < obj.radius + block.width / 2.0
				condition_2 = abs((block.position - obj.position).x) < obj.radius + block.width / 2.0 and abs((block.position - obj.position).y) <= obj.radius + block.height / 2
				if condition_x or condition_y or condition_2:
					Handler.bomb_explosion(wm, obj, block)
					break

			for tank in wm.tanks.values():
				if abs((tank.position - obj.position).x) < obj.radius + tank.size.x / 2.0 and abs((tank.position - obj.position).y) <= obj.radius + tank.size.y / 2: 
					Handler.bomb_explosion(wm, obj, tank)

		#check collision for tank
		elif isinstance(obj, Tank):
			if cmp(obj.velocity.x, 0) * cmp(obj.velocity.x + obj.acceleration.x * wm.cycle_time, 0) < 0:
				obj.velocity.x = 0
			before_x = obj.position.x + Handler.sign(obj.velocity.x) * obj.size.x / 2.0
			after_x  = obj.position.x + Handler.sign(obj.velocity.x) * obj.size.x / 2.0 + wm.cycle_time * obj.velocity.x + .5 *  (wm.cycle_time ** 2) * obj.acceleration.x
			before_y = obj.position.y + Handler.sign(obj.velocity.y) * obj.size.y / 2.0
			after_y  = obj.position.y + Handler.sign(obj.velocity.y) * obj.size.y / 2.0 + wm.cycle_time * obj.velocity.y + .5 *  (wm.cycle_time ** 2) * obj.acceleration.y
			
			for block in wm.blocks:
				condition_x = cmp(before_x, block.position.x - Handler.sign(obj.velocity.x) * block.width / 2.0) * cmp(after_x, block.position.x - Handler.sign(obj.velocity.x) * block.width / 2.0) <= .001 and abs(obj.position.y - block.position.y)  <= obj.size.y / 2.0 + block.height / 2.0 + .001        
				condition_y = cmp(before_y, block.position.y - Handler.sign(obj.velocity.y) * block.height / 2.0) * cmp(after_y, block.position.y - Handler.sign(obj.velocity.y) * block.height / 2.0) <= .001 and abs(obj.position.x  - block.position.x)  <= obj.size.x / 2.0 + block.width / 2.0 + .001
				if condition_x:
					obj.velocity.x = 0
					obj.acceleration.x = 0
				if condition_y:
					obj.last_velocity_y_sign = Handler.sign(obj.velocity.y)
					obj.velocity.y = 0
					obj.acceleration.y = 0 

	@staticmethod				
	def updateAcceleration(wm, obj):
		#obj is now just tank 
		if Handler.isOnAir(obj):
			obj.acceleration = Vector(0, wm.physics_gravity)
		else:
			obj.acceleration = Vector(-Handler.sign(obj.velocity.x) * obj.mu, wm.physics_gravity)  	

	@staticmethod
	def tank_updateManaAndHealthAndLauncher(wm, tank):
		if isinstance(tank, AttackerTank):
			if tank.health < tank.healthMax:
				if tank.health + tank.healthReg * wm.cycle_time > tank.healthMax:
					tank.health = tank.healthMax
				else:
					tank.health += tank.healthReg * wm.cycle_time
			tank.launcherLength = tank.launcherLength_min + (tank.mana / tank.manaMax) * (tank.launcherLength_max - tank.launcherLength_min)
		
		if tank.mana < tank.manaMax:
			if tank.mana + tank.manaReg * wm.cycle_time > tank.manaMax:
				tank.mana = tank.manaMax
			else:
				tank.mana += tank.manaReg * wm.cycle_time
				if isinstance(tank, AttackerTank):
					tank.mana += ((tank.healthMax - tank.health) / tank.healthMax) * tank.manaReg * wm.cycle_time

	@staticmethod	
	def updateVelocity(wm, obj):
		if not isinstance(obj, DynamicObject):
			return TypeError("the argument must be a <DynamicObject>")
		
		obj.velocity += obj.acceleration * wm.cycle_time
		
		Handler.checkCollision(wm, obj)

	@staticmethod	
	def updatePosition(wm, obj):
		obj.position.x += obj.velocity.x * wm.cycle_time + .5 * obj.acceleration.x * wm.cycle_time ** 2.0
		obj.position.y += obj.velocity.y * wm.cycle_time + .5 * obj.acceleration.y * wm.cycle_time ** 2.0

	@staticmethod
	def doActions(wm, tank, actions):
		if type(actions) != list:
			return

		if basictypes.Actions.shoot in actions:
			Handler.tank_shoot(wm, tank)
		if basictypes.Actions.jump in actions:
			Handler.tank_jump(tank)
		if basictypes.Actions.goright in actions:
			Handler.tank_goRight(tank)
		if basictypes.Actions.goleft in actions:
			Handler.tank_goLeft(tank)
		if basictypes.Actions.increaseangle in actions:
			Handler.tank_increaseAngle(wm, tank)
		if basictypes.Actions.decreaseangle in actions:
			Handler.tank_decreaseAngle(wm, tank)

	@staticmethod		
	def updateRespawningTank(wm, tank):
		tank.respawn_time -= wm.cycle_time
		if tank.respawn_time <= 0:
			Handler.resetTank(wm, tank)
			
		
###############################################	

	@staticmethod
	def deleteDisconnectedTanks(wm):
		tanks = dict(wm.tanks.items() + wm.respawning_tanks.items())
		for pid in tanks.keys():
			if wm.tanks_lastSeen[pid] > constvars.max_disconnectTime:
				wm.disconnected_tanks[pid] = copy.deepcopy(tanks[pid])
				if pid in wm.tanks:
					del wm.tanks[pid]
				elif pid in wm.respawning_tanks:
					del wm.respawning_tanks[pid]
				#del Handler.tanks_lastSeen[pid]

	@staticmethod
	def updateLastSeenTanks(wm):
		for pid in wm.tanks_lastSeen:
			wm.tanks_lastSeen[pid] += 1

	@staticmethod	
	def update(wm, allClientsData):
		for data in allClientsData:
			if type(data) == dict and basictypes.DataNames.pid in data:
				pid = data[basictypes.DataNames.pid]
				wm.tanks_lastSeen[pid] = 0
				if pid in wm.disconnected_tanks:
					if isinstance(wm.disconnected_tanks[pid], AttackerTank) and wm.disconnected_tanks[pid].respawn_time > 0.0:
						wm.respawning_tanks[pid] = copy.deepcopy(wm.disconnected_tanks[pid])
					else:
						wm.tanks[pid] = copy.deepcopy(wm.disconnected_tanks[pid])
					del wm.disconnected_tanks[pid]
				elif pid in wm.respawning_tanks:
					pass #age bad az mordan leave beede be fana mire ehtemalan
				elif not pid in wm.tanks:
					Handler.addTank(wm, data)
				else:
					if basictypes.DataNames.action in data:
						Handler.doActions(wm, wm.tanks[pid], data[basictypes.DataNames.action])
		Handler.deleteDisconnectedTanks(wm)
		Handler.updateLastSeenTanks(wm)	

		bomb_index = len(wm.bombs) - 1
		while bomb_index >=0:
			Handler.updateAcceleration(wm, wm.bombs[bomb_index])
			Handler.updateVelocity(wm, wm.bombs[bomb_index])
			bomb_index -=1

		bomb_index = len(wm.bombs) - 1
		while bomb_index >=0:
			Handler.updatePosition(wm, wm.bombs[bomb_index])
			bomb_index -= 1

		for pid in wm.tanks.keys():
			Handler.updateAcceleration(wm, wm.tanks[pid])
			Handler.updateVelocity(wm, wm.tanks[pid])
			Handler.updatePosition(wm, wm.tanks[pid])
			Handler.tank_updateManaAndHealthAndLauncher(wm, wm.tanks[pid])

		##updating respawning tanks
		for pid in wm.respawning_tanks.keys():
			Handler.updateRespawningTank(wm, wm.respawning_tanks[pid])	

