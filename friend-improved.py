from __future__ import division
import numpy as np
from sklearn.cluster import KMeans

class User():
	id = 0
	bookmarks = {}
	tags = {}
	count = 0
	def __init__(self,id):
		self.id = id
		self.tags = {}
		self.bookmarks = {}
		self.count = 0

users = {}


def read_data():
	for line in open('dataset/user_taggedbookmarks.dat'):
		fields = line.split('\t')
		uid = fields[0]
		bid = fields[1]
		tid = fields[2]

		if not uid in users:
			users[uid] = User(uid)

		if not tid in users[uid].tags:
			users[uid].tags[tid] = 0
		users[uid].count += 1
		users[uid].tags[tid] += 1

		users[uid].bookmarks[bid] = 1


read_data()

S = []
n = 1867
total_tags = 53388

alpha = 0.5
beta = 0.5

def ts(key1,key2):
	#calculate mean_vu and mean_vm
	vu_mean = vm_mean = 0
	for key in users[key1].tags:
		vu_mean += users[key1].tags[key]
	vu_mean = vu_mean/total_tags
	for key in users[key2].tags:
		vm_mean += users[key2].tags[key]
	vm_mean = vm_mean/total_tags

	#Pearsons formula to calulate similarity
	numerator = 0
	den1 = den2 = 0
	for key in users[key1].tags:
		if key in users[key2].tags:
			#vuj, vmj are tag based user profiles for the tag 'key'
			vuj = users[key1].tags[key]/users[key1].count
			vmj = users[key2].tags[key]/users[key2].count
			numerator += ( (vuj - vu_mean)*(vmj - vm_mean) )
			den1 += pow((vuj-vu_mean),2)
			den2 += pow((vmj-vm_mean),2)
	#print(key1,den1,den2)
	den1 = den1**(1.0/2)
	den2 = den2**(1.0/2)
	if(den1 != 0 and den2 != 0):
		ans = numerator/(den1*den2)
		return ans
	else:
		return 0

def ui(key1,key2):
	numerator = 0
	den = len(users[key1].bookmarks)
	for key in users[key1].bookmarks:
		if key in users[key2].bookmarks:
			numerator += 1

	ans = numerator/den
	return ans

matrix =[[0 for x in range(0,1868)] for x in range(0,1868)] 
import csv
mapping = {}
reader = csv.reader(open('mapping.csv', 'r'))
for row in reader:
	k, v = row
	if(k.isdigit() and v.isdigit()):
		mapping[int(k)] = int(v)


def frs():
	ct = 0
	ct2 = 0
	for key1 in users:
		u = users[key1]
		for key2 in users:
			if(key1 != key2):
				m = users[key2]
				sim = ts(key1,key2)
				sim = (sim+1)/2
				if(mapping[int(key1)] and mapping[int(key2)]):
					print(sim)
					matrix[mapping[int(key1)]][mapping[int(key2)]] = sim
					ct += 1
					if(ct == 200):
						ct2 = 1
						break
		if(ct2):
			break

frs()
k_means = KMeans()
k_means.fit(matrix)
print(k_means.labels_)

