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
import time
import os

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
        # Switch off status LED
        camera.SetStatusLED(camera.CamIndex,False)

    def CreateFile(name='test'):
        if not os.path.exists(name):
            f = open(name+'.txt', 'w')
            f.close()
        else:
            print 'A file with this name already exists!'



    global img, databuffer

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
    bounds = QtCore.QRectF(0,0,753,479)
    roi.maxBounds = bounds


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

    amphist = imagewidget.addPlot(colspan=1,title='Amplitude<br>in ROI')
    amphist.setMaximumWidth(100)
    amphist.hideAxis('bottom')

    timeplot = imagewidget.addPlot(colspan=1,title='Time Evolution')
    timeplot.setMaximumWidth(400)

    # Another plot area for displaying ROI data
    imagewidget.nextRow()
    p2 = imagewidget.addPlot(colspan=1)
    p2.setMaximumHeight(200)

    texthtml = '<div style="text-align: center"><span style="color: #FFF; font-size: 16pt;">Beam Properties</span><br>\
    <span style="color: #FFF; font-size: 10pt;">Horizontal Position: 233,2</span><br>\
    <span style="color: #FFF; font-size: 10pt;">Vertical Position: 233,2</span><br>\
    <span style="color: #FFF; font-size: 10pt;">Horizontal Waist: 233,2</span><br>\
    <span style="color: #FFF; font-size: 10pt;">Vertical Waist: 233,2</span></div>'

    text = pg.TextItem(html=texthtml, anchor=(0.,0.), border='w', fill=(0, 0, 255, 100))
    textbox = imagewidget.addPlot()
    textbox.addItem(text)
    textbox.setMaximumWidth(200)
    textbox.setMaximumHeight(200)
    textbox.setMinimumWidth(200)
    textbox.setMinimumHeight(200)
    textbox.hideAxis('left')
    textbox.hideAxis('bottom')
    text.setTextWidth(190)
    text.setPos(0.02,0.75)
    # textbox.setAspectLocked(True)
    # textbox.setRange(xRange=(0,200))
    # textbox.setLimits(xMin=0,xMax=200)




    #cross hair
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    view.addItem(vLine, ignoreBounds=True)
    view.addItem(hLine, ignoreBounds=True)


    databuffer = np.zeros([7,100])
    bufferrange = np.arange(100)
    databuffer[0,:] = bufferrange
    starttime = time.time()




    '''Errorhandling not implemented properly!!'''

    if RealData:

        camera.GetDeviceKeyList()
        NumberCams = camera.GetDeviceKeyListSize()
        if NumberCams != 0:
            for i in range(NumberCams):
                camera.GetDeviceKeyListEntry(camindex=i)
                serial = camera.GetDeviceInformation()
                ui.choosecam.addItem(serial)
                i += 1
            ui.choosecam.addItem('Test') #only for testing!!



        else:
            print 'ERROR -- No cameras found!!'

        CamIndex = ui.choosecam.currentIndex()
        camera.GetDeviceKeyListEntry(camindex=CamIndex)
        print camera.CamIndex.value, 'Camera Index'
        camera.StartCam()
        InitializeCam(camera,ui)







    win.show()


                
    def updateview():

        global ImageArray, img

        # simulation.NewImage()
        # simulation.AddWhiteNoise()
        # simulation.AddRandomGauss()
        # simulation.SimulateTotalImage()
        hold = False
        hold = ui.hold.isChecked()

        if hold==False:
            
            if ui.horRadio.isChecked():
                # view.setRange(QtCore.QRectF(0, 0, 754, 480))
                ui.x0Spin.setRange(0.,754.)
                ui.y0Spin.setRange(0.,480.)
                bounds = QtCore.QRectF(0,0,753,479)
                roi.maxBounds = bounds
                roisize = roi.size()
                roipos = roi.pos()
                if roisize[1] >= 480:
                    print roisize, roipos, 'ROI'
                    roi.setSize([200,200],finish=False)
                if roipos[1] >= (480-roisize[1]):
                    print roisize, roipos, 'ROI'
                    roi.setPos([200,200],finish=False)
                    roi.setSize([200,200],finish=False)
                    

                if RealData==False:
                    simulation.ChooseImage()
                    ImageArray = simulation.image
                else:
                    camera.GrabNextImage()
                    ImageArray = camera.ImageArray
            elif ui.vertRadio.isChecked():
                # view.setRange(QtCore.QRectF(0, 0, 480, 754))
                ui.x0Spin.setRange(0.,480.)
                ui.y0Spin.setRange(0.,754.)
                bounds = QtCore.QRectF(0,0,479,753)
                roi.maxBounds = bounds
                roisize = roi.size()
                roipos = roi.pos()
                if roisize[0] >= 480:
                    roi.setSize([200,200],finish=False)
                if roipos[0] >= (480-roisize[0]):
                    roi.setPos([200,200],finish=False)
                    roi.setSize([200,200],finish=False)


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

            if ui.connect.isChecked():
                upddateroipos(databuffer[3,-1],databuffer[4,-1])
            
            updateRoi()

        else:
            if RealData:
                camera.GrabNextImage()





            
            
      

    def updateRoi():

        

        global ImageArray, img, databuffer

        selected = roi.getArrayRegion(ImageArray.T, img)
        amplitude = selected.sum()
        p2.plot(selected.sum(axis=1), clear=True)

        '''Shift buffer one step forward'''
        databuffer[1:,:-1] = databuffer[1:,1:]
        actualtime = time.time()
        databuffer[1,-1] = actualtime - starttime
        databuffer[2,-1] = amplitude



        datahor = selected.sum(axis=1)
        FittedParamsHor = MatTools.FitGaussian(datahor)[0]
        xhor = np.arange(datahor.size)

        if ui.fitCheck.isChecked():
            p2.plot(MatTools.gaussian(xhor,*FittedParamsHor), pen=(0,255,0))


        p3.plot(selected.sum(axis=0), clear=True).rotate(90)

        # yamp,xamp = np.histogram(amplitude, bins=np.array(1))
        # print yamp,xamp,'Hist'
        xamp = np.array([1.,2.])
        yamp = np.array([amplitude])
        amphist.plot(xamp, yamp, stepMode=True, clear=True, fillLevel=0, brush=(0,0,255,150))

        datavert = selected.sum(axis=0)
        FittedParamsVert = MatTools.FitGaussian(datavert)[0]
        xvert = np.arange(datavert.size)

        if ui.fitCheck.isChecked():
            p3.plot(MatTools.gaussian(xvert,*FittedParamsVert), pen=(0,255,0)).rotate(90)
            poshor = FittedParamsHor[2]+roi.pos()[0]
            posvert = FittedParamsVert[2]+roi.pos()[1]
            waistx = FittedParamsHor[1]
            waisty = FittedParamsVert[1]

            databuffer[3,-1] = poshor
            databuffer[4,-1] = posvert
            databuffer[5,-1] = waistx
            databuffer[6,-1] = waisty

            updatetext(amplitude,poshor,posvert,waistx,waisty)

            

            


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



        updatetimescrolling()



    def updatetext(amplitude,x,y,waistx,waisty):

        text.setHtml('<div style="text-align: center"><span style="color: #FFF; font-size: 16pt;">Beam Properties</span><br>\
            <span style="color: #FFF; font-size: 10pt;">Amplitude: %0.2f</span><br>\
            <span style="color: #FFF; font-size: 10pt;">Horizontal Position: %0.2f</span><br>\
            <span style="color: #FFF; font-size: 10pt;">Vertical Position: %0.2f</span><br>\
            <span style="color: #FFF; font-size: 10pt;">Horizontal Waist: %0.2f</span><br>\
            <span style="color: #FFF; font-size: 10pt;">Vertical Waist: %0.2f</span></div>' %(amplitude,x,y,waistx,waisty))

    def updatehold():
        global hold
        hold = True
        print hold, 'Hold'


    def updatecam():
        camera.StopCam()
        CamIndex = ui.choosecam.currentIndex()
        print ui.choosecam.currentIndex(), 'Current Index'
        camera.GetDeviceKeyListEntry(camindex=CamIndex)
        camera.StartCam()
        InitializeCam(camera,ui)
        # print 'Camera changed!', camera.CamIndex.value


    def updatetimescrolling():


        if ui.fitCheck.isChecked():
            ui.poshorRadio.setEnabled(True)
            ui.posvertRadio.setEnabled(True)
            ui.waisthorRadio.setEnabled(True)
            ui.waistvertRadio.setEnabled(True)
            ui.distRadio.setEnabled(True)
            if ui.ampRadio.isChecked():
                timeplot.plot(databuffer[0,:],databuffer[2,:],clear=True)

            if ui.poshorRadio.isChecked():
                timeplot.plot(databuffer[0,:],databuffer[3,:],clear=True)

            if ui.posvertRadio.isChecked():
                timeplot.plot(databuffer[0,:],databuffer[4,:],clear=True)

            if ui.waisthorRadio.isChecked():
                timeplot.plot(databuffer[0,:],databuffer[5,:],clear=True)

            if ui.waistvertRadio.isChecked():
                timeplot.plot(databuffer[0,:],databuffer[6,:],clear=True)

            if ui.distRadio.isChecked():
                distance = np.sqrt((databuffer[3,:]-ui.x0Spin.value())**2+\
                    (databuffer[4,:]-ui.y0Spin.value())**2)
                timeplot.plot(databuffer[0,:],distance,clear=True)

        else:
            ui.ampRadio.setChecked(True)
            timeplot.plot(databuffer[0,:],databuffer[2,:],clear=True)
            ui.poshorRadio.setEnabled(False)
            ui.posvertRadio.setEnabled(False)
            ui.waisthorRadio.setEnabled(False)
            ui.waistvertRadio.setEnabled(False)
            ui.distRadio.setEnabled(False)

    def saveroisize():
        global origroisize
        origroisize = roi.size()


    def upddateroipos(x,y):
        
        imagesize = ImageArray.shape
        xpos = x-int(origroisize[0]/2.)
        xsize = origroisize[0]
        ysize = origroisize[1]
        if xpos < 0:
            xpos = 0
        ypos = y-int(origroisize[1]/2.)
        if ypos < 0:
            ypos = 0
        if xpos + origroisize[0] >= imagesize[1]:
            xsize = imagesize[1] - xpos - 1
        if ypos + origroisize[1] >= imagesize[0]:
            ysize = imagesize[0] - ypos - 1


        roi.setPos([xpos,ypos],finish=False)
        roi.setSize([xsize,ysize],finish=False)
        # roi.stateChanged()





    viewtimer = QtCore.QTimer()

    ui.choosecam.currentIndexChanged[int].connect(updatecam)

    ui.connect.toggled.connect(saveroisize)
    
    roi.sigRegionChangeFinished.connect(updateRoi)

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
    # camera.InitializeCam()
    # camera.StartCam()
    StartGUI(camera)
    camera.StopCam()




