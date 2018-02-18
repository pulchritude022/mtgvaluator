import numpy as np
import cv2
import os.path
import urllib
import requests
import json


class Card:
	def __init__(self, id):
		self.id = id
		
		self._downloadImage()
		self._getMetaData()
		self.siftDesc = self._calcSiftDescriptors()
		
	def getImage(self):
		return cv2.imread(self._getImgFilename(), cv2.IMREAD_COLOR)
		
	def compare(self, desc):
	
		MATCH_COUNT = 8
		try:
			bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
			matches = bf.match(self.siftDesc, desc)
			matches = sorted(matches, key = lambda x:x.distance)
			if len(matches) > MATCH_COUNT:
				sum = 0
				for m in matches[:MATCH_COUNT]:
					sum = sum + m.distance
				#print self.getName(), sum/MATCH_COUNT
				return sum/MATCH_COUNT
			else:
				return float('inf')
		except:
			return float('inf')
		
	def getName(self):
		try:
			return self.metaData['name']
		except:
			return '???'
	
	def getPriceUSD(self):
		try:
			return self.metaData['usd']
		except:
			return '0'
		
	def _getMetaData(self):
		uriString = 'https://api.scryfall.com/cards/multiverse/'+str(self.id)
		print 'Fetching :' + uriString
		r = requests.get(uriString, auth=('Bearer','x'))
		self.metaData = r.json()
	
	def _getImgFilename(self):
		return "..\data\%d.png" % self.id
		
	def _downloadImage(self):
		fn = self._getImgFilename()
		if not os.path.isfile(fn):
			print 'File "%s" not found. Loading from Gatherer...' % fn
			url = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%d&type=card" % self.id
			urllib.urlretrieve(url, fn)
	
	def _calcSiftDescriptors(self):
		sift = cv2.ORB.create(scaleFactor=1.05)
		# IMREAD_COLOR or IMREAD_GRAYSCALE
		tmp, des = sift.detectAndCompute(cv2.imread(self._getImgFilename(), cv2.IMREAD_GRAYSCALE), None)
		return des
	