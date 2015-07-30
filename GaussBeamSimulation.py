# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 15:57:43 2015

@author: Michael
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm



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


class GaussBeamSimulation:

	'''Class allows to simulate a gauss beam profile image captured by a camera'''

	def __init__(self):
		self.width = 754
		self.height = 480


	def NewImage(self):
		self.image = np.zeros((self.height,self.width))

	def AddWhiteNoise(self,expectation=50):
		noise =  np.random.poisson(expectation,self.image.shape).astype(int)
		self.image += noise

	def AddRandomGauss(self,meanamplitude=200,meansigmax=40,meansigmay=40,meanposition=[376,239]):
		amplitude = np.random.poisson(meanamplitude)
		sigmax = np.random.poisson(meansigmax)
		sigmay = np.random.poisson(meansigmay)
		position = [0,0]
		position[0] = np.random.poisson(meanposition[0])
		position[1] = np.random.poisson(meanposition[1])
		rotationangle = np.random.uniform(0,np.pi)
		offset = 0.

		ny,nx = self.image.shape

		x = np.arange(self.width)
		y = np.arange(self.height)

		XY = np.meshgrid(x,y)

		XYflat = np.array(XY).reshape(2,nx*ny).T



		params = [amplitude,sigmax,position[0],position[1],sigmay,rotationangle,offset]


		gaussflat = gaussian2(XYflat,*params)
		gauss = np.array(gaussflat).reshape(ny,nx)

		self.image +=gauss



	def ShowImage(self):
		plt.figure()
		plt.imshow(self.image, cmap = cm.Greys_r)
		plt.colorbar()
		plt.show()


if __name__=="__main__":
	test = GaussBeamSimulation()
	test.NewImage()
	test.AddWhiteNoise()
	test.AddRandomGauss()
	test.ShowImage()


