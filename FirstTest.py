# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:18:13 2015

@author: Michael
"""

from ctypes import *
import numpy as np


class CameraKey(Structure):
	'''Struct that holds the key of a camera'''

	_fields_ = [
	("m_serial",c_uint),
	("mp_manufacturer_str",POINTER(c_char)),
	("mp_product_str",POINTER(c_char)),
	("m_busy",c_uint),
	("mp_private",c_void_p)
	]

	def __init__(self):
		pass

		

class VRmagicUSBCam_API:
	'''Functions for the VR Magic USB Camera.'''

	def __init__(self, dllPath='vrmusbcam2.dll'):
		self.dll = cdll.LoadLibrary(dllPath)


	def GetDeviceKeyList(self):

		KeyList = self.dll.VRmUsbCamUpdateDeviceKeyList()

		size=0
		size=c_uint(size)
		NumberCams = self.dll.VRmUsbCamGetDeviceKeyListSize(byref(size))
		No = size

		CamIndex = 0
		CamIndex = c_uint(CamIndex)

		s=CameraKey()

		Key = self.dll.VRmUsbCamGetDeviceKeyListEntry(CamIndex,byref(s))

		ID = c_uint(0)

		ErrID = self.dll.VRmUsbCamGetProductId(s,byref(ID))





		print KeyList, 'KeyList'
		print NumberCams, 'Number of cameras', No.value
		print Key, 'Key', s
		print ErrID, 'ID', ID

if __name__=="__main__":
	check = VRmagicUSBCam_API()
	check.GetDeviceKeyList()
