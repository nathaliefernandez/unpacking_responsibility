import matplotlib.pyplot as plt
import matplotlib.patches as patches

from hierarchy import Hierarchy
from draw import COLOR


class Situation(Hierarchy):
	'''
	'''
	def __init__(self, data=None, **attr):

		if 'hierarchy' in attr:
			Hierarchy.__init__(self, data, **attr['hierarchy'])

		if 'situation' in attr:
			if 'values' in attr['situation']:
				self.assign_values(attr['situation']['values'])
			self.evaluate(self.nodes()[0])
		
		

	def situation(self):
		roots = []
		for node in self.nodes():
			if self.predecessors(node) == []:
				roots.append((node, self.node[node]['value']))
			else:
				print 'aggregate %s' % node, self.node[node]['value']
		return roots

