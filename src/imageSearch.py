import requests
import json
import os.path
import base64
import sys

import time

start = time.time()


googleUrl = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDQIIuk-4ub77cNoscLwweQHyWcrwTZwe0"
#requestBody = '{"requests":[{"image":{"source":{"imageUri":"http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=439355&type=card"}},"features":[{"type":"TEXT_DETECTION","maxResults":1}]}]}'

with open("wretched_camel_raw.png", "rb") as imageFile:
    strImage = base64.b64encode(imageFile.read())

requestBody = '{"requests":[{"image":{"content":"'+strImage+'"},"features":[{"type":"TEXT_DETECTION","maxResults":1}]}]}'

#headers = {'content-length': str(sys.getsizeof(requestBody))}

r = requests.post (googleUrl, data=requestBody) #headers=headers)

requestJson = json.loads(r.text)
#print(requestJson)

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

end = time.time()
print ("time elapsed: " + str(end - start))