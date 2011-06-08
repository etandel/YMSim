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


def create_opts_dlgs():
    class GetOpts(QtGui.QGroupBox):

	def __init__(self, window_title):
		super(GetOpts, self).__init__()
		self._initUI(window_title)

	def _initUI(self, window_title):
		self.setWindowTitle(window_title)
		self._create_widgets()
		self._design_layout()
		self._describe_behavior()
		
		

	def _design_layout(self):
		main_layout = QtGui.QVBoxLayout()
		for child in self.children():
			main_layout.addWidget(child)
		self.setLayout(main_layout)

	def _describe_behavior(self):
		self.connect(self.okcancel.ok, QtCore.SIGNAL('clicked()'), self._do_ok)
		self.connect(self.okcancel.cancel, QtCore.SIGNAL('clicked()'), self._do_cancel)

	def _do_ok(self):
		#validate
		#mandar entrada para função createXXX
		#metodo abstrato apenas
		pass

	def _do_cancel(self):
		self.hide()

	def _atribute_type_error(self):
		msgbox = QtGui.QMessageBox(self)
		msgbox.setText(u"Atributos de pista devem conter apenas números.")
		msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
		msgbox.setDefaultButton(QtGui.QMessageBox.Ok)
		msgbox.exec_()
			
    class Curve(GetOpts):
	def _create_widgets(self):
		self.radius_edit = LabeledEdit('Raio:', parent = self)
		self.angle_edit = LabeledEdit('Arco:', parent = self)
		self.okcancel = OkCancel(self)

	def _do_ok(self):
		radius = tracks.validate_float(self.radius_edit.edit.text())
		angle = tracks.validate_float(self.angle_edit.edit.text())
		if angle == None or radius == None:
			self._atribute_type_error()

  
    class Straight(GetOpts):
	def _create_widgets(self):
		self.straight = LabeledEdit('Comprimento:', parent = self)
		self.okcancel = OkCancel(self)


    class Clothoid(GetOpts):
	def _create_widgets(self):
		self.okcancel = OkCancel(self)


    return {
   	'curve': Curve(u'Opções de Curva'),
   	'straight': Straight(u'Opções de Reta:'),
   	'clothoid': Clothoid(u'opções de Clotóide'),
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

        self._initUI()


    def _initUI(self):
	self._create_widgets()
	self._design_layout()
	self._describe_behavior()

	self.setWindowTitle('YMCircuit')




    def _create_widgets(self):
	self.track_menu = TrackMenu(self)
	self.testBtn3 = QtGui.QPushButton('Test3', self)

	self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)	
	self.splitter.addWidget(self.testBtn3)
	self.splitter.addWidget(self.track_menu)

    def _design_layout(self):
	main_layout = QtGui.QVBoxLayout()
	main_layout.addWidget(self.splitter)
	self.setLayout(main_layout)
	pass

    def _describe_behavior(self):
	pass


def main():

    app = QtGui.QApplication(sys.argv)
    wind = MainWindow(); wind.showMaximized()
    global track_opts_dlgs
    track_opts_dlgs = create_opts_dlgs()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
