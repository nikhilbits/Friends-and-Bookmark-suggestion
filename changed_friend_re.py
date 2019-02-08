from __future__ import division
import math
import csv

class User:
	bookmarks = {}
	b_tags = {}
	u_t_vector = {}
	u_mean = 0
	id = 0
	u_friends = {}
	u_count = 0
	def __init__(self, id):
		self.id = id
		self.u_count = 0
		self.u_mean = 0
		self.bookmarks = {}
		self.u_t_vector = {}
		self.u_tags = {}
		self.u_friends = {}

class Bookmark:
	id = 0
	tags = {}
	def __init__(self, id):
		self.id = id
		self.tags = {}

users = {}
bookmarks = {}
S = []
alpha = 0.5
beta = 0.5
unique = {}

def read_data():
	for line in open('dataset/user_taggedbookmarks.dat'):
		fields = line.split('\t')
		uid = fields[0]
		bid = fields[1]
		tid = fields[2]
		
		if(not uid in users):
			users[uid] = User(uid)
		users[uid].u_count += 1
		users[uid].bookmarks[bid] = 1
		if(not tid in users[uid].u_tags):
			users[uid].u_tags[tid] = 0
		users[uid].u_tags[tid] += 1

		
	for line in open('dataset/user_contacts.dat'):
		fields = line.split('\t')
		uid = fields[0]
		cid = fields[1]  
		users[uid].u_friends[cid] = 1
		
	for line in open('dataset/bookmark_tags.dat'):
		fields = line.split('\t')
		bid = fields[0]
		tid = fields[1]
		
		if(not bid in bookmarks):
			bookmarks[bid] = Bookmark(bid)
			
		bookmarks[bid].tags[tid] = 1

def rem_cold_users():
	r = dict(users)
	for i in users:
		if ((r[i].u_count <= 5) or (len(r[i].bookmarks) <= 5)):
			del r[i]
			print("removed %s" %(i))
	return r

def vector():
	for u in users:
		s = 0
		for t in users[u].u_tags:
			users[u].u_t_vector[t] = users[u].u_tags[t]/users[u].u_count
			s += users[u].u_tags[t]
		#users[u].u_mean = s/len(users[u].u_tags)
		users[u].u_mean = s/53388

def tag_similarity(u1,u2):
	vu_mean = users[u1].u_mean
	vm_mean = users[u2].u_mean
	
	numerator = 0
	den1 = 0
	den2 = 0
	den = 0
	num = 0

	for t in users[u1].u_tags:
		if(t in users[u2].u_tags):
			numerator += ( (users[u1].u_t_vector[t] - vu_mean) * (users[u2].u_t_vector[t] - vm_mean) )
			den1 += (users[u1].u_t_vector[t] - vu_mean)*(users[u1].u_t_vector[t] - vu_mean)
			den2 += (users[u2].u_t_vector[t] - vm_mean)*(users[u2].u_t_vector[t] - vm_mean)
			num = (users[u1].u_t_vector[t] - users[u2].u_t_vector[t])*(users[u1].u_t_vector[t] - users[u2].u_t_vector[t])
			den +=1
	den1 = math.sqrt(den1)
	den2 = math.sqrt(den2)
	if(den1 == 0 or den2 ==0):
		if den == 0:
			return -1 , -1
		else:
			num = math.sqrt(num/den)
			return -1 , num
	else:
		if den == 0:
			res = numerator/(den1*den2)
			return res , -1
		else:
			res = numerator/(den1*den2)
			num = math.sqrt(num/den)
			return res , num
	''' if den ==0:
		return -1
	else:
		num = math.sqrt(num/den)
		return num '''
	

def user_interest(u1,u2):
	numerator = 0
	denominator = len(users[u1].bookmarks)
	for b in users[u1].bookmarks:
		if(b in users[u2].bookmarks):
			numerator += 1
	if(denominator != 0):
		res = numerator/denominator
	else:
		res = 0
	return res

def frs():
	counter = 1
	for u1 in users:
		print(" %s / 1867" %(counter))
		for u2 in users:
			if(u1 != u2):
				user1 = users[u1]
				user2 = users[u2]
				sim1 , sim2 = tag_similarity(u1,u2)
				user_interest1 = user_interest(u1,u2)
				user_interest2 = user_interest(u2,u1)
				if(sim1>alpha and sim2 >alpha and (user_interest1>beta or user_interest2>beta)):
					S.append((u1,u2))
					#print((u1,u2))
		counter += 1
					
def calc_precision():
	true_positive = 0
	for i in S:
		if(i[1] in users[i[0]].u_friends):
			true_positive += 1
	return true_positive/len(S)

def calc_satisfaction():
	for i in S:
		if(not i[0] in unique):
			unique[i[0]] = []
		unique[i[0]].append(i[1])

	satisfied = 0
	for u in unique:
		for j in unique[u]:
			if(j in users[u].u_friends):
				satisfied += 1
				break
	return satisfied/len(unique)

def b_sim(b1,b2):
	intersection = 0
	union = 0
	if((b1 in bookmarks) and (b2 in bookmarks)):
		intersection = len( list(set(bookmarks[b1].tags.keys()) & set(bookmarks[b2].tags.keys())) )
		union = len( list(set(bookmarks[b1].tags.keys()) | set(bookmarks[b2].tags.keys())) )
	sim_t = 0
	if(union != 0):
		sim_t = intersection/union
	return sim_t

def calc_nov_seren():
	novel = 0
	serendipitous = 0
	denom = 0
	for u in unique:
		for f in unique[u]:
			for b in users[f].bookmarks:
				if(not b in users[u].bookmarks):
					novel += 1
				flag = 1
				for resource in users[u].bookmarks:
					if(b_sim(resource,b) > 0.5):
						flag = 0
						break
				if(flag == 1):
					serendipitous += 1
					
			denom += len(users[f].bookmarks)
	if(denom != 0):
		res_novel = novel/denom
		res_seren = serendipitous/denom 
	else:
		res_novel = 0
		res_seren = 0
	return (res_novel,res_seren)



read_data()
#users = rem_cold_users()
vector()
frs()
precision = calc_precision()
satisfaction = calc_satisfaction()
#print(S)
print(precision)
print(satisfaction)
nov_seren = calc_nov_seren()
novelty = nov_seren[0]
serendipity = nov_seren[1]
print(novelty)
print(serendipity)
