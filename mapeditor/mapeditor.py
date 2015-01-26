#! /usr/bin/python

__author__ = 'Amin'

from gamemap import *

myMap  = Map()

### ai map
"""
myMap.name = 'ai'

myMap.attacker_explosion_const = 0.0
myMap.attacker_momentum_const  = 0.0

myMap.defender_explosion_const = 0.0

myMap.attacker_healthCost = 0
"""


### ice map
"""
myMap.name = 'ice'
myMap.attacker_mu = 2.0
myMap.defender_mu = 1.0

myMap.attacker_width  = 3.0
myMap.attacker_height = 1.5

myMap.defender_jumpSpeed = 15.0

myMap.defender_width  = 1.5
myMap.defender_height = 1.5

myMap.guiData.tank_colors_mana.me   = (128, 64, 0)
myMap.guiData.tank_colors_mana.left = (250, 125, 125)

myMap.field_width  = 40.0 # meter
myMap.field_height = 16.0  # meter

myMap.physics_gravity     = -15.0
myMap.attacker_shootSpeed = 20.0

import vector
import block
myMap.blocks.append(block.Block(vector.Vector(-10.0, 9.0), 6.0, 0.5))
myMap.blocks.append(block.Block(vector.Vector(+10.0, 9.0), 6.0, 0.5))
"""

myMap.fillBlocks()
myMap.loadResources()

saveMap(myMap)
newMap = loadMap('empty_room')
