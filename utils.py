#coding: UTF-8
import unicodedata
from math import ceil

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

def val_from_percent(percent, min_, max_):
    return int(ceil(min_ + (max_ - min_) * (percent / 100.0)))

def percent_from_val(val, min_, max_):
    return (float(val - min_) / max_min) / 100.0

def sluggify(s):
    if not isinstance(s, unicode):
        s = unicode(s)
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').replace(' ', '_').lower()
