{"configured": True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

from physics.physics import *
from gallery.land_vehicles import *
from utils import *


car = Car(Condition(4.47, 11.84, Position(0,0), psi = sp.pi/2))

car.move(0 , 30, car.acc_long_trac, car.acc_lat, dt = 0.1)

print(len(car.conditions))
