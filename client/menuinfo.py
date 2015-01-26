#! /usr/bin/python

__author__ = 'Kiamehr & Amin'

import basictypes

class MenuInfo:

##############

	def __init__(self, pid=-1, host='localhost', port=10000, team=basictypes.Teams.left, tanktype=basictypes.TankTypes.attacker, isAI=False, w=1000, h=400):

		self.pid      = pid # player id
		self.host     = host
		self.port     = port
		self.team     = team
		self.tanktype = tanktype
		self.isAI     = isAI

		self.monitor_width  = w
		self.monitor_height = h