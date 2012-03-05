#!/usr/bin/env python2
#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

"""GUI for circuit creation"""

import sys
from PyQt4 import QtGui, QtCore
import tracks 
from scipy import pi
#from spiral import *
from drawcircuit import *

class MainWindow(QtGui.QWidget):
  
    def __init__(self):
        super(MainWindow, self).__init__()
        self._initUI()


    def _initUI(self):
        self.setWindowTitle('YMCircuit')
        self._create_menu()
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()


    def _create_widgets(self):
        pass

    def _design_layout(self):
        pass

    def _create_menu(self):
        pass

    def _describe_behavior(self):
        pass


circuit = tracks.Circuit()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.show()
    sys.exit(app.exec_())
