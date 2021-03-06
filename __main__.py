#!/usr/bin/env python2
#coding: UTF-8

"""GUI for circuit creation"""

import os
import sys
import csv

import scipy as sp
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget, QSlider, QSpinBox, QGroupBox
from PyQt4.QtGui import QMessageBox, QFileDialog

from TrackCreator import tracks
from simulator.physics import Car, Position
from TrackCreator.drawcircuit import CircuitWidget
from utils import val_from_percent, percent_from_val, sluggify


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

class LabeledFloatEdit(QWidget):
    def __init__(self, label_txt='', placeholder='', parent=None):
        super(LabeledFloatEdit, self).__init__(parent)
        self.label = QtGui.QLabel(label_txt, self)
        self.edit = FloatEdit(placeholder, self)
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)

    @property
    def value(self):
        return self.edit.value
        

class TupleLabeledFloatEdit(QWidget):
    def __init__(self, label_names, parent):
        super(TupleLabeledFloatEdit, self).__init__(parent)
        self.label_names = label_names
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()

    def _create_widgets(self):
        for name in self.label_names:
            setattr(self, sluggify(name), LabeledFloatEdit(label_txt=name, parent=self))

    def _design_layout(self):
        main_layout = QtGui.QHBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)

class LogWindow(QWidget):
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


class CircuitMenuButtons(QWidget):
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


class CircuitParamsWidget(QGroupBox):
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


class CircuitMenuDock(QWidget):
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
        logstr += u' e orientação ' + unicode(circuit[-1].orient * 180/sp.pi) + u'.\n'
        logwindow.append(logstr)
        self.window().statusBar().showMessage(logstr, 4000)


class CarStatesWidget(QGroupBox):
    def __init__(self, parent):
        super(CarStatesWidget, self).__init__(u'Estado do Veículo', parent)
        self._initUI()

    def _initUI(self):
        self._create_widgets()
        self._design_layout()

    def _create_widgets(self):
        self._pos_edit = TupleLabeledFloatEdit(('X', 'Y'), self)
        self._speed_edit = TupleLabeledFloatEdit(('Long', 'Lat'), self)
        self._acc_edit = TupleLabeledFloatEdit(('Long', 'Lat'), self)

    def _design_layout(self):
        main_layout = QtGui.QFormLayout()
        main_layout.addRow(u'Posição:', self._pos_edit)
        main_layout.addRow(u'Velocidade:', self._speed_edit)
        main_layout.addRow(u'Aceleração:', self._acc_edit)
        self.setLayout(main_layout)

    @property
    def pos(self):
        return self._pos_edit

    @property
    def speed(self):
        return self._speed_edit

    @property
    def acc(self):
        return self._acc_edit


class TimeLineWidget(QGroupBox):
    def __init__(self, parent):
        super(TimeLineWidget, self).__init__('Linha do Tempo', parent)
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
        self.time_spinner.setRange(*Controller.get_spinner_range())

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.connect(self.time_slider, QtCore.SIGNAL('sliderMoved(int)'), self._slider_changed)
        self.connect(self.time_slider, QtCore.SIGNAL('valueChanged(int)'), self._slider_changed)

        self.connect(self.time_spinner, QtCore.SIGNAL('valueChanged(int)'), self._spinner_changed)
    
    def _slider_changed(self, val):
        self.time_spinner.setValue(val_from_percent(val, *Controller.get_spinner_range()))

    def _spinner_changed(self, val):
        self.window().circuit_draw.max_index = val


class SimDock(QWidget):
    def __init__(self, parent):
        super(SimDock, self).__init__(parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()

    def _create_widgets(self):
        self.time_line = TimeLineWidget(self)
        self.states = CarStatesWidget(self)

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        main_layout.insertSpacing(-1, 300)
        self.setLayout(main_layout)

    def _describe_behavior(self):
        pass


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
        circuit_io_m = file_m.addMenu('&Circuit')
        circuit_io_m.addAction('&Load', self._load_circuit)
        circuit_io_m.addAction('&Save', self._save_circuit)

        sim_io_m = file_m.addMenu('&Simulation')
        sim_io_m.addAction('&Load', self._load_sim)
        sim_io_m.addAction('&Save', self._save_sim)

        view_m = menu_bar.addMenu('&View')
        logshort = QtGui.QKeySequence(Qt.Key_Control + Qt.Key_L)
        view_m.addAction('Log', self._show_log_window)
        
        help_m = menu_bar.addMenu('&Help')

    def _show_log_window(self):
        logwindow.show()

    def _save_circuit(self):
        fname = QFileDialog.getSaveFileName(self, 'Save Circuit', os.path.expanduser('~'), 'CSV Files (*.csv )')
        if fname:
            with open(fname, 'w') as f:
                writer = csv.writer(f)
                for line in self.window().circuit.to_matrix():
                    writer.writerow([str(param) for param in line])

    def _load_circuit(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Circuit', os.path.expanduser('~'), 'CSV Files (*.csv )')
        if fname:
            try:
                with open(fname) as f:
                    track_list = [[float(param) for param in row] for row in csv.reader(f)]
            except ValueError:
                QMessageBox.critical(self, 'Erro!', u'Não foi possível carregar circuito. Arquivo mal formado.')
            else:
                self.circuit = tracks.Circuit(track_list, csv=True)
            
    def _save_sim(self):
        fname = QFileDialog.getSaveFileName(self, 'Save Simulation', os.path.expanduser('~'), 'CSV Files (*.csv )')
        if fname:
            with open(fname, 'w') as f:
                writer = csv.writer(f)
                for line in self.window().car.conditions:
                    writer.writerow([str(param) for param in line])

    def _load_sim(self):
        fname = QFileDialog.getSaveFileName(self, 'Load Simulation', os.path.expanduser('~'), 'CSV Files (*.csv )')

app = QtGui.QApplication(sys.argv)
wind = MainWindow(); wind.show()
logwindow = LogWindow()
sys.exit(app.exec_())

