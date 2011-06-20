#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

import scipy as sp
from physics.physics import Position
from re import match

def validate_float(input_val):
	try:
		value = float(input_val)
	except:
		value = None

	return value


class _Track(object):
	def __init__(self, psi = 0, position = Position(0,0)):
		self.psi = psi
		self.position = position
		

class _Straight_Track(_Track):
	def __init__(self, length, psi = 0, position = Position(0,0)):
		super(_Straight_Track, self).__init__(psi, position)

		self.length = length
		self.radius = sp.inf


class _Curve_Track(_Track):
	def __init__(self, radius, angle, psi = 0, position = Position(0,0)):
		super(_Curve_Track, self).__init__(psi, position)

		self.radius = radius
		self.angle = angle

class Circuit(list):
	def __init__(self, width, psi):
		super(Circuit, self).__init__()

		self.width = width
		self.append(_Track(psi))

	def create_straight(self, length):
		last_track = self[-1]

		psi = last_track.psi
		X = last_track.position.X + length * sp.cos(psi)
		Y = last_track.position.Y + length * sp.sin(psi)
		position = Position(X,Y)
		self.append(_Straight_Track(length, psi, position))
	

	def create_curve(self, radius, angle):
		last_track = self[-1]

		psi = sp.pi - angle + last_track.psi	
		position = Position(0,0) #calculate position
		self.append(_Curve_Track(radius, angle, psi, position))

	def create_clothoide(self):
		pass
