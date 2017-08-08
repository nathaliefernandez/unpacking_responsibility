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


	if 'priors' in data:
		data['priors'] = [(str(u), float(v)) for u,v in file['hierarchy']['priors']]

	if unicode('situation') in file:
		situation = {}
		situation['values'] = [(str(u), int(v)) for u,v in file['situation']['values']]
		situation['thresholds'] = [(str(u), int(v)) for u,v in file['situation']['thresholds']]
		
		if 'names' in attr:
			hierarchy = Situation(hierarchy=data, situation=situation, names=attr['names'])
		else:
			hierarchy = Situation(hierarchy=data, situation=situation)
	else: 
		if 'names' in attr:
			hierarchy = Situation(data, names=attr['names'])
		else:
			hierarchy = Situation(data)


	return hierarchy