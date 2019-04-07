# -*- coding: utf-8 -*-
import json
import snap
import ctypes
import operator

# read file
with open('result5.json', 'r') as myfile:
    data=myfile.read()

# parse file
objs = json.loads(data)

# new graphs
G = snap.TNEANet.New()

n = 0
LIMIT = 2000

for obj in objs:
	if n < LIMIT:
		G.AddNode(id(obj['title']))
		n += 1
	else:
		break

for obj in objs:
	for _id in obj['links']:
		if n < LIMIT:
			G.AddNode(id(_id))
			n += 1
		else:
			break

for obj in objs:
	for _id, times in obj['links'].items():
		for x in xrange(1,times):
			try:
				G.AddEdge(id(obj['title']),id(_id))
			except:
				pass

PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)

result = {}
for item in PRankH:
	result[item] = PRankH[item]

sorted_result = sorted(result.items(), key=operator.itemgetter(1),reverse=True)

f = open('20182_IT4868_Assignment01_Group9_ranking.txt','w')
f.write('Kiến_trúc_Đà_Lạt\t'+str(G.GetNodes())+'\n')
f.write('Pagerank\tTitle\n')
for item in sorted_result:
	rank = "%.4f"%item[1]
	title = ''.join(ctypes.cast(item[0], ctypes.py_object).value).encode('utf-8')
	f.write(rank)
	f.write('\t')
	f.write(title)
	f.write('\n')

f.close()
