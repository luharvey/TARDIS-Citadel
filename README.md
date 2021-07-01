# TARDIS-Citadel
Scripts and directory structure to run bulk TARDIS simulations to fine tune parameters.

1.) Copy the example console file and save as SIMULATION_NAME.txt. Fill in the various ranges of parameter spaces you wish to permutate over.
2.) Ensure the csvy models are placed within the csvy folder and that their paths match those in the console file.
3.) Within the scripts folder run: 'python chameleon_circuit.py SIMULATION_NAME' to calculate all possible permuations of the parameter space ranges specified within the console file, then create the necessary YAML and CSVY files.
4.) Run: 'python geronimo.py SIMULATION_NAME' to run the input files as TARDIS simulations, sending the output spectra to the synthetic_spectra directory.
5.) Run: 'python display.py SIMULATION_NAME TARGET_NAME e/p' to overplot the synthesised spectra with the reference spectra to be placed in the reference_spectra directory. The e or p flag indicates whether to use the early or peak reference spectrum.
