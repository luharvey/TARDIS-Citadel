import sys
import glob
import numpy as np
from shutil import copyfile
import os

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

def extract_brackets(string):
	for i in range(len(string)):
		if string[i] == '[':
			mindex = i
			break
	for i in range(mindex, len(string)):
		if string[i] == ']':
			maxdex = i
			break
	return string[mindex+1:maxdex]

def num_array(array):
	output = []
	for i in array:
		try:
			output.append(int(i))
		except:
			output.append(float(i))
	return output

def mkspan(params):
	return np.linspace(params[0], params[1], params[2])

def change_inner_vel(file, v):
	with open(file, 'r') as f:
		lines = f.readlines()

	for h in range(len(lines)):
		if 'v_inner_boundary' in lines[h]:
			line_split = lines[h].split(sep = ' ')
			line_split[1] = str(v)
			lines[h] = line_split[0] + ' ' + line_split[1] + ' ' + line_split[2]
			break

	with open(file, 'w') as f:
		for j in lines:
			f.write(j)

def new_yml(n, l, t, c):
	copyfile('../ymls/template.yml', '../ymls/' + sys.argv[1] + '/' + str(n) + '.yml')
	with open('../ymls/' + sys.argv[1] + '/' + str(n) + '.yml', 'r') as f:
		lines = f.readlines()

	for h in range(len(lines)):
		if 'luminosity_requested:' in lines[h]:
			line_array = lines[h].split(sep = ' ')
			for k in range(len(line_array)):
				if line_array[k] == 'LUMINOSITY':
					line_array[k] = str(l)
			new_line = ''
			for k in line_array[:-1]:
				new_line += k + ' '
			new_line += 'log_lsun\n'
			lines[h] = new_line

		if 'time_explosion:' in lines[h]:
			line_array = lines[h].split(sep = ' ')
			for k in range(len(line_array)):
				if line_array[k] == 'TIME':
					line_array[k] = str(t)
			new_line = ''
			for k in line_array[:-1]:
				new_line += k + ' '
			new_line += 'day\n'
			lines[h] = new_line

		if 'csvy_model:' in lines[h]:
			line_array = lines[h].split(sep = ' ')
			for k in range(len(line_array)):
				if line_array[k] == 'CSVY\n':
					line_array[k] = c
			new_line = line_array[0] + ' ' + line_array[1] + '\n'
			lines[h] = new_line

	with open('../ymls/' + sys.argv[1] + '/' + str(n) + '.yml', 'w') as f:
		for h in lines:
			f.write(h)

if len(sys.argv) != 2:
	print('\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Checking to find the console file for the parameter space ranges
console = glob.glob('../console/' + sys.argv[1] + '.txt')
if len(console) == 0:
	print(text.RED + '\nFAILURE: ' + text.END + 'no console file found at ' + '../console/' + sys.argv[1] + '.txt\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

if os.path.isdir('../reference_spectra') == False:
	os.makedirs('../reference_spectra')
if os.path.isdir('../synthetic_spectra') == False:
	os.makedirs('../synthetic_spectra')
if os.path.isdir('../blueprints') == False:
	os.makedirs('../blueprints')
if os.path.isdir('../csvy') == False:
	os.makedirs('../csvy')

try:
	#Reading in the parameter space ranges from the console file
	with open(console[0], 'r') as file:
		lines = file.readlines()
		L = mkspan(num_array(extract_brackets(lines[0]).split(sep = ',')))
		T = mkspan(num_array(extract_brackets(lines[1]).split(sep = ',')))
		C = extract_brackets(lines[2]).split(sep = ',')
		V = mkspan(num_array(extract_brackets(lines[3]).split(sep = ',')))
except:
	print(text.RED + '\nFAILURE: ' + text.END + 'failed reading in the console file ../console/' + sys.argv[1] + '.txt\n')
	exit()

#Calculating all the possible permutations
combos = [[i, j, k, l] for i in L for j in T for k in V for l in C]
for i in range(len(combos)):
	combos[i][0] = round(combos[i][0], 2)
	combos[i][1] = round(combos[i][1], 1)
	combos[i][2] = int(round(combos[i][2], 0))

#Extracting the directoryies from the csvy paths
C_dirs = []
for k in range(len(C)):
	C_split = C[k].split(sep = '/')
	C_dir = ''
	for i in range(len(C_split)-1):
		C_dir += C_split[i] + '/'
	C_dirs.append(C_dir)

#Copying the necessary csvy files with the corresponding inner velocity
for i in V:
	for k in range(len(C_dirs)):
		copyfile(C[k], C_dirs[k] + str(int(round(i, 0))) + '.csvy')
		change_inner_vel(C_dirs[k] + str(int(round(i, 0))) + '.csvy', int(round(i, 0)))

#Writing the blueprint file
with open('../blueprints/' + sys.argv[1] + '.bp', 'w') as file:
	file.write('simulation_number luminosity_requested time_explosion v_inner csvy \n')
	for i in range(len(combos)):
		file.write(str(i+1) + ' ' + str(combos[i][0]) + ' ' + str(combos[i][1]) + ' ' + str(combos[i][2]) + ' ' + combos[i][3] + ' \n')

try:
	os.makedirs('../ymls/' + sys.argv[1])
except:
	print(text.RED + '\nFAILURE: ' + text.END + 'there already exists a directory ' + text.BOLD + '../ymls/' + sys.argv[1] + text.END + '\nOperation aborted to prevent overwriting\n')
	exit()

for i in range(len(combos)):
	#Select the correct csvy directory
	for k in range(len(C_dirs)):
		if C_dirs[k] in combos[i][3]:
			index = k
	new_yml(i+1, combos[i][0], combos[i][1], '../' + C_dirs[index] + str(combos[i][2]) + '.csvy')

print(text.GREEN + '\nSUCCESS: ' + text.END + 'csvy and yml files constructed\nNow run: ' + text.GREEN + 'python geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
