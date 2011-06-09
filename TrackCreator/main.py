import TrackCreatorGui

#GUI stuff
app = QtGui.QApplication(sys.argv)
wind = MainWindow(); wind.showMaximized()
track_opts_dlgs = create_opts_dlgs()
sys.exit(app.exec_())

