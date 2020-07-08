import sys, os

os.system("cp ../Functions.py .")

# Loading all functions (maybe not needed)
from Functions import cost_function_C, VQE_circuit, cost_function_cobyla, time_vs_shots
from Functions import scatter_plot, best_candidate_finder, F_opt_finder, cv_a_r, save_object
from Functions import plot_comparison, random_graph_producer, brute_force_solver, PI
from Functions import load_files, analyze_results

import numpy as np
import pandas as pd

if len(sys.argv) < 4:
    raise ValueError("Please insert number of shots, cost function type and CVaR alpha value")
n_shots = sys.argv[1]
n_cost  = sys.argv[2]
n_alpha = sys.argv[3]

os.system("mkdir -p files")

# Create random Max-Cut problem
# Number of vertices
n = 10

# Number of edges
E = 20

# Random seed
seed = 2000

W2 = random_graph_producer(n, E, seed, verbosity=True)


# Variables declaration
WEIGHTS    = W2
N_QBITS    = n
DEPTH      = 2
SHOTS      = int(n_shots)
BACKEND    = 'qasm_simulator'
FINAL_EVAL = 128
COST       = n_cost
ALPHA      = float(n_alpha)

N_repetitions = 100
#shots_list = [8, 16, 32, 64, 128]


# A small scan, but we can get some results
#for shot in shots_list:
results_current = []
output = 0
file_name = "files/Scan_" + str(n) + "qbits_" + str(SHOTS) + ".pkl"
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

copy_command = "cp {0} ../files".format(file_name)
os.system(copy_command)
