from __future__ import division
import csv
"""
dictionary = {}
prev = -1
def read():
	ctr = 0
	for line in open('/home/anmol/Documents/gitcode/winter_project/dataset/user_taggedbookmarks.dat'):
		fields = line.split('\t')
		if(not fields[0] in dictionary):
			dictionary[fields[0]] = ctr

			ctr += 1


booktag = {}
def bookt():
  for line in open('/home/anmol/Documents/gitcode/winter_project//dataset/bookmark_tags.dat'):
    fields = line.split('\t')
    booktag[(fields[0],fields[1])] = fields[1]





read()
w = csv.writer(open("mapping.csv", "w"))
for key, val in dictionary.items():
	w.writerow([key, val])

bookt()
w = csv.writer(open("booktags.csv", "w"))
for key, val in booktag.items():
	w.writerow([key, val])


"""

#new code:
class Bookmark():
	id = 0
	tags = {}
	def __init__(self,id):
		self.id = id
		self.tags = {}

bookmarks = {}
def read_bookmarks():
	for line in open('dataset/bookmark_tags.dat'):
		fields = line.split('\t')
		bid = fields[0]
		tid = fields[1]
		if(not bid in bookmarks):
			bookmarks[bid] = Bookmark(bid)
		bookmarks[bid].tags[tid] = 1

read_bookmarks()
print('Bookmarks Read')
book_sim = {}
total = len(bookmarks)
index = 0
for i in bookmarks:
	index += 1
	print(''+str(index)+'/'+str(total))
	for j in bookmarks:
		if(i != j):
			intersection = len(list( (set(bookmarks[i].tags.keys()) & set(bookmarks[j].tags.keys())) ))
			union = len(list( (set(bookmarks[i].tags.keys()) | set(bookmarks[j].tags.keys())) ))
			book_sim[(i,j)] = intersection/union



w = csv.writer(open("book_sim.csv", "w"))
for key, val in book_sim.items():
	w.writerow([key, val])
