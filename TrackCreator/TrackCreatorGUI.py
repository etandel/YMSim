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

class CircuitMenuButtons(QtGui.QWidget):
    def __init__(self, parent):
        super(CircuitMenuButtons, self).__init__(parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()

    def _create_widgets(self):
        self.left_turn = QtGui.QPushButton(u'Curva Esq', self)
        self.straight = QtGui.QPushButton('Reta', self)
        self.right_turn = QtGui.QPushButton('Curva Dir', self)
        self.clear = QtGui.QPushButton('Limpar', self)
        self.back = QtGui.QPushButton('Voltar', self)

    def _design_layout(self):
        main_layout = QtGui.QHBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)
        
    def _describe_behavior(self):
        self.connect(self.left_turn, QtCore.SIGNAL('clicked()'), self._do_left_turn)
        self.connect(self.straight, QtCore.SIGNAL('clicked()'), self._do_straight)
        self.connect(self.right_turn, QtCore.SIGNAL('clicked()'), self._do_right_turn)
        self.connect(self.clear, QtCore.SIGNAL('clicked()'), self._do_clear)
        self.connect(self.back, QtCore.SIGNAL('clicked()'), self._do_back)

    def _do_left_turn(self):
        self.window().circuit.create_curve()
        self.parent().print_log(u'curva para a esquerda')
        self.window().circuit_draw.updateGL()

    def _do_straight(self):
        self.window().circuit.create_straight()
        self.parent().print_log(u'reta')
        self.window().circuit_draw.updateGL()

    def _do_right_turn(self):
        self.window().circuit.create_curve(-tracks.constants['angle'])
        self.parent().print_log(u'curva para a direita')
        self.window().circuit_draw.updateGL()

    def _do_clear(self):
        self.parent().log.clear()
        circuit = tracks.Circuit() 
        self.window().circuit = circuit
        self.window().circuit_draw.updateGL()

    def _do_back(self):
        pass

class CircuitMenuDock(QtGui.QWidget):
    def __init__(self, parent):
        super(CircuitMenuDock, self).__init__(parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()

    def _create_widgets(self):
        self.menu = CircuitMenuButtons(self)
        self.log = QtGui.QTextEdit(self)

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.log.setReadOnly(True)

    def print_log(self, track_type):
        circuit = self.window().circuit
        new_track = circuit[-1]
        last_track = circuit[-tracks.constants['diff_index']]
        logstr = u'Adicionada ' + track_type + u' com posição inicial ' + unicode(last_track.position) + u' e posição final ' + unicode(new_track.position) + u'.\n' + unicode(circuit[-1].orient * 180/pi)
        self.log.append(logstr)
        self.window().statusBar().showMessage(logstr, 4000)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.circuit = tracks.Circuit()
        self._initUI()


    def _initUI(self):
        self.setWindowTitle('YMCircuit')
        self._create_menu()
        self._create_widgets()
        self._describe_behavior()


    def _create_widgets(self):
        circuit_draw = CircuitWidget(self)
        self.setCentralWidget(circuit_draw)
        self.circuit_draw = circuit_draw

        l_dock_area, r_dock_area = QtCore.Qt.LeftDockWidgetArea , QtCore.Qt.RightDockWidgetArea
        circuit_menu = QtGui.QDockWidget('Circuit Menu', self)
        circuit_menu.setAllowedAreas(l_dock_area | r_dock_area)
        circuit_menu.setWidget(CircuitMenuDock(self))
        self.addDockWidget(r_dock_area, circuit_menu)

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_m = menu_bar.addMenu('&File')
        view_m = menu_bar.addMenu('&View')
        track_m = menu_bar.addMenu('&Track')
        help_m = menu_bar.addMenu('&Help')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.show()
    sys.exit(app.exec_())

