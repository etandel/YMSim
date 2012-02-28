#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

import scipy as sp
from physics.physics import Position
from re import match
from collections import namedtuple

def validate_float(input_val):
    try:
        value = float(input_val)
    except:
        value = None

    return value

constants = {
    'length': 3 , #meters
    'radius': 2 , #meters
    'angle': sp.pi/4 , #rad
    'pts_per_meter': 10 ,
}

TrackInfo = namedtuple('TrackInfo', 'orient position')

class _Track(object):
    def __init__(self, orient = 0, position = Position(0,0)):
        self.orient = orient
        self.position = position
        

class _Straight_Track(_Track):
    def __init__(self, orient = 0, position = Position(0,0)):
        super(_Straight_Track, self).__init__(orient, position)

        self.length = constants['length']
        self.radius = sp.inf


class _Curve_Track(_Track):
    def __init__(self, orient = 0, position = Position(0,0)):
        super(_Curve_Track, self).__init__(orient, position)

        self.radius = constants['radius']
        self.angle = constants['angle']

class Circuit(list):
    def __init__(self):
        super(Circuit, self).__init__()
        self.append(_Track())

    def create_straight(self):
        last_track = self[-1]
        length = constants['length']
        orient = last_track.orient
        X = last_track.position.X + length * sp.cos(orient)
        Y = last_track.position.Y - length * sp.sin(orient)
        position = Position(X,Y)
        self.append(_Straight_Track(orient, position))
        return TrackInfo(orient, position)
        
    def create_curve(self, angle=constants['angle']):
        last_track = self[-1]
        orient  = last_track.orient + constants['angle']

        x0 = last_track.position.X
        y0 = last_track.position.Y
        R = constants['radius']
        #the following math is based on Mauro's matlab program
        X = x0 + sp.cos(last_track.orient) * R * sp.sin(angle) - sp.sin(last_track.orient) * R * (1 - sp.cos(angle))
        Y = y0 + sp.sin(last_track.orient) * R * sp.sin(angle) + sp.cos(last_track.orient) * R * (1 - sp.cos(angle))

        position = Position(X,Y)
        self.append(_Curve_Track(orient, position))
        return TrackInfo(orient, position)

