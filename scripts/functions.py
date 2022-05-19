import tardis
from os.path import exists
from os import makedirs
import pandas as pd

def run_simulation(path, folder):
	name = path.split(sep = '/')[-1].split(sep = '.')[0]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	spec = sim.runner.spectrum_virtual

	with open('../synthetic_spectra/' + folder + '/' + name + '.txt', 'w') as file:
		for j in range(len(spec.wavelength.value)):
			file.write(str(spec.wavelength.value[j]) + ' ' + str(spec.luminosity_density_lambda.value[j]) + ' \n')

	return

def run_simulation_csv(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	spec = sim.runner.spectrum_virtual

	path = '../synthetic_spectra/' + folder + '/spectra.csv'

	if exists(path) == False:
		with open(path, 'w') as file:
			file.write('wl')
			for j in range(len(spec.wavelength.value)):
				file.write(',' + str(spec.wavelength.value[j]))
			file.write('\n')

		makedirs('../synthetic_spectra/' + folder + '/temp')

	with open('../synthetic_spectra/' + folder + '/temp/' + name + '.csv', 'w') as f:
		f.write(name + '\n')
		for l in spec.luminosity_density_lambda.value:
			f.write(str(l) + '\n')

	#if exists(path):
	#	with open(path, 'a') as file:
	#		file.write(name)
	#		for j in range(len(spec.wavelength.value)):
	#			file.write(',' + str(spec.luminosity_density_lambda.value[j]))
	#		file.write('\n')
	#
	#else:
	#	with open(path, 'w') as file:
	#		file.write('wl')
	#		for j in range(len(spec.wavelength.value)):
	#			file.write(',' + str(spec.wavelength.value[j]))
	#		file.write('\n')
	#		file.write(name)
	#		for j in range(len(spec.wavelength.value)):
	#			file.write(',' + str(spec.luminosity_density_lambda.value[j]))
	#		file.write('\n')

	return

def transpose_csv(path):
	df = pd.read_csv(path, index_col = 0, header = None).T
	df.to_csv(path, index = 0)

	return