from situation import Situation
from evaluate import pivotal, pivotality, criticality, prob_pivotal
from draw import draw, draw_outcomes


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
	data['priors'] = [(str(u), float(v)) for u,v in file['hierarchy']['priors']]
	data['thresholds'] = [(str(u), int(v)) for u,v in file['hierarchy']['thresholds']]

	if unicode('situation') in file:
		situation = {}
		situation['values'] = [(str(u), int(v)) for u,v in file['situation']['values']]
		
		hierarchy = Situation(hierarchy=data, situation=situation)
		hierarchy.evaluate(hierarchy.nodes()[0])
	else: 
		hierarchy = Situation(hierarchy=hierarchy)

		

	if 'draw' in attr:
		fig = draw(hierarchy, data=data)
		if unicode('situation') in file or 'situation' in attr:
			draw_outcomes(hierarchy, fig, ID=data['ID'])
			# draw(hierarchy, situation=situation, ID=data['ID'])
	
	return hierarchy