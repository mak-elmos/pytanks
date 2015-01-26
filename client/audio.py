#! /usr/bin/python

__author__ = 'Kia'

import pygame
import pygame.locals
import random
class Audio:
	def __init__(self):
		pass

	def init(self):
		pygame.init ()
		pygame.mixer.init ()
		pygame.mixer.pre_init (44100, -16, 2, 2048)
		pygame.mixer.set_num_channels(8)
		self.main_music = pygame.mixer.Sound('sounds/main_music.wav')
		self.main_music_chanel = pygame.mixer.Channel(1)
		
		self.get_shot1 = pygame.mixer.Sound('sounds/get_shot1.wav')
		self.get_shot2 = pygame.mixer.Sound('sounds/get_shot2.wav')
		self.get_shot3 = pygame.mixer.Sound('sounds/get_shot3.wav')
		self.get_shot_sounds = [self.get_shot1, self.get_shot2, self.get_shot3]
		self.get_shot_sounds_chanel = pygame.mixer.Channel(2)
		self.move_sound = pygame.mixer.Sound('sounds/move.wav')
		self.move_sound_chanel = pygame.mixer.Channel(3)
		self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
		self.jump_sound_chanel = pygame.mixer.Channel(4)
		self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
		self.shoot_sound_chanel = pygame.mixer.Channel(5)
	def play_background_music(self):
		self.main_music_chanel.play (self.main_music, -1)
		
	def play_get_shot_sound(self):
		sound = random.choice (self.get_shot_sounds)
		self.get_shot_sounds_chanel.play (sound, 0)
		
	
	def play_tank_movement(self):
		if not self.move_sound_chanel.get_busy():
			self.move_sound_chanel.play (self.move_sound, 0)
	def play_tank_jump (self) :
		if self.jump_sound_chanel.get_busy():
			self.jump_sound_chanel.stop ()
			self.jump_sound_chanel.play (self.jump_sound, 0)
		else:
			self.jump_sound_chanel.play (self.jump_sound, 0)

	def play_tank_shoot (self):
		if self.shoot_sound_chanel.get_busy():
			self.shoot_sound_chanel.stop ()
			self.shoot_sound_chanel.play (self.shoot_sound, 0)
		else :
			self.shoot_sound_chanel.play (self.shoot_sound, 0)
