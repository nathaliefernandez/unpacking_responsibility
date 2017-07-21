from networkx import DiGraph
from itertools import product
from fractions import Fraction
import networkx as nx
import numpy as np
from random import shuffle


class Hierarchy(DiGraph):
	'''
	creates hierarchy/DiGraph
	parameters:
		attributes
			list        priors
			3D list     structure
			2D list     threshold
	return:
		Hierarchy
	'''
	def __init__(self, data=None, **attr):
		if 'structure' in attr:
			data = attr['structure']

		# shuffle(data)

		DiGraph.__init__(self, data, **attr)
		
		# add prior attributes
		self.assign_priors()

		if 'sample' in attr:
			if 'values' in self.graph:
				self.assign_values(self.graph['values'])

		return 

	'''
	return:
		list	group nodes in hierarchy
	'''
	def groups(self):
		return filter(lambda a: a[-1] == 'g', self.nodes())

	'''
	return:
		list	root nodes in hierarchy
	'''
	def roots(self):
		return filter(lambda a: a[-1] == 'n', self.nodes())

	'''
	return:
		list    longest path in directed acyclic DiGraph, reversed
	'''
	def longest_path(self):
		return list(reversed(nx.dag_longest_path(self)))

	def path(self, cause, effect):

		node = cause
		path = []
		i = 0

		while cause != effect:

			if self.successors(cause) == [effect]:
				cause = effect
			
			for node in self.successors(cause):
				path.append(node)
				cause = node

		return path

	'''
	adds an attribute to the graph that specifies the
	longest path in the graph starting at every node
	adds attribute to the root node specifying the longest path
	return:
		None
	'''
	def paths(self):
		copy = self.copy()
		self.graph['paths'] = {}
		while len(copy.edges()) != 0:
			if copy.longest_path() != []:
				subgraph = copy.longest_path()

				if list(copy.longest_path())[0] not in self.graph['paths']:
					self.node[subgraph[0]]['level'] = len(subgraph)
					self.graph['paths'][list(copy.longest_path())[0]] = subgraph

				copy.remove_edge(list(copy.longest_path())[1], list(copy.longest_path())[0])
		for node in self.nodes():
			if not self.node[node].get('level'):
				self.node[node]['level'] = 1
		return None