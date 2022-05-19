import sys
import glob
from os import makedirs
from text import text
from functions import run_simulation_csv, transpose_csv
import time
import multiprocessing as mp
import shutil
from pandas import read_csv

if len(sys.argv) < 2:
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
	#Overwriting the current synthetic_spectra directory for the simulation
	if '-o' in sys.argv:
		try:
			shutil.rmtree('../synthetic_spectra/' + sys.argv[1])
			makedirs('../synthetic_spectra/' + sys.argv[1])
		except:
			pass
	else:	
		print(text.RED + '\nFAILURE: ' + text.END + 'there already exists a directory ' + text.BOLD + '../synthetic_spectra/' + sys.argv[1] + text.END + '\nOperation aborted to prevent overwriting\n')
		exit()

t0 = time.time()

#Running the sims in a single process
if '-s' in sys.argv:
	#t0 = time.time()
	for i in paths:
		run_simulation_csv(i, sys.argv[1])
		#name = i.split(sep = '/')[-1].split(sep = '.')[0]
		#
		#sim = tardis.run_tardis(i)
		#spec = sim.runner.spectrum_virtual
		#
		#with open('../synthetic_spectra/' + sys.argv[1] + '/' + name + '.txt', 'w') as file:
		#	for j in range(len(spec.wavelength.value)):
		#		file.write(str(spec.wavelength.value[j]) + ' ' + str(spec.luminosity_density_lambda.value[j]) + ' \n')
	#t = time.time()-t0

else:
	from functools import partial
	
	#t0 = time.time()
	pool = mp.Pool(int(2*mp.cpu_count()/3))
	pool.map(partial(run_simulation_csv, folder = sys.argv[1]), paths)
	pool.close()
	pool.join()
	#t = time.time()-t0


#Combining all the files into the one spectra.csv
spec_paths = glob.glob('../synthetic_spectra/' + sys.argv[1] + '/temp/*.csv')
for p in spec_paths:
	num = p.split(sep = '/')[-1][:-4]
	d = read_csv(p)

	with open('../synthetic_spectra/' + sys.argv[1] + '/spectra.csv') as f:
		f.write(str(num))
		for j in d['lum']:
			f.write(',' + str(j))

		f.write('\n')


transpose_csv('../synthetic_spectra/' + sys.argv[1] + '/spectra.csv')
shutil.rmtree('../ymls/' + sys.argv[1])



#Recording the time
t = time.time()-t0
with open('../blueprints/' + sys.argv[1] + '.bp', 'a') as f:
	f.write('\nSimulation time (multiprocess ' + str(mp.cpu_count()) + 'CPU): ' + str(int(t)) + 's')












