#!/usr/bin/env python2
#coding: UTF-8
"""GUI for simulation"""

import sys
import csv

from scipy import pi
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSlider
from PyQt4.QtCore import Qt

from TrackCreator import tracks
from simulator.physics import Car
from simulator.draw import CircuitWidget

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

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        map(main_layout.addWidget, self.children())
        main_layout.insertSpacing(-1, 300)
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.connect(self.time_slider, QtCore.SIGNAL('sliderMoved(int)'), self._slider_chaged)

    def _slider_chaged(self, val):
        self.window().draw_circuit.max_index = val

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.circuit = tracks.Circuit()
        self.car = Car()
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
        circuit_menu.setWidget(SimDock(self))
        self.addDockWidget(r_dock_area, circuit_menu)

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_m = menu_bar.addMenu('&File')
        file_m.addAction('&Load track', self._load_track)
        file_m.addAction('&Load acc profile', self._load_acc_profile)
        file_m.addAction('&Save trajectory', self._save_traj)

        track_m = menu_bar.addMenu('&Track')
        help_m = menu_bar.addMenu('&Help')

    def _save_traj(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Trajectory', filter='CSV Files (*.csv )')
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            for cond in self.car.conditions:
                X = str(track.position.X)
                Y = str(track.position.Y)
                writer.writerow((X,Y))

    def _load_track(self):
        raise NotImplemented

    def _load_acc_profile(self):
        raise NotImplemented

app = QtGui.QApplication(sys.argv)
wind = MainWindow(); wind.show()
sys.exit(app.exec_())

