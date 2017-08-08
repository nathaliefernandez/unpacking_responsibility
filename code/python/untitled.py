from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions
from names import *

import numpy as np
import networkx as nx

count = 0

while count < len(nodes):
	name = get_first_name()

	if len(name) < 7 and name not in names:
		names.append(name)
		count += 1

h = {} 
h.append(structure=[['0n', 'o'], ['1n', '0g'], ['2n', '0g'], ['0g', 'o']])

s = {}
s.append(thresholds=[['0g', 1], ['o', 2]])
s.append(values=[['0n', 0], ['1n', 1], ['2n', 1]])

hierarchy = Situation(hierarchy=h, situation=s)

fig = draw(hierarchy, ID=1, file='/instructions/comprehension1.png')


situation = draw_outcomes(hierarchy, fig, ID=case)



plt.close()