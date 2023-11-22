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

def where(target, array):
	for i in range(len(array)):
		if target == array[i]:
			return i 

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
		f.write('lum\n')
		for l in spec.luminosity_density_lambda.value:
			f.write(str(l) + '\n')

	return

def extract(sim, output_path):
    spectrum = sim.runner.spectrum_virtual
    wl0 = list(spectrum.wavelength.value)
    lum0 = list(spectrum.luminosity_density_lambda.value)
    wl0.reverse()
    lum0.reverse()
    wavelength, luminosity = [], []
    for i in range(len(wl0)):
        if 3000 <= wl0[i] <= 12000:
            wavelength.append(wl0[i])
            luminosity.append(lum0[i])
        elif wl0[i] > 12000:
            break

    #Extracting temperature profile
    velocity = []
    temperature = []
    v = sim.model.velocity.value/1e5
    step = v[1]-v[0]
    temperature = sim.plasma.t_rad
    velocity = v[:-1] + step/2
    density = sim.model.density.value

    #Extracting silicon ionisation profiles
    #'Si':14
    Z = 14
    Si = list(sim.model.abundance.T[Z])
    si_ionisation_profiles = {0:[], 1:[], 2:[], 3:[]}

    for j in range(len(velocity)):
        shell = sim.plasma.ion_number_density[j][Z]
        tot = sum(shell)

        for i in [0, 1, 2, 3]:
            si_ionisation_profiles[i].append(shell[i]/tot)

    #Extracting calcium ionisation profiles
    #'Ca':20
    Z = 20
    Ca = list(sim.model.abundance.T[Z])
    ca_ionisation_profiles = {0:[], 1:[], 2:[], 3:[]}

    for j in range(len(velocity)):
        shell = sim.plasma.ion_number_density[j][Z]
        tot = sum(shell)

        for i in [0, 1, 2, 3]:
            ca_ionisation_profiles[i].append(shell[i]/tot)

    #Writing to output files
    pd.DataFrame({'wavelength':wavelength, 'luminosity':luminosity}).to_csv(f'{output_path}_spectrum.csv', index = 0)
    pd.DataFrame({'velocity':velocity, 'density':density, 'temperature':temperature, 'si':Si, 'ca':Ca,\
        'si0':si_ionisation_profiles[0], 'si1':si_ionisation_profiles[1], 'si2':si_ionisation_profiles[2], 'si3':si_ionisation_profiles[3],\
        'ca0':ca_ionisation_profiles[0], 'ca1':ca_ionisation_profiles[1], 'ca2':ca_ionisation_profiles[2], 'ca3':ca_ionisation_profiles[3]}).to_csv(f'{output_path}_profiles.csv', index = 0)

def run_simulation_extract(path, folder):
	name = path.split(sep = '/')[-1][:-4]

	sim = tardis.run_tardis(path, show_convergence_plots = False)
	spec = sim.runner.spectrum_virtual

	directory = f'../synthetic_spectra/{folder}'
	
	if exists(directory) == False:
		makedirs(directory)

	extract(sim, f'{directory}/{name}')

	return

def transpose_csv(path):
	df = pd.read_csv(path, index_col = 0, header = None).T
	df.to_csv(path, index = 0)

	return