from copy import deepcopy, copy
from itertools import combinations, product, permutations
from json import dump, dumps
import pprint 


NODES = ['0n', '1n', '2n', '3n', '4n', '0g', '1g', '2g', 'o']


def generate(nodes):
	structures = []
	structure = []
	structures = __generate(structures, structure, nodes, 'o')
	# structures = discard_violations(structures, [])

	structures = [item for item in structures if structures.count(item) == 1] 

	# for s in structures:
	# 	print s

	print 'cases', len(structures)

	return structures

def __generate(structures, structure, left, node):

	if filter(lambda a: a[-1] == 'n', left) == [] and connected(structure):
		if structure in structures: 
			return structures
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

# print connected([('n1', '2'), ('2', '3'), ('3', '4'), ('4', 'o')])
# print connected([('n4', 'o'), ('g1', 'o'), ('g0', 'g1'), ('n0', 'g0'), ('n1', 'g0'), ('n2', 'g0'), ('n3', 'g1')])



# generate(NODES)

def json(structures):

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

		d['experiments'][ID]['situation'] = []

		for j, perm in enumerate(product(*[(0, 1) for v in xrange(len(roots))])):
			case = j
			
			d['experiments'][ID]['situation'].append({'thresholds' : {}})


			for op in ['dis', 'con', 'maj']:
				d['experiments'][ID]['situation'][case]['thresholds'][op] = thresholds(structure, op)

			d['experiments'][ID]['situation'][case]['values'] = values(roots, perm)
		

	with open('data.json', 'w') as f:
		dump(d, f, sort_keys=True, indent=4, separators=(',   ', ': '))

	return 

def thresholds(structure, op):
	groups = []

	for x, y in structure:
		if x not in groups and x[-1] != 'n':
			groups.append(x)
		if y not in groups and y[-1] != 'n':
			groups.append(y)



	if op == 'dis':
		thresholds = [(group, 1) for group in groups]

	elif op == 'con':
		thresholds = []

		for group in groups:
			preds = 0
			for x, y in structure:
				if y == group:
					preds += 1
			thresholds.append((group, preds))

	elif op == 'maj':
		thresholds = []

		for group in groups:
			preds = 0
			for x, y in structure:
				if y == group:
					preds += 1
			thresholds.append((group, preds/2))

	return thresholds


def values(roots, values):

	res = []
	for node, value in enumerate(values):
		res.append((roots[node], value))
		
	return res

json(generate(NODES))
# generate(NODES)

		