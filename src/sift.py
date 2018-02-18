import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from card import Card
import pickle

def findAndDrawMatches(img1, img2):
	orb = cv2.ORB.create()
	kp1, des1 = orb.detectAndCompute(img1, None)
	kp2, des2 = orb.detectAndCompute(img2, None)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
	matches = bf.match(des1, des2)
	matches = sorted(matches, key = lambda x:x.distance)
	good = matches[:100]
	
	# Get bounding box
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
						matchesMask = matchesMask,
						flags = 2)
	img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None, **draw_params)
	#img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
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
		193531, # Survival Cache
		170991, # Kor Cartpgrapher
		259701, # Disentomb
		370724, # Sengir Vampire
		218077, # Thundering Tanadon
		233065, # Death-Hood Cobra
		423759, # Precise Strike
		423746, # Embraal Gear-Smasher
		423749, # Frontline Rebel
		423744, # Chandra's Revolution
		423745, # Destructive Tampering
		423723, # Defiant Salvager
		423721, # Cruel Finality
		423725, # Fen Hauler
		423737, # Resourceful Return
		423718, # Aether Poisoner
		423719, # Alley Strangler
		423740, # Vengeful Rebel
		423734, # Night Market Aeronaut
		423727, # Fourth Bridge Prowler
		423736, # Renegade's Gateway
		423723, # Defiant Salvager
		423697, # Bastion Inventer
		423699, # Dispersal Technician
		423701, # Hinterland Drake
		423707, # Negate
		423713, # Skyship Plunderer
		423693, # Aether Swooper
		423717, # Wind-Kin Raiders
		423714, # Take into Custody
		423711, # Shielded Aether Thief
		423706, # Metallic Rebuke
		423712, # Shipwreck Moray
		423675, # Bastion Enforcer
		423684, # Deft Dimissal
		423681, # Dawnfeather Eagle
		423677, # Caught in the Brights
		423683, # Decommission
		423687, # Ghirapur Osprey
		423670, # Aether Inspector
		423669, # Aeronaut Admiral
		423673, # Alley Evasion
		423674, # audacious Infiltrator 
		413368, # Marked by Honor
		383195, # Borderland Marauder
		383223, # Dauntless River Marshal
		383309, # Midnight Gaurd
		383357, # Ranger's Guile
		383438, # Will-Forged Golem
		383372, # Scrapyard Mongerl
		383374, # Selfless Cathar 
		383230, # Encrust 
		383259, # Goblin RoughRider
		383246, # Foundry Street Denizen
		383386, # Solemn Offering
		383183, # Amphin Pathmage
		383376, # Shadowcloak Vampire
		383271, # Hunter's Ambush
		3900, # Danan
	]
	
	SCORE_THRESH = 32
	CARD_DB_FILENAME = '..\data\carddb.pickle'
	showMatches = True
	
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
	
		# Capture frame-by-frame
		ret, frame = cap.read()
		
		cv2.imshow('capture',frame)
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayFrame = cv2.resize(grayFrame, (0,0), fx=0.6, fy=0.6)
		sift = cv2.ORB.create(scaleFactor=1.05)
		tmp, des = sift.detectAndCompute(grayFrame, None)
		if des is None:
			continue
		
		# Find highest scoring card in the database
		start = time.time()
		card = None
		score = float('inf')
		for id, c in carddb.iteritems():
			s = c.compare(des)
			if s < score:
				score = s
				card = c
		#print score
		# Ensure it's a card we recognize
		if (score < SCORE_THRESH):
			cv2.imshow('card', card.getImage())
			if showMatches:
				cv2.imshow('matches', findAndDrawMatches(card.getImage(), frame))
			
			# NEW MATCH!!
			if prevcard == None or card.id != prevcard.id:
				prevcard = card
				count = count + 1
				price = round(float(card.getPriceUSD())/5., 2)
				total = total + price
				print 'Total: $%.02f (%d cards) %s @ $%s [%.02f]' % (total, count, card.getName(), price, score)
		
		
		#print time.time()-start

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	main2()