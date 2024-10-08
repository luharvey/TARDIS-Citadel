#Module import
import tardis
from os.path import exists
from os import makedirs
import pandas as pd
from datetime import datetime

#Searching an array for the index of a target string or value
def where(target, array):
	for i in range(len(array)):
		if target == array[i]:
			return i 

#Extracting spectrum from finished simulation
def extract(sim, output_path):
	#Extracting and casting wavelength and luminosity arrays
	spectrum = sim.transport.transport_state.spectrum_virtual
	wl0 = list(spectrum.wavelength.value)
	lum0 = list(spectrum.luminosity_density_lambda.value)

	#Reversing arrays to be ascending in wavelength
	wl0.reverse()
	lum0.reverse()

	#Cutting spectrum to optical/NIR region
	wavelength, luminosity = [], []
	for i in range(len(wl0)):
		if 3000 <= wl0[i] <= 12000:
			wavelength.append(wl0[i])
			luminosity.append(lum0[i])
		elif wl0[i] > 12000:
			break

	#Recording simulation runtime
	t = datetime.now()
	finish_time = t.strftime("%d-%m-%Y_%H-%M-%S")

	#Write
	pd.DataFrame({'wavelength':wavelength, 'luminosity':luminosity}).to_csv(f'{output_path}_spectrum_{finish_time}.csv', index = 0)

#Running tardis
def run_simulation_extract(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	spec = sim.transport.transport_state.spectrum_virtual

	directory = f'../synthetic_spectra/{folder}'
	
	if exists(directory) == False:
		makedirs(directory)

	extract(sim, f'{directory}/{name}')

#=--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--=

"""
	Previous formulation in which the output luminosity arrays from the different simulations were written to different rows of a master csv file which was then transposed after completion. With parallelisation this
	causes issues with multiple processes writing to the same csv file simultaneously.
"""

#Running tardis simulation with spectrum output to csv
def run_simulation_csv(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	#Simulation and spectrum extraction
	sim = tardis.run_tardis(path, show_convergence_plots = False)
	spec = sim.transport.transport_state.spectrum_virtual

	#Creating directory
	path = '../synthetic_spectra/' + folder + '/spectra.csv'
	if exists(path) == False:
		with open(path, 'w') as file:
			file.write('wl')
			for j in range(len(spec.wavelength.value)):
				file.write(',' + str(spec.wavelength.value[j]))
			file.write('\n')

		makedirs('../synthetic_spectra/' + folder + '/temp')

	#Write
	with open('../synthetic_spectra/' + folder + '/temp/' + name + '.csv', 'w') as f:
		f.write('lum\n')
		for l in spec.luminosity_density_lambda.value:
			f.write(str(l) + '\n')

#Tranposing of csv (switch rows and columns)
def transpose_csv(path):
	df = pd.read_csv(path, index_col = 0, header = None).T
	df.to_csv(path, index = 0)