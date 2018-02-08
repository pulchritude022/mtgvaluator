import json

with open('data.txt') as json_file:
	data = json.load(json_file)
	for card in data['cards']:
		print (card['name'] + " " + card['set_name'])