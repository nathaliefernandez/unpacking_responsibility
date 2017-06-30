from networkx import DiGraph
from itertools import product
from fractions import Fraction
import networkx as nx
import numpy as np


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
        DiGraph.__init__(self, data, **attr)

        # add prior attributes
        self.assign_priors()
        # add threshold attributes
        self.assign_thresholds()

        if 'values' in self.graph:
            self.assign_values(self.graph['values'])

        return None

    '''
    assign priors to root nodes
    '''
    def assign_priors(self):
        if 'priors' in self.graph:
            for node, prior in self.graph['priors']:
                self.node[node]['prior'] = prior
        return None

    '''
    assign thresholds to root nodes
        return: None
    '''
    def assign_thresholds(self):
        if 'thresholds' in self.graph:
            for node, threshold in self.graph['thresholds']:
                self.node[node]['threshold'] = threshold
        return None


    '''
    assign values and assigns them to each node
    '''
    def assign_values(self, values):
        for node, value in values:
            self.assign_value(node, value)
        return None


    def assign_value(self, node, value):
        self.node[node]['value'] = value
        return None

    '''
    samples values and assigns them to each node
    return:
        None
    '''
    #samples values and assigns them to nodes
    def sample_values(self):
        for node in self.nodes():
            if 'prior' in self.node[node]:
                prior = self.node[node]['prior']
                self.sample_value(node, prior)
        return None

    '''
    sample one value for instances where hierarchy
    does not have a graph attribute of priors
    return:
        None
    '''
    def sample_value(self, node, prior):
        self.node[node]['value'] = np.random.choice([0, 1], p=[1-prior, prior])
        return self.node[node]['value']
    '''
    return node's value
    event:  str             node
    return: int/True/False  value
    '''
    def value(self, event):
        return self.node[event]['value']

    '''
    clear value of every node in self except root nodes
    return:
        None
    '''
    def clear_values(self):
        for node in self.nodes():
            if 'value' in self.node[node] and self.predecessors(node) != []:
                self.clear_value(node)
        return None

    def clear_value(self, node):
        del self.node[node]['value']
        return None
    '''
    evaluate the outcome of an event
    samples root values if not assigned
    if root node has no prior, uses prior of .5
    parameters:
        event:  str     node
    return: int     outcome of node*multiplier
    '''
    def evaluate(self, event, **attr):
        values = {}
        attr = dict(attr)

        if self.predecessors(event) == []:
            if 'value' in self.node[event]:
                return self.value(event)
            else:
                return self.sample_value(event, self.node[event].get('prior') if 'prior' in self.node[event] else .5)

        # recursively call evaluate on predecessors until dict of values is complete
        for pred in self.predecessors(event):
            value = self.evaluate(pred, **attr)
            values[pred] = value*self.node[pred]['multiplier'] if 'multiplier' in self.node[pred] else value*1
        
        
        if 'value' not in self.node[event]:
            self.node[event]['func'] = lambda values:sum(values.values()) >= self.node[event]['threshold']
            self.node[event]['value'] = int(self.node[event].get('func')(values))


        return self.value(event)

    def situation(self):
        roots = []
        for node in self.nodes():
            if 'value' in self.node[node]:
                if self.predecessors(node) == []:
                    roots.append((node, self.node[node]['value']))
                else:
                    print 'aggregate %s' % node, self.node[node]['value']
        return roots

    '''
    finds path from root node to effect
    return:
        list            path
    '''
    def longest_path_from(self, cause, effect, p):
        if self.successors(cause) == []:
            print 'path', p
            self.node[p[-1]]['path'] = p
            return None
        print 'suc', self.successors(cause)
        for c in self.successors(cause):
            
            p.append(c)
            self.longest_path_from(c, effect, p)


    '''
    return:
        list    longest path in directed acyclic DiGraph, reversed
    '''
    def longest_path(self):
        return list(reversed(nx.dag_longest_path(self)))

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

