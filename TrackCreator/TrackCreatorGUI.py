#!/usr/bin/env python2
#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

"""GUI for circuit creation"""

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import tracks 
from scipy import pi
from drawcircuit import CircuitWidget

class FloatEdit(QtGui.QLineEdit):
    def __init__(self, placeholder='', parent=None):
        super(FloatEdit, self).__init__(parent)

        self.setPlaceholderText(placeholder) 
        self.setValidator(QtGui.QDoubleValidator(self))

    @property
    def value(self):
        try:
            val = float(self.text())
        except ValueError:
            val = None
        return val

class LogWindow(QtGui.QWidget):
    def __init__(self, logstring = ''):
        super(LogWindow, self).__init__()
        self.logstring = logstring
        self._initUI()

    def _initUI(self):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()
        
    def _create_widgets(self):
        self.log = QtGui.QTextEdit(self)

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.log)
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.log.setReadOnly(True)

    def append(self, logstr):
        self.log.append(logstr)

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
        self.undo = QtGui.QPushButton('Desfazer', self)

    def _design_layout(self):
        creation_layout = QtGui.QHBoxLayout()
        creation_layout.addWidget(self.left_turn)
        creation_layout.addWidget(self.straight)
        creation_layout.addWidget(self.right_turn)
        
        undo_layout = QtGui.QHBoxLayout()
        undo_layout.addWidget(self.clear)
        undo_layout.addWidget(self.undo)
        
        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(creation_layout)
        main_layout.addLayout(undo_layout)
        self.setLayout(main_layout)
        
    def _describe_behavior(self):
        self.connect(self.left_turn, QtCore.SIGNAL('clicked()'), self._do_left_turn)
        self.connect(self.straight, QtCore.SIGNAL('clicked()'), self._do_straight)
        self.connect(self.right_turn, QtCore.SIGNAL('clicked()'), self._do_right_turn)
        self.connect(self.clear, QtCore.SIGNAL('clicked()'), self._do_clear)
        self.connect(self.undo, QtCore.SIGNAL('clicked()'), self._do_undo)

    def _do_left_turn(self):
        angle = self.parent().options.angle
        radius = self.parent().options.radius
        width = self.parent().options.width
        if angle and radius and width:
            self.window().circuit.create_curve(angle, radius, width)
            self.parent().print_log(u'curva para a esquerda')
            self.window().circuit_draw.updateGL()

    def _do_straight(self):
        length = self.parent().options.length
        width = self.parent().options.width
        if length and width:
            self.window().circuit.create_straight(length, width)
            self.parent().print_log(u'reta')
            self.window().circuit_draw.updateGL()

    def _do_right_turn(self):
        angle = self.parent().options.angle
        radius = self.parent().options.radius
        width = self.parent().options.width
        if angle and radius and width:
            self.window().circuit.create_curve(-angle, radius, width)
            self.parent().print_log(u'curva para a direita')
            self.window().circuit_draw.updateGL()

    def _do_clear(self):
        circuit = tracks.Circuit() 
        self.window().circuit = circuit
        self.window().circuit_draw.updateGL()

    def _do_undo(self):
        wind = self.window()
        wind.circuit.remove_last()
        wind.circuit_draw.updateGL()

class CircuitParamsWidget(QtGui.QGroupBox):
    def __init__(self, parent):
        super(CircuitParamsWidget, self).__init__(u'Opções', parent)
        self._initUI()

    def _initUI(self):
        self._create_widgets()
        self._design_layout()

    def _create_widgets(self):
        self._length_edit = FloatEdit('Comp. da reta', self)
        self._radius_edit = FloatEdit("Raio da curva", self)
        self._angle_edit  = FloatEdit(u"Arco da curva", self)
        self._width_edit  = FloatEdit(u"Largura do trecho", self)

    def _design_layout(self):
        main_layout = QtGui.QFormLayout()
        main_layout.addRow('Comprimento:', self._length_edit)
        main_layout.addRow('Raio:', self._radius_edit)
        main_layout.addRow('Arco:', self._angle_edit)
        main_layout.addRow('Largura:', self._width_edit)
        self.setLayout(main_layout)

    @property
    def length(self):
        return self._length_edit.value

    @property
    def radius(self):
        return self._radius_edit.value

    @property
    def angle(self):
        return self._angle_edit.value

    @property
    def width(self):
        return self._width_edit.value

class CircuitMenuDock(QtGui.QWidget):
    def __init__(self, parent):
        super(CircuitMenuDock, self).__init__(parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()

    def _create_widgets(self):
        self.menu = CircuitMenuButtons(self)
        self.options = CircuitParamsWidget(self)

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        main_layout.insertSpacing(-1, 300)
        self.setLayout(main_layout)

    def print_log(self, track_type):
        circuit = self.window().circuit
        new_track = circuit[-1]
        last_track = circuit[-tracks.constants['diff_index']]

        logstr = u'Adicionada ' + track_type + u' com posição inicial ' + unicode(last_track.position)
        logstr += u', posição final ' + unicode(new_track.position)
        logstr += u' e orientação ' + unicode(circuit[-1].orient * 180/pi) + u'.\n'
        logwindow.append(logstr)
        self.window().statusBar().showMessage(logstr, 4000)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.circuit = tracks.Circuit()
        self.logstring = ''
        self._initUI()


    def _initUI(self):
        self.setWindowTitle('YMCircuit')
        self._create_menu()
        self._create_widgets()


    def _create_widgets(self):
        circuit_draw = CircuitWidget(self)
        self.setCentralWidget(circuit_draw)
        self.circuit_draw = circuit_draw

        l_dock_area, r_dock_area = Qt.LeftDockWidgetArea , Qt.RightDockWidgetArea
        circuit_menu = QtGui.QDockWidget('Circuit Menu', self)
        circuit_menu.setAllowedAreas(l_dock_area | r_dock_area)
        circuit_menu.setWidget(CircuitMenuDock(self))
        self.addDockWidget(r_dock_area, circuit_menu)

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_m = menu_bar.addMenu('&File')

        view_m = menu_bar.addMenu('&View')
        logshort = QtGui.QKeySequence(Qt.Key_Control + Qt.Key_L)
        view_m.addAction('Log', self._show_log_window)
        
        track_m = menu_bar.addMenu('&Track')
        help_m = menu_bar.addMenu('&Help')

    def _show_log_window(self):
        logwindow.show()


app = QtGui.QApplication(sys.argv)
wind = MainWindow(); wind.show()
logwindow = LogWindow()
sys.exit(app.exec_())

