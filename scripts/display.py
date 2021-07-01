import matplotlib.pyplot as plt 
import glob
import numpy as np 
import sys

#Text properties
class text:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

def import_spectrum(path):
	wl, lum = [], []
	with open(path, 'r') as file:
		for i in file.readlines():
			wl0, lum0, _ = i.split(sep = ' ')
			wl.append(float(wl0))
			lum.append(float(lum0))

	return wl, lum

def import_reference_spectra(target):
	specs = glob.glob('../reference_spectra/' + target + '/*')

	dates = []

	for i in specs:
		array = i.split(sep = '/')
		filename = array[len(array)-1]
		dates.append(float(filename[:len(filename)-4]))

	sorted_dates = []
	sorted_specs = []

	for i in sorted(zip(dates, specs)):
		sorted_dates.append(i[0])
		sorted_specs.append(i[1])

	early = (import_spectrum(sorted_specs[0]))
	peak = (import_spectrum(sorted_specs[1]))

	return early, peak

if len(sys.argv) != 4:
	print('\nRun: ' + text.GREEN + 'python display.py ' + text.RED + text.BOLD + 'SIMULATION_NAME TARGET_NAME e/p\n' + text.END)
	exit()

#Checking to find the console file for the parameter space ranges
paths = glob.glob('../synthetic_spectra/' + sys.argv[1] + '/*.txt')
if len(paths) == 0:
	print(text.RED + '\nFAILURE: ' + text.END + 'no spectra found at ' + '../synthetic_spectra/' + sys.argv[1] + '/*.txt\nRun: ' + text.GREEN + 'python geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

ref_check = glob.glob('../reference_spectra/' + sys.argv[2] + '/*')
if len(ref_check) == 0:
	print(text.RED + '\nFAILURE: ' + text.END + 'no reference spectra found for ' + sys.argv[2] + '\nAdd reference spectra to ../reference_spectra/' + sys.argv[2] + '\n')
	exit()
early, peak = import_reference_spectra(sys.argv[2])

if sys.argv[3] == 'e':
	ref_spec = early
elif sys.argv[3] == 'p':
	ref_spec = peak
else:
	print(text.RED + '\nFAILURE: ' + text.END + 'invalid argument ' + sys.argv[3] + '\nRun: ' + text.GREEN + 'python display.py ' + text.RED + text.BOLD + 'SIMULATION_NAME TARGET_NAME e/p\n' + text.END)
	exit()

sim_ids = []
for i in paths:
	sim_ids.append(float(i.split(sep = '/')[-1].split(sep = '.')[0]))

zipped = zip(sim_ids, paths)
ordered = sorted(zipped)

paths = [ordered[i][1] for i in range(len(ordered))]
sim_ids = [ordered[i][0] for i in range(len(ordered))]


for i in range(len(paths)):
	fig = plt.figure(figsize = (14, 6))
	wl, lum = import_spectrum(paths[i])
	plt.plot(ref_spec[0], ref_spec[1], color = '#CCCCCC')
	plt.plot(wl, lum, label = sim_ids[i])
	plt.legend()
	plt.xlim(3500, 9000)
	plt.ylim(0.9*np.amin(ref_spec[1]), 1.1*np.amax(ref_spec[1]))
	plt.xlabel(r'$\lambda$ ($\AA$)')
	plt.ylabel(r'$L$ ($erg$ $s^{-1}$ $\AA^{-1}$)')
	plt.tight_layout()
	plt.show()

