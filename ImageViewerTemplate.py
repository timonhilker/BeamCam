# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



class Ui_Form(object):
    
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1200, 800)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))


        self.x0Spin = QtGui.QDoubleSpinBox(Form)
        self.x0Spin.setProperty("value", 200.)
        self.x0Spin.setObjectName(_fromUtf8("x0Spin"))
        self.gridLayout.addWidget(self.x0Spin, 1, 0, 1, 1)

        self.x0label = QtGui.QLabel(Form)
        self.x0label.setObjectName(_fromUtf8("x0label"))
        self.gridLayout.addWidget(self.x0label, 1, 1, 1, 1)

        self.y0Spin = QtGui.QDoubleSpinBox(Form)
        self.y0Spin.setProperty("value", 10)
        self.y0Spin.setObjectName(_fromUtf8("y0Spin"))
        self.gridLayout.addWidget(self.y0Spin, 2, 0, 1, 1)

        self.y0label = QtGui.QLabel(Form)
        self.y0label.setObjectName(_fromUtf8("y0label"))
        self.gridLayout.addWidget(self.y0label, 2, 1, 1, 1)

        self.sigmaxSpin = QtGui.QDoubleSpinBox(Form)
        self.sigmaxSpin.setProperty("value", 200.)
        self.sigmaxSpin.setObjectName(_fromUtf8("sigmaxSpin"))
        self.gridLayout.addWidget(self.sigmaxSpin, 3, 0, 1, 1)

        self.sigmaxlabel = QtGui.QLabel(Form)
        self.sigmaxlabel.setObjectName(_fromUtf8("sigmaxlabel"))
        self.gridLayout.addWidget(self.sigmaxlabel, 3, 1, 1, 1)

        self.sigmaySpin = QtGui.QDoubleSpinBox(Form)
        self.sigmaySpin.setProperty("value", 200.)
        self.sigmaySpin.setObjectName(_fromUtf8("sigmaySpin"))
        self.gridLayout.addWidget(self.sigmaySpin, 4, 0, 1, 1)

        self.sigmaylabel = QtGui.QLabel(Form)
        self.sigmaylabel.setObjectName(_fromUtf8("sigmaylabel"))
        self.gridLayout.addWidget(self.sigmaylabel, 4, 1, 1, 1)

        self.rotangleSpin = QtGui.QDoubleSpinBox(Form)
        self.rotangleSpin.setProperty("value", 200.)
        self.rotangleSpin.setObjectName(_fromUtf8("rotangleSpin"))
        self.gridLayout.addWidget(self.rotangleSpin, 5, 0, 1, 1)

        self.rotanglelabel = QtGui.QLabel(Form)
        self.rotanglelabel.setObjectName(_fromUtf8("rotanglelabel"))
        self.gridLayout.addWidget(self.rotanglelabel, 5, 1, 1, 1)




        self.camsettingslabel = QtGui.QLabel(Form)
        self.camsettingslabel.setObjectName(_fromUtf8("camsettingslabel"))
        self.gridLayout.addWidget(self.camsettingslabel, 2, 2, 1, 2)

        self.exposureSpin = QtGui.QDoubleSpinBox(Form)
        self.exposureSpin.setProperty("value", 200.)
        self.exposureSpin.setObjectName(_fromUtf8("exposureSpin"))
        self.gridLayout.addWidget(self.exposureSpin, 3, 2, 1, 1)

        self.exposurelabel = QtGui.QLabel(Form)
        self.exposurelabel.setObjectName(_fromUtf8("exposurelabel"))
        self.gridLayout.addWidget(self.exposurelabel, 3, 3, 1, 1)

        self.gainSpin = QtGui.QDoubleSpinBox(Form)
        self.gainSpin.setProperty("value", 200.)
        self.gainSpin.setObjectName(_fromUtf8("gainSpin"))
        self.gridLayout.addWidget(self.gainSpin, 4, 2, 1, 1)

        self.gainlabel = QtGui.QLabel(Form)
        self.gainlabel.setObjectName(_fromUtf8("gainlabel"))
        self.gridLayout.addWidget(self.gainlabel, 4, 3, 1, 1)




        self.orientationlabel = QtGui.QLabel(Form)
        self.orientationlabel.setObjectName(_fromUtf8("orientationlabel"))
        self.gridLayout.addWidget(self.orientationlabel, 2, 4, 1, 1)


        self.horRadio = QtGui.QRadioButton(Form)
        self.horRadio.setObjectName(_fromUtf8("horRadio"))
        self.gridLayout.addWidget(self.horRadio, 3, 4, 1, 1)
        self.vertRadio = QtGui.QRadioButton(Form)
        self.vertRadio.setChecked(True)
        self.vertRadio.setObjectName(_fromUtf8("vertRadio"))
        self.gridLayout.addWidget(self.vertRadio, 4, 4, 1, 1)
        self.stack = QtGui.QStackedWidget(Form)
        self.stack.setObjectName(_fromUtf8("stack"))



        self.optionslabel = QtGui.QLabel(Form)
        self.optionslabel.setObjectName(_fromUtf8("optionslabel"))
        self.gridLayout.addWidget(self.optionslabel, 2, 5, 1, 1)

        self.fitCheck = QtGui.QCheckBox(Form)
        self.fitCheck.setObjectName(_fromUtf8("fitCheck"))
        self.gridLayout.addWidget(self.fitCheck, 3, 5, 1, 1)

        self.trackCheck = QtGui.QCheckBox(Form)
        self.trackCheck.setObjectName(_fromUtf8("trackCheck"))
        self.gridLayout.addWidget(self.trackCheck, 4, 5, 1, 1)




        self.plot = GraphicsLayoutWidget(Form)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 6)



        self.retranslateUi(Form)
        self.stack.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "VRmagic USB Cam Live View", None, QtGui.QApplication.UnicodeUTF8))
        # self.pixelModeCheck.setText(QtGui.QApplication.translate("Form", "pixel mode", None, QtGui.QApplication.UnicodeUTF8))
        self.x0label.setText(QtGui.QApplication.translate("Form", "x(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.y0label.setText(QtGui.QApplication.translate("Form", "y(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.sigmaxlabel.setText(QtGui.QApplication.translate("Form", "sigma x", None, QtGui.QApplication.UnicodeUTF8))
        self.sigmaylabel.setText(QtGui.QApplication.translate("Form", "sigma y", None, QtGui.QApplication.UnicodeUTF8))
        self.rotanglelabel.setText(QtGui.QApplication.translate("Form", "Rotation angle", None, QtGui.QApplication.UnicodeUTF8))
        self.camsettingslabel.setText(QtGui.QApplication.translate("Form", "Camera settings", None, QtGui.QApplication.UnicodeUTF8))
        self.exposurelabel.setText(QtGui.QApplication.translate("Form", "Exposure time", None, QtGui.QApplication.UnicodeUTF8))
        self.gainlabel.setText(QtGui.QApplication.translate("Form", "Gain", None, QtGui.QApplication.UnicodeUTF8))
        

        self.orientationlabel.setText(QtGui.QApplication.translate("Form", "Orientation", None, QtGui.QApplication.UnicodeUTF8))
        self.horRadio.setText(QtGui.QApplication.translate("Form", "horizontal", None))
        self.vertRadio.setText(QtGui.QApplication.translate("Form", "vertical", None))

        self.optionslabel.setText(QtGui.QApplication.translate("Form", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.fitCheck.setText(QtGui.QApplication.translate("Form", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.trackCheck.setText(QtGui.QApplication.translate("Form", "Track", None, QtGui.QApplication.UnicodeUTF8))


from pyqtgraph import GraphicsLayoutWidget
