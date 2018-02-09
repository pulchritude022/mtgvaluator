from SimpleCV import Image
from SimpleCV.Features import HueHistogramFeatureExtractor
from SimpleCV.Features import EdgeHistogramFeatureExtractor
import numpy as np
import cv2


class Card:
	def __init__(self, img, histSize = 64):
		self.img = img
		self.histSize = histSize
		
	#def getcv2Histogram(self):
		#hist = cv2.calcHist([img], [0, 1, 2], mask=NULL, 16,
		#			[0, 180, 0, 256, 0, 256])
		#hist = cv2.normalize(hist).flatten()
		#return hist
	
	def getHistogram(self):
		return self.img.histogram(self.histSize)
		
	def dct_hash(self):
		img = self._float_version(self.img)
		small_img = cv2.CreateImage((32, 32), 32, 1)
		cv2.Resize(img[20:190, 20:205], small_img)

		dct = cv2.CreateMat(32, 32, cv2.CV_32FC1)
		cv2.DCT(small_img, dct, cv2.CV_DXT_FORWARD)
		dct = dct[1:9, 1:9]

		avg = cv2.Avg(dct)[0]
		dct_bit = cv2.CreateImage((8,8),8,1)
		cv2.CmpS(dct, avg, dct_bit, cv2.CV_CMP_GT)

		return [dct_bit[y, x]==255.0
				for y in xrange(8)
				for x in xrange(8)]


	def _float_version(self, img):
		tmp = cv2.CreateImage( cv2.GetSize(img), 32, 1)
		cv2.ConvertScale(img, tmp, 1/255.0)
		return tmp
	
	def compare(self, card):
		return self._chi2Distance(self.getHistogram(), card.getHistogram())
	
	def _chi2Distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])

		# return the chi-squared distance
		return d