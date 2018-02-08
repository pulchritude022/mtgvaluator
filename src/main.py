from SimpleCV import Camera
from SimpleCV import Image
from SimpleCV.Features import HueHistogramFeatureExtractor
from SimpleCV.Features import EdgeHistogramFeatureExtractor
import numpy as np
import cv2


def getFeatures (img):
	#fe = HueHistogramFeatureExtractor(64);
	#fe = EdgeHistogramFeatureExtractor(64);
	tmpImg = img.scale(223,310)
	#return fe.extract(tmpImg)
	return tmpImg.histogram(64)
	
def gethist1 (img):
	hist = cv2.calcHist([img], [0, 1, 2], mask=NULL, 16,
				[0, 180, 0, 256, 0, 256])
	hist = cv2.normalize(hist).flatten()
	return hist
		
	
def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])

	# return the chi-squared distance
	return d
	


swarmFeat = getFeatures(Image("swarm_intelligence.jpg"))

# Initialize the camera
cam = Camera(prop_set={'height':600, 'width':800})
#cam.live()
for i in range (500):
	# Get Image from camera
	img = cam.getImage()
	
	img = img.rotate90().flipHorizontal()
	print '{:2f}'.format(chi2_distance(swarmFeat, gethist1(img)))
	
	#print img.findBlobs()
	# Show the image
	img.show()
	

print swarmFeat