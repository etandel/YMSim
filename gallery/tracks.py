{'configured': False}

import scipy as sp
from physics.physics import Position
from utils import get_float
from re import match

FLOAT_ERROR = "Valor invalido. Digite apenas numeros reais.  "

class Track:
	pass

class Straight_Track(Track):
	def __init__(self, width, length, psi = 0, position = Position(0,0)):
		self.width = width
		self.length = length
		self.radius = sp.inf
		self.psi = psi
		self.position = position


class Curve_Track(Track):
	def __init__(self, width, radius, angle, psi = 0, position = Position(0,0)):
		self.width = width
		self.radius = radius
		self.angle = angle
		self.psi = psi
		self.position = position



def create_straight(width, last_track):
	psi = last_track.psi
	length = get_float("Digite o comprimento da reta: ", FLOAT_ERROR)
	X = last_track.position.X + length * sp.cos(psi)
	Y = last_track.position.Y + length * sp.sin(psi)
	position = Position(X,Y)
	return Straight_Track(width, length, psi, position)
	

def create_curve(width, last_track):
	radius = get_float("Digite o raio da curva: ", FLOAT_ERROR)
	angle = get_float("Digite o angulo do arco de curva (em radianos): ", FLOAT_ERROR)
	psi = sp.pi - angle + last_track.psi	
	position = Position(0,0) #calculate position
	return Curve_Track(width, radius, angle, psi, position)

def get_next_track(width, last_track):
	menu = match(r"(R|C)", raw_input("Digite se o pedaco eh uma RETA ou uma CURVA: ").upper())
	if menu:
		menu = menu.group(1)
		if menu == "R":
			create = create_straight
		elif menu == "C":
			create = create_curve
		else:
			return None
		return create(width, last_track)

def create_circuit():
	circuit = []
	width = get_float("Digite a largura do circuito: ", FLOAT_ERROR )

	psi = get_float("Digite o angulo que o primeiro pedaco faz com o eixo X: ", FLOAT_ERROR)
	circuit.append(Straight_Track(width, 0, psi))
	next_track = get_next_track(width, circuit[-1])
	while next_track:
		circuit.append(next_track)
		get_next_track(width, circuit[-1])


create_circuit()
track:
		circuit.append(next_track)
		get_next_track(width, circuit[-1])


create_circuit()
track:
		circuit.append(next_track)
		get_next_track(width, circuit[-1])


create_circuit()
track:
		circuit.append(next_track)
		get_next_track(width, circuit[-1])


create_circuit()
