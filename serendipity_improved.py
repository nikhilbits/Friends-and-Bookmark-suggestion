#somehow finishes
# still takes a lots of time around 10 mins
# to be improved
import time

bookmarks = {}
tags = {}
count = {}
ans = {}
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
            count[bid] = 0
        bookmarks[bid].append(tid)
        count[bid]+=1
        if tid not in tags:
            tags[tid] = []
        tags[tid].append(bid)

    print("reading done")

    try:
        for bid in bookmarks:
            temp = {}
            for tid in bookmarks[bid]:
                for key in tags[tid]:
                    if bid == key:
                        continue
                    if key in visited:
                        continue;
                    if key in temp:
                        temp[key]+=1
                    else:
                        temp[key] = 1
            visited[bid] = True
            for r_key in temp:
                union_count = count[bid] + count[r_key] - temp[r_key]
                if ((float(temp[r_key])/union_count) < 0.5):
                    if bid not in ans:
                        ans[bid] = []
                    ans[bid].append(r_key)
                    if r_key not in ans:
                        ans[r_key] = []
                    ans[r_key].append(bid)
    except Exception as err:
        print(err)

    print("calculating the result is done")


read_bks()
#write the result in a file so that we do not need to run this file again
for key in ans:
    print(len(ans[key]))
