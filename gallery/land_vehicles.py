{'configured': False}

from physics.physics import *
from utils import *


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
