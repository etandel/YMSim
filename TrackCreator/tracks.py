#coding: UTF-8
from re import match
from collections import namedtuple

import scipy as sp

from simulator.physics import Position

constants = {
    'length': 0.1 , #meters
    'radius': 0.2 , #meters
    'angle': sp.pi/12 , #rad
    'diff_index': 200 ,
    'width': 1.0 ,
}

TrackInfo = namedtuple('TrackInfo', 'orient position')

class _Track(object):
    def __init__(self, orient=0, position=Position(0,0)):
        self.length = 0
        self.angle = 0
        self.width = 0
        self.radius = sp.inf
        self.orient = orient
        self.position = position
        

class StraightTrack(_Track):
    def __init__(self, length, width, orient=0, position=Position(0,0)):
        super(StraightTrack, self).__init__(orient, position)
        self.length = length
        self.radius = sp.inf
        self.width = width


class CurveTrack(_Track):
    def __init__(self, radius, angle, width, orient=0, position=Position(0,0)):
        super(CurveTrack, self).__init__(orient, position)
        self.radius = radius
        self.angle = angle
        self.width = width

def margin_left(pos, orient, width):
    X = pos.X
    Y = pos.Y
    return Position(X-sp.sin(orient)*width/2, Y+sp.cos(orient)*width/2)
    
def margin_right(pos, orient, width):
    X = pos.X
    Y = pos.Y
    return Position(X+sp.sin(orient)*width/2, Y-sp.cos(orient)*width/2)

class Circuit(list):
    def __init__(self, track_list=None, csv=False):
        super(Circuit, self).__init__()
        if csv:
            self._append_from_matrix(track_list)
        elif track_list:
            for t in track_list:
                self.append(t)
                self.left  = [l for l in track_list.left]
                self.right = [r for r in track_list.right]
        else:
            self.append(_Track())
            self.left  = []
            self.right = []

    def _append_from_matrix(self, track_list):
        self.left  = []
        self.right = []
        for row in track_list:
            width = row[0]
            position = Position(row[5], row[6])
            orient = row[4]
            radius = row[1]
            if radius == sp.inf: #straight track
                length = row[2]
                self.append(StraightTrack(length, width, orient, position))
            else:
                angle = row[3]
                self.append(CurveTrack(radius, angle, width, orient, position))
            self.left.append(margin_left(position, orient, width))
            self.right.append(margin_right(position, orient, width))

    def to_matrix(self):
        track_list = [
            [track.width,
             track.radius,
             track.length,
             track.angle,
             track.orient,
             track.position.X,
             track.position.Y]
            for track in self]
        return track_list

    def create_straight(self, length, width):
        last_track = self[-1]
        orient = last_track.orient

        # the following math is good old linear algebra:
        # get the last two points, create a versor on that direction
        # and then the line comes natural: r: (x0 + Vx * t, y0 + Vy * t)
        if len(self) > 1:
            last_pos = self[-1].position
            before_last_pos = self[-2].position
            ori_vec = [last_pos.X - before_last_pos.X, last_pos.Y - before_last_pos.Y]
            ori_mod = sp.sqrt(ori_vec[0]**2 + ori_vec[1]**2)
            ori_vec[0] /= ori_mod
            ori_vec[1] /= ori_mod
        else:
            ori_vec = (1,0)
            orient = last_track.orient

        x0 = last_track.position.X
        y0 = last_track.position.Y
        dl = length / constants['diff_index']
        for i in range(1, constants['diff_index']+1):
            X = x0 + i*dl*ori_vec[0]
            Y = y0 + i*dl*ori_vec[1]
            position = Position(X,Y)

            self.left.append(margin_left(position, orient, width))
            self.right.append(margin_right(position, orient, width))
            self.append(StraightTrack(length, width, orient, position))
        return TrackInfo(orient, position)
        
    def create_curve(self, angle, radius, width, rad=False):
        if not rad: #angle parameter is not in radians
            angle = angle * sp.pi/180.0 
        
        last_track = self[-1]
        #the following math is based on Mauro's matlab program
        R = radius if angle > 0 else -radius
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
            self.left.append(margin_left(position, orient, width))
            self.right.append(margin_right(position, orient, width))

            self.append(CurveTrack(radius, angle, width, orient, position))
        return TrackInfo(orient, position)

    def remove_last(self):
        for i in xrange(-constants['diff_index'],0):
            self.pop(i)
            self.left.pop(i)
            self.right.pop(i)

