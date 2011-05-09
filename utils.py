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

