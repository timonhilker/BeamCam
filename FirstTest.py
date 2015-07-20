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
	('m_serial',c_uint),
	('mp_manufacturer_str',POINTER(c_char)),
	('mp_product_str',POINTER(c_char)),
	('m_busy',c_uint),
	('mp_private',POINTER(c_void_p))
	]

	def __init__(self):
		pass

		

class VRmagicUSBCam_API:
	'''Functions for the VR Magic USB Camera.'''

	def __init__(self, dllPath='vrmusbcam2.dll'):
		self.dll = cdll.LoadLibrary(dllPath)


	def ShowErrorInformation(self):

		inf = POINTER(c_char)
		addr = self.dll.VRmUsbCamGetLastError()
		# addr = c_int(addr)

		message = cast(addr, inf)

		Message = []
		i = 0
		while message[i] != '\0':
			Message.append(message[i])
			i += 1
		Message = ''.join(Message)
		print '!ERROR!: ', Message


	def GetDeviceKeyList(self):

		Error = self.dll.VRmUsbCamUpdateDeviceKeyList()

		if Error==0:
			self.ShowErrorInformation()

		print 'KeyList'

	def GetDeviceKeyListSize(self):

		No=c_uint(0)
		Error = self.dll.VRmUsbCamGetDeviceKeyListSize(byref(No))

		print 'Number of cameras', No.value
		if Error==1:
			return No.value
		else:
			self.ShowErrorInformation()

		


	def GetDeviceKeyListEntry(self):

		CamIndex = 0
		CamIndex = c_uint(CamIndex)

		Key_p = POINTER(CameraKey)
		self.dll.VRmUsbCamGetDeviceKeyListEntry.argtypes = [c_uint,POINTER(POINTER(CameraKey))]
		
		self.key = POINTER(CameraKey)()
		
		Key = self.dll.VRmUsbCamGetDeviceKeyListEntry(CamIndex,byref(self.key))

		if Key==0:
			self.ShowErrorInformation()
			return 0
		else:
			return 1
		

	def GetDeviceInformation(self,keytest=0):

		if keytest==0:
			print 'No valid key available!'
		else:
			ID = c_uint(0)

			ErrID = self.dll.VRmUsbCamGetProductId(self.key,byref(ID))

			inf = POINTER(c_char)()

			Errinf = self.dll.VRmUsbCamGetSerialString(self.key,byref(inf))

			print 'Key', self.key
			print ErrID, 'ID', ID.value

			serial = []
			i = 0
				
			while inf[i] != '\0':
				serial.append(inf[i])
				i += 1
			serial = ''.join(serial)
			print 'Serial String: ', serial
			print 'Busy: ', self.key.contents.m_busy





		# print KeyList, 'KeyList'
		# print NumberCams, 'Number of cameras', No.value
		# print Key, 'Key', s
		# print ErrID, 'ID', ID.value
		# print inf[0:10], 'SerialString'
		

if __name__=="__main__":
	check = VRmagicUSBCam_API()
	check.GetDeviceKeyList()
	check.GetDeviceKeyListSize()
	keycheck = check.GetDeviceKeyListEntry()
	check.GetDeviceInformation(keycheck)
