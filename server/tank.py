#! /usr/bin/python

__author__ = 'Milad'

from dynamicobject import *

class Tank(DynamicObject):
    """
    get from father
        :param position
        :param mass
        :param velocity
        :param accelaration

    :param PID
    :param mana (optional)
    :param manaRate (optional)
    """

    
    last_velocity_y_sign = None
    size     = None
    speed    = None
    mu       = None
    mana     = None
    manaMax  = None
    manaReg  = None
    manaCost = None

    respawn_time_default = None
    respawn_time         = None

    explosion_const = None

    def __init__(self, team, pos, vel, acc):
        super(Tank, self).__init__(pos, vel, acc)
        self.team = team        
