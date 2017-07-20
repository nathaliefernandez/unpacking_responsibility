from hierarchy import Hierarchy
from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from situation import Situation
from fractions import Fraction
from itertools import product
from simulate import simulate
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
import networkx as nx
import json


'''
open input file and save to a dict
'''
with open('pilot.json', 'r') as data:
	file = json.load(data)
data.close()

# list of cases to run
cases = len(file['experiments'])

for case in xrange(cases):

	cause = file['experiments'][case]['situation']['cause']

	if 'effect' in file['experiments'][case]['situation']:
		effect = file['experiments'][case]['situation']['effect']
	else:
		effect = 'o'

	hierarchy = simulate(file['experiments'][case], cause=cause, effect=effect)


	fig = draw(hierarchy, ID=case)
	
	fig = highlight_cause_effect(hierarchy, fig, cause, effect, ID=case)

	situation = draw_outcomes(hierarchy, fig, ID=case)


	pivr = pivotality(hierarchy, cause, effect, root=True)
	piv = pivotality(hierarchy, cause, effect)

	crit = criticality(hierarchy, cause, effect)


	predictions = show_predictions(hierarchy, fig, cause, effect, ID=case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	plt.close()