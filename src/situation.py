from hierarchy import Hierarchy


class Situation(Hierarchy):
	'''
	'''
	def __init__(self, data=None, **attr):
		Hierarchy.__init__(self, data, **attr)

	def situation(self):
		roots = []
		print self.nodes()
		for node in self.nodes():
			if self.predecessors(node) == None:
				roots.append((node, self.node[node]['value']))
			else:
				print 'node', node
				print 'aggregate %s' % node, self.node[node]['value']
		return roots