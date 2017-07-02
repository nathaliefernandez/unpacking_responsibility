from hierarchy import Hierarchy
from itertools import product
from fractions import Fraction

import networkx as nx

'''
Return whether a cause is pivotal
if the cause was different, the effect would have been different
parameters:
    Hierarchy   hierarchy
    str         cause
    str         effect
    dict        attr containing effect value
return: True or False
'''
def pivotal(hierarchy, cause, effect, **attr):
    
    # set initial outcome
    outcome = hierarchy.evaluate(effect)
    copy = hierarchy.copy()
    copy.clear_values()

    if attr.has_key('values'):
        copy.assign_values(attr['values'])

    if attr.has_key('e_value'):
        if outcome != attr['e_value']:
            return False
    
    copy.node[cause]['value'] = int(not hierarchy.node[cause]['value'])
    
    new = copy.evaluate(effect) 
    
    if outcome != new:
        return True
    else:
        return False

'''
Calculate pivotaility
parameters:
    Hierarchy   hierarchy
    int         level ???change to str???
    str         cause node
    str         effect node
return:
    Fraction
'''
def pivotality(hierarchy, cause, effect, **attr):
    if pivotal(hierarchy, cause, effect, attr=attr):
        return 1

    copy = hierarchy.copy()

    if attr.has_key('root'):
        exogenous = filter(lambda a: copy.predecessors(a) == [] and nx.has_path(copy, a, effect), copy.nodes())
    else:
        exogenous = filter(lambda a: nx.has_path(copy, a, effect), copy.nodes())
    
    if effect in exogenous:
        exogenous.remove(effect)
    if cause in exogenous:
        exogenous.remove(cause)

    actual_values = map(hierarchy.value, exogenous)

    def distance(values):
        distance = 0
        for a, b in zip(values, actual_values):
            if a != b:
                distance += 1
        return distance

    closest_distance = len(exogenous) + 1
    closest_hierarchy = None

    for values in product(*[(0, 1) for v in xrange(len(exogenous))]):
        copy.clear_values()

        for node, value in zip(exogenous, values):
            copy.node[node]['value'] = value
        if attr.has_key('e_value'):
            piv = pivotal(copy, cause, effect, e_value=attr.get('e_value'), values=zip(exogenous, values))

        else:
            piv = pivotal(copy, cause, effect, values=zip(exogenous, values))
        if distance(values) < closest_distance and piv:
            closest_distance = distance(values)
            closest_hierarchy = values

    return Fraction(1, closest_distance + 1) if closest_hierarchy != None else 0

'''
find the probability that a node will be pivotal through sampling
parameters:
    Hierarchy   hierarchy
    str         node
    str         effect
    int         samples
return:
    float       criticality calculated through sampling
'''
def prob_pivotal(hierarchy, node, effect, samples=100, **attr):
    count = 0
    total = 0

    for sample in xrange(samples):
        # create a deepcopy of the hierarchy
        copy = hierarchy.copy()

        # sample root nodes to create a new situation
        if 'priors' in hierarchy.graph:
           copy.sample_values()
        else:
            for i in filter(lambda a: a[0] == str(0), hierarchy.nodes()):
                copy.sample_value(i, copy.node[i].get('prior'))

        # evaluate the effect that occured in the situation
        copy.evaluate(effect)

        # if we are considering only cases specified by e_value
        if attr.has_key('e_value'):
            # if the effect in this situation matches e_value increase total
            if copy.value(effect) == attr['e_value']:
                total += 1
                # if the node was pivotal for the account increase count
                if pivotal(copy, node, effect, attr['e_value']):
                    count += 1
        else:
            if pivotal(copy, node, effect, None):

                count += 1

        # if total is still zero, we are evaluvating prob_pivotal for all cases
        # set total to the sample size
        if total == 0:
            total = samples

    return float(count)/total

'''
P(cause=pivotal, effect=e_value)/P(effect=e_value) = P(cause=pivotal | effect=e_value)
parameters:
    Hierarchy   hierarchy
    str         cause
    str         effect
    dict        attr / e_value(target effect value)
return:
    float       criticality
'''
def criticality(hierarchy, cause, effect, **attr):

    copy = hierarchy.copy()
    exogenous = filter(lambda a: copy.predecessors(a) == [], copy.nodes())

    count = 0
    total = 0

    for settings in list(product(*[(0, 1) for v in xrange(len(exogenous))])):
        values = list(zip(exogenous, settings))
        copy.clear_values()
        copy.assign_values(values)

        outcome = copy.evaluate(effect)

        copy.clear_values()
        if attr.has_key('e_value'):
            if outcome == attr['e_value']:
                total += 1
                if pivotal(copy, cause, effect, attr['e_value']):
                    count += 1
        else:
            total = len(list(product(*[(0, 1) for v in xrange(len(exogenous))])))
            if pivotal(copy, cause, effect):
                count += 1

    return float(count)/total

def unpacked_pivotality(hierarchy, cause, effect, **attr):

    if hierarchy.longest_path_from(cause, effect, []) != []:

        piv = []
        nodes = hierarchy.longest_path_from(cause, effect, [])

        for n in hierarchy.node[cause]['path']:
            p = pivotality(hierarchy, node, effect, attr['e_value'] if attr.has_key('e_value') else None)
            piv.append(p)

        return sum(piv)/float(len(piv))
    else:
        return 'cannot be unpacked'