from tank import *
from vector import *
import constvars
import basictypes

__autor__ = 'Milad'

class AttackerTank(Tank):
    """
    :param LD: Luncher Directionzavie lole tank
    """

    launcherDirection_first = None
    launcherDirection_max   = None
    launcherDirection_min   = None
    launcherDirection_speed = None

    launcherLength     = None
    launcherLength_min = None
    launcherLength_max = None

    launcherDirection = None
    shootSpeed = None
    speed    = None

    health     = None
    healthMax  = None
    healthReg  = None
    healthCost = None

    momentum_const  = None

    def __init__(self, team,  pos, vel=Vector(0, 0), acc=Vector(0, 0)):
        """
        :param size: vector(width, height)
        :param pos: position
        :param v: velocity
        :param a: acceleration
        :param ld: launcherDirection(jahate lole)
        :return: a Tank with given parameter
        """
        super(AttackerTank, self).__init__(team, pos, vel, acc)
