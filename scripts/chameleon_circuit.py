#Module import
import sys
import glob
import numpy as np
from shutil import copyfile
import os
from text import text

#Text processing function to remove outer brackets if present
def extract_brackets(string):
	#Initialise indices
	mindex, maxdex = 0, len(string)
	#Search for opening bracket
	for i in range(len(string)):
		if string[i] == '[':
			mindex = i+1
			break
	#Search for closing bracket
	for i in range(mindex, len(string)):
		if string[i] == ']':
			maxdex = i
			break
	return string[mindex:maxdex]

#Casting array values to integers where possible, floats otherwise
def num_array(array):
	output = []
	for i in array:
		#Attempt integer casting
		try:
			output.append(int(i))
		#Resort to float casting
		except:
			output.append(float(i))
	return output

#Wrapper for np.linspace function taking array input
def mkspan(params):
	return np.linspace(params[0], params[1], params[2])

#Locate and edit the inner boundary parameter from the specified csvy file
def change_inner_vel(file, v):
	#Read
	with open(file, 'r') as f:
		lines = f.readlines()
	#Locate and edit inner boundary parameter
	for h in range(len(lines)):
		if 'v_inner_boundary' in lines[h]:
			line_split = lines[h].split(sep = ' ')
			line_split[1] = str(v)
			lines[h] = line_split[0] + ' ' + line_split[1] + ' ' + line_split[2]
			break
	#Write
	with open(file, 'w') as f:
		for j in lines:
			f.write(j)

#Write new yml input file from given template with specified parameters
def new_yml(n, l, t, c, template = 'template.yml'):
	#Copy
	copyfile('../ymls/' + template, '../ymls/' + sys.argv[1] + '/' + str(n) + '.yml')
	#Read
	with open('../ymls/' + sys.argv[1] + '/' + str(n) + '.yml', 'r') as f:
		lines = f.readlines()

	#Update parameters
	for h in range(len(lines)):
		#Luminosity
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
		#Time
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
		#Model
		if 'csvy_model:' in lines[h]:
			line_array = lines[h].split(sep = ' ')
			for k in range(len(line_array)):
				if line_array[k] == 'CSVY\n':
					line_array[k] = c
			new_line = line_array[0] + ' ' + line_array[1] + '\n'
			lines[h] = new_line
	#Write
	with open('../ymls/' + sys.argv[1] + '/' + str(n) + '.yml', 'w') as f:
		for h in lines:
			f.write(h)

#Testing for user input and returning help prompt if a simulation name has not been provided
if len(sys.argv) < 2:
	print('\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Checking to find the console file for the parameter space ranges
console = glob.glob('../console/' + sys.argv[1] + '.txt')
if len(console) == 0:
	#Console file not found
	print(text.RED + '\nFAILURE: ' + text.END + 'no console file found at ' + '../console/' + sys.argv[1] + '.txt\nRun: ' + text.GREEN + 'python chameleon_circuit.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
	exit()

#Creating relevant directories if missing
if os.path.isdir('../reference_spectra') == False:
	os.makedirs('../reference_spectra')
if os.path.isdir('../synthetic_spectra') == False:
	os.makedirs('../synthetic_spectra')
if os.path.isdir('../blueprints') == False:
	os.makedirs('../blueprints')
if os.path.isdir('../csvy') == False:
	os.makedirs('../csvy')

#Switch between creating permutation grid or simply creating a simulation sequence
sequence = False

#Reading console file and extracting arrays
try:
	#Read
	with open(console[0], 'r') as file:
		lines = file.readlines()
		#Permutation grid
		if lines[0].split(sep = ': ')[-1] == 'citadel\n': 
			#Luminosity
			L = mkspan(num_array(extract_brackets(lines[1]).split(sep = ',')))
			#Time
			T = mkspan(num_array(extract_brackets(lines[2]).split(sep = ',')))
			#Model
			C = extract_brackets(lines[3]).split(sep = ',')
			#Inner velocity
			V = mkspan(num_array(extract_brackets(lines[4]).split(sep = ',')))
		#Simulation sequence
		elif lines[0].split(sep = ': ')[-1] == 'citadel_sequence\n':
			sequence = True
			#Luminosity
			L = num_array(extract_brackets(lines[1]).split(sep = ','))
			#Time
			T = num_array(extract_brackets(lines[2]).split(sep = ','))
			#Model
			C = extract_brackets(lines[3]).split(sep = ',')
			#Inner velocity
			V = num_array(extract_brackets(lines[4]).split(sep = ','))
		#Error checking for header
		else:
			print(text.RED + '\nFAILURE: ' + text.END + 'console file is missing the console_fomat header\n')
			exit()
#Error checking for reading console file
except:
	print(text.RED + '\nFAILURE: ' + text.END + 'failed reading in the console file ../console/' + sys.argv[1] + '.txt\n')
	exit()

#Extracting the directories from the csvy paths
C_dirs = []
for k in range(len(C)):
	C_split = C[k].split(sep = '/')
	C_dir = ''
	for i in range(len(C_split)-1):
		C_dir += C_split[i] + '/'
	C_dirs.append(C_dir)

#Creating the necessary csvy model files with the corresponding inner velocity
for i in V:
	for k in range(len(C_dirs)):
		copyfile(C[k], C_dirs[k] + str(int(round(i, 0))) + '.csvy')
		change_inner_vel(C_dirs[k] + str(int(round(i, 0))) + '.csvy', int(round(i, 0)))

#Assigning simulation sequence order
if sequence:
	combos = [[L[i], T[i], V[i], l] for i in range(len(L)) for l in C]
#Calculating all the simulation permutations
else:
	combos = [[i, j, k, l] for i in L for j in T for k in V for l in C]

#Rounding and casting
for i in range(len(combos)):
	combos[i][0] = round(combos[i][0], 2)
	combos[i][1] = round(combos[i][1], 2)
	combos[i][2] = int(round(combos[i][2], 0))

#Writing the blueprint file for indexing of simulation outputs
with open('../blueprints/' + sys.argv[1] + '.bp', 'w') as file:
	file.write('simulation_number luminosity_requested time_explosion v_inner csvy \n')
	for i in range(len(combos)):
		file.write(str(i+1) + ' ' + str(combos[i][0]) + ' ' + str(combos[i][1]) + ' ' + str(combos[i][2]) + ' ' + combos[i][3] + ' \n')

#Checking for overwrite
try:
	os.makedirs('../ymls/' + sys.argv[1])
#Exit with warning if found
except:
	print(text.RED + '\nFAILURE: ' + text.END + 'there already exists a directory ' + text.BOLD + '../ymls/' + sys.argv[1] + text.END + '\nOperation aborted to prevent overwriting\n')
	exit()

#Checking option for high resolution simulation
if '-h' in sys.argv:
	template_file = 'template_high_res.yml'
else:
	template_file = 'template.yml'

#Creating yml input files
for i in range(len(combos)):
	#Select the correct csvy directory
	for k in range(len(C_dirs)):
		if C_dirs[k] in combos[i][3]:
			index = k
	new_yml(i+1, combos[i][0], combos[i][1], '../' + C_dirs[index] + str(combos[i][2]) + '.csvy', template = template_file)

#Successful execution message
print(text.GREEN + '\nSUCCESS: ' + text.END + 'csvy and yml files constructed\nNow run: ' + text.GREEN + 'python geronimo.py ' + text.RED + text.BOLD + 'SIMULATION_NAME\n' + text.END)
