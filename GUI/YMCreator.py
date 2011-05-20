# -*- coding: UTF-8 -*-
{'configured': False}

"""Module for circuit creation"""

import sys
from PyQt4 import QtGui, QtCore

class GetOpts(QtGui.QWidget):
  
    def __init__(self, track_type):
        super(GetOpts, self).__init__()
        
        self.initUI(track_type)
        
    def initUI(self, track_type):
	layout = self.make_all(self, track_type)
	self.setLayout(layout)

        self.resize(350, 300)

    def make_all(self, parent, track_type):
	if track_type == 'Escolha o tipo de pedaço: ':
		layout = self.make_default(self)
	elif track_type == 'Reta':
		layout = self.make_straight(self)
	elif track_type == 'Curva':
		layout = self.make_curve(self)
	else:
		layout = self.make_clothoid(self)

	return layout 
	

    def make_default(self, parent):
	return QtGui.QVBoxLayout()

    def make_straight(self, parent):
        length = QtGui.QLabel('Comprimento: ', parent)

        length_edit = QtGui.QLineEdit('Digite o comprimento.', parent)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(length, 1, 0)
        grid.addWidget(length_edit, 1, 1)

        self.setWindowTitle(u'Opções de Reta')

	return grid

    def make_curve(self, parent):
        angle = QtGui.QLabel(u'Arco: ', parent)
        radius = QtGui.QLabel('Raio: ', parent)

        angle_edit = QtGui.QLineEdit('Digite o arco de curva.', parent)
        radius_edit = QtGui.QLineEdit('Digite o raio da curva.', parent)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(angle, 1, 0)
        grid.addWidget(angle_edit, 1, 1)

        grid.addWidget(radius, 2, 0)
        grid.addWidget(radius_edit, 2, 1)

        self.setWindowTitle(u'Opções de Curva')

	return grid

    def make_clothoid(self, parent):
	pass


class TrackCreator(QtGui.QGroupBox):
    def __init__(self, parent):
        super(TrackCreator, self).__init__('Escolha o tipo de trecho:', parent)
        self.initUI(parent)

    def initUI(self, parent):
	#create main widgets and layouts
	straight = QtGui.QPushButton('Reta', self)
	curve = QtGui.QPushButton('Curva', self)
	clothoid = QtGui.QPushButton(u'Clotóide', self)
	self.main_layout = QtGui.QVBoxLayout()

	#create buttons
	self.main_layout.addWidget(straight)
	self.main_layout.addWidget(curve)
	self.main_layout.addWidget(clothoid)

	parent.connect(straight, QtCore.SIGNAL('clicked()'), self.straight_dialog)
	parent.connect(curve, QtCore.SIGNAL('clicked()'), self.curve_dialog)
	parent.connect(clothoid, QtCore.SIGNAL('clicked()'), self.clothoid_dialog)

	#make layout
	self.main_layout.addWidget(straight)
	self.main_layout.addWidget(curve)
	self.main_layout.addWidget(clothoid)
	self.setLayout(self.main_layout)

    def straight_dialog(self):
	dlg = GetOpts("Reta")
	dlg.show()

    def curve_dialog(self):	
	pass

    def clothoid_dialog(self):	
	pass
	

class MainWindow(QtGui.QWidget):
  
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()


    def initUI(self):
	self.setWindowTitle('YMCircuit')
	self.maximize()

	track_creator = TrackCreator(self)

	testBtn3 = QtGui.QPushButton('Test3', self)

	splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)	
	splitter.addWidget(testBtn3)
	splitter.addWidget(track_creator)

	vbox = QtGui.QVBoxLayout()
	vbox.addWidget(splitter)
	self.setLayout(vbox)


    def maximize(self):
	screen = QtGui.QDesktopWidget().screenGeometry()
       	self.setGeometry(0,0, screen.width(), screen.height())
		
        

def main():

    app = QtGui.QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    app.exec_()


if __name__ == '__main__':
    main()
