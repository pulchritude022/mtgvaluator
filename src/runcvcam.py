import numpy as np
import cv2
import requests
import json
import os.path
import base64
import sys
import time

def processImage():
	googleUrl = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDQIIuk-4ub77cNoscLwweQHyWcrwTZwe0"
	#requestBody = '{"requests":[{"image":{"source":{"imageUri":"http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=439355&type=card"}},"features":[{"type":"TEXT_DETECTION","maxResults":1}]}]}'

	with open("TMPIMG.png", "rb") as imageFile:
		strImage = base64.b64encode(imageFile.read())

	requestBody = '{"requests":[{"image":{"content":"'+strImage+'"},"features":[{"type":"TEXT_DETECTION","maxResults":1}]}]}'

	#headers = {'content-length': str(sys.getsizeof(requestBody))}

	r = requests.post (googleUrl, data=requestBody) #headers=headers)

	requestJson = json.loads(r.text)
	#print(requestJson)

	try:
		cardName = requestJson['responses'][0]['textAnnotations'][0]['description']
		#strip out spaces and add +
		allTheNames = cardName.split('\n')
		cardTitle = allTheNames[0]
		print(cardTitle)
		cardTitle.replace(" ", "+")

		uriString = 'https://api.scryfall.com/cards/named?exact='+cardTitle
		r = requests.get(uriString, auth=('Bearer','x'))
		jsonData = r.json()

		print ("price in USD: "+jsonData['usd'])
	except:
		print "No data found."

def main():
	cap = cv2.VideoCapture(0)

	for i in range(100):
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

			
	print "Ending focusing"
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		# Display the resulting frame
		cv2.imshow('frame',frame)
		cv2.imwrite('TMPIMG.png',frame)

		processImage()

		time.sleep(1)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()