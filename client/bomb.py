#! /usr/bin/python

__author__ = 'Milad'

from dynamicobject import *
import constvars

class Bomb(DynamicObject):
	
    """
    :param radius (Default = 0)
    """
    def __init__(self, pos=None, vel=Vector(0, 0), acc=Vector(0, 0)):
        super(Bomb, self).__init__(pos, vel, acc)
