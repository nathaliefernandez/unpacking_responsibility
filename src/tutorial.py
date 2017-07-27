from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions
from names import *

import numpy as np
import networkx as nx

COLOR = [(0, 100), (220, 100), (120, 60), (280, 100), (24, 100)]

# h = {} 
# h['structure'] = [['0n', 'o'], ['1n', '0g'], ['2n', '0g'], ['0g', 'o']]

# s = {}
# s['thresholds'] = [['0g', 2], ['o', 1]]
# s['values'] = [['0n', 1], ['1n', 1], ['2n', 0]]

# hierarchy = Situation(hierarchy=h, situation=s, comprehension=True, names=['Claude', 'Barry', 'Jacob'])
# hierarchy.node['0g']['team'] = 'A'

# fig = draw(hierarchy, size=True, fig=(7.5, 5), arrow=['0g'], file='experiment/static/images/instructions/image4.png')
# situation = draw_outcomes(hierarchy, fig, arrow=['0g'], file='experiment/static/images/instructions/image4.png')
# hierarchy.evaluate('0g')
# situation = draw_outcomes(hierarchy, fig, arrow=['0g'], file='experiment/static/images/instructions/image5.png')
# fig = draw(hierarchy, size=True, fig=fig, file='experiment/static/images/instructions/image6.png')

# hierarchy.evaluate('o')
# situation = draw_outcomes(hierarchy, fig, file='experiment/static/images/instructions/image7.png')



# hierarchy.remove_node('0g')
# hierarchy.add_edges_from([('1n', 'o'), ('2n', 'o')])

# fig = draw(hierarchy, fig=(7.5, 5), arrow=['0n', '1n', '2n'], file='experiment/static/images/instructions/image1.png')
# fig = draw(hierarchy, fig=fig, arrow=['0n', '1n', '2n'], file='experiment/static/images/instructions/image2.png')

# situation = draw_outcomes(hierarchy, fig, arrow=['0n', '1n', '2n'], file='experiment/static/images/instructions/image3.png')

h = {} 
h['structure'] = [['0n', 'o'], ['1n', '0g'], ['2n', '0g'], ['0g', 'o']]

s = {}
s['thresholds'] = [['0g', 2], ['o', 1]]
s['values'] = [['0n', 1], ['1n', 1], ['2n', 0]]

hierarchy = Situation(hierarchy=h, situation=s, names=['Claude', 'Barry', 'Jacob'])

fig = draw(hierarchy, size=True, fig=(7.5, 5), arrow=['0g', '0n'], file='experiment/static/images/instructions/image10.png')
situation = draw_outcomes(hierarchy, fig, arrow=['0g', '0n'], file='experiment/static/images/instructions/image10.png')

plt.close()
