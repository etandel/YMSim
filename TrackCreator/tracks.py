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


class _Track:
	def __init__(self, width, psi = 0, position = Position(0,0)):
		self.width = width
		self.psi = psi
		self.position = position
		

class _Straight_Track(_Track):
	def __init__(self, width, length, psi = 0, position = Position(0,0)):
		super(_Straight_Track, self).__init__(width, psi, position)

		self.length = length
		self.radius = sp.inf


class _Curve_Track(_Track):
	def __init__(self, width, radius, angle, psi = 0, position = Position(0,0)):
		super(_Curve_Track, self).__init__(width, psi, position)

		self.radius = radius
		self.angle = angle

class Circuit(list):
	def __init__(self, width, psi):
		super(Circuit, self).__init__()

		self.width = width
		self.append(self.create_straight(0, psi))

	def create_straight(self, length):
		psi = last_track.psi
		X = last_track.position.X + length * sp.cos(psi)
		Y = last_track.position.Y + length * sp.sin(psi)
		position = Position(X,Y)
		self.append(_Straight_Track(width, length, psi, position))
	

	def create_curve(self, radius, angle):
		psi = sp.pi - angle + last_track.psi	
		position = Position(0,0) #calculate position
		self.append(_Curve_Track(width, radius, angle, psi, position))
