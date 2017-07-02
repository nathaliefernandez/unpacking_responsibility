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
	node = '0_4'
	
	effect = hierarchy.nodes()[0]
	copy = hierarchy.copy()

	pivr = pivotality(copy, node, effect, root=True)
	piv = pivotality(copy, node, effect)
	print 'piv roots', pivr
	print 'piv', piv


