# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:18:13 2015

@author: Michael
"""

from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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

class ImageFormat(Structure):
	'''Struct that holds the image format'''

	_fields_ = [
	('m_width',c_uint),
	('m_height',c_uint),
	('m_color_format',c_int),
	('m_image_modifier',c_int)
	]

	def __init__(self):
		pass

class Image(Structure):
	'''Struct that holds the image'''

	_fields_ = [
	('m_image_format',ImageFormat),
	('mp_buffer',POINTER(c_char)),
	('m_pitch',c_uint),
	('m_time_stamp',c_double),
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

		self.CamIndex = 0
		self.CamIndex = c_uint(self.CamIndex)

		# Key_p = POINTER(CameraKey)
		self.dll.VRmUsbCamGetDeviceKeyListEntry.argtypes = [c_uint,POINTER(POINTER(CameraKey))]
		
		self.key = POINTER(CameraKey)()
		
		Key = self.dll.VRmUsbCamGetDeviceKeyListEntry(self.CamIndex,byref(self.key))

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

	def TakePicture(self,keytest=0):
		if keytest==0:
			print 'No valid key available!'
		elif self.key.contents.m_busy!=0:
			print 'Camera is busy!'
		else:
			Error = self.dll.VRmUsbCamOpenDevice(self.key,byref(self.CamIndex))
			if Error==0:
				self.ShowErrorInformation()
			else:
				print 'Device opend successfully'

				format = ImageFormat()
				format.m_width = 754
				format.m_height = 482
				format.m_color_format = 4
				format.m_image_modifier = 0

				inf = POINTER(c_char)()

				Error = self.dll.VRmUsbCamGetStringFromColorFormat(format.m_color_format,byref(inf))

				color = []
				i = 0
				
				while inf[i] != '\0':
					color.append(inf[i])
					i += 1
				color = ''.join(color)
				print 'Color format: ', color

				pixeldepth = c_uint(0)


				Error = self.dll.VRmUsbCamGetPixelDepthFromColorFormat(format.m_color_format,byref(pixeldepth))

				print 'Pixel Depth: ', pixeldepth.value

				self.dll.VRmUsbCamNewImage.argtypes = [POINTER(POINTER(Image)),ImageFormat]
		
				self.image_p = POINTER(Image)()

				Error = self.dll.VRmUsbCamNewImage(byref(self.image_p),format)


				print 'Pitch: ', self.image_p.contents.m_pitch

				if Error==0:
					self.ShowErrorInformation()

				


				if Error==1:
					print'Image taken!'

					ImageList = list(self.image_p.contents.mp_buffer[0:(format.m_height)*int(self.image_p.contents.m_pitch)])
					# print ImageList[0:10]
					# print len(ImageList)
					ImageList = [ord(i) for i in ImageList]
					print len(ImageList)

					self.ImageArray = np.array(ImageList)
					self.ImageArray = np.reshape(self.ImageArray,(format.m_height,int(self.image_p.contents.m_pitch)))
					self.ImageArray = self.ImageArray[:,:format.m_width]


					# for j in range(format.m_height):
					# 	for i in range(format.m_width):
					# 		self.ImageArray[j,i] = ord(self.image_p.contents.mp_buffer[j*int(pixeldepth.value)+i*int(self.image_p.contents.m_pitch)])

							# print ord(ImageList[i*int(pixeldepth.value)+j*int(self.image_p.contents.m_pitch)])

					plt.figure()
					plt.imshow(self.ImageArray, cmap = cm.Greys_r)




					name_p = c_char_p('Test.png')
					Error = self.dll.VRmUsbCamSavePNG(name_p,self.image_p,c_int(0))
					if Error==0:
						self.ShowErrorInformation()
					if Error==1:
						print'Image saved!'

				Error = self.dll.VRmUsbCamFreeImage(byref(self.image_p))

				if Error==0:
					self.ShowErrorInformation()



				




		Error = self.dll.VRmUsbCamFreeDeviceKey(byref(self.key))
		if Error==0:
			self.ShowErrorInformation()

		Error = self.dll.VRmUsbCamCloseDevice(self.CamIndex)
		if Error==0:
			self.ShowErrorInformation()


	def TakePictureGrabbing(self,keytest=0):
		if keytest==0:
			print 'No valid key available!'
		elif self.key.contents.m_busy!=0:
			print 'Camera is busy!'
		else:
			Error = self.dll.VRmUsbCamOpenDevice(self.key,byref(self.CamIndex))
			if Error==0:
				self.ShowErrorInformation()
			else:
				print 'Device opend successfully'

				format = ImageFormat()
				format.m_width = 754
				format.m_height = 482
				format.m_color_format = 4
				format.m_image_modifier = 0

				inf = POINTER(c_char)()

				Error = self.dll.VRmUsbCamGetStringFromColorFormat(format.m_color_format,byref(inf))

				color = []
				i = 0
				
				while inf[i] != '\0':
					color.append(inf[i])
					i += 1
				color = ''.join(color)
				print 'Color format: ', color

				pixeldepth = c_uint(0)


				Error = self.dll.VRmUsbCamGetPixelDepthFromColorFormat(format.m_color_format,byref(pixeldepth))

				print 'Pixel Depth: ', pixeldepth.value

				self.dll.VRmUsbCamLockNextImageEx.argtypes = [c_uint,c_uint,POINTER(POINTER(Image)),POINTER(c_uint)]
		
				source_image_p = POINTER(Image)()

				framesdropped = c_uint(0)

				Error = self.dll.VRmUsbCamStart(c_uint(1))

				Error = self.dll.VRmUsbCamLockNextImageEx2(c_uint(1),c_uint(0),byref(source_image_p),byref(framesdropped))
				if Error==0:
					self.ShowErrorInformation()

				self.image_p = POINTER(Image)()
				buffer_ini = POINTER(c_ubyte)(c_ubyte(0))
				buffer_ini_pitch = c_uint(format.m_width+2)

				Error = self.dll.VRmUsbCamSetImage(byref(self.image_p),format,buffer_ini,buffer_ini_pitch)
				if Error==0:
					self.ShowErrorInformation()

				Error = self.dll.VRmUsbCamConvertImage(source_image_p,self.image_p)
				if Error==0:
					self.ShowErrorInformation()

				Error = self.dll.VRmUsbCamUnlockNextImage(c_uint(1),byref(source_image_p))
				if Error==0:
					self.ShowErrorInformation()



				Error = self.dll.VRmUsbCamStop(c_uint(1))
				if Error==0:
					self.ShowErrorInformation()


				# print 'Pitch: ', self.image_p.contents.m_pitch

				if Error==0:
					self.ShowErrorInformation()

				# Error = 1


				if Error==1:
					print'Image taken!'

					ImageList = list(self.image_p.contents.mp_buffer[0:(format.m_height)*int(self.image_p.contents.m_pitch)])
					# print ImageList[0:10]
					# print len(ImageList)
					ImageList = [ord(i) for i in ImageList]
					print len(ImageList)

					self.ImageArray = np.array(ImageList)
					self.ImageArray = np.reshape(self.ImageArray,(format.m_height,int(self.image_p.contents.m_pitch)))
					self.ImageArray = self.ImageArray[:,:format.m_width]


					# for j in range(format.m_height):
					# 	for i in range(format.m_width):
					# 		self.ImageArray[j,i] = ord(self.image_p.contents.mp_buffer[j*int(pixeldepth.value)+i*int(self.image_p.contents.m_pitch)])

							# print ord(ImageList[i*int(pixeldepth.value)+j*int(self.image_p.contents.m_pitch)])

					plt.figure()
					plt.imshow(self.ImageArray, cmap = cm.Greys_r)






					name_p = c_char_p('Test.png')
					Error = self.dll.VRmUsbCamSavePNG(name_p,self.image_p,c_int(0))
					if Error==0:
						self.ShowErrorInformation()
					if Error==1:
						print'Image saved!'

				Error = self.dll.VRmUsbCamFreeImage(byref(self.image_p))

				if Error==0:
					self.ShowErrorInformation()



				




		Error = self.dll.VRmUsbCamFreeDeviceKey(byref(self.key))
		if Error==0:
			self.ShowErrorInformation()

		Error = self.dll.VRmUsbCamCloseDevice(self.CamIndex)
		if Error==0:
			self.ShowErrorInformation()


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
	check.TakePicture(keycheck)
	# check.TakePictureGrabbing(keycheck)
	plt.show()
