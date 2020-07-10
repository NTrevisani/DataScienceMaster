import sys, os

os.system("cp ../Functions.py .")

# Loading all functions (maybe not needed, at least not ALL)
from Functions import cost_function_C, VQE_circuit, cost_function_cobyla, time_vs_shots
from Functions import scatter_plot, best_candidate_finder, F_opt_finder, cv_a_r, save_object
from Functions import plot_comparison, random_graph_producer, brute_force_solver, PI
from Functions import load_files, analyze_results

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# Solve the Max-Cut problem using brute-force approach
# and save the solution
brute_solution, brute_cost = brute_force_solver(W2, verbosity=True)


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
shots_list    = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 256]

# Load results
load_string = "../files/{0}qbits_{1}/Scan_{2}qbits".format(N_QBITS, COST, N_QBITS) 
results = load_files(load_string, shots_list)
df, df_plot = analyze_results(results, shots_list, W2, brute_solution, COST)

# Create folder for figures
folder_name = ""
if COST == 'mean':
    folder_name = "figures/{0}qbits_mean/".format(n)
elif COST == 'cvar':
    folder_name = "figures/{0}qbits_cvar_{1}/".format(n, n_alpha)
save_command = "mkdir -p {0}".format(folder_name)
os.system(save_command)


# Actual plotting

# Cost function evaluations vs shots
save_name = folder_name + "nfev_vs_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = df_plot.shots,
             y       = df_plot.nfevs,
             title   = "Number of cost function evaluations vs shots",
             xlabel  = "Shots",
             ylabel  = "Cost function evaluations",
             y_err   = df_plot.nfevs * y_unc_rel,
             save_as = save_name)

# Total circuit evaluations vs shots
save_name = folder_name + "nfev_x_shots_vs_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = df_plot.shots,
             y       = df_plot.nfevs*df_plot.shots,
             title   = "Number of total circuit evaluations vs shots",
             xlabel  = "Shots",
             ylabel  = "Total circuits evaluations",
             y_err   = (df_plot.nfevs*df_plot.shots) * y_unc_rel,
             save_as = save_name)

# Average solution cost function vs shots
save_name = folder_name + "cost_vs_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = df_plot.shots,
             y       = df_plot.cost,
             title   = "Average solution cost function vs shots",
             xlabel  = "Shots",
             ylabel  = "Average solution cost function",
             save_as = save_name,
             y_err   = df_plot.cost * y_unc_rel,
             ylim    = (-brute_cost, 0))

# Fraction of good solutions vs shots
save_name = folder_name + "frac_vs_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = df_plot.shots,
             y       = df_plot.frac,
             title   = "Fraction of good solutions vs shots",
             xlabel  = "Shots",
             ylabel  = "Fraction of good solutions",
             y_err   = df_plot.frac * y_unc_rel,
             save_as = save_name)

# Mean distance from optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = 1 / np.sqrt(df_plot.shots),
             y       = brute_cost + df_plot.cost,
             do_fit   = True,
             fit_func = "1-exp",
             title   = r"Mean distance from optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
             xlabel  = r"$1 / \sqrt{Shots}$",
             ylabel  = "Distance from optimal cost function value",
             y_err   = (brute_cost + df_plot.cost) * y_unc_rel,
             save_as = save_name)

# Fraction of good solutions vs total circuit evaluations
save_name = folder_name + "frac_vs_nfev_x_shots"
y_unc_rel = 1 / (np.sqrt(df_plot.shots) * np.sqrt(N_repetitions))

scatter_plot(x       = df_plot.nfevs*df_plot.shots,
             y       = df_plot.frac,
             title   = "Fraction of good solutions vs total circuit evaluations",
             xlabel  = "Total circuits evaluations",
             ylabel  = "Fraction of good solutions",
             y_err   = df_plot.frac * y_unc_rel,
             save_as = save_name)
