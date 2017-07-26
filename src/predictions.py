from hierarchy import Hierarchy
from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from situation import Situation
from fractions import Fraction
from itertools import product
from simulate import simulate

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
import networkx as nx
import json


'''
open input file and save to a dict
'''
with open('data.json', 'r') as data:
	file = json.load(data)
data.close()

# list of cases to run
cases = len(file['experiments'])
graph = []
for case in xrange(0, 2):
	print 'case', case
	# simulate the case and return the hierarchy
	
	nodes = [str(u) for u,v in file['experiments'][case]['hierarchy']['structure']]
	roots = filter(lambda a: a[-1] == 'n', nodes)

	

	for situation in xrange(len(list(product(*[(0, 1) for v in xrange(len(roots))])))):
		for op in ['dis', 'con', 'maj']:
			print 'case:', case
			print 'situation:', situation
			print 'op', op
			hierarchy = simulate(file['experiments'][case], situation=situation, op=op, draw=True)

			hierarchy.evaluate('o')
			copy = hierarchy.copy()
			 
			for root in roots:
				piv = pivotality(copy, root, 'o')
				pivr = pivotality(copy, root, 'o', root=True)
				up = unpacked_pivotality(copy, root, 'o')

				graph.append((case, situation, op, root, up, float(pivr), float(piv)))
			print
			print
	graph.sort(key=lambda a: a[-1])


fig = plt.figure(figsize=(12, 12))
	
ax = plt.axes([0, 0, 1, 1])
fig.add_axes(ax)
ax.set_xticklabels(map(lambda g: 'case %d situation %d op %s cause %s' % (g[0], g[1], g[2], g[3]), graph), fontdict=None, minor=False, rotation='vertical')
ax.axis('on')
plt.grid(True)
plt.xlim(0, len(graph))

print
x = 0
for g in graph:
	ax.scatter(x, g[-1], c='k', zorder=2)
	ax.scatter(x, g[-2], c='b', zorder=1)
	if g[-2] == 0:
		print 'g', g
		print

	x+=1
fig.savefig('test.png')

plt.show()


y_pos = np.arange(len(graph))

piv = map(lambda a: a[-1], graph)
plt.bar(y_pos, piv, align='center', alpha=0.5, zorder=2)


pivr = map(lambda a: a[-2], graph)
plt.bar(y_pos, pivr, align='center', alpha=0.0, zorder=1)

cases = map(lambda g: 'case %d situation %d op %s cause %s' % (g[0], g[1], g[2], g[3]), graph)


plt.xticks(y_pos, cases, rotation='vertical')
plt.ylabel('pivotality')
 
plt.show()