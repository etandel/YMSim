#!/usr/bin/env python2
#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

"""GUI for circuit creation"""
"""TODO:
    -> Describe dialogs' behavior;
    -> set minimum/max window size of all;
    -> find a way to connect 'close event'; 
"""

import sys
from PyQt4 import QtGui, QtCore
import tracks 
from scipy import pi
#from spiral import *
from drawcircuit import *

class LabeledEdit(QtGui.QWidget):
        def __init__(self, label_txt='', edit_txt='', parent=None, layout_type = 'Horizontal'):
                super(LabeledEdit, self).__init__(parent)
                self._initUI(label_txt, edit_txt, layout_type)

        def _initUI(self, label_txt, edit_txt, layout_type):

                main_layout = self._make_layout(layout_type)
                self._make_label(label_txt)
                self._make_edit(edit_txt)
                main_layout.addWidget(self.label)
                main_layout.addWidget(self.edit)
                self.setLayout(main_layout)

        def _make_edit(self, text):
                self.edit = QtGui.QLineEdit(text, self)

        def _make_label(self, text):
                self.label = QtGui.QLabel(text, self)

        def _make_layout(self, layout_type):
                if layout_type == 'Horizontal':
                        return QtGui.QHBoxLayout()
                else:
                        return QtGui.QVBoxLayout()


class OkCancel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OkCancel, self).__init__(parent)
        self._initUI()

    def _initUI(self):
        main_layout = QtGui.QHBoxLayout()
        self.ok = QtGui.QPushButton('OK', self)
        self.cancel = QtGui.QPushButton('Cancelar', self)

        main_layout.addWidget(self.ok)
        main_layout.addWidget(self.cancel)

        self.setLayout(main_layout)



class TrackMenu(QtGui.QWidget):
    def __init__(self, parent):
        super(TrackMenu, self).__init__(parent)
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

    def _design_layout(self):
        main_layout = QtGui.QHBoxLayout()
        map(main_layout.addWidget, self.children())
        self.setLayout(main_layout)
        
    def _describe_behavior(self):
        self.connect(self.left_turn, QtCore.SIGNAL('clicked()'), self._do_left_turn)
        self.connect(self.straight, QtCore.SIGNAL('clicked()'), self._do_straight)
        self.connect(self.right_turn, QtCore.SIGNAL('clicked()'), self._do_right_turn)
        self.connect(self.clear, QtCore.SIGNAL('clicked()'), self._do_clear)

    def _do_left_turn(self):
        circuit.create_curve(-tracks.constants['angle'])
        self._print_log(u'curva para a esquerda')
        self.window().circuit_draw.updateGL()

    def _do_straight(self):
        circuit.create_straight()
        self._print_log(u'reta')
        self.window().circuit_draw.updateGL()

    def _do_right_turn(self):
        circuit.create_curve()
        self._print_log(u'curva para a direita')
        self.window().circuit_draw.updateGL()

    def _do_clear(self):
        self.parent().parent().log.clear()
        global circuit
        circuit = tracks.Circuit() 
        self.window().circuit_draw.circuit = circuit
        self.window().circuit_draw.updateGL()

    def _print_log(self, track_type):
        new_track = circuit[-1]
        last_track = circuit[-tracks.constants['diff_index']]
        logstr = u'Adicionada ' + track_type + u' com posição inicial ' + unicode(last_track.position) + u' e posição final ' + unicode(new_track.position) + u'.\n' + unicode(circuit[-1].orient * 180/pi)
        self.parent().parent().log.append(logstr)
        


class RightSplitter(QtGui.QGroupBox):
    def __init__(self, parent):
        super(RightSplitter, self).__init__('Escolha o tipo de trecho:', parent)
        self._initUI(parent)

    def _initUI(self, parent):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()

    def _create_widgets(self):
        self.menu = TrackMenu(self)
        self.log = QtGui.QTextEdit(self)

        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.menu)
        self.splitter.addWidget(self.log)

    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)

    def _describe_behavior(self):
        self.log.setReadOnly(True)



class MainWindow(QtGui.QWidget):
  
    def __init__(self):
        super(MainWindow, self).__init__()
        self._initUI()


    def _initUI(self):
        self._create_widgets()
        self._design_layout()
        self._describe_behavior()
        self.setWindowTitle('YMCircuit')


    def _create_widgets(self):
        self.right = RightSplitter(self)
        self.circuit_draw = CircuitWidget(circuit, self)

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)    
        self.splitter.addWidget(self.circuit_draw)
        self.splitter.addWidget(self.right)


    def _design_layout(self):
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)


    def _describe_behavior(self):
        pass


circuit = tracks.Circuit()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.show()
    sys.exit(app.exec_())
