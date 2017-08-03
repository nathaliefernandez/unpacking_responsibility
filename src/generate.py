from copy import deepcopy, copy
from itertools import combinations, product, permutations
from json import dump, dumps
import pprint
import numpy as np
from situation import Situation
from evaluate import pivotality


NODES = ['0n', '1n', '2n', '3n', '4n', '0g', '1g', '2g', 'o']



def json(d):
	with open('data.json', 'w') as f:
		dump(d, f, sort_keys=True, indent=4, separators=(',   ', ': '))
	return None

'''
calss recursive function to generate all possible structures
parameters:
	nodes 	list
return:
	strctures 	list
'''
def generate(nodes):
	structures = []
	structure = []
	structures = __generate(structures, structure, nodes, 'o')
	# structures = discard_violations(structures, [])

	structures = [item for item in structures if structures.count(item) == 1] 

	# for s in structures:
	# 	print s

	return structures

'''
recursively generates structures
parameters:
	structures 		list 		list of structures so far
	structure 		list 		structure being created
	left 			list 		nodes left to be used
	node 			str 		node we are using
return:
	structures 		list

'''
def __generate(structures, structure, left, node):

	if filter(lambda a: a[-1] == 'n', left) == [] and connected(structure):

		# if structure already in structures, return
		if structure in structures: 
			return structures
		# if no nodes left to add and is connected, add structure and return
		elif left == [] and connected(structure):
			return structures.append(structure)

	left = deepcopy(left)
	left.remove(node)
	structure = deepcopy(structure)

	for i in reversed(range(len(filter(lambda a: a[-1] == 'n', left))+1)):
		if node == 'o' and i <= 1:
			break
		nodes = deepcopy(left)

		for combo in combinations(nodes[:], i):


			temp_nodes = deepcopy(nodes)
			temp_structure = deepcopy(structure)
			

			for c in combo:

				edge = (c, node)


				temp_structure.append(edge)

				if c[-1] != 'n':
					structures = __generate(structures, temp_structure, temp_nodes, c)
				temp_nodes.remove(c)


				if filter(lambda a: a[-1] == 'n', temp_nodes) == [] and connected(temp_structure):
					if structure not in structures:
						structures.append(temp_structure)
					break

	
	return structures
						
def connected(structure):

	mlist = []
	nlist = []

	for m, n in structure:
		mlist.append(m)
		nlist.append(n)
	
	concat =  mlist + nlist

	invalid = filter(lambda a: concat.count(a) < 3 or a == 'o', concat) 
	invalid =filter(lambda a: a[-1] != 'n', invalid)


	if filter(lambda a: a != invalid[0], invalid) == []:
		if len(invalid) < 2:
			return False
		return True
	return False

def experiments(structures):

	d = {'experiments' : []}


	# ****get all permutations of possible values*****
	roots = filter(lambda a: a[-1] == 'n', NODES)

	length = len(list(product(*[(0, 1) for v in xrange(len(roots))])))
	for i, structure in enumerate(structures):
		ID = i

		# define ID number
		d['experiments'].append({'ID': ID})

		d['experiments'][ID]['hierarchy'] = {}
		d['experiments'][ID]['hierarchy']['structure'] = structure

		d['experiments'][ID]['situation'] = {}


		d['experiments'][ID]['situation']['thresholds'] = thresholds(structure)

		d['experiments'][ID]['situation']['values'] = []
		for case, perm in enumerate(product(*[(0, 1) for v in xrange(len(roots))])):
			d['experiments'][ID]['situation']['values'].append(values(roots, perm))



	return d	

def thresholds(structure):
	groups = []
	for x, y in structure:
		if x not in groups and x[-1] != 'n':
			groups.append(x)
		if y not in groups and y[-1] != 'n':
			groups.append(y)

	pnodes = {}
	maxp = 0
	for group in groups:
		preds = 0
		for x, y in structure:
			if y == group:
				preds += 1
			pnodes[group] = preds
			if maxp < preds:
				maxp = preds


	thresholds = []
	for perm in product(range(1, maxp+1), repeat=len(groups)):

		threshold = []
		for i, group in enumerate(groups):

			if perm[i] > pnodes[group]:
				break

			threshold.append((group, perm[i]))

		if len(threshold) == len(groups) and threshold not in thresholds:
			thresholds.append(threshold)

	return thresholds


def values(roots, values):

	res = []
	for node, value in enumerate(values):
		res.append((roots[node], value))
		
	return res

def sample(d, n):

	leaves = filter(lambda a: a[-1] == 'n', NODES)

	length = len(list(product(*[(0, 1) for v in xrange(len(leaves))])))

	used = []
	extreme = []
	slight = []
	none = []
	samples = {'experiments' : []}
	for i in xrange(n):
		
		while len(used) == i:
			experiment = np.random.choice(len(d['experiments']))
			values = np.random.choice(length)
			thresholds = np.random.choice(len(d['experiments'][experiment]['situation']['thresholds']))


			if (experiment, values, thresholds) not in used and len(d['experiments'][experiment]['situation']['thresholds'][thresholds]) < 4:

				hierarchy = d['experiments'][experiment]['hierarchy']
				situation = {}
				situation['thresholds'] = d['experiments'][experiment]['situation']['thresholds'][thresholds]
				situation['values'] = d['experiments'][experiment]['situation']['values'][values]

				s = Situation(hierarchy=hierarchy, situation=situation) 

				s.evaluate(s.outcome())
				cause = np.random.choice(leaves)

				j=0
				while pivotality(s, cause, s.outcome()) == 0:
					cause = np.random.choice(leaves)
					j+=1
					if j > len(leaves):
						break

				if (pivotality(s, cause, s.outcome()) - pivotality(s, cause, s.outcome(), root=True)) == 0 and len(none) < 4:
					used.append((experiment, values, thresholds))
					none.append((experiment, values, thresholds))
				
				if (pivotality(s, cause, s.outcome()) - pivotality(s, cause, s.outcome(), root=True)) > 0:
					if (pivotality(s, cause, s.outcome()) - pivotality(s, cause, s.outcome(), root=True)) > .25 and len(extreme) < 4:
						used.append((experiment, values, thresholds))
						extreme.append((experiment, values, thresholds))
					elif len(slight) < 4:
						used.append((experiment, values, thresholds))
						slight.append((experiment, values, thresholds))


		situation['cause'] = cause

		sample = {'ID' : i+12}
		sample['hierarchy'] = hierarchy
		sample['situation'] = situation

		samples['experiments'].append(sample)

	for i in samples['experiments']:
		print i

		print ', '

	return 






sample(experiments(generate(NODES)), 12)