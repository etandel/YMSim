#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)


import scipy as sp

def euler(func_i, diff, dt = 0.1):
	return func_i + (diff)*dt

class Position:
        def __init__(self, X,Y):
                self.X = X
                self.Y = Y
	def distance_to(self, position):
		return sp.sqrt((position.X - self.X)**2 + (position.Y - self.Y)**2)


class Condition:
        """Classe que armazena as condicoes atuais de um veiculo, que sao, em ordem: acc_max, tau, position = (0,0), psi = 0, speed = 0, radius = sp.inf."""

        def __init__(self, acc_max, tau, position, psi = 0, speed = 0, omega = 0, radius = sp.inf):
                self.position = position
                self.speed = speed
                self.acc_max = acc_max
                self.tau = tau
                self.radius = radius
                self.psi = psi
		self.omega = omega


class Vehicle_Dynamics():
	def __init__(self):
		pass

	def acc_long_trac(self, v, tau, acc_max):
		return acc_max - v/tau

	def acc_long_break(self, v, tau, acc_max):
		pass 

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
	def __init__(self, conditions):
		self.conditions = []
		self.conditions.append(conditions)


	def move(self, ti, tf, acc_long, acc_lat, dt=0.1):
		tmax = (tf-ti)/dt
		i = len(self.conditions)
		while i <= tmax:
			self.conditions.append(self.get_next_conditions(self.conditions[i-1], acc_long, acc_lat, dt))
			i += 1
