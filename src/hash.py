#!/usr/bin/python
import os
import sys
import glob
import math
from PIL import Image
from 

EXTS = 'jpg', 'jpeg', 'gif', 'png'

def hamming(h1, h2):
	h, d = 0, h1 ^ h2
	while d:
		h += 1
		d &= d - 1
	return h


def phash(im):
	if not isinstance(im, Image.Image):
		im = Image.open(im)
	im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
	avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
	return reduce(lambda x, (y, z): x | (z << y),
				  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
				  0)

avg = lambda x: sum([i*c for i, c in enumerate(x)]) / (sum(x) + 0.1)
update = lambda oldi, oldv, newi, newv: (oldi, oldv) if oldv > newv else (newi, newv) 

def otsu_hash(im):
	if not isinstance(im, Image.Image):
		im = Image.open(im)
	im = im.convert('L')
	hist = im.histogram()
	tot_avg = avg(hist)
	max_i, max_score = 0, 0
	for i in range(len(hist)):
		num1, avg1 = sum(hist[:i]), avg(hist[:i])
		num2, avg2 = sum(hist[i:]), avg(hist[i:])
		score = num1 * (avg1 - tot_avg)**2 + num2 * (avg2 - tot_avg)**2
		max_i, max_score = update(max_i, max_score, i, score)
	im = im.resize((8, 8), Image.ANTIALIAS)
	return reduce(lambda x, (y, z): x | (z<<y), 
				  enumerate(map(lambda i: 0 if i < max_i else 1, im.getdata())),
				  0)

def otsu_hash2(im):
	if not isinstance(im, Image.Image):
		im = Image.open(im)
	im = im.convert('L')
	hist = im.histogram()
	tot_avg = avg(hist)
	max_i, max_score = 0, 0
	for i in range(len(hist)):
		num1, avg1 = sum(hist[:i]), avg(hist[:i])
		num2, avg2 = sum(hist[i:]), avg(hist[i:])
		score = num1 * (avg1 - tot_avg)**2 + num2 * (avg2 - tot_avg)**2
		max_i, max_score = update(max_i, max_score, i, score)
	im = im.resize((8, 8), Image.ANTIALIAS)
	x, y = 8, 8 
	up_score, down_score, n_up, n_down = 0, 0, 0, 0
	for i in range(x):
		for j in range(y):
			score = math.sqrt((i-x/2)**2 + (j-y/2)**2)
			if im.getpixel((i, j)) > max_i:
				up_score += score
				n_up += 1
			else:
				down_score += score
				n_down += 1
	if up_score/n_up <= down_score/n_down:
		return reduce(lambda x, (y, z): x | (z<<y), 
					  enumerate(map(lambda i: 0 if i < max_i else 1, im.getdata())), 0)
	else:
		return reduce(lambda x, (y, z): x | (z<<y), 
					  enumerate(map(lambda i: 0 if i >= max_i else 1, im.getdata())), 0)
					  
def createPhash():
	

def test():
	img1 = 'mummy_paramount_raw.png'
	img1p = phash(img1)
	img1o = otsu_hash(img1)
	img1o2 = otsu_hash2(img1)
	print '%X, %X, %X' % (img1p, img1o, img1o2)
	
	img2 = '../data/48194.png'
	img2p = phash(img2)
	img2o = otsu_hash(img2)
	img2o2 = otsu_hash2(img2)
	print '%X, %X, %X' % (img2p, img2o, img2o2)
	
	print hamming(img1p, img2p)
	print hamming(img1o, img2o)
	print hamming(img1o2, img2o2)
	
	
    
def demo(sys):
	if len(sys.argv) <= 1 or len(sys.argv) > 3:
		print "Usage: %s image.jpg [dir]" % sys.argv[0]
	else:
		im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
		h = otsu_hash2(im)
		print "hash: " + str(h)

		os.chdir(wd)
		images = []
		for ext in EXTS:
			images.extend(glob.glob('..\data\*.%s' % ext))

		seq = []
		errors = 0
		prog = int(len(images) > 50 and sys.stdout.isatty())
		for f in images:
			try:
				seq.append((f, hamming(otsu_hash2(f), h)))
				if prog:
					perc = 100. * prog / len(images)
					x = int(2 * perc / 5)
					print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
					print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
					sys.stdout.flush()
					prog += 1
			except:
				errors = errors + 1

		if prog: print
		for f, ham in sorted(seq, key=lambda i: i[1])[:50]:
			print "%d\t%s" % (ham, f)
		print "Errors: " + str(errors)

if __name__ == '__main__':
	test()
	demo(sys)