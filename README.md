# TARDIS-Citadel
Scripts and directory structure to run bulk TARDIS simulations to fine tune parameters.

1.) Copy the example console file and save as NAME.txt. Fill in the various ranges of parameter spaces you wish to permutate over.

2.) Ensure the csvy models are placed within the csvy folder and that their paths match those in the console file.

3.) Within the scripts folder run: 'python chameleon_circuit.py NAME' to calculate all possible permuations of the parameter space ranges specified within the console file, then create the necessary YAML and CSVY files.

4.) Run: 'python geronimo.py NAME' to run the input files as TARDIS simulations, sending the output spectra to a single csv file in the synthetic_spectra directory. (../synthetic_spectra/NAME/spectra.csv)



Flags:

-s: run the simulations without the aid of multiprocessing

-o: overwrite the existing synthetic spectra folder corresponding to the same name

-n: specify the size of groups to split the simulations into (set to number of CPUs by default)

-h: (chameleon_circuit.py flag) creates yml files with 10 times the final photon packet count for smooth simulations



Dependancies:
TARDIS and the dependancies therein. Advised to create a conda environment from the environment definition file offered in the TARDIS repository: https://github.com/tardis-sn/tardis
Multiprocessing (install with pip): 'pip install multiprocess'
