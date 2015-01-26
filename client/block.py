__author__ = 'Milad'
from staticobject import *
class Block (StaticObject):
    def __init__(self, pos, width, height):
        """

        :param pos: Vector
        :param size: Vector
        """
        super(Block, self).__init__(pos)
        self.width  = width
        self.height = height
