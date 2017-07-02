<<<<<<< HEAD
=======

>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
from hierarchy import Hierarchy
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
	structure = [(str(u), str(v)) for u,v in file['experiments'][case]['structure']]
	priors = [(str(u), float(v)) for u,v in file['experiments'][case]['priors']]
	thresholds = [(str(u), int(v)) for u,v in file['experiments'][case]['thresholds']]

	hierarchy = Hierarchy(structure, priors=priors, thresholds=thresholds)

	if 'draw' in attr:
		if 'show' in attr:
			draw(hierarchy, attr['draw'], show=attr['show'])
		else:
			draw(hierarchy, attr['draw'])

<<<<<<< HEAD
	return hierarchy
=======
	return hierarchy
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
