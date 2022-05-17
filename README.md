# TARDIS-Citadel
Scripts and directory structure to run bulk TARDIS simulations to fine tune parameters.

1.) Copy the example console file and save as SIMULATION_NAME.txt. Fill in the various ranges of parameter spaces you wish to permutate over.

2.) Ensure the csvy models are placed within the csvy folder and that their paths match those in the console file.

3.) Within the scripts folder run: 'python chameleon_circuit.py SIMULATION_NAME' to calculate all possible permuations of the parameter space ranges specified within the console file, then create the necessary YAML and CSVY files.

4.) Run: 'python geronimo.py SIMULATION_NAME' to run the input files as TARDIS simulations, sending the output spectra to the synthetic_spectra directory.

In lieu of running geronimo.py, chose to run multi_geronimo.py with which the simulations will be run with a multiprocessing pool across the number of cores on the system.
