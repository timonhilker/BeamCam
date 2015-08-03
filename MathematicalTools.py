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

    




