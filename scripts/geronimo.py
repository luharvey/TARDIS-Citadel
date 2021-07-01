import sys
import glob
from os import makedirs
from text import text

if len(sys.argv) != 2:
	print('\nRun: ' + text.GREEN + 'python geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Checking to find the console file for the parameter space ranges
paths = glob.glob('../ymls/' + sys.argv[1] + '/*.yml')
if len(paths) == 0:
	print(text.RED + '\nFAILURE: ' + text.END + 'no yml files found at ' + '../ymls/' + sys.argv[1] + '/*.yml\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

try:
	makedirs('../synthetic_spectra/' + sys.argv[1])
except:
	print(text.RED + '\nFAILURE: ' + text.END + 'there already exists a directory ' + text.BOLD + '../synthetic_spectra/' + sys.argv[1] + text.END + '\nOperation aborted to prevent overwriting\n')
	exit()

import tardis

for i in paths:
	name = i.split(sep = '/')[-1].split(sep = '.')[0]

	sim = tardis.run_tardis(i)
	spec = sim.runner.spectrum_virtual

	with open('../synthetic_spectra/' + sys.argv[1] + '/' + name + '.txt', 'w') as file:
		for j in range(len(spec.wavelength.value)):
			file.write(str(spec.wavelength.value[j]) + ' ' + str(spec.luminosity_density_lambda.value[j]) + ' \n')