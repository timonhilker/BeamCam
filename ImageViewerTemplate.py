# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



class Ui_Form(object):
    
    def setupUi(self, Form):
        '''Defines the general properties of the window'''
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1200, 1000)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        '''Defines the spin box for x0'''
        self.x0Spin = QtGui.QDoubleSpinBox(Form)
        self.x0Spin.setRange(0.,754.)
        self.x0Spin.setProperty("value", 350)
        self.x0Spin.setObjectName(_fromUtf8("x0Spin"))
        self.gridLayout.addWidget(self.x0Spin, 1, 0, 1, 1)
        
        '''Defines the label for the x0 spin box'''
        self.x0label = QtGui.QLabel(Form)
        self.x0label.setObjectName(_fromUtf8("x0label"))
        self.gridLayout.addWidget(self.x0label, 1, 1, 1, 1)

        '''Defines the spin box for y0'''
        self.y0Spin = QtGui.QDoubleSpinBox(Form)
        self.y0Spin.setRange(0.,480.)
        self.y0Spin.setProperty("value", 240)
        self.y0Spin.setObjectName(_fromUtf8("y0Spin"))
        self.gridLayout.addWidget(self.y0Spin, 2, 0, 1, 1)
        
        '''Defines the label for the y0 spin box'''
        self.y0label = QtGui.QLabel(Form)
        self.y0label.setObjectName(_fromUtf8("y0label"))
        self.gridLayout.addWidget(self.y0label, 2, 1, 1, 1)

        '''Defines the spin box for the horizontal waist'''
        self.sigmaxSpin = QtGui.QDoubleSpinBox(Form)
        self.sigmaxSpin.setRange(0.,100.)
        self.sigmaxSpin.setProperty("value", 30.)
        self.sigmaxSpin.setObjectName(_fromUtf8("sigmaxSpin"))
        self.gridLayout.addWidget(self.sigmaxSpin, 3, 0, 1, 1)

        '''Defines the label for the horizontal waist spin box'''
        self.sigmaxlabel = QtGui.QLabel(Form)
        self.sigmaxlabel.setObjectName(_fromUtf8("sigmaxlabel"))
        self.gridLayout.addWidget(self.sigmaxlabel, 3, 1, 1, 1)

        '''Defines the spin box for the vertical waist'''
        self.sigmaySpin = QtGui.QDoubleSpinBox(Form)
        self.sigmaySpin.setRange(0.,100.)
        self.sigmaySpin.setProperty("value", 50.)
        self.sigmaySpin.setObjectName(_fromUtf8("sigmaySpin"))
        self.gridLayout.addWidget(self.sigmaySpin, 4, 0, 1, 1)

        '''Defines the label for the vertical waist spin box'''
        self.sigmaylabel = QtGui.QLabel(Form)
        self.sigmaylabel.setObjectName(_fromUtf8("sigmaylabel"))
        self.gridLayout.addWidget(self.sigmaylabel, 4, 1, 1, 1)

        # self.rotangleSpin = QtGui.QDoubleSpinBox(Form)
        # self.rotangleSpin.setProperty("value", 200.)
        # self.rotangleSpin.setObjectName(_fromUtf8("rotangleSpin"))
        # self.gridLayout.addWidget(self.rotangleSpin, 5, 0, 1, 1)

        # self.rotanglelabel = QtGui.QLabel(Form)
        # self.rotanglelabel.setObjectName(_fromUtf8("rotanglelabel"))
        # self.gridLayout.addWidget(self.rotanglelabel, 5, 1, 1, 1)


        self.choosecam = QtGui.QComboBox()
        self.choosecam.setObjectName(_fromUtf8("choosecam"))
        self.gridLayout.addWidget(self.choosecam, 1, 2, 1, 1)
        # self.choosecam.addItem("Test 1")
        # self.choosecam.addItem("Test 2")


        '''Defines the text label for camera settings'''
        self.camsettingslabel = QtGui.QLabel(Form)
        self.camsettingslabel.setObjectName(_fromUtf8("camsettingslabel"))
        self.gridLayout.addWidget(self.camsettingslabel, 2, 2, 1, 2)

        '''Defines the spin box for the exposure time'''
        self.exposureSpin = QtGui.QDoubleSpinBox(Form)
        self.exposureSpin.setRange(0.,100.)
        self.exposureSpin.setProperty("value", 1.)
        self.exposureSpin.setDecimals(4)
        self.exposureSpin.setSingleStep(0.1)
        self.exposureSpin.setObjectName(_fromUtf8("exposureSpin"))
        self.gridLayout.addWidget(self.exposureSpin, 3, 2, 1, 1)

        '''Defines the label for the exposure time spin box'''
        self.exposurelabel = QtGui.QLabel(Form)
        self.exposurelabel.setObjectName(_fromUtf8("exposurelabel"))
        self.gridLayout.addWidget(self.exposurelabel, 3, 3, 1, 1)

        '''Defines the spin box for the gain value'''
        self.gainSpin = QtGui.QSpinBox(Form)
        self.gainSpin.setRange(16,64)
        self.gainSpin.setProperty("value", 16)
        self.gainSpin.setObjectName(_fromUtf8("gainSpin"))
        self.gridLayout.addWidget(self.gainSpin, 4, 2, 1, 1)

        '''Defines the label for the gain value spin box'''
        self.gainlabel = QtGui.QLabel(Form)
        self.gainlabel.setObjectName(_fromUtf8("gainlabel"))
        self.gridLayout.addWidget(self.gainlabel, 4, 3, 1, 1)



        '''Defines the 'Hold' push button'''
        self.hold =  QtGui.QPushButton('Hold')
        self.hold.setObjectName(_fromUtf8("hold"))
        self.gridLayout.addWidget(self.hold, 1, 4, 1, 1)
        self.hold.setCheckable(True)
        self.hold.setToolTip('Pause the live view')
        # self.hold.setChecked(False)

        '''Defins the text box for the 'orientation' heading'''
        self.orientationlabel = QtGui.QLabel(Form)
        self.orientationlabel.setObjectName(_fromUtf8("orientationlabel"))
        self.gridLayout.addWidget(self.orientationlabel, 2, 4, 1, 1)

        '''Defines the buttons for choosing the orientation'''
        self.horRadio = QtGui.QRadioButton(Form)
        self.horRadio.setChecked(True)
        self.horRadio.setObjectName(_fromUtf8("horRadio"))
        self.gridLayout.addWidget(self.horRadio, 3, 4, 1, 1)
        self.vertRadio = QtGui.QRadioButton(Form)
        # self.vertRadio.setChecked(True)
        self.vertRadio.setObjectName(_fromUtf8("vertRadio"))
        self.gridLayout.addWidget(self.vertRadio, 4, 4, 1, 1)
        self.stack = QtGui.QStackedWidget(Form)
        self.stack.setObjectName(_fromUtf8("stack"))


        '''Defines the heading for the 'options' column'''
        self.optionslabel = QtGui.QLabel(Form)
        self.optionslabel.setObjectName(_fromUtf8("optionslabel"))
        self.gridLayout.addWidget(self.optionslabel, 1, 5, 1, 1)

        '''Defines the check box for fitting'''
        self.fitCheck = QtGui.QCheckBox(Form)
        self.fitCheck.setObjectName(_fromUtf8("fitCheck"))
        self.gridLayout.addWidget(self.fitCheck, 2, 5, 1, 1)
        self.fitCheck.setChecked(True)

        '''Defines the check box for tracking'''
        self.trackCheck = QtGui.QCheckBox(Form)
        self.trackCheck.setObjectName(_fromUtf8("trackCheck"))
        self.gridLayout.addWidget(self.trackCheck, 3, 5, 1, 1)
        self.trackCheck.setChecked(True)

        '''Defines the check box for the reference beam'''
        self.refCheck = QtGui.QCheckBox(Form)
        self.refCheck.setObjectName(_fromUtf8("refCheck"))
        self.gridLayout.addWidget(self.refCheck, 4, 5, 1, 1)
        self.refCheck.setChecked(True)





        '''Defines the plot widget'''
        self.plot = GraphicsLayoutWidget(Form)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 6)


        '''Puts everything together'''
        self.retranslateUi(Form)
        self.stack.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        '''Sets the right names to the objects'''

        Form.setWindowTitle(QtGui.QApplication.translate("Form", "VRmagic USB Cam Live View", None, QtGui.QApplication.UnicodeUTF8))
        # self.pixelModeCheck.setText(QtGui.QApplication.translate("Form", "pixel mode", None, QtGui.QApplication.UnicodeUTF8))
        self.x0label.setText(QtGui.QApplication.translate("Form", "x(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.y0label.setText(QtGui.QApplication.translate("Form", "y(0)", None, QtGui.QApplication.UnicodeUTF8))
        self.sigmaxlabel.setText(QtGui.QApplication.translate("Form", "Waist horizontal", None, QtGui.QApplication.UnicodeUTF8))
        self.sigmaylabel.setText(QtGui.QApplication.translate("Form", "Waist vertical", None, QtGui.QApplication.UnicodeUTF8))
        # self.rotanglelabel.setText(QtGui.QApplication.translate("Form", "Rotation angle", None, QtGui.QApplication.UnicodeUTF8))
        self.camsettingslabel.setText(QtGui.QApplication.translate("Form", "Camera settings", None, QtGui.QApplication.UnicodeUTF8))
        self.exposurelabel.setText(QtGui.QApplication.translate("Form", "Exposure time [ms]", None, QtGui.QApplication.UnicodeUTF8))
        self.gainlabel.setText(QtGui.QApplication.translate("Form", "Gain", None, QtGui.QApplication.UnicodeUTF8))
        

        self.orientationlabel.setText(QtGui.QApplication.translate("Form", "Orientation", None, QtGui.QApplication.UnicodeUTF8))
        self.horRadio.setText(QtGui.QApplication.translate("Form", "horizontal", None))
        self.vertRadio.setText(QtGui.QApplication.translate("Form", "vertical", None))

        self.optionslabel.setText(QtGui.QApplication.translate("Form", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.fitCheck.setText(QtGui.QApplication.translate("Form", "Show Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.trackCheck.setText(QtGui.QApplication.translate("Form", "Track Beam", None, QtGui.QApplication.UnicodeUTF8))
        self.refCheck.setText(QtGui.QApplication.translate("Form", "Show Reference Beam", None, QtGui.QApplication.UnicodeUTF8))


from pyqtgraph import GraphicsLayoutWidget
