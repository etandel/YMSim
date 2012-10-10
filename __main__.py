#!/usr/bin/env python2
#coding: UTF-8

"""GUI for circuit creation"""

import sys
import csv

from scipy import pi
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSlider, QSpinBox

from TrackCreator import tracks 
from simulator.physics import Car
from TrackCreator.drawcircuit import CircuitWidget
from utils import val_from_percent, percent_from_val


class Controller(object):

    @classmethod
    def broadcast_change(cls):
        cls.window.sim_opts.widget().time_spinner.setRange(*cls.get_spinner_range())

    @classmethod
    def get_spinner_range(cls):
        return (0, len(cls.window.circuit))


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
        Controller.broadcast_change()

    def _do_straight(self):
        length = self.parent().options.length
        width = self.parent().options.width
        if length and width:
            self.window().circuit.create_straight(length, width)
            self.parent().print_log(u'reta')
            self.window().circuit_draw.updateGL()
        Controller.broadcast_change()

    def _do_right_turn(self):
        angle = self.parent().options.angle
        radius = self.parent().options.radius
        width = self.parent().options.width
        if angle and radius and width:
            self.window().circuit.create_curve(-angle, radius, width)
            self.parent().print_log(u'curva para a direita')
            self.window().circuit_draw.updateGL()
        Controller.broadcast_change()

    def _do_clear(self):
        circuit = tracks.Circuit() 
        self.window().circuit = circuit
        self.window().circuit_draw.updateGL()
        Controller.broadcast_change()

    def _do_undo(self):
        wind = self.window()
        wind.circuit.remove_last()
        wind.circuit_draw.updateGL()
        Controller.broadcast_change()


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


class SimDock(QtGui.QWidget):
    def __init__(self, parent):
        super(SimDock, self).__init__(parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()

    def _create_widgets(self):
        self.time_slider = QSlider(Qt.Horizontal, self)
        self.time_slider.setTickInterval(1)
        self.time_slider.setSliderPosition(self.time_slider.maximum())

        self.time_spinner = QSpinBox(self)
        self.time_spinner.setRange(0, len(self.window().circuit))

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        main_layout.insertSpacing(-1, 300)
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.connect(self.time_slider, QtCore.SIGNAL('sliderMoved(int)'), self._slider_changed)
        self.connect(self.time_slider, QtCore.SIGNAL('valueChanged(int)'), self._slider_changed)

        self.connect(self.time_spinner, QtCore.SIGNAL('valueChanged(int)'), self._spinner_changed)

    def _slider_changed(self, val):
        self.time_spinner.setValue(val_from_percent(val, *Controller.get_spinner_range()))

    def _spinner_changed(self, val):
        self.window().circuit_draw.max_index = val

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        Controller.window = self
        self.car = Car()
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
        allowed_areas = l_dock_area | r_dock_area
        self.setDockOptions(self.AnimatedDocks | self.ForceTabbedDocks | self.VerticalTabs)

        self.circuit_opts = self._create_dock_widget(allowed_areas, 'Circuit Creation', CircuitMenuDock)
        self.sim_opts = self._create_dock_widget(allowed_areas, 'Simulation Menu', SimDock)

        self.addDockWidget(r_dock_area, self.circuit_opts)
        self.addDockWidget(r_dock_area, self.sim_opts)
        self.tabifyDockWidget(self.sim_opts, self.circuit_opts)

    def _create_dock_widget(self, allowed_areas, name, widget):
        dock = QtGui.QDockWidget(name, self)
        dock.setAllowedAreas(allowed_areas)
        dock.setFeatures(dock.DockWidgetFeatures(dock.AllDockWidgetFeatures & ~dock.DockWidgetClosable))
        dock.setWidget(widget(self))
        return dock
        
    def _create_menu(self):
        menu_bar = self.menuBar()

        file_m = menu_bar.addMenu('&File')
        file_m.addAction('&Load', self._load)
        file_m.addAction('&Save', self._save)

        view_m = menu_bar.addMenu('&View')
        logshort = QtGui.QKeySequence(Qt.Key_Control + Qt.Key_L)
        view_m.addAction('Log', self._show_log_window)
        
        track_m = menu_bar.addMenu('&Track')
        help_m = menu_bar.addMenu('&Help')

    def _show_log_window(self):
        logwindow.show()

    def _save(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Circuit', '/home/echobravo/Misc', 'CSV Files (*.csv )')
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            for track in self.window().circuit:
                X = str(track.position.X)
                Y = str(track.position.Y)
                writer.writerow((X,Y))

    def _load(self):
        pass

#TODO: Finish this function
#        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Circuit', '/home/echobravo/Misc', 'CSV Files (*.csv )')
#        with open(fname) as f:
#            for row in csv.reader(f):
#                X = float(row[0])
#                Y = float(row[1])
                

app = QtGui.QApplication(sys.argv)
wind = MainWindow(); wind.show()
logwindow = LogWindow()
sys.exit(app.exec_())

