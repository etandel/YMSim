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
    'length': 3.0 , #meters
    'radius': 2.0 , #meters
    'angle': sp.pi/12 , #rad
    'diff_index': 50 ,
    'width': 1.0 ,
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
        #the following math is based on Mauro's matlab program
        orient = last_track.orient
        x0 = last_track.position.X
        y0 = last_track.position.Y
        dl = constants['length'] / constants['diff_index']
        for i in range(1, constants['diff_index']+1):
            X = last_track.position.X + dl * i * sp.cos(orient)
            Y = last_track.position.Y - dl * i * sp.sin(orient)
            position = Position(X,Y)
            self.append(_Straight_Track(orient, position))
        return TrackInfo(orient, position)
        
    def create_curve(self, angle=constants['angle']):
        last_track = self[-1]
        #the following math is based on Mauro's matlab program
        R = constants['radius'] if angle < 0 else -constants['radius']
        beta = last_track.orient
        x0 = last_track.position.X
        y0 = last_track.position.Y
        da = angle/constants['diff_index']
        for i in range(1, constants['diff_index'] + 1): 
            xl = R * sp.sin(da*i);
            yl = R * (1 - sp.cos(da*i));   
            X = x0 + sp.cos(beta) * xl - sp.sin(beta) * yl
            Y = y0 + sp.sin(beta) * xl + sp.cos(beta) * yl

            orient = (beta + da*i)
            position = Position(X,Y)
            self.append(_Curve_Track(orient, position))
        return TrackInfo(orient, position)


