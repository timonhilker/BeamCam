# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 12:41:23 2015

@author: Michael
"""

import numpy as np
import random
from matplotlib import pylab as plt
import scipy as sp
from scipy.optimize import leastsq

def gaussian(x, *p):
    '''returns gaussfunction'''
    A,sigx,x0,off = p
    A = A*(sigx*np.sqrt(2*np.pi))
    g = (A/(sigx*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-x0)/sigx)**2)+off

    return g



def rotmatrix(alpha):
    return np.array([[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha),  np.cos(alpha)]])


def gaussian2(xy, *p):
    '''returns gaussfunction for arbitrarily positioned and rotated 2d gauss'''
    A, sx, x0, y0, sy,alpha,off = p
    # M = np.array([[Bx,Bxy],[Bxy,By]])
    R = rotmatrix(alpha)
    M = np.dot(R,np.dot(np.array([[1./sx**2,0],[0,1./sy**2]]),R.T))
    r = np.array([xy[:,0]-x0,xy[:,1]-y0])
    g = A*np.exp(-0.5*np.sum(np.dot(M,r)*r,axis=0)) + off
    # print g
    return g



def FitGaussian(data):

    def split(arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr   = arr[size:]
        arrs.append(arr)
        arrs = np.array(arrs)
        arrs = np.mean(arrs, axis=1)
        return arrs

    # x = np.arange(data.size)
    # data = split(data,10)

    # print data

    def errf(params):
        x = np.arange(data.size)
        return (data-gaussian(x,*params)) #take only every 10th value

    x0ini = np.argmax(data)
    Aini = data[x0ini]
    sigxini = 10.
    offini = 1000.

    p0 = [Aini,sigxini,x0ini,offini]
    # args = [A,sigx,x0,off]

    fitres = leastsq(errf,p0)

    # print fitres, 'FitRes'

    return fitres

    




