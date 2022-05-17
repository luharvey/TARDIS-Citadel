import sys
import glob
from os import makedirs
from text import text

if len(sys.argv) != 2:
	print('\nRun: ' + text.GREEN + 'python multi_geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
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

import multiprocessing as mp
from functions import run_simulation
from functools import partial
import time

t0 = time.time()
pool = mp.Pool(int(2*mp.cpu_count()/3))
pool.map(partial(run_simulation, folder = sys.argv[1]), paths)
pool.close()
pool.join()
t = time.time()-t0

with open('../blueprints/' + sys.argv[1] + '.bp', 'a') as f:
	f.write('\nSimulation time: ' + str(int(t)) + 's')