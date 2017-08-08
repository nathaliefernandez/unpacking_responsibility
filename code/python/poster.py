from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import draw, highlight_cause_effect, draw_outcomes, show_predictions
from names import *

import numpy as np
import networkx as nx
import json



'''
open input file and save to a dict
'''
with open('poster.json', 'r') as data:
	file = json.load(data)
data.close()

# list of cases to run
cases = len(file['experiments'])

names = []
index = [0]

for i in xrange(cases):
 
	nodes = [u for u,v in file['experiments'][i]['situation']['values']]

	index.append(index[i]+len(nodes))

	count = 0
	while count < len(nodes):
		name = get_first_name()

		if len(name) < 7 and name not in names:
			names.append(name)
			count += 1



for case in xrange(cases):

	cause = file['experiments'][case]['situation']['cause']

	if 'effect' in file['experiments'][case]['situation']:
		effect = file['experiments'][case]['situation']['effect']
	else:
		effect = 'o'



	hierarchy = simulate(file['experiments'][case], cause=cause, effect=effect, names=['']*5)


	fig = draw(hierarchy, file='../../presentations/posters/unpacking_responsibility/criticality%d.png'%case)
	
	situation = draw_outcomes(hierarchy, fig, file='../../presentations/posters/unpacking_responsibility/situation%d.png'%case)


	pivr = pivotality(hierarchy, cause, effect, root=True)
	piv = pivotality(hierarchy, cause, effect)

	crit = criticality(hierarchy, cause, effect, e_value=True)

	# print 'case', case
	
	# print 'crit', crit
	# print 'piv', pivr
	# print 'piv*', piv
	# print
	
	predictions = highlight_cause_effect(hierarchy, fig, cause, effect, file='../../presentations/posters/unpacking_responsibility/highlighted%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	predictions = show_predictions(hierarchy, fig, cause, effect, file='../../presentations/posters/unpacking_responsibility/predictions%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	plt.close()

	causes = filter(lambda a: hierarchy.predecessors(a) == [], hierarchy.nodes())
	
	n_groups = 5
	model = tuple([pivotality(hierarchy, cause, effect) for cause in causes])
	alt = tuple([pivotality(hierarchy, cause, effect, root=True) for cause in causes])
 
	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8
 
	rects1 = plt.bar(index, model, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Our Model')
 
	rects2 = plt.bar(index + bar_width, alt, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Alternative')
 
	plt.xlabel('Person')
	plt.ylabel('Scores')
	plt.title('Scores by person')
	plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
	plt.legend()
 
	plt.tight_layout()
	fig.savefig('../../presentations/posters/unpacking_responsibility/graph%d.png'%case)
	plt.close()