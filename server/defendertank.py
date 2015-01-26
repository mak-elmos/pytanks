#! /usr/bin/python
__author__ = 'Milad'

from tank import *
from vector import *
import constvars

class DefenderTank(Tank):

    speed     = None
    jumpSpeed = None

    def __init__(self, team, pos, vel=Vector(0, 0), acc=Vector(0, 0)):
        super(DefenderTank, self).__init__(team, pos, vel, acc)
