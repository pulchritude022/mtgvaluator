import urllib
import os
from mvid import getMultiverseIds

def download(id):
	url = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%d&type=card" % id
	fn = "..\data\%d.png" % id
	urllib.urlretrieve(url, fn)
	
	
def main():
	for id in getMultiverseIds():
		fn = "..\data\%d.png" % id
		if os.path.isfile(fn):
			print fn + ' exists'
		else:
			print 'Downloading ' + str(id) + '.png ...'
			download(id)
	
if __name__ == "__main__":
	main()