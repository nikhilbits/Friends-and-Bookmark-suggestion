#never finishes
# brute force
# to be improved
import time

bookmarks = {}
result = {}
visited = {}

def intersect(a, b):
    #return the intersection of two lists
    return list(set(a) & set(b))

def union(a, b):
    #return the union of two lists
    return list(set(a) | set(b))

def read_bks():
    for line in open('dataset/bookmark_tags.dat'):
        fields = line.split('\t')
        bid = fields[0]
        tid = fields[1]
        if not bid in bookmarks:
            bookmarks[bid] = []
        bookmarks[bid].append(tid)

    for bid in bookmarks:
        for key in bookmarks:
            if key == bid or key in visited:
                continue
            list1 = intersect(bookmarks[bid] , bookmarks[key])
            list2 = union(bookmarks[bid] , bookmarks[key])
            sim = float(len(list1))/len(list2)
            if sim < 0.5:
                if not bid in result:
                    result[bid] = []
                result[bid].append(key)
                if not key in result:
                    result[key] = []
                result[key].append(bid)
        visited[bid] = True


start_time = time.time()
read_bks()
time_taken = time.time() - start_time
#write the result in a file so that we do not need to run this file again
for key in result:
    print(len(result[key]))
