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
		try:
			FLANN_INDEX_KDTREE = 0
			index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
			search_params = dict(checks = 50)
			flann = cv2.FlannBasedMatcher(index_params, search_params)
			
			# Find all descriptor matches
			matches = flann.knnMatch(self.siftDesc,desc,k=2)
			
			# Count up 'good' matches
			score = 0
			for m,n in matches:
				if m.distance < 0.7*n.distance:
					#score = score + (m.distance/n.distance)
					score = score + 1
			return score
		except:
			return 0
		
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
		sift = cv2.xfeatures2d_SIFT.create()
		# IMREAD_COLOR or IMREAD_GRAYSCALE
		tmp, des = sift.detectAndCompute(cv2.imread(self._getImgFilename(), cv2.IMREAD_GRAYSCALE), None)
		return des
	