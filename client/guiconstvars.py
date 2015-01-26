#! /usr/bin/python

__author__ = 'Amin'

#########################################
################# keys ##################


from pygame.locals import *
import basictypes


keys_events = {}

keys_actions_press = {}
keys_actions_down  = {}

# events
keys_events[basictypes.Events.quitgame]  = [K_q]
keys_events[basictypes.Events.pausegame] = [K_p, K_ESCAPE]
keys_events[basictypes.Events.showgui]   = [K_s]
keys_events[basictypes.Events.training]  = [K_t]
keys_events[basictypes.Events.changebot] = [K_c]

# actions
keys_actions_press[basictypes.Actions.goleft]        = [K_LEFT]
keys_actions_press[basictypes.Actions.goright]       = [K_RIGHT]
keys_actions_press[basictypes.Actions.increaseangle] = [K_UP]
keys_actions_press[basictypes.Actions.decreaseangle] = [K_DOWN]

keys_actions_down[basictypes.Actions.jump]  = [K_LSHIFT, K_RSHIFT, K_SPACE]
keys_actions_down[basictypes.Actions.shoot] = [K_LSHIFT, K_RSHIFT, K_SPACE]


#########################################




#########################################
################ Display ################


display_name   = "pytanks"

resolutions = ['750*300', '1000*400', '1500*600', '1600*640', '1800*720']

#########################################
