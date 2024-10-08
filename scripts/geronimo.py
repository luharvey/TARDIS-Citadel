#Module import
import sys
import glob
from os import makedirs
from text import text
from functions import run_simulation_csv, transpose_csv, where, run_simulation_extract
import time
import multiprocess as mp
import shutil
from pandas import read_csv
from numpy import ceil

#Testing for user input and returning help prompt if a simulation name has not been provided
if len(sys.argv) < 2:
	print('\nRun: ' + text.GREEN + 'python geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Checking to find the console file for the parameter space ranges
paths = glob.glob('../ymls/' + sys.argv[1] + '/*.yml')
if len(paths) == 0:
	print(text.RED + '\nFAILURE: ' + text.END + 'no yml files found at ' + '../ymls/' + sys.argv[1] + '/*.yml\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Creating simulation spectrum output directory with overwrite check
try:
	makedirs('../synthetic_spectra/' + sys.argv[1])
except:
	#Checking for overwrite user input option
	if '-o' in sys.argv:
		try:
			shutil.rmtree('../synthetic_spectra/' + sys.argv[1])
			makedirs('../synthetic_spectra/' + sys.argv[1])
		except:
			pass
	else:	
		print(text.RED + '\nFAILURE: ' + text.END + 'there already exists a directory ' + text.BOLD + '../synthetic_spectra/' + sys.argv[1] + text.END + '\nOperation aborted to prevent overwriting\n')
		exit()

#Checking for user input specification of number of CPUs over which to parallelise
if '-n' in sys.argv:
	ncut = int(sys.argv[where('-n', sys.argv) + 1])
else:
	ncut = int(mp.cpu_count()/2)

#Recording start time
t0 = time.time()

#Diving the simulations into sets to parallelise
split = []
for n in range(int(ceil(len(paths)/ncut))):
	split.append(paths[n*ncut:(n+1)*ncut])

#=--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--=

#Main program
if __name__ == '__main__':

	#Setting the parallel processes running
	for k in split:
		p = []
		for path in k:
			p.append(mp.Process(target = run_simulation_extract, args = (path,sys.argv[1],)))
			p[-1].start()
		for process in p:
			process.join()
	
	#Removing the input files after successful simulations
	shutil.rmtree('../ymls/' + sys.argv[1])
	
	#Recording the overall simulation grid time
	t = time.time()-t0
	with open('../blueprints/' + sys.argv[1] + '.bp', 'a') as f:
		f.write('\nSimulation time (multiprocess ' + str(mp.cpu_count()) + 'CPU): ' + str(int(t)) + 's')
