import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from card import Card
import pickle

def findAndDrawMatches(img1, img2):
	sift = cv2.xfeatures2d_SIFT.create()
	kp1, des1 = sift.detectAndCompute(img1, None)
	kp2, des2 = sift.detectAndCompute(img2, None)


	MIN_MATCH_COUNT = 10
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	# store all the good matches as per Lowe's ratio test.
	good = []
	for m,n in matches:
		if m.distance < 0.7*n.distance:
			good.append(m)

	src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
	dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

	M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
	matchesMask = mask.ravel().tolist()

	h,w,ch = img1.shape
	pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
	dst = cv2.perspectiveTransform(pts,M)

	img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
		
	draw_params = dict(matchColor = (0,255,0), # draw matches in green color
					   singlePointColor = None,
					   matchesMask = matchesMask, # draw only inliers
					   flags = 2)

	img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
	#plt.imshow(img3, 'gray'),plt.show()
	return img3

def concat_images(imga, imgb):
	"""
	Combines two color image ndarrays side-by-side.
	"""
	print imga.shape, imgb.shape
	ha,wa = imga.shape[:2]
	hb,wb = imgb.shape[:2]
	max_height = np.max([ha, hb])
	total_width = wa+wb
	new_img = np.zeros(shape=(max_height, total_width, 3))
	new_img[:ha,:wa]=imga
	new_img[:hb,wa:wa+wb]=imgb
	return new_img

def concat_images2(imga, imgb):
	"""
	Combines two color image ndarrays side-by-side.
	"""
	print imga.shape, imgb.shape
	ha,wa = imga.shape[:2]
	hb,wb = imgb.shape[:2]
	max_height = np.max([ha, hb])
	total_width = wa+wb
	new_img = np.zeros(shape=(ha-hb, wb, 3))
	new_img = np.concatenate((imgb, new_img), axis=0)
	new_img = np.concatenate((imga, new_img),axis=1)
	return new_img
	
	
def main2():
	dbIds = [
		270371,	# Ogre Jailbreaker
		425846,	# Rootborn Defenses
		270958,	# Isperia's Skywatch
		270370,	# Urban Burgeoning
		253549,	# Spawn of Rix Maadi
		401967,	# Nettle Drone
		401935,	# Kor Entanglers
		401859,	# Dominator Drone
		401942,	# Looming Spires
		407612,	# Boulder Salvo
		407524,	# Affa Protector
		407566,	# Grip of the Roil
		402012,	# Roil Spout
		401939,	# Lavastep Raider
		401812,	# Angelic Gift
		402026,	# Scythe Leopard
		407671,	# Bone Saw
		407633,	# Scion Summoner
		414460,	# Gnarlwood Dryad
		414393,	# Murder
	]
	
	SCORE_THRESH = 60
	CARD_DB_FILENAME = '..\data\carddb.pickle'
	showMatches = False
	
	# Load from serialized dict
	carddb = {}
	try:
		with open(CARD_DB_FILENAME, 'rb') as handle:
			carddb = pickle.load(handle)
	except:
		print "Pickle Database not found. Creating new..."
	
	for i in dbIds:
		if i not in carddb.keys():
			carddb[i] = Card(i)
	# Save new dict out
	with open(CARD_DB_FILENAME, 'wb') as handle:
		pickle.dump(carddb, handle, protocol=pickle.HIGHEST_PROTOCOL)
	
	
	cap = cv2.VideoCapture(0)

	prevcard = None
	total = 0.0	# USD Dollars
	count = 0
	while(True):
		# Check for 'q' key to break from loop
		# 'm' will start showing matches
		# 'n' will stop showing matches
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		if key == ord('m'):
			if not showMatches:
				print "Updating matches"
				showMatches = True
		if key == ord('n'):
			if showMatches:
				print "Stopped updating matches"
				cv2.destroyWindow('matches')
				showMatches = False
	
		start = time.time()
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv2.imshow('capture',frame)
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		sift = cv2.xfeatures2d_SIFT.create()
		tmp, des = sift.detectAndCompute(grayFrame, None)
		if des is None:
			continue
		
		# Find highest scoring card in the database
		card = None
		score = 0
		for id, c in carddb.iteritems():
			s = c.compare(des)
			if s > score:
				score = s
				card = c
		
		# Ensure it's a card we recognize
		if (score > SCORE_THRESH):
			cv2.imshow('card', card.getImage())
			if showMatches:
				cv2.imshow('matches', findAndDrawMatches(card.getImage(), frame))
			
			# NEW MATCH!!
			if prevcard == None or card.id != prevcard.id:
				prevcard = card
				count = count + 1
				total = total + float(card.getPriceUSD())
				print 'Total: $%.02f (%d cards) %s @ $%s' % (total, count, card.getName(), card.getPriceUSD())
		
		
		#print time.time()-start

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	main2()