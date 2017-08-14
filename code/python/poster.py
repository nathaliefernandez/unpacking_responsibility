from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from itertools import product
from simulate import *
from draw import *
from names import *

import numpy as np
import networkx as nx
import json

h = Situation

'''
open input file and save to a dict
'''
with open('../json/experiment1.json', 'r') as data:
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



for case in [1, 5, 7, 12, 13, 14]:

	cause = file['experiments'][case]['situation']['cause']


	if 'effect' in file['experiments'][case]['situation']:
		effect = file['experiments'][case]['situation']['effect']
	else:
		effect = 'o'



	hierarchy = simulate(file['experiments'][case], cause=cause, effect=effect, names=['']*5)

	print case
	fig = draw(hierarchy, fig=(15, 10), file='../../../presentations/posters/unpacking_responsibility/criticality%d.png'%case)
	
	situation = draw_outcomes(hierarchy, fig, file='../../../presentations/posters/unpacking_responsibility/situation%d.png'%case)


	pivr = pivotality(hierarchy, cause, effect, root=True)
	piv = pivotality(hierarchy, cause, effect)

	crit = criticality(hierarchy, cause, effect, e_value=True)

	# print 'case', case
	
	# print 'crit', crit
	# print 'piv', pivr
	# print 'piv*', piv
	# print
	
	predictions = highlight_cause_effect(hierarchy, fig, cause, None, file='../../../presentations/posters/unpacking_responsibility/highlighted%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	if case == 0:
		predictions = highlight_cause_effect(hierarchy, fig, '0n', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/prev%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		
		hierarchy.node['0n']['value'] = 0
		# hierarchy.node['2n']['value'] = 1
		hierarchy.evaluate('o')

		fig = draw(hierarchy, fig=(5, 3.333), file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case)
		situation = draw_outcomes(hierarchy, fig, file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case)
		predictions = highlight_cause_effect(hierarchy, fig, cause, None, file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		predictions = highlight_cause_effect(hierarchy, fig, '0n', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

		hierarchy.node[cause]['value'] = 0
		hierarchy.evaluate('o')

		fig = draw(hierarchy, fig=(5, 3.333), file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case)
		situation = draw_outcomes(hierarchy, fig, file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case)
		predictions = highlight_cause_effect(hierarchy, fig, cause, None, file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		# predictions = highlight_cause_effect(hierarchy, fig, '0n', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
	if case == 1:
		predictions = highlight_cause_effect(hierarchy, fig, '0g', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/prev%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		
		hierarchy.node['0g']['value'] = 0
		# hierarchy.node['2n']['value'] = 1

		fig = draw(hierarchy, fig=(5, 3.333), file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case)
		situation = draw_outcomes(hierarchy, fig, file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case)
		predictions = highlight_cause_effect(hierarchy, fig, cause, None, file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		predictions = highlight_cause_effect(hierarchy, fig, '0g', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/after%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

		hierarchy.node[cause]['value'] = 0
		hierarchy.node[effect]['value'] = 0

		fig = draw(hierarchy, fig=(5, 3.333), file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case)
		situation = draw_outcomes(hierarchy, fig, file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case)
		predictions = highlight_cause_effect(hierarchy, fig, cause, None, file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)
		# predictions = highlight_cause_effect(hierarchy, fig, '0n', None, highlight='r', file='../../../presentations/posters/unpacking_responsibility/pivotal%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	predictions = show_predictions(hierarchy, fig, cause, effect, file='../../../presentations/posters/unpacking_responsibility/predictions%d.png'%case, pivotalityr=pivr, pivotality=piv, criticality=crit)

	plt.close()
	print hierarchy.node[cause]
	causes = filter(lambda a: hierarchy.predecessors(a) == [], hierarchy.nodes())
	
	# objects = ('Our model', 'Alternative model', 'Participants')
	# y_pos = np.arange(len(objects))
	# performance = [10,8,6]
 
	# plt.bar(y_pos, performance, align='center', alpha=0.5)
	# # plt.xticks(y_pos, objects)

	# plt.ylabel('responsibility')
	# plt.title('Judgments')

	# # n_groups = 5
	# # model = tuple([pivotality(hierarchy, cause, effect) for cause in causes])
	# # alt = tuple([pivotality(hierarchy, cause, effect, root=True) for cause in causes])

	

	# objects = ('Our model', 'Alternative model', 'Participants')
	# y_pos = np.arange(len(objects))
 # 	performance = [pivotality(hierarchy, cause, effect),pivotality(hierarchy, cause, effect, root=True),.1]
 # 	plt.bar(y_pos, performance, align='center', color=hierarchy.node[cause]['color'])
 # 	plt.ylabel('Responsibility')
 # 	plt.title('Judgments')
 # 	ax = fig.gca()
	# plt.xticks(y_pos, ['Our model', 'Alternative', 'Participants'])
	# # Place a legend to the right of this smaller subplot.
	# plt.legend(bbox_to_anchor=(0, 0), loc=2, borderaxespad=0.)
	# # plt.show()
	# # fig.savefig('../../../presentations/posters/unpacking_responsibility/graph%d.png'%case)
	# plt.close()