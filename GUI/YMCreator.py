{'configured': False}

"""Module for circuit creation"""

import sys
from PyQt4 import QtGui, QtCore


class TrackCreator():
	def __init__(self, parent):
		self.track_list = self.make_track_list(parent)
		self.main_container = QtGui.QGroupBox('Escolha o tipo de trecho:')
		self.main_layout = QtGui.QHBoxLayout()
		self.options = QtGui.QGroupBox("Opcoes:", parent)
		self.main_container.setLayout(self.main_layout)
	
	def make_track_list(self, parent):
		track_type = QtGui.QComboBox(parent)
		track_type.addItem("Reta")
		track_type.addItem("Curva")
		track_type.addItem("Clotoide")
		parent.connect(track_type, QtCore.SIGNAL('activated(QString)'), self.on_track_chosen)
		return track_type

	def on_track_chosen(self, text):
		if text == 'Reta':
			self.options = QtGui.QHBoxLayout(self,track_type)

			length_edit = QtGui.QLineEdit(parent = MainWindow)
			length_edit.setText("Digite o comprimento da reta.")
			
			gerate_button = QtGui.QPushButton('Gerar Trecho', None)
			
			self.options_layout.addWidget(length_edit)
			self.options_layout_.addWidget(generate_button)

			#doreta
			pass
		elif text == 'Curva':
			#docurva
			pass
		elif text == 'Clotoide':
			#doclot
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
	splitter.addWidget(track_creator.container)

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
