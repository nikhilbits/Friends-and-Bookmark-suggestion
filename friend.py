from __future__ import division
import csv


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

#Getting similarity between 2 bookmarks
def book_sim(i,j):
	if(i in bookmarks and j in bookmarks):
		intersection = len(list( (set(bookmarks[i].tags.keys()) & set(bookmarks[j].tags.keys())) ))
		union = len(list( (set(bookmarks[i].tags.keys()) | set(bookmarks[j].tags.keys())) ))
		sim = intersection/union
		return sim
	else:
		return -1



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



#Store contacts of users
contacts = {}
for line in open('dataset/user_contacts.dat'):
	fields = line.split('\t')
	if(not ( ((fields[0],fields[1]) in contacts) or ((fields[1],fields[0])in contacts) )):
			contacts[(fields[0],fields[1])] = 1



#resources = {}

"""
booktags = {}
reader = csv.reader(open('booktags.csv', 'r'))
for row in reader:
	k, v = row
	booktags[k] = v




tagsim = {}
def ressim():
	flag = 0
	for key1,value1 in booktags.items():
		fields1 = "a"
		fields2 = "b"
		union = 0
		intersection = 0
		for key2,valu1e2 in booktags.items():
			if(key1 != key2):
				fields1=key1.split("'")
				fields2=key2.split("'")
				union = union + 1
				if(booktags[key1] == booktags[key2]):
					intersection += 1
					flag = 1		#just to test for 1 pair

		tagsim[(fields1[1],fields2[1])] = intersection/union
		if(flag):
			break
"""

total_usrs = len(users)
true_positive = 0
true_recs = 0
g_novel = 0
g_satisfied = 0
g_serendipitous = 0
g_stf_denom = 0
g_seren_denom = 0
g_novel_denom = 0

def frs():
	counter = 0
	tr = 0
	tp = 0
	satisfied = 0
	satisfied_denom = 0
	novel = 0
	serendipitous = 0
	seren_denom = 0
	novel_denom = 0
	for key1 in users:
		counter += 1
		print(''+str(counter)+'/'+str(total_usrs))
		u = users[key1]
		flag = 0
		recom = 0
		for key2 in users:
			if(key1 != key2):
				m = users[key2]
				#sim = ts(key1,key2)
				user_interest1 = ui(key1,key2)
				user_interest2 = ui(key2,key1)
				#print(sim)
				if(user_interest1 > beta or user_interest2 > beta):
					#this friend is recommended to user (key1)
					S.append((key1,key2))

					tr += 1		#total recommendations
					recom = 1	#current friend is recommended
					#print("tr %s"%(tr))
					#To check if it is a positive contact 
					if( ( (key1,key2) in contacts ) or ( (key2,key1) in contacts)):
						tp += 1
						flag = 1

					#To check if recommended bookmarks are serendipitous 
					for i in users[key2].bookmarks:
						check = 1
						for j in users[key1].bookmarks:
							sim = book_sim(i,j)
							if(sim>0.5):
								check = 0
								break
						if(check==1):
							serendipitous += 1
						seren_denom += 1

					#To check if recommended bookmarks are novel
					for b in users[key2].bookmarks:
						if(not b in users[key1].bookmarks):
							novel += 1
						novel_denom += 1
		if(recom == 1):
			satisfied_denom += 1
		if(flag == 1 and recom == 1):
			satisfied += 1


	global g_stf_denom
	g_stf_denom = satisfied_denom
	global true_positive
	true_positive= tp
	global true_recs
	true_recs = tr
	global g_novel
	g_novel = novel
	global g_serendipitous
	g_serendipitous = serendipitous
	global g_satisfied
	g_satisfied = satisfied
	global g_seren_denom
	g_seren_denom = seren_denom
	global g_novel_denom
	g_novel_denom = novel_denom





frs()

precision = true_positive/true_recs
percentage_satisfied = g_satisfied/g_stf_denom
novelty = g_novel/g_novel_denom
serendipity = g_serendipitous/g_seren_denom

print("Satisfied Users: %s " %(percentage_satisfied))
print("Precision: %s " %(precision))
print("Novelty: %s " %(novelty))
print("Serendipity: %s" %(serendipity))

