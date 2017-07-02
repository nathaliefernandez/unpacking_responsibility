from hierarchy import Hierarchy
from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from fractions import Fraction
from itertools import product
from simulate import simulate

import networkx as nx
import json

'''
open input file and save to a dict
'''
with open('experiments.json', 'r') as data:
	file = json.load(data)
data.close()

# list of cases to run
cases = [28]




for case in cases:
	print 'case', case
	# simulate the case and return the hierarchy
	hierarchy = simulate(case, file, draw='graph%d.png' % case)
<<<<<<< HEAD
	node = '0_4'
	
	effect = hierarchy.nodes()[0]
	copy = hierarchy.copy()

	pivr = pivotality(copy, node, effect, root=True)
	piv = pivotality(copy, node, effect)
	print 'piv roots', pivr
	print 'piv', piv




=======

	effect = hierarchy.nodes()[0]
	# hierarchy.assign_values([('0_0', 0),('0_1', 0),('0_2', 0),('0_3', 0),('0_4', 0)])
	# hierarchy.evaluate(effect)


	# for each node find 
	# 		if pivotal or pivotality
	#		criticality
	#		probability of being pivotal
	#for node in :

	# piv = pivotality(hierarchy, node, effect)
	# piv2 = pivotality(hierarchy, node, effect, root=True)
	# crit = criticality(hierarchy, node, effect, e_value=1)
	# prob1 = prob_pivotal(hierarchy, node, effect, e_value=1)
	# prob = prob_pivotal(hierarchy, node, effect, 100)
	#print 'pivotality of %s:' % node, piv
	# print 'pivotality of %s with changes only in root nodes' % node, piv2
	# print 'criticality of %s:' % node, crit
	# print 'probability of %s being pivotal where effect is true:' % node, prob1
	# print 'probability of %s being pivotal:' % node, prob
		
	# if hierarchy.predecessors(node) == []:
	# 	up = unpacked_pivotality(hierarchy, node, effect, e_value=True)
	# 	print 'unpacked pivotality of %s:' % node, up
	# up = unpacked_pivotality(hierarchy, '0_2', '2_0', e_value=True)




	node = hierarchy.nodes()[3]		
	print 'node', node

	copy = hierarchy.copy()
	exogenous = filter(lambda a: nx.has_path(copy, a, effect), copy.nodes())
	exogenous.remove(effect)
	exogenous.remove(node)

	actual_values = [0, 0, 0, 0, 0, 0]
		

	def distance(values):
		distance = 0

		for a, b in zip(values, actual_values):
			if a != b:
				distance += 1
		return distance

	for n, value in zip(exogenous, actual_values):
		copy.node[n]['value'] = value

	pivr = pivotality(copy, node, effect, root=True)
	piv = pivotality(copy, node, effect)
	print 'piv roots', pivr
	print 'piv', piv
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6














