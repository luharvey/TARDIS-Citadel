import sys
import glob
from os import makedirs
from text import text
from functions import run_simulation_csv, transpose_csv, where, run_simulation_extract
import time
import multiprocess as mp
import shutil
from pandas import read_csv
#from functools import partial
from numpy import ceil



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

if '-n' in sys.argv:
	ncut = int(sys.argv[where('-n', sys.argv) + 1])
else:
	ncut = int(mp.cpu_count()/2)

t0 = time.time()

split = []
for n in range(int(ceil(len(paths)/ncut))):
	split.append(paths[n*ncut:(n+1)*ncut])

if __name__ == '__main__':

	#Running the sims in a single process
	if '-s' in sys.argv:
		for i in paths:
			run_simulation_csv(i, sys.argv[1])
	
	else:
		for k in split:
			p = []

			for path in k:
				#p.append(mp.Process(target = run_simulation_csv, args = (path,sys.argv[1],)))
				p.append(mp.Process(target = run_simulation_extract, args = (path,sys.argv[1],)))
				p[-1].start()

			for process in p:
				process.join()
	
	
	#Combining all the files into the one spectra.csv
	spec_paths = glob.glob('../synthetic_spectra/' + sys.argv[1] + '/temp/*.csv')
	for p in spec_paths:
		num = p.split(sep = '/')[-1][:-4]
		d = read_csv(p)
	
		with open('../synthetic_spectra/' + sys.argv[1] + '/spectra.csv', 'a') as f:
			f.write(str(num))
			for j in d['lum']:
				f.write(',' + str(j))
	
			f.write('\n')
	
	
	#transpose_csv('../synthetic_spectra/' + sys.argv[1] + '/spectra.csv')
	shutil.rmtree('../ymls/' + sys.argv[1])
	#shutil.rmtree('../synthetic_spectra/' + sys.argv[1] + '/temp')
	
	#Recording the time
	t = time.time()-t0
	with open('../blueprints/' + sys.argv[1] + '.bp', 'a') as f:
		f.write('\nSimulation time (multiprocess ' + str(mp.cpu_count()) + 'CPU): ' + str(int(t)) + 's')



