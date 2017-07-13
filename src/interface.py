from hierarchy import Hierarchy
from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from situation import Situation
from fractions import Fraction
from itertools import product
from simulate import simulate

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

for case in xrange(1, 2):
	print 'case', case
	# simulate the case and return the hierarchy
	
	nodes = [str(u) for u,v in file['experiments'][case]['hierarchy']['structure']]
	roots = filter(lambda a: a[-1] == 'n', nodes)

	# for situation in xrange(len(list(product(*[(0, 1) for v in xrange(len(roots))])))):
	# 	hierarchy = simulate(file['experiments'][case], situation=situation, draw=True)
	hierarchy = simulate(file['experiments'][case], situation=0, op='con', draw=True)

	node = '0n'
	effect = hierarchy.outcome()

	hierarchy.evaluate(effect)

	hierarchy.print_situation() 
	print
	print

	copy = hierarchy.copy()

	# pivr = pivotality(copy, node, effect, root=True)
	# print 'piv roots', pivr
	# print

	# piv = pivotality(copy, node, effect)


	# print 'piv', piv

	pivr = pivotality(copy, node, effect, root=True)
	print '__piv roots', pivr
	print

	piv = pivotality(copy, node, effect)


	print '__piv', piv

	# hierarchy = Hierarchy([["0_0", "1_0"], ["0_1", "1_0"], ["0_2", "1_0"], ["0_3", "1_1"], ["0_4", "1_1"], ["1_0", "2_0"], ["1_1", "2_0"]])

	# hierarchy.assign_values([["0_0", 0], ["0_1", 0], ["0_2", 0], ["0_3", 0], ["0_4", 0], ["1_0", 0], ["1_1", 0]])

	# hierarchy.assign_thresholds([["1_1", 1], ["1_0", 2], ["2_0", 2]])
	
	# hierarchy.evaluate('2_0')
	

	

	# up = unpacked_pivotality(hierarchy, '0_0', '2_0')
	# print up