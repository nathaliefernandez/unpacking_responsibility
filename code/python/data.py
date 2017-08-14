import csv
from evaluate import pivotal, pivotality, criticality, prob_pivotal, unpacked_pivotality
from fractions import Fraction
from simulate import *
import json

with open('../json/pilot.json', 'r') as data:
	file = json.load(data)
data.close()

# list of cases to run
cases = len(file['experiments'])


with open('model.csv', 'w') as csvfile:
	fieldnames = ['trial', 'index', 'rating']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for case in xrange(cases):

		cause = file['experiments'][case]['situation']['cause']

		if 'effect' in file['experiments'][case]['situation']:
			effect = file['experiments'][case]['situation']['effect']
		else:
			effect = 'o'


		hierarchy = simulate(file['experiments'][case], cause=cause, effect=effect)


		pivr = pivotality(hierarchy, cause, effect, root=True)
		piv = pivotality(hierarchy, cause, effect)

		crit = criticality(hierarchy, cause, effect, e_value=True)

		writer.writerow({'trial': case, 'index' : 'criticality', 'rating': crit})
		writer.writerow({'trial': case, 'index' : 'alternative', 'rating': 100*float(Fraction(pivr))})
		writer.writerow({'trial': case, 'index' : 'newmodel', 'rating': 100*float(Fraction(piv))})



	
# with open('model.csv', 'w') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})