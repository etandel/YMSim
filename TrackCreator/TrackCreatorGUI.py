#coding: UTF-8
{'configured': True}
PROJECT_DIR = "/home/echobravo/Projects/YMSim"
from sys import path
path.append(PROJECT_DIR)

"""GUI for circuit creation"""

import sys
from PyQt4 import QtGui, QtCore
import tracks

class LabeledEdit(QtGui.QWidget):
        def __init__(self, label_txt='', edit_txt='', parent=None, layout_type = 'Horizontal'):
                super(LabeledEdit, self).__init__(parent)
                self._initUI(label_txt, edit_txt, layout_type)

        def _initUI(self, label_txt, edit_txt, layout_type):

                main_layout = self._make_layout(layout_type)
                label = self._make_label(label_txt)
                edit = self._make_edit(edit_txt)
                main_layout.addWidget(label)
                main_layout.addWidget(edit)
                self.setLayout(main_layout)

        def _make_edit(self, text):
                return QtGui.QLineEdit(text, self)

        def _make_label(self, text):
                return QtGui.QLabel(text, self)

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


def create_opts_dlgs():
    class Curve(QtGui.QGroupBox):
	def __init__(self):
        	super(Curve, self).__init__()
		self._initUI()

	def _initUI(self):
		self.setWindowTitle(u'Opções de Curva')
		self._create_widgets()
		self._design_layout()

	def _create_widgets(self):
		self.radius_edit = LabeledEdit('Raio:', parent = self)
		self.angle_edit = LabeledEdit('Arco:', parent = self)
		self.okcancel = OkCancel(self)

	def _design_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.addWidget(self.radius_edit)
		main_layout.addWidget(self.angle_edit)
		main_layout.addWidget(self.okcancel)
		self.setLayout(main_layout)

	def _describe_behavior(self):
		self.connect(okcancel.ok, QtCore.SIGNAL('clicked()'), self._do_ok)
		self.connect(okcancel.cancel, QtCore.SIGNAL('clicked()'), self._do_cancel)
		

	def _do_ok(self):
		pass

	def _do_cancel(self):
		pass
  
    class Straight(QtGui.QGroupBox):
	def __init__(self):
        	super(Straight, self).__init__()
		self._initUI()

	def _initUI(self):
		self.setWindowTitle(u'Opções de Reta:')
		self._create_widgets()
		self._design_layout()


	def _create_widgets(self):
		self.straight = LabeledEdit('Comprimento:', parent = self)
		self.okcancel = OkCancel(self)

	def _design_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.addWidget(self.straight)
		main_layout.addWidget(self.okcancel)
		self.setLayout(main_layout)


    class Clothoid(QtGui.QGroupBox):
	pass


    return {
   	'curve': Curve(),
   	'straight': Straight(),
   	'clothoid': Clothoid(),
    }
        

class TrackMenu(QtGui.QGroupBox):
    def __init__(self, parent):
        super(TrackMenu, self).__init__('Escolha o tipo de trecho:', parent)
        self._initUI(parent)

    def _initUI(self, parent):
	self._create_widgets()
	self._design_layout()
	self._describe_behavior()

    def _describe_behavior(self):
	self.connect(self.straight, QtCore.SIGNAL('clicked()'), self._straight_dialog)
	self.connect(self.curve, QtCore.SIGNAL('clicked()'), self._curve_dialog)
	self.connect(self.clothoid, QtCore.SIGNAL('clicked()'), self._clothoid_dialog)


    def _create_widgets(self):
	self.straight = QtGui.QPushButton('Reta', self)
	self.curve = QtGui.QPushButton('Curva', self)
	self.clothoid = QtGui.QPushButton(u'Clotóide', self)

    def _design_layout(self):
	self.main_layout = QtGui.QHBoxLayout()
	
	self.main_layout.addWidget(self.straight)
	self.main_layout.addWidget(self.curve)
	self.main_layout.addWidget(self.clothoid)
	self.setLayout(self.main_layout)

    def _straight_dialog(self):
	for dlg in track_opts_dlgs:
		track_opts_dlgs[dlg].hide()
   	track_opts_dlgs['straight'].show()
	
    def _curve_dialog(self):	
	for dlg in track_opts_dlgs:
		track_opts_dlgs[dlg].hide()
    	track_opts_dlgs['curve'].show()

    def _clothoid_dialog(self):	
	for dlg in track_opts_dlgs:
		track_opts_dlgs[dlg].hide()
    	track_opts_dlgs['clothoid'].show()
	

class MainWindow(QtGui.QWidget):
  
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()


    def initUI(self):
	self.setWindowTitle('YMCircuit')
	self.maximize()

	track_menu = TrackMenu(self)

	testBtn3 = QtGui.QPushButton('Test3', self)

	splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)	
	splitter.addWidget(testBtn3)
	splitter.addWidget(track_menu)

	vbox = QtGui.QVBoxLayout()
	vbox.addWidget(splitter)
	self.setLayout(vbox)


    def maximize(self):
	screen = QtGui.QDesktopWidget().screenGeometry()
       	self.setGeometry(0,0, screen.width(), screen.height())
		
        

def main():

    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.show()
    global track_opts_dlgs
    track_opts_dlgs = create_opts_dlgs()
    app.exec_()


if __name__ == '__main__':
    main()
