import tardis
from os.path import exists
from os import makedirs
import pandas as pd

def run_simulation(path, folder):
	name = path.split(sep = '/')[-1].split(sep = '.')[0]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	#spec = sim.runner.spectrum_virtual
	spec = sim.transport.transport_state.spectrum_virtual

	with open('../synthetic_spectra/' + folder + '/' + name + '.txt', 'w') as file:
		for j in range(len(spec.wavelength.value)):
			file.write(str(spec.wavelength.value[j]) + ' ' + str(spec.luminosity_density_lambda.value[j]) + ' \n')

	#return

def where(target, array):
	for i in range(len(array)):
		if target == array[i]:
			return i 

	#return

def run_simulation_csv(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	#spec = sim.runner.spectrum_virtual
	spec = sim.transport.transport_state.spectrum_virtual

	path = '../synthetic_spectra/' + folder + '/spectra.csv'

	if exists(path) == False:
		with open(path, 'w') as file:
			file.write('wl')
			for j in range(len(spec.wavelength.value)):
				file.write(',' + str(spec.wavelength.value[j]))
			file.write('\n')

		makedirs('../synthetic_spectra/' + folder + '/temp')

	with open('../synthetic_spectra/' + folder + '/temp/' + name + '.csv', 'w') as f:
		f.write('lum\n')
		for l in spec.luminosity_density_lambda.value:
			f.write(str(l) + '\n')

	#return

def extract(sim, output_path):
	spectrum = sim.transport.transport_state.spectrum_virtual
	#spectrum = sim.runner.spectrum_virtual
	wl0 = list(spectrum.wavelength.value)
	lum0 = list(spectrum.luminosity_density_lambda.value)
	wl0.reverse()
	lum0.reverse()
	wavelength, luminosity = [], []
	for i in range(len(wl0)):
		if 3000 <= wl0[i] <= 12000:
			avelength.append(wl0[i])
			uminosity.append(lum0[i])
		elif wl0[i] > 12000:
			break

	#Writing to output files
	pd.DataFrame({'wavelength':wavelength, 'luminosity':luminosity}).to_csv(f'{output_path}_spectrum.csv', index = 0)

def run_simulation_extract(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	#spec = sim.runner.spectrum_virtual
	spec = sim.transport.transport_state.spectrum_virtual

	directory = f'../synthetic_spectra/{folder}'
	
	if exists(directory) == False:
		makedirs(directory)

	extract(sim, f'{directory}/{name}')

	#return

def transpose_csv(path):
	df = pd.read_csv(path, index_col = 0, header = None).T
	df.to_csv(path, index = 0)

	#return