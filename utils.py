{"configured": True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

def copy(self, dest):
        dest.position = self.position
        dest.speed = self.speed
        dest.acc_max = self.acc_max
        dest.tau = self.tau
        dest.radius = self.radius
        dest.psi = self.psi

def frange(initial, final, step):
                lst = []
                while initial <= final:
                        lst.append(initial)
                        initial = initial + step
                return lst

def is_valid_input(val, expected):
	return type(val) == expected

def get_float(in_message, error_message):
	while True:
		try:
			value = float(raw_input(in_message))
		except:
			print(error_message)
		else:
			break
	return value
