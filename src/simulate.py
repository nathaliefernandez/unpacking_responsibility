from situation import Situation
from evaluate import pivotal, pivotality, criticality, prob_pivotal
from draw import draw


import matplotlib.pyplot as plt


'''
simulates the case
parameters:
	int		case number
	dict	loaded input file 
return:
	None
'''
def simulate(case, file, **attr):
	hierarchy = {}

	hierarchy['structure'] = [(str(u), str(v)) for u,v in file['experiments'][case]['hierarchy']['structure']]
	hierarchy['priors'] = [(str(u), float(v)) for u,v in file['experiments'][case]['hierarchy']['priors']]
	hierarchy['thresholds'] = [(str(u), int(v)) for u,v in file['experiments'][case]['hierarchy']['thresholds']]

	if 'situation' in attr:
		situation = {}
		situation['values'] = [(str(u), int(v)) for u,v in file['experiments'][case]['situation']['values']]
		
		hierarchy = Situation(hierarchy=hierarchy, situation=situation)
	else: 
		hierarchy = Situation(hierarchy=hierarchy)

	if 'draw' in attr:
		if 'show' in attr:
			draw(hierarchy, attr['draw'], show=attr['show'])
		else:
			draw(hierarchy, attr['draw'])

	return hierarchy