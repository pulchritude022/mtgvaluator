import requests
import json
import os.path

#add tha card to the dictionary, will save to a text file for now
cardName = input("Card Name : ")
setName = input("Set Name : ")
uriString = 'https://api.scryfall.com/cards/named?exact='+cardName+'&set='+setName
print (uriString)
r = requests.get(uriString, auth=('Bearer','x'))
jsonData = r.json()
for id in jsonData['multiverse_ids']:
	multi_id = id;

#how to store images?
png_uri = jsonData['image_uris']['png']

data = {}
data['cards'] = []

if not os.path.isfile('data.txt'):
		data['cards'].append({
		'name': jsonData['name'],
		'multiverse_id': multi_id,
		'image': png_uri,
		'set_name': jsonData['set_name'],
		'price_usd': jsonData['usd']
		})
else:
	with open('data.txt') as json_file:
		data = json.load(json_file)

		data['cards'].append({
			'name': jsonData['name'],
			'multiverse_id': multi_id,
			'image': png_uri,
			'set_name': jsonData['set_name'],
			'price_usd': jsonData['usd']
			})

with open('data.txt', 'w') as outfile:
	json.dump(data, outfile)