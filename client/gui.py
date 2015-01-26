#! /usr/bin/python

__author__ = 'Kiamehr'


########################################
from math import *                      #
import basictypes                       #
import guiconstvars                     #
import constvars                        #
import pygame                           #
from tank import *                      #
from pygame.locals import *             #
import random                           # 
import audio                            #
########################################




###########################################################
#______________________class gui__________________________#
###########################################################
###########################################################

class GUI:
	
###########################################################
	def __init__ (self):
		self.display_name   = guiconstvars.display_name

		self.screen  = None
		self.actions = []
		self.events  = []

		self.canShow = True

###########################################################
	def init(self, wm, monitor_width, monitor_height):
		
		
		
		
		
		self.monitor_width  = monitor_width
		self.monitor_height = monitor_height

		self.offset_width  = int(self.monitor_width / 10.0)
		self.offset_height = int(self.monitor_height / 10.0)

		pygame.init()
		self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height))
		
		
		
		pygame.display.set_caption(self.display_name)
		self.meter2pixel_height = self.monitor_height / wm.map.field_height
		self.meter2pixel_width  = self.monitor_width  / wm.map.field_width
		self.offset_height_area = float(self.offset_height)
		self.offset_width_area  = float(self.offset_width)
		self.whole_score = 0
		
		#playing main music and import other musics:
		self.audio = audio.Audio ()
		self.audio.init ()
		self.audio.play_background_music ()
		
		#loading images:
		self.background = wm.map.guiData.background.convert_alpha()
		self.background = pygame.transform.scale(self.background, (self.monitor_width, self.monitor_height) )

		self.pause_screen = wm.map.guiData.pause_screen.convert_alpha()
		self.pause_screen = pygame.transform.scale(self.pause_screen, (int(float(self.monitor_width)/3), int(float(self.monitor_height)/3)))
		self.pause_screen_pos = self.pause_screen.get_rect()
		self.pause_screen_pos.center = (self.monitor_width/2, self.monitor_height/2)
		
		self.tank_attacker_pic1 = wm.map.guiData.tank_attacker.convert_alpha() 
		self.tank_attacker_pic2 = pygame.transform.flip (wm.map.guiData.tank_attacker.convert_alpha(), True, False)
		self.attacker_pics = [self.tank_attacker_pic1, self.tank_attacker_pic2]
		
		self.tank_defender_pic1 = wm.map.guiData.tank_defender.convert_alpha()
		self.tank_defender_pic2 = pygame.transform.flip (wm.map.guiData.tank_defender.convert_alpha(), True, False)
		self.defender_pics = [self.tank_defender_pic1, self.tank_defender_pic2]
		
		
		self.loole = wm.map.guiData.launcher.convert_alpha()
		
		
		bomb_radius_new = int ( ( 1 - 2 * (self.offset_height_area / self.monitor_height)) * (wm.map.bomb_radius * self.meter2pixel_height) )
		self.bomb_pic_list = []
		for b in wm.map.guiData.bombs:
			bomb = b.convert_alpha()
			bomb = pygame.transform.scale (bomb , (2 * bomb_radius_new, 2 * bomb_radius_new))
			self.bomb_pic_list.append(bomb)
		self.goloole_pos = self.bomb_pic_list[0].get_rect ()
		
		self.digits = []
		for i in range (10) :
			self.digits.append (wm.map.guiData.digits[i].convert_alpha())

		self.block = wm.map.guiData.block.convert_alpha ()
		
		self.winner_left  = wm.map.guiData.winner_left.convert_alpha ()
		self.winner_right  = wm.map.guiData.winner_right.convert_alpha ()
######################################################

	def fillActionsAndEvents(self):


		self.actions = []
		self.events  = []

		#check for pressed keys - start

		pressed_keys = pygame.key.get_pressed()
		for index in guiconstvars.keys_actions_press:
			for key in guiconstvars.keys_actions_press[index]:
				if pressed_keys[key]:
					self.actions.append(index)

		#check for pressed keys - end

		#---------

		#check for tapped keys - start

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				for index in guiconstvars.keys_actions_down:
					if event.key in guiconstvars.keys_actions_down[index]:
						self.actions.append(index)

				for index in guiconstvars.keys_events:
					if event.key in guiconstvars.keys_events[index]:
						self.events.append(index)


			if event.type == pygame.QUIT:
				self.events.append(basictypes.Events.quitgame)
		#check for tapped keys - end



####################################################

	def getActions(self):
		return self.actions
####################################################
	def getEvents (self):
		return self.events

#################################################### for score

	def resized_pic_of_digit (self, pic) :
		width  = self.monitor_width -  2 * (self.offset_width)
		height = self.offset_height
		
		if width / 5.0 < height :
			return pygame.transform.scale (pic , (width / 10 - 4 , width / 5 - 8))
		return pygame.transform.scale (pic , (height / 2 - 4 , height  - 8))
#################################################### for digits
	def num2digits (self, num) :
		digits = []
		str_num = str (num)
		for i in str_num :
			digits.append (int (i))
		return digits

#################################################### for score
	def size_of_digits (self):
		width  = self.monitor_width -  2 * (self.offset_width)
		height = self.offset_height
		
		if width / 5.0 < height :
			return (width / 10 - 4, width / 5 - 8)
		return (height / 2 - 4 , height - 8)

