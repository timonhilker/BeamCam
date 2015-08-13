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





def Create2DGaussian(RoiShape,*Parameters):




    x = np.arange(RoiShape[1])
    y = np.arange(RoiShape[0])

    XY = np.meshgrid(x,y)

    XYflat = np.array(XY).reshape(2,RoiShape[1]*RoiShape[0]).T

    # params = [amplitude,sigmax,position[0],position[1],sigmay,rotationangle,offset]


    gaussflat = gaussian2(XYflat,*Parameters)
    gauss = np.array(gaussflat).reshape(ny,nx)

    return gauss

def ellipse(x,sigmax,sigmay):
    return np.sqrt((sigmay**2)*(1-((x**2)/(sigmax**2))))





def StartGUI(camera='Simulation is used'):

    def InitializeCam(camera,ui):
        ExpoTime = camera.GetExposureTime(camera.CamIndex)
        ui.exposureSpin.setProperty("value", ExpoTime)
        GainValue = camera.GetGainValue(camera.CamIndex)
        ui.gainSpin.setProperty("value", GainValue)


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
    view.setRange(QtCore.QRectF(0, 0, 754, 754))

    # Custom ROI for selecting an image region
    roi = pg.ROI([310, 210], [200, 200],pen='b')
    roi.addScaleHandle([0.5, 1], [0.5, 0.5])
    roi.addScaleHandle([0, 0.5], [0.5, 0.5])
    view.addItem(roi)
    roi.setZValue(10)  # make sure ROI is drawn above

    symbol = ['x']
    peak = pg.PlotDataItem(symbol = symbol,symbolPen='g',Pen=None,symbolBrush='g',symbolSize=25)
    view.addItem(peak)
    peak.setZValue(20)

    symbol = ['x']
    peakpos = pg.PlotDataItem(symbol = symbol,symbolPen='r',Pen=None,symbolBrush='r',symbolSize=25)
    view.addItem(peakpos)
    peakpos.setZValue(20)


    contour = pg.PlotDataItem()
    contour.setPen('g')
    view.addItem(contour)
    contour.setZValue(30)


    refcontour = pg.PlotDataItem()
    refcontour.setPen('r')
    view.addItem(refcontour)
    refcontour.setZValue(25)




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

    if RealData:
        InitializeCam(camera,ui)

    win.show()


                
    def updateview():

        global ImageArray, img

        # simulation.NewImage()
        # simulation.AddWhiteNoise()
        # simulation.AddRandomGauss()
        # simulation.SimulateTotalImage()

        if ui.horRadio.isChecked():
            view.setRange(QtCore.QRectF(0, 0, 754, 480))
            ui.x0Spin.setRange(0.,754.)
            ui.y0Spin.setRange(0.,480.)
            if RealData==False:
                simulation.ChooseImage()
                ImageArray = simulation.image
            else:
                camera.GrabNextImage()
                ImageArray = camera.ImageArray
        elif ui.vertRadio.isChecked():
            view.setRange(QtCore.QRectF(0, 0, 480, 754))
            ui.x0Spin.setRange(0.,480.)
            ui.y0Spin.setRange(0.,754.)
            if RealData==False:
                simulation.ChooseImage()
                ImageArray = simulation.image.T
            else:
                camera.GrabNextImage()
                ImageArray = camera.ImageArray.T

        if RealData:
            camera.SetExposureTime(camera.CamIndex,ui.exposureSpin.value())
            camera.SetGainValue(camera.CamIndex,ui.gainSpin.value())




        
        img.setImage(ImageArray.T)

        # contour.clear()
        updateRoi()

    def updateRoi():

        

        global ImageArray, img

        selected = roi.getArrayRegion(ImageArray.T, img)
        p2.plot(selected.sum(axis=1), clear=True)



        datahor = selected.sum(axis=1)
        FittedParamsHor = MatTools.FitGaussian(datahor)[0]
        xhor = np.arange(datahor.size)

        if ui.fitCheck.isChecked():
            p2.plot(MatTools.gaussian(xhor,*FittedParamsHor), pen=(0,255,0))


        p3.plot(selected.sum(axis=0), clear=True).rotate(90)

        datavert = selected.sum(axis=0)
        FittedParamsVert = MatTools.FitGaussian(datavert)[0]
        xvert = np.arange(datavert.size)

        if ui.fitCheck.isChecked():
            p3.plot(MatTools.gaussian(xvert,*FittedParamsVert), pen=(0,255,0)).rotate(90)


        if ui.trackCheck.isChecked():

            
            # view.addItem(peak)

            

            hLine.setPos(FittedParamsVert[2]+roi.pos()[1])
            vLine.setPos(FittedParamsHor[2]+roi.pos()[0])

            vLine.show()
            hLine.show()

            # view.addItem(hLine)
            # view.addItem(vLine)    
            pos = np.array([[(FittedParamsHor[2]+roi.pos()[0]),(FittedParamsVert[2]+roi.pos()[1])]])           
            peak.setData(pos,clear=True)


            # peakposition = np.array([[ui.x0Spin.value(),ui.y0Spin.value()]])
            # peakpos.setData(peakposition,clear=True)

            x = np.linspace(-(FittedParamsHor[1]),(FittedParamsHor[1]),1000)
            sigmax = FittedParamsHor[1]
            sigmay = FittedParamsVert[1]
            y = ellipse(x,sigmax,sigmay)

            x = np.append(x,-x)
            y = np.append(y,-y)
            
            x += FittedParamsHor[2]+roi.pos()[0]
            y += FittedParamsVert[2]+roi.pos()[1]
            # X,Y = np.meshgrid(x,y)
            # contour.clear()
            contour.setData(x,y,clear=True)

        else:
            # view.removeItem(hLine)
            # view.removeItem(vLine)
            vLine.hide()
            hLine.hide()
            contour.clear()
            peak.clear()


        if ui.refCheck.isChecked():

            peakposition = np.array([[ui.x0Spin.value(),ui.y0Spin.value()]])
            peakpos.setData(peakposition,clear=True)


            sigmax = ui.sigmaxSpin.value()
            sigmay = ui.sigmaySpin.value()
            x = np.linspace(-(sigmax),(sigmax),1000)
            y = ellipse(x,sigmax,sigmay)

            x = np.append(x,-x)
            y = np.append(y,-y)
            
            x += ui.x0Spin.value()
            y += ui.y0Spin.value()
            # X,Y = np.meshgrid(x,y)
            # contour.clear()
            refcontour.setData(x,y,clear=True)




        else:
            peakpos.clear()
            refcontour.clear()


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
    StartGUI(camera)
    camera.StopCam()




