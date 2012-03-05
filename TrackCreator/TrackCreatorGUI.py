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
from drawcircuit import CircuitWidget

class MainWindow(QtGui.QMainWindow):
  
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
        draw_circuit = CircuitWidget(circuit, self)
        self.setCentralWidget(draw_circuit)

        l_dock_area, r_dock_area = QtCore.Qt.LeftDockWidgetArea , QtCore.Qt.RightDockWidgetArea
        circuit_menu = QtGui.QDockWidget('Circuit Menu', self)
        circuit_menu.setAllowedAreas(l_dock_area | r_dock_area)
        circuit_menu.setWidget(QtGui.QWidget(self))
        self.addDockWidget(r_dock_area, circuit_menu)

    def _design_layout(self):
        pass

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_m = menu_bar.addMenu('&File')
        view_m = menu_bar.addMenu('&View')
        track_m = menu_bar.addMenu('&Track')
        help_m = menu_bar.addMenu('&Help')

    def _describe_behavior(self):
        pass


circuit = tracks.Circuit()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.show()
    sys.exit(app.exec_())
