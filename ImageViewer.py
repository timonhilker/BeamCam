# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:18:13 2015

@author: Michael
"""


import GaussBeamSimulation as Sim
reload(Sim)
import MathematicalTools as MatTools
reload(MatTools)
import VRmUsbCamAPI as CamAPI
reload(CamAPI)

from ctypes import *
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys

from ImageViewerTemplate import Ui_Form
# reload(ImageViewerTemplate)


RealData = False






def StartGUI():

    global img

    app = QtGui.QApplication([])

    win = QtGui.QWidget()

    ui = Ui_Form()
    ui.setupUi(win)

    # Image widget
    imagewidget = ui.plot
    view = imagewidget.addViewBox()
    view.setAspectLocked(True)
    img = pg.ImageItem(border='k')
    view.addItem(img)
    view.setRange(QtCore.QRectF(0, 0, 754, 480))

    # Custom ROI for selecting an image region
    roi = pg.ROI([310, 210], [200, 200],pen=(0,9))
    roi.addScaleHandle([0.5, 1], [0.5, 0.5])
    roi.addScaleHandle([0, 0.5], [0.5, 0.5])
    view.addItem(roi)
    roi.setZValue(10)  # make sure ROI is drawn above


    peak = pg.GraphItem()
    symbol = ['x']
    view.addItem(peak)
    roi.setZValue(20)

    p3 = imagewidget.addPlot(colspan=1)
    # p3.rotate(90)
    p3.setMaximumWidth(200)

    # Another plot area for displaying ROI data
    imagewidget.nextRow()
    p2 = imagewidget.addPlot(colspan=1)
    p2.setMaximumHeight(200)

    #cross hair
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    view.addItem(vLine, ignoreBounds=True)
    view.addItem(hLine, ignoreBounds=True)

    #curve for contourplot
    # curve = pg.IsocurveItem(level=0)
    # curve.setParentItem(img)  ## make sure isocurve is always correctly displayed over image
    # curve.setZValue(10)

                
    # win.show()


    # layout = QtGui.QGridLayout()
    # win.setLayout(layout)
    # win.setWindowTitle('VRmagic USB Cam Live View')
    # layout.addWidget(imagewidget, 1, 2, 3, 1)
    # win.resize(1100, 870)
    win.show()


                
    def updateview():

        global ImageArray, img

        # simulation.NewImage()
        # simulation.AddWhiteNoise()
        # simulation.AddRandomGauss()
        # simulation.SimulateTotalImage()

        if RealData==False:
            simulation.ChooseImage()
            ImageArray = simulation.image
        else:
            camera.GrabNextImage()
            ImageArray = camera.ImageArray


        
        img.setImage(ImageArray.T)

        updateRoi()

    def updateRoi():

        global ImageArray, img

        selected = roi.getArrayRegion(ImageArray.T, img)
        p2.plot(selected.sum(axis=1), clear=True)

        datahor = selected.sum(axis=1)
        FittedParamsHor = MatTools.FitGaussian(datahor)[0]
        xhor = np.arange(datahor.size)
        p2.plot(MatTools.gaussian(xhor,*FittedParamsHor), pen=(0,255,0))


        p3.plot(selected.sum(axis=0), clear=True).rotate(-90)

        datavert = selected.sum(axis=0)
        FittedParamsVert = MatTools.FitGaussian(datavert)[0]
        xvert = np.arange(datavert.size)
        p3.plot(MatTools.gaussian(xvert,*FittedParamsVert), pen=(0,255,0)).rotate(-90)

        hLine.setPos(FittedParamsVert[2]+roi.pos()[1])
        vLine.setPos(FittedParamsHor[2]+roi.pos()[0])


            
        pos = np.array([[(FittedParamsHor[2]+roi.pos()[0]),(FittedParamsVert[2]+roi.pos()[1])]])
        peak.setData(pos=pos,symbol=symbol,size=25, symbolPen='g', symbolBrush='g')
            
        # print roi.pos, 'ROI Position'



        # print 'ROI Sum: ', selected.sum(axis=1)


    roi.sigRegionChanged.connect(updateRoi)

    viewtimer = QtCore.QTimer()
    viewtimer.timeout.connect(updateview)
    viewtimer.start(0)

    app.exec_()
    viewtimer.stop()



if RealData==False:
    simulation = Sim.GaussBeamSimulation()
    simulation.CreateImages()
    StartGUI()
else: 
    camera = CamAPI.VRmagicUSBCam_API()
    camera.InitializeCam()
    camera.StartCam()
    StartGUI()
    camera.StopCam()




