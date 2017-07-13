from situation import Situation
from evaluate import pivotal, pivotality, criticality, prob_pivotal
from draw import draw, highlight_cause_effect

import matplotlib.pyplot as plt


'''
simulates the case
parameters:
	int		case number
	dict	loaded input file 
return:
	None
'''
def simulate(file, **attr):
	data = {}

	if unicode('ID') in file:
		data['ID'] = file['ID']

	data['structure'] = [(str(u), str(v)) for u,v in file['hierarchy']['structure']]
	print data['structure']
	print
	
	if 'priors' in data:
		data['priors'] = [(str(u), float(v)) for u,v in file['hierarchy']['priors']]

	if unicode('situation') in file:
		if 'situation' in attr and 'op' in attr:
			situation = {}
			situation['values'] = [(str(u), int(v)) for u,v in file['situation'][attr['situation']]['values']]
			situation['thresholds'] = [(str(u), int(v)) for u,v in file['situation'][attr['situation']]['thresholds'][attr['op']]]
			
			hierarchy = Situation(hierarchy=data, situation=situation)
			hierarchy.evaluate(hierarchy.outcome())

			if 'draw' in attr:
				fig = draw(hierarchy, data=data, file='hierarchy.png')
		else:
			situation = []
			# for s in xrange(len(file['situation'])):
			for s in xrange(1):
				situation.append({})
				situation[s]['values'] = [(str(u), int(v)) for u,v in file['situation'][s]['values']]
				for op in file['situation'][s]['thresholds']:
					situation[s]['thresholds'] = {}
					situation[s]['thresholds'][op] = [(str(u), int(v)) for u,v in file['situation'][s]['thresholds'][op]]
					
					hierarchy = Situation(hierarchy=data, situation=situation[s], op=op)
					hierarchy.evaluate(hierarchy.outcome())

					if 'draw' in attr:
						fig = draw(hierarchy, data=data, file='hierarchy.png')
	else: 
		hierarchy = Situation(data)


		fig = draw(hierarchy, data=data, file = 'hierarchy.png')

		# fig = highlight_cause_effect(hierarchy, fig, '1_0', None, ID=3)

		# fig = highlight_cause_effect(hierarchy, fig, 'n0', hierarchy.outcome(), ID=3)

		# fig = highlight_cause_effect(hierarchy, fig, '2_0', None, ID=3)


		if unicode('situation') in file or 'situation' in attr:
			draw(hierarchy, fig=fig, situation=situation, data=data)
	
	return hierarchy