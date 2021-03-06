#coding: UTF-8
from collections import namedtuple

import scipy as sp

def euler(func_i, diff, dt = 0.1):
    return func_i + (diff)*dt

Position = namedtuple('Position', 'X Y')

_ConditionBase = namedtuple('Condition', 'acc_max tau position psi  speed  omega  radius')

class Condition(_ConditionBase):
    """
    Classe que armazena as condicoes atuais de um veiculo, que sao, em ordem:
    acc_max, tau, position=(0,0), psi=0, speed=0, radius=sp.inf.
    """

    def __new__(cls, acc_max, tau, position, psi=0, speed=0, omega=0, radius=sp.inf):
        # add default values
        return super(Move, cls).__new__(cls, acc_max, tau, position, psi, speed, omega, radius)

class Vehicle_Dynamics():

    def acc_long_trac(self, v, tau, acc_max):
        return acc_max - v/tau

    def acc_long_break(self, v, tau, acc_max):
        raise NotImplemented

    def acc_lat(self, v, tau, acc_max, rad):
        return v**2/rad    

    def get_speed(self, acc_long, conditions):
        ai = acc_long(conditions.speed, conditions.tau, conditions.acc_max)
        return euler(conditions.speed, ai) 

    def get_next_conditions(self, conds_i, acc_long_trac, acc_lat, dt = 0.1):
        speed = self.get_speed(acc_long_trac, conds_i)

        omega = acc_lat(conds_i.speed, conds_i.tau, conds_i.acc_max, conds_i.radius)/speed
        psi = euler(conds_i.psi, omega, dt)

        speed_x = speed*sp.cos(psi)
        speed_y = speed*sp.sin(psi)

        X = euler(conds_i.position.X, speed_x, dt)
        Y = euler(conds_i.position.Y, speed_y, dt)

        conds_f = Condition(conds_i.acc_max, conds_i.tau, Position(X,Y), psi, speed, omega, radius=conds_i.radius)
        return conds_f


class Car(Vehicle_Dynamics):
    def __init__(self, init_conditions=[]):
        self.conditions = []
        self.conditions += init_conditions
        self.i = len(self.conditions)


    def move(self, ti, tf, acc_long, acc_lat, dt=0.1):
        imax = (tf-ti)/dt
        i = self.i
        while i <= imax:
            self.conditions.append(self.get_next_conditions(self.conditions[i-1], acc_long, acc_lat, dt))
            i += 1

