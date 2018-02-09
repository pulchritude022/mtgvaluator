from SimpleCV import Camera
from SimpleCV import Image
from SimpleCV.Features import HueHistogramFeatureExtractor
from SimpleCV.Features import EdgeHistogramFeatureExtractor
import numpy as np
import cv2
from card import Card


def getFeatures (img):
	#fe = HueHistogramFeatureExtractor(64);
	#fe = EdgeHistogramFeatureExtractor(64);
	tmpImg = img.scale(223,310)
	#return fe.extract(tmpImg)
	return tmpImg.histogram(64)
	
#def gethist1 (img):
#	hist = cv2.calcHist([img], [0, 1, 2], mask=NULL, 16,
#				[0, 180, 0, 256, 0, 256])
#	hist = cv2.normalize(hist).flatten()
#	return hist
		
	
def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])

	# return the chi-squared distance
	return d
	
	
swarmRaw = Card(Image("swarm_intelligence_raw.png"))
camelRaw = Card(Image("wretched_camel_raw.png"))
mummyRaw = Card(Image("mummy_paramount_raw.png"))

swarmCard = Card(Image("swarm_intelligence.jpg"))
camelCard = Card(Image("wretched_camel.jpg"))
mummyCard = Card(Image("mummy_paramount.jpg"))

cards = [swarmCard, camelCard, mummyCard]
rawCards = [swarmRaw, camelRaw, mummyRaw]

print swarmRaw.dct_hash()
print camelRaw.dct_hash()
print mummyRaw.dct_hash()

print swarmCard.dct_hash()
print camelCard.dct_hash()
print mummyCard.dct_hash()

# Initialize the camera
cam = Camera(prop_set={'height':600, 'width':800})
cam.live()
for i in range (100):
	k = cv2.waitKey(1) & 0xFF
	# press 'q' to exit
	if k == ord('q'):
		break
	# Get Image from camera
	img = cam.getImage()
	img = img.rotate90().flipHorizontal()
	
	card = Card(img)
	max = 10000000
	index = -1
	for i, c in enumerate(cards):
		val = card.compare(c)
		if (val < max):
			max = val
			index = i
		
	print("{0:.2f} {1:.2f} {2:.2f}".format(card.compare(swarmCard), card.compare(camelCard), card.compare(mummyCard)))
	print index+1
	
	
	#print img.findBlobs()
	# Show the image
	img.show()
	

print swarmFeat