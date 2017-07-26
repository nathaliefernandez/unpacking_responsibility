from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions
from names import *

import numpy as np
import networkx as nx


h = {} 
h['structure'] = [['0n', 'o'], ['1n', '0g'], ['2n', '0g'], ['0g', 'o']]

s = {}
s['thresholds'] = [['0g', 1], ['o', 2]]
s['values'] = [['0n', 0], ['1n', 1], ['2n', 1]]

hierarchy = Situation(hierarchy=h, situation=s, comprehension=True)

fig = draw(hierarchy, file='experiment/static/images/instructions/comprehension1.png')

situation = draw_outcomes(hierarchy, fig, file='experiment/static/images/instructions/comprehension1.png')


plt.close()

h = {} 
h['structure'] = [['0n', 'o'], ['1n', 'o'], ['2n', 'o']]

s = {}
s['thresholds'] = [['o', 1]]
s['values'] = [['0n', 0], ['1n', 1], ['2n', 1]]

hierarchy = Situation(hierarchy=h, situation=s)

fig = draw(hierarchy, file='experiment/static/images/instructions/comprehension2.png')


