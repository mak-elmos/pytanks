#! /usr/bin/python

__author__ = 'Milad'

from object import *
from vector import *

class DynamicObject(Object):
    """
    get from father :
        position
        prevPositions
    velocity  
    acceleration
    """

    def __init__(self, pos, vel=Vector(0, 0), acc=Vector(0, 0)):
       # if type(pos) !=Vector or type(v) !=Vector  or type(a) !=Vector :
         #   raise TypeError ("argumant must be a Vector")
        super(DynamicObject, self).__init__(pos)
        self.velocity = vel
        self.acceleration = acc

