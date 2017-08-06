from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import *
from names import *

import numpy as np
import networkx as nx

COLOR = [(0, 100), (220, 100), (120, 60), (280, 100), (24, 100)]
RED0 = (hsl_to_rgb(0, 100, 65), hsl_to_rgb(0, 100, 33))
BLUE0 = (hsl_to_rgb(220, 100, 65), hsl_to_rgb(220, 100, 33))
RED1 = (hsl_to_rgb(0, 100, 50), hsl_to_rgb(0, 100, 18))
BLUE1 = (hsl_to_rgb(220, 100, 50), hsl_to_rgb(220, 100, 18))
RED2 = (hsl_to_rgb(0, 100, 35), hsl_to_rgb(0, 100, 6))
BLUE2 = (hsl_to_rgb(220, 100, 35), hsl_to_rgb(220, 100, 6))


for i in xrange(10):
 
	nodes = ['0n', '1n', '2n', '3n', '4n']
	names =[]
	count = 0
	while count < len(nodes):
		name = get_first_name()

		if len(name) < 5 and name not in names:
			names.append(name)
			count += 1
h = {} 
h['structure'] = [['0n', 'o'], ['1n', 'o'], ['2n', 'o'], ['3n', 'o'], ['4n', 'o']]

s = {}
s['thresholds'] = [['o', 3]]
s['values'] = [['0n', 0], ['1n', 1], ['2n', 1]]

hierarchy = Situation(hierarchy=h, situation=s, names=['']*50)
# hierarchy.node['0g']['team'] = 'A'

# hierarchy.node['0n']['color'] = RED1[0]
# hierarchy.node['1n']['color'] = RED0[0]
# hierarchy.node['2n']['color'] = BLUE0[0]
# hierarchy.node['3n']['color'] = RED0[0]
# hierarchy.node['4n']['color'] = BLUE0[0]
# hierarchy.node['0g']['team'] = 'A'
# hierarchy.node['1g']['team'] = 'B'

# hierarchy.node['0n']['color'] = '.7'
# hierarchy.node['1n']['color'] = '.7'
# hierarchy.node['2n']['color'] = '.7'
# hierarchy.node['3n']['color'] = '.7'
# hierarchy.node['4n']['color'] = '.7'
# hierarchy.node['0g']['color'] = '.5'
# hierarchy.node['1g']['color'] = '.5'

hierarchy.node['0n']['color'] = BLUE0[0]
hierarchy.node['1n']['color'] = BLUE0[0]
hierarchy.node['2n']['color'] = BLUE0[0]
hierarchy.node['3n']['color'] = BLUE0[0]
hierarchy.node['4n']['color'] = RED0[0]


hierarchy.node['0n']['ec'] = BLUE0[1]
hierarchy.node['1n']['ec'] = BLUE0[1]
hierarchy.node['2n']['ec'] = BLUE0[1]
hierarchy.node['3n']['ec'] = BLUE0[1]
hierarchy.node['4n']['ec'] = RED0[1]
# hierarchy.node['0g']['color'] = RED1[0]
# hierarchy.node['1g']['color'] = RED1[0]

# hierarchy.node['5n']['color'] = '.6'
# hierarchy.node['6n']['color'] = '.6'
# hierarchy.node['7n']['color'] = '.6'
# hierarchy.node['8n']['color'] = '.6'
# hierarchy.node['9n']['color'] = '.6'

# hierarchy.node['o']['color'] = BLUE2[0]
# hierarchy.node['o']['ec'] = BLUE2[1]

# hierarchy.node['0n']['ec'] = RED1[1]
# hierarchy.node['1n']['ec'] = RED0[1]
# hierarchy.node['2n']['ec'] = BLUE0[1]
# hierarchy.node['3n']['ec'] = RED0[1]
# hierarchy.node['4n']['ec'] = BLUE0[1]

fig = draw(hierarchy, size=True, fig=(7.5, 5), election=True, file='../../presentations/MSRP2017/image30.png')


# hierarchy.node['o']['color'] = RED2[0]
# hierarchy.node['o']['ec'] = RED2[1]

# hierarchy.node['0g']['ec'] = RED1[1]
# hierarchy.node['1g']['ec'] = RED1[1]

# hierarchy.node['0n']['ec'] = '.35'
# hierarchy.node['1n']['ec'] = '.35'
# hierarchy.node['2n']['ec'] = '.35'
# hierarchy.node['3n']['ec'] = '.35'
# hierarchy.node['4n']['ec'] = '.35'
# hierarchy.node['0g']['ec'] = '.25'
# hierarchy.node['1g']['ec'] = '.25'
# hierarchy.node['5n']['ec'] = '.28'
# hierarchy.node['6n']['ec'] = '.28'
# hierarchy.node['7n']['ec'] = '.28'
# hierarchy.node['8n']['ec'] = '.28'
# hierarchy.node['9n']['ec'] = '.28'



fig = draw(hierarchy, size=True, fig=(7.5, 5), election=True, file='../../presentations/MSRP2017/image30.png')
highlight_cause_effect(hierarchy, fig, None, '4n', file='../../presentations/MSRP2017/image30.png')
# fig = draw_outcomes(hierarchy, fig, election=True, file='../../presentations/MSRP2017/image21.png')

# hierarchy.node['0g']['color'] = BLUE1[0]
# hierarchy.node['0g']['ec'] = BLUE1[1]


# fig = draw(hierarchy, size=True, fig=(7.5, 5), election=True, file='../../presentations/MSRP2017/image27.png')


# fig = draw(hierarchy, size=True, election=True, file='../../presentations/MSRP2017/image3.png')

# h = {} 
# h['structure'] = [['0n', '0g'], ['1n', '0g'], ['2n', '1g'], ['3n', '1g'], ['0g', 'o'], ['1g', 'o']]

# s = {}
# s['thresholds'] = [['0g', 1], ['1g', 1], ['o', 2]]
# s['values'] = [['0n', 1], ['1n', 1], ['2n', 0], ['3n', 0]]

# hierarchy = Situation(hierarchy=h, situation=s, names=['', '', '', ''])
# hierarchy.node['0g']['team'] = 'B'
# hierarchy.node['1g']['team'] = 'C'


# fig = draw(hierarchy, size=True, fig=(7.5, 5), election=True, file='../../presentations/MSRP2017/image3.png')
# situation = draw_outcomes(hierarchy, fig, election=True, file='../../presentations/MSRP2017/image4.png')