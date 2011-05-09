class Track:
	pass

class Straight_Track(Track):
	def __init__(self, friction, width, length):
		self.friction = friction
		self.width = width
		self.length = length
		self.radius = sp.inf


class Curve_Track(Track):
	def __init__(self, friction, width, radius, angle):
		self.friction = friction
		self.width = width
		self.radius = radius
		self.angle = angle
