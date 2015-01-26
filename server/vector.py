#! /usr/bin/python

__author__ = 'Milad'

class Vector(object):
    """
    float x
    float y
    """

    def __init__(self, x, y):
        """
        :type self: Vector
        """
        self.x = x
        self.y = y

    def __add__(self, v2):
        """
        :type v2: Vector
        :param :v2
        :return: self+v2
        """
        return Vector(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        """
        :type v2: Vector
        :param :v2
        :return: self-v2
        """
        return Vector(self.x - v2.x , self.y - v2.y)
    def __mul__(self, a):
        """
        :type a :float
        :param : a
        :return : Vector (a*self)
        """
        return Vector(self.x * a, self.y * a)
    '''def __eq__(self, other):
        """
        :param other: other Vector
        :return: True if self == other
        """
        if self.x == other.x and self.y == other.y :
            return True
        return False'''
    def __abs__(self):
        """
        :return: size of Vector
        """
        return (self.x ** 2 + self.y ** 2) ** .5
    def __str__(self):
        return "Vector(" + str(self.x) + "," + str(self.y) + ")"
    def dot(self,v2):
        """
        :param v2:
        :return: dot of self and v2
        """
        return self.x * v2.x + self.y + v2.y




        
