from hierarchy import Hierarchy


class Situation(Hierarchy):
	'''
	'''
	def __init__(self, data=None, **attr):
		if 'hierarchy' in attr:
			attr = attr['hierarchy']
			Hierarchy.__init__(self, data, **attr)

		elif 'situation' in attr:
			if 'values' in attr['situation']:
				self.assign_values(attr['situation']['values'])

	def situation(self):
		roots = []
		for node in self.nodes():
			if self.predecessors(node) == []:
				roots.append((node, self.node[node]['value']))
			else:
				print 'aggregate %s' % node, self.node[node]['value']
		return roots