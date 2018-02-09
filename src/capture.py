from SimpleCV import Camera
from SimpleCV import Image
from SimpleCV.Features import HueHistogramFeatureExtractor
from SimpleCV.Features import EdgeHistogramFeatureExtractor
import numpy as np
import cv2
from card import Card


swarmCard = Card(Image("swarm_intelligence.jpg"))
camelCard = Card(Image("wretched_camel.jpg"))
mummyCard = Card(Image("mummy_paramount.jpg"))

cards = [swarmCard, camelCard, mummyCard]

print swarmCard.getHistogram()
print camelCard.getHistogram()
print mummyCard.getHistogram()

# Initialize the camera
cam = Camera(prop_set={'height':223, 'width':311})
for i in range (200):
	# Get Image from camera
	img = cam.getImage()
	img = img.rotate90().flipHorizontal()
	print i
	img.show()
	

img.save("mummy_paramount_raw.png")