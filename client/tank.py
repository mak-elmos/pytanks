#! /usr/bin/python

__author__ = 'Milad & Amin'

from dynamicobject import *

class Tank(DynamicObject):
    """
    get from father
        :param position
        :param prevPositions
        :param mass
        :param velocity
        :param accelaration

    :param PID
    :param mana (optional)
    :param manaRate (optional)
    """


    def __init__(self, team=None, tanktype=None, pos=None, ld=None, ll=None, vel=Vector(0, 0), acc=Vector(0, 0), size=None, rspwn=0):
        super(Tank, self).__init__(pos, vel, acc)
        self.team              = team
        self.tanktype          = tanktype
        self.size              = size
        self.launcherDirection = ld
        self.launcherLength    = ll
        self.health            = 0
        self.mana              = 0

        self.respawn_time = rspwn
