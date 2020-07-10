import sys, os

os.system("cp ../Functions.py .")

# Loading all functions (maybe not needed, at least not ALL)
from Functions import cost_function_C, VQE_circuit, cost_function_cobyla, time_vs_shots
from Functions import scatter_plot, best_candidate_finder, F_opt_finder, cv_a_r, save_object
from Functions import plot_comparison, random_graph_producer, brute_force_solver, PI
from Functions import load_files, analyze_results

import numpy as np
import pandas as pd

# Declare these variables in case they are not passed as input arguments
n_n = 10
n_E = 20

# Input arguments
if len(sys.argv) < 4:
    raise ValueError("Please insert number of shots, cost function type and CVaR alpha value")
n_shots = sys.argv[1]
n_cost  = sys.argv[2]
n_alpha = sys.argv[3]

if len(sys.argv) > 4:
    n_n     = sys.argv[4]
if len(sys.argv) > 5:
    n_E     = sys.argv[5]

# Print input values
print("Shots:         {0}".format(n_shots))
print("Cost function: {0}".format(n_cost))
print("Alpha:         {0}".format(n_alpha))
print("N vertices:    {0}".format(n_n))
print("N edges:       {0}".format(n_E))
    
# Create random Max-Cut problem
# Number of vertices
n = int(n_n)

# Number of edges
E = int(n_E)

# Random seed
seed = 2000

# Now create Max-Cut QUBO matrix
W2 = random_graph_producer(n, E, seed, verbosity=True)


# Variables declaration
WEIGHTS       = W2
N_QBITS       = n
DEPTH         = 2
SHOTS         = int(n_shots)
BACKEND       = 'qasm_simulator'
FINAL_EVAL    = 128
COST          = n_cost
ALPHA         = float(n_alpha)
N_repetitions = 100


# Create folder for output file
folder_name = ""
if COST == 'cost':
    folder_name = "files/{0}qbits_mean".format(n)
elif COST == 'cvar':
    folder_name = "files/{0}qbits_cvar_{1}".format(n, n_alpha)
save_command = "mkdir -p {0}".format(folder_name)
os.system(save_command)


# Actual optimizations
results_current = []
output = 0
file_name = "{0}/Scan_{1}qbits_{2}shots.pkl".format(folder_name, str(n), str(SHOTS))
print(file_name)
for rep in range(N_repetitions):
    output = time_vs_shots(SHOTS,
                           WEIGHTS,
                           N_QBITS,
                           DEPTH,
                           BACKEND,
                           FINAL_EVAL,
                           COST)

    if rep % 20 == 0:
        print("Done with", str(SHOTS), "shots, repetition", rep)
    results_current.append(output)

save_object(results_current, file_name) 


# Create new directory in upper folder
new_dir_command = "mkdir -p ../{0}".format(folder_name)
os.system(new_dir_command)

# Copy file there
copy_command = "cp {0} ../{1}".format(file_name, folder_name)
os.system(copy_command)

# Finally, delete the original output folder
delete_command = "rm {0}".format(file_name)
os.system(delete_command)
