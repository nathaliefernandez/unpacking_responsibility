from copy import deepcopy, copy
from itertools import combinations, product

NODES = ['n0', 'n1', 'n2', 'n3', 'n4', 'g0', 'g1', 'g2', 'o']

def generate(nodes):
	structures = []
	structure = []
	structures = __generate(structures, structure, nodes, 'o')
	# structures = discard_violations(structures, [])

	print
	structures = [item for item in structures if structures.count(item) == 1] 
	print

	for s in structures:
		print s

	print 'cases', len(structures)

	return structures

def __generate(structures, structure, left, node):

	if filter(lambda a: a[0] == 'n', left) == [] and connected(structure):
		if structure in structures: 
			return structures
		elif left == [] and connected(structure):
			return structures.append(structure)

	left = deepcopy(left)
	left.remove(node)
	structure = deepcopy(structure)

	for i in reversed(range(len(filter(lambda a: a[0] == 'n', left))+1)):
		if node == 'o' and i <= 1:
			break
		nodes = deepcopy(left)


		for combo in combinations(nodes[:], i):


			temp_nodes = deepcopy(nodes)
			temp_structure = deepcopy(structure)
			

			for c in combo:

				# print 'structures', structures

				edge = (c, node)


				temp_structure.append(edge)

				if c[0] != 'n':
					structures = __generate(structures, temp_structure, temp_nodes, c)
				temp_nodes.remove(c)


				if filter(lambda a: a[0] == 'n', temp_nodes) == [] and connected(temp_structure):
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
	invalid =filter(lambda a: a[0] != 'n', invalid)


	if filter(lambda a: a != invalid[0], invalid) == []:
		if len(invalid) < 2:
			return False
		return True
	return False

# print connected([('n1', '2'), ('2', '3'), ('3', '4'), ('4', 'o')])
# print connected([('n4', 'o'), ('g1', 'o'), ('g0', 'g1'), ('n0', 'g0'), ('n1', 'g0'), ('n2', 'g0'), ('n3', 'g1')])



generate(NODES)

		