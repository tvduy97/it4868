# -*- coding: utf-8 -*-
import json
import snap
import ctypes
import operator

# read file
with open('result12.json', 'r') as myfile:
    data=myfile.read()

# parse file
objs = json.loads(data)

myList = {}
n=1
for obj in objs:
	temp = {
		"id": n,
		"link": list(),
	}
	myList[obj['title']] = temp
	n += 1
	for page in obj['links']:
		temp = {
			"id": n,
			"link": list(),
		}
		myList[page] = temp
		n += 1

for obj in objs:
	for page,times in obj['links'].items():
		for x in xrange(1,times):
			myList[obj['title']]['link'].append(myList[page]['id'])

# new graphs
G = snap.TNEANet.New()

n = 0
LIMIT = 64161

#Add node to graph
for node in myList.values():
	if n < LIMIT:
		try:
			G.AddNode(node['id'])
			n += 1
		except:
			pass
	else:
		break

#Add edge to graph
for node1 in myList.values():
	for node2 in node1['link']:
		try:
			G.AddEdge(node1['id'], node2)
		except:
			pass

myList2 = {}
for title,nodeInfor in myList.items():
	myList2[nodeInfor['id']] = title

print(len(myList2))

PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)

result = {}
for item in PRankH:
	result[item] = PRankH[item]

sorted_result = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
print(G.GetNodes())
print(G.GetEdges())
f = open('20182_IT4868_Assignment01_Group9_ranking.txt','w')
f.write('Kiến trúc Đà Lạt\t'+str(G.GetNodes())+'\n')
f.write('Pagerank\tTitle\n')
for item in sorted_result:
	rank = "%.4f"%item[1]
	try:
		title = myList2[item[0]].encode('utf-8')
	except:
		title = str(myList2[item[0]])
	f.write(rank)
	f.write('\t')
	f.write(title)
	f.write('\n')

f.close()