#####################################################
	def show (self, wm, winner):
	
		if winner == basictypes.Teams.none :
			if not self.canShow:
				return 

			
			def changed_x_y  (pos_list):
					
				x2 = pos_list [0] + (wm.map.field_width / 2.0)
				y2 = -1 * pos_list [1] + wm.map.field_height
					
				return [x2, y2]



			# main window
			
			self.screen.blit (self.background, (0, 0))
			
			
				
			#drawing blocks
			
			for block in wm.map.blocks :
				
				
				block_new_pos = changed_x_y ([block.position.x, block.position.y])
				
				main_block_height = int ( ( 1 - 2 * (self.offset_height_area / self.monitor_height)) * (block.height * self.meter2pixel_height))
				main_block_width = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (block.width * self.meter2pixel_width) )
				block_y_pos = int ( (1 - 2 * (self.offset_height_area / self.monitor_height)) * (block_new_pos [1] * self.meter2pixel_height)) - (main_block_height//2) + (self.offset_height_area)
				block_x_pos = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (block_new_pos [0] * self.meter2pixel_width)) - (main_block_width//2) + (self.offset_width_area)
				block_height = int ( ( 1 - 2 * (self.offset_height_area / self.monitor_height)) * (0.5 * self.meter2pixel_height))
				block_width = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (0.5 * self.meter2pixel_width) )
					
				for i in range (0, int(block.height / 0.5)) : 
					
					for j in range (0, int(block.width / 0.5)) :
						
						self.screen.blit ( pygame.transform.scale (self.block, (block_width, block_height)), (block_x_pos+ block_width * j, block_y_pos+ block_height * i))
			
			
			 
			#drawing other tanks
			
			for pid in wm.tanks:
				tank = wm.tanks[pid]
				
				
				if tank.tanktype == basictypes.TankTypes.attacker :
					if tank.respawn_time < 0.0001 :
						tank_is_alive = True
					else:
						tank_is_alive = False
						
				if tank.tanktype == basictypes.TankTypes.attacker :
					
					if tank.team == basictypes.Teams.left :
						tank_pic = self.attacker_pics [0]
					else:
						tank_pic = self.attacker_pics [1]
					
				if tank.tanktype == basictypes.TankTypes.defender :
					
					if tank.team == basictypes.Teams.left :
						tank_pic = self.defender_pics [0]
					else:
						tank_pic = self.defender_pics [1]
				
				
				tank_new_pos = changed_x_y ([tank.position.x, tank.position.y])
				
				tank_height = int ( ( 1 - 2 * (self.offset_height_area / self.monitor_height)) * (tank.size.y * self.meter2pixel_height))
				tank_width = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (tank.size.x * self.meter2pixel_width) )
				tank_y_pos = int ( (1 - 2 * (self.offset_height_area / self.monitor_height)) * (tank_new_pos [1] * self.meter2pixel_height)) - (tank_height // 2) + (self.offset_height_area)
				tank_x_pos = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (tank_new_pos [0] * self.meter2pixel_width)) - (tank_width // 2) + (self.offset_width_area)
				
				if tank.tanktype == basictypes.TankTypes.attacker and tank_is_alive :
					self.screen.blit (pygame.transform.scale (tank_pic, (tank_width, tank_height)), (tank_x_pos, tank_y_pos))
				if tank.tanktype == basictypes.TankTypes.defender:
					self.screen.blit (pygame.transform.scale (tank_pic, (tank_width, tank_height)), (tank_x_pos, tank_y_pos))
				#drawing launcher for other tanks
				
				if tank.tanktype == basictypes.TankTypes.attacker and tank_is_alive:
					
					if tank.team == basictypes.Teams.left :
						launcher_start_position = 0
					else:
						launcher_start_position = tank_width
					
					loole = pygame.transform.scale(self.loole, (int(float(tank.launcherLength)* self.meter2pixel_width), int(float(tank.launcherLength)*self.meter2pixel_width / 5) ) )
					loole_pos =loole.get_rect ()
					tank_radian_direction = pi * tank.launcherDirection / 180.0
					
			
					tank_center_x = int (tank_x_pos + launcher_start_position + (loole_pos.width * cos (tank_radian_direction) / 2) )
					tank_center_y = int (-(loole_pos.width * sin (tank_radian_direction) / 2) + (tank_y_pos) )
						
					
						
					tank_luncher = pygame.transform.rotate (loole, tank.launcherDirection)
					tank_luncher_pos = tank_luncher.get_rect ()
					tank_luncher_pos.center = (tank_center_x, tank_center_y)
					self.screen.blit (tank_luncher, tank_luncher_pos)
			
				#drawing mana for other tanks
				
				if tank.team == basictypes.Teams.left :
					mana_start_position = 0
					mana_direction = 1
				else:
					mana_start_position = tank_width
					mana_direction = -1

				if tank.tanktype == basictypes.TankTypes.attacker :
					mana_height = tank_y_pos - (int(float(tank.launcherLength)*self.meter2pixel_width)) - 3
				else:
					mana_height = tank_y_pos - (int(float(0.2)*self.meter2pixel_width)) - 3
				tank_mana = tank.mana
				if tank.team == basictypes.Teams.left :
					tank_color = wm.map.guiData.tank_colors_mana.left
				else :
					tank_color = wm.map.guiData.tank_colors_mana.right
				
				if tank.tanktype == basictypes.TankTypes.defender:
					pygame.draw.line (self.screen, tank_color , (tank_x_pos + mana_start_position, mana_height), (tank_x_pos + mana_start_position + (mana_direction * int(tank_mana) * tank_width/100), mana_height), 2)
				if tank.tanktype == basictypes.TankTypes.attacker and tank_is_alive :
					pygame.draw.line (self.screen, tank_color , (tank_x_pos + mana_start_position, mana_height), (tank_x_pos + mana_start_position + (mana_direction * int(tank_mana) * tank_width/100), mana_height), 2)
				
			
			
			
			#drawing health for other tanks
				if tank.tanktype == basictypes.TankTypes.attacker :
					if tank.team == basictypes.Teams.left :
						health_start_position = 0
						health_direction = 1
					else:
						health_start_position = tank_width
						health_direction = -1

					if tank.tanktype == basictypes.TankTypes.attacker :
						health_height = tank_y_pos - (int(float(tank.launcherLength)*self.meter2pixel_width)) - 10
					else:
						mana_height = tank_y_pos - (int(float(0.2)*self.meter2pixel_width)) - 10
					tank_health = tank.health
					if tank.team == basictypes.Teams.left :
						tank_color = wm.map.guiData.tank_colors_health.left
					else :
						tank_color = wm.map.guiData.tank_colors_health.right
					if tank.tanktype == basictypes.TankTypes.defender:
						pygame.draw.line (self.screen, tank_color , (tank_x_pos + health_start_position, health_height), (tank_x_pos + health_start_position + (health_direction * int(tank_health) * tank_width/100), health_height), 2)	
					if tank.tanktype == basictypes.TankTypes.attacker and tank_is_alive :
						pygame.draw.line (self.screen, tank_color , (tank_x_pos + health_start_position, health_height), (tank_x_pos + health_start_position + (health_direction * int(tank_health) * tank_width/100), health_height), 2)	
					
			#drawing my tank 
			
			if isinstance(wm.mytank, Tank):
				
			
				if wm.mytank.tanktype == basictypes.TankTypes.attacker :
					if wm.mytank.respawn_time < 0.0001 :
						mytank_is_alive = True
						
					else:
						mytank_is_alive = False
					
				if wm.mytank.tanktype == basictypes.TankTypes.attacker :
					
					if wm.mytank.team == basictypes.Teams.left :
						mytank_pic = self.attacker_pics [0]
					else:
						mytank_pic = self.attacker_pics [1]
					
				if wm.mytank.tanktype == basictypes.TankTypes.defender :
					
					if wm.mytank.team == basictypes.Teams.left :
						mytank_pic = self.defender_pics [0]
					else:
						mytank_pic = self.defender_pics [1]
				
				mytank_new_pos = changed_x_y ([wm.mytank.position.x,  wm.mytank.position.y])
					
				mytank_height = int ( ( 1 - 2 * (self.offset_height_area / self.monitor_height)) * (wm.mytank.size.y * self.meter2pixel_height))
				mytank_width = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (wm.mytank.size.x * self.meter2pixel_width) )
				mytank_y_pos = int ( (1 - 2 * (self.offset_height_area / self.monitor_height)) * (mytank_new_pos [1] * self.meter2pixel_height)) - (mytank_height // 2) + (self.offset_height_area)
				mytank_x_pos = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (mytank_new_pos [0] * self.meter2pixel_width)) - (mytank_width // 2) + (self.offset_width_area)
					
				if wm.mytank.tanktype == basictypes.TankTypes.attacker and mytank_is_alive :
					self.screen.blit (pygame.transform.scale (mytank_pic, (mytank_width, mytank_height)), (mytank_x_pos, mytank_y_pos))
				if wm.mytank.tanktype == basictypes.TankTypes.defender:
					self.screen.blit (pygame.transform.scale (mytank_pic, (mytank_width, mytank_height)), (mytank_x_pos, mytank_y_pos))
				
				#drawing luncher for my tank
				
				if wm.mytank.tanktype == basictypes.TankTypes.attacker and mytank_is_alive:
					
					if wm.mytank.team == basictypes.Teams.left :
						launcher_start_position = 0
					else:
						launcher_start_position = mytank_width
					
					mytank_radian_direction = pi * wm.mytank.launcherDirection / 180.0
					loole = pygame.transform.scale(self.loole, (int(float(wm.mytank.launcherLength)* self.meter2pixel_width), int(float(wm.mytank.launcherLength)*self.meter2pixel_width / 5) ) )
					loole_pos =loole.get_rect ()
					mytank_center_x = int (mytank_x_pos + launcher_start_position + (loole_pos.width * cos (mytank_radian_direction) / 2) )
					mytank_center_y = int (-(loole_pos.width * sin (mytank_radian_direction) / 2) + (mytank_y_pos) )
				
					
					
						
					mytank_luncher = pygame.transform.rotate (loole, wm.mytank.launcherDirection)
					mytank_luncher_pos = mytank_luncher.get_rect ()
					mytank_luncher_pos.center = (mytank_center_x, mytank_center_y)
					self.screen.blit (mytank_luncher, mytank_luncher_pos)
			
				#drawing mana for my tank
			
				if wm.mytank.team == basictypes.Teams.left :
					mana_start_position = 0
					mana_direction = 1
				else:
					mana_start_position = mytank_width
					mana_direction = -1

				if wm.mytank.tanktype == basictypes.TankTypes.attacker :
					mana_height = mytank_y_pos - (int(float(wm.mytank.launcherLength)*self.meter2pixel_width)) - 3
				else:
					mana_height = mytank_y_pos - (int(float(0.2)*self.meter2pixel_width)) - 3
				mytank_mana = wm.mytank.mana
				if wm.mytank.tanktype == basictypes.TankTypes.attacker and mytank_is_alive:
					pygame.draw.line (self.screen, wm.map.guiData.tank_colors_mana.me , (mytank_x_pos + mana_start_position, mana_height), (mytank_x_pos + mana_start_position + (mana_direction * int(mytank_mana) * mytank_width/100), mana_height), 2)
				if wm.mytank.tanktype == basictypes.TankTypes.defender :
					pygame.draw.line (self.screen, wm.map.guiData.tank_colors_mana.me , (mytank_x_pos + mana_start_position, mana_height), (mytank_x_pos + mana_start_position + (mana_direction * int(mytank_mana) * mytank_width/100), mana_height), 2)
			
			#drawing health for my tank
				if wm.mytank.tanktype == basictypes.TankTypes.attacker :
					if wm.mytank.team == basictypes.Teams.left :
						health_start_position = 0
						health_direction = 1
					else:
						health_start_position = mytank_width
						health_direction = -1

					if wm.mytank.tanktype == basictypes.TankTypes.attacker :
						health_height = mytank_y_pos - (int(float(wm.mytank.launcherLength)*self.meter2pixel_width)) - 10
					else:
						health_height = mytank_y_pos - (int(float(0.2)*self.meter2pixel_width)) - 10
					mytank_health = wm.mytank.health
					if wm.mytank.tanktype == basictypes.TankTypes.attacker and mytank_is_alive:
						pygame.draw.line (self.screen, wm.map.guiData.tank_colors_health.me , (mytank_x_pos + health_start_position, health_height), (mytank_x_pos + health_start_position + (health_direction * int(mytank_health) * mytank_width/100), health_height), 2)
					if wm.mytank.tanktype == basictypes.TankTypes.defender:
						pygame.draw.line (self.screen, wm.map.guiData.tank_colors_health.me , (mytank_x_pos + health_start_position, health_height), (mytank_x_pos + health_start_position + (health_direction * int(mytank_health) * mytank_width/100), health_height), 2)
					
			#drawing bombs

			for bomb in wm.bombs:
				
				bomb_new_pos = changed_x_y ([bomb.position.x, bomb.position.y])
				bomb_y_pos = int ( (1 - 2 * (self.offset_height_area / self.monitor_height)) * (bomb_new_pos [1] * self.meter2pixel_height)) + (self.offset_height_area)
				bomb_x_pos = int ( ( 1 - 2 * (self.offset_width_area / self.monitor_width)) * (bomb_new_pos [0] * self.meter2pixel_width)) + (self.offset_width_area)
				
				bomb_pic = self.bomb_pic_list [bomb.bid % 5]
				bomb_pic_pos = self.goloole_pos
				bomb_pic_pos.center = (bomb_x_pos, bomb_y_pos) 

				self.screen.blit (bomb_pic, bomb_pic_pos)
			
			
			#score
			
			
			score_left = self.num2digits (wm.score_left)
			score_right = self.num2digits (wm.score_right)
			
			start_pos = (self.offset_width_area + 2 , self.offset_height_area - self.size_of_digits ()[1] - 4 )
			for i in score_left :
				self.screen.blit (self.resized_pic_of_digit (self.digits [i]), start_pos)
				start_pos = (start_pos [0] + self.size_of_digits ()[0] , start_pos [1])
			
			start_pos = (self.monitor_width - self.offset_width_area - self.size_of_digits ()[0] - 2 , self.offset_height_area - self.size_of_digits ()[1] - 4 )
			
			for j in range (len (score_right)) :
				i = score_right [len (score_right) - j - 1]
				self.screen.blit (self.resized_pic_of_digit (self.digits [i]), start_pos)
				start_pos = (start_pos [0] - self.size_of_digits ()[0] , start_pos [1])
			
			
			
			
			
			#respawn time:
			if isinstance(wm.mytank, Tank):
				if wm.mytank.tanktype == basictypes.TankTypes.attacker and not mytank_is_alive:
					respawn_time_list = self.num2digits (int (wm.mytank.respawn_time))
					start_pos = int ((self.monitor_width // 2 ) - ((len (respawn_time_list) *  ((self.monitor_height - 2*self.offset_height)//2)) // 2))
					for respawn_time in respawn_time_list :
						self.screen.blit (pygame.transform.scale (self.digits [respawn_time] , ( (self.monitor_height - 2*self.offset_height)//2, (self.monitor_height - 2*self.offset_height))), (start_pos, self.offset_height))
						start_pos = start_pos + (self.monitor_height - 2*self.offset_height)//2
			#drawing pause screen
			
			if wm.game_state  == basictypes.GameStates.pause :
				self.screen.blit (self.pause_screen, self.pause_screen_pos)
			#updating!
			
			pygame.display.update()
		
		else :
			self.show_winner (winner)                             
#####################################################
	def playSound (self, wm):
		
		if isinstance(wm.mytank, Tank):
			if wm.mytank.tanktype == basictypes.TankTypes.attacker :
					if wm.mytank.respawn_time < 0.0001 :
						mytank_is_alive = True
					else:
						mytank_is_alive = False
					
			if not wm.game_state  == basictypes.GameStates.pause and wm.mytank.tanktype == basictypes.TankTypes.attacker:
				if mytank_is_alive:
					#play sound of shoot of my tank attacker:
					if basictypes.Actions.shoot in self.getActions() :
						if wm.mytank.mana >= wm.mytank.manaCost :
							self.audio.play_tank_shoot ()
					#play sound of movement of my tank :
					if basictypes.Actions.goleft in self.getActions()  or  basictypes.Actions.goright in self.getActions() :
						self.audio.play_tank_movement()
				
			if not wm.game_state  == basictypes.GameStates.pause  and wm.mytank.tanktype == basictypes.TankTypes.defender:
				#play sound of jump of my tank defender:
				if basictypes.Actions.jump in self.getActions() :
					if wm.mytank.mana >= wm.mytank.manaCost :
						self.audio.play_tank_jump ()
				
				#play sound of movement of my tank defender:
				if basictypes.Actions.goleft in self.getActions()  or  basictypes.Actions.goright in self.getActions() :
					self.audio.play_tank_movement()
					
		#play sound when get shot :
		whole_score = wm.score_left + wm.score_right
		if wm.score_left == 0 and wm.score_right == 0:
			self.whole_score = 0
		if self.whole_score < whole_score :
			self.whole_score = whole_score
			self.audio.play_get_shot_sound ()
		
####################################################

	def show_winner (self, team):
		if team == basictypes.Teams.right :
			self.screen.blit (pygame.transform.scale (self.winner_right , (self.monitor_width, self.monitor_height)), (0, 0))
		if team == basictypes.Teams.left :
			self.screen.blit (pygame.transform.scale (self.winner_left , (self.monitor_width, self.monitor_height)), (0, 0))
		
		pygame.display.update ()
