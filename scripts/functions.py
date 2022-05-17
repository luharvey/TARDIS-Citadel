import tardis

def run_simulation(path, folder):
	name = path.split(sep = '/')[-1].split(sep = '.')[0]

	sim = tardis.run_tardis(path)
	spec = sim.runner.spectrum_virtual

	with open('../synthetic_spectra/' + folder + '/' + name + '.txt', 'w') as file:
		for j in range(len(spec.wavelength.value)):
			file.write(str(spec.wavelength.value[j]) + ' ' + str(spec.luminosity_density_lambda.value[j]) + ' \n')