from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions
from names import *

import numpy as np
import networkx as nx

COLOR = [(0, 100), (220, 100), (120, 60), (280, 100), (24, 100)]


h = {} 
h['structure'] = [['0n', 'o'], ['1n', '0g'], ['2n', '0g'], ['0g', 'o']]

s = {}
s['thresholds'] = [['0g', 1], ['o', 2]]
s['values'] = [['0n', 1], ['1n', 1], ['2n', 0]]

hierarchy = Situation(hierarchy=h, situation=s, comprehension=True, names=['', '', ''])
hierarchy.node['0g']['team'] = 'A'

fig = draw(hierarchy, size=True, fig=(7.5, 5), file='experiment/static/images/instructions/comprehension1.png')
situation = draw_outcomes(hierarchy, fig, file='experiment/static/images/instructions/comprehension1.png')

h = {} 
h['structure'] = [['0n', '0g'], ['1n', '0g'], ['2n', '1g'], ['3n', '1g'], ['0g', 'o'], ['1g', 'o']]

s = {}
s['thresholds'] = [['0g', 1], ['1g', 1], ['o', 2]]
s['values'] = [['0n', 1], ['1n', 1], ['2n', 0], ['3n', 0]]

hierarchy = Situation(hierarchy=h, situation=s, comprehension=True, names=['', '', '', ''])
hierarchy.node['0g']['team'] = 'B'
hierarchy.node['1g']['team'] = 'C'


fig = draw(hierarchy, size=True, fig=(7.5, 5), file='experiment/static/images/instructions/comprehension2.png')
situation = draw_outcomes(hierarchy, fig, file='experiment/static/images/instructions/comprehension2.png')