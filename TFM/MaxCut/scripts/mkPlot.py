"""
python mkPlot.py 10 mean     22
python mkPlot.py 10 cvar_0.5 22
python mkPlot.py 10 cvar_0.2 22

python mkPlot.py 11 mean     27
python mkPlot.py 11 cvar_0.5 27
python mkPlot.py 11 cvar_0.2 27

python mkPlot.py 12 mean     33
python mkPlot.py 12 cvar_0.5 33
python mkPlot.py 12 cvar_0.2 33

python mkPlot.py 13 mean     39
python mkPlot.py 13 cvar_0.5 39
python mkPlot.py 13 cvar_0.2 39
"""

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

# Input arguments
if len(sys.argv) < 4:
    raise ValueError("""Please insert: 
    number of qbits 
    cost function type 
    number of edges""")

n_n     = sys.argv[1]
n_cost  = sys.argv[2]
n_E     = sys.argv[3]

# Print input values
print("Cost function: {0}".format(n_cost))
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
brute_solution, brute_cost, eigenvalues = brute_force_solver(W2, verbosity=True)
mean_eig = np.mean(eigenvalues)


# Variables declaration
WEIGHTS       = W2
N_QBITS       = n
DEPTH         = 2
BACKEND       = 'qasm_simulator'
FINAL_EVAL    = 128
COST          = n_cost
N_repetitions = 100
shots_list    = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 256]


# Load results
load_string = "../files/{0}qbits_{1}edges_{2}/Scan".format(N_QBITS, E, COST) 
results = load_files(load_string, shots_list)
df, df_plot = analyze_results(results, shots_list, W2, brute_solution, COST)


# Create folder for figures
folder_name = "figures/{0}qbits_{1}edges_{2}/".format(N_QBITS, E, COST)
save_command = "mkdir -p {0}".format(folder_name)
os.system(save_command)


# Actual plotting

# Cost function evaluations vs shots/(Hilbert space dimension)
save_name = folder_name + "nfev_vs_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots/2**N_QBITS,
             y       = df_plot.nfevs,
             title   = "Number of cost function evaluations vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Cost function evaluations",
             y_err   = df_plot.nfevs * y_unc_rel,
             save_as = save_name)

# Cost function evaluations vs shots
save_name = folder_name + "nfev_vs_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots,
             y       = df_plot.nfevs,
             title   = "Number of cost function evaluations vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Cost function evaluations",
             y_err   = df_plot.nfevs * y_unc_rel,
             save_as = save_name)


# Total circuit evaluations vs shots/(Hilbert space dimension)
save_name = folder_name + "nfev_x_shots_vs_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots/2**N_QBITS,
             y       = df_plot.nfevs*df_plot.shots,
             title   = "Number of total circuit evaluations vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Total circuits evaluations",
             y_err   = (df_plot.nfevs*df_plot.shots) * y_unc_rel,
             save_as = save_name)

# Total circuit evaluations vs shots
save_name = folder_name + "nfev_x_shots_vs_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots,
             y       = df_plot.nfevs*df_plot.shots,
             title   = "Number of total circuit evaluations vs shots",
             xlabel  = "Shots",
             ylabel  = "Total circuits evaluations",
             y_err   = (df_plot.nfevs*df_plot.shots) * y_unc_rel,
             save_as = save_name)


# Average solution cost function vs shots/(Hilbert space dimension)
save_name = folder_name + "cost_vs_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots/2**N_QBITS,
             y       = df_plot.cost,
             title   = "Average solution cost function vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Average solution cost function",
             save_as = save_name,
             y_err   = df_plot.cost * y_unc_rel,
             ylim    = (-brute_cost, 0))

# Average solution cost function vs shots
save_name = folder_name + "cost_vs_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots,
             y       = df_plot.cost,
             title   = "Average solution cost function vs shots",
             xlabel  = "Shots",
             ylabel  = "Average solution cost function",
             save_as = save_name,
             y_err   = df_plot.cost * y_unc_rel,
             ylim    = (-brute_cost, 0))


# Relative solution cost function vs shots/(Hilbert space dimension)
save_name = folder_name + "rel_cost_vs_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots / 2**N_QBITS,
             y       = df_plot.cost / brute_cost,
             title   = "Relative solution cost function vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Relative solution cost function",
             save_as = save_name,
             y_err   = (df_plot.cost / brute_cost) * y_unc_rel,
             ylim    = (-1, 0))

# Relative solution cost function vs shots
save_name = folder_name + "rel_cost_vs_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots,
             y       = df_plot.cost / brute_cost,
             title   = "Relative solution cost function vs shots",
             xlabel  = "Shots",
             ylabel  = "Relative solution cost function",
             save_as = save_name,
             y_err   = (df_plot.cost / brute_cost) * y_unc_rel,
             ylim    = (-1, 0))


# Fraction of good solutions vs shots/(Hilbert space dimension)
save_name = folder_name + "frac_vs_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots/2**N_QBITS,
             y       = df_plot.frac,
             title   = "Fraction of good solutions vs normalized shots",
             xlabel  = "Shots / dim(H)",
             ylabel  = "Fraction of good solutions",
             y_err   = df_plot.frac * y_unc_rel,
             save_as = save_name)

# Fraction of good solutions vs shots
save_name = folder_name + "frac_vs_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = df_plot.shots,
             y       = df_plot.frac,
             title   = "Fraction of good solutions vs shots",
             xlabel  = "Shots",
             ylabel  = "Fraction of good solutions",
             y_err   = df_plot.frac * y_unc_rel,
             save_as = save_name)


# Mean difference with optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = np.sqrt(2**N_QBITS/df_plot.shots),
             y       = brute_cost + df_plot.cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title   = r"Mean difference with optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
             xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
             ylabel  = "difference with optimal cost function value",
             y_err   = (brute_cost + df_plot.cost) * y_unc_rel,
             save_as = save_name)

# Mean difference with optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x        = 1 / np.sqrt(df_plot.shots),
             y        = brute_cost + df_plot.cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title    = r"Mean difference with optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
             xlabel   = r"$1 / \sqrt{Shots}$",
             ylabel   = "difference with optimal cost function value",
             y_err    = (brute_cost + df_plot.cost) * y_unc_rel,
             save_as  = save_name)


# Difference with mean cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "diff_mean_vs_inv_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x       = np.sqrt(2**N_QBITS/df_plot.shots),
             y       = mean_eig + df_plot.cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title   = r"Difference with mean cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
             xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
             ylabel  = "Difference with mean cost function",
             y_err   = (brute_cost + df_plot.cost) * y_unc_rel,
             ylim    = (-brute_cost + mean_eig, 10),
             save_as = save_name)

# Difference with mean cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "diff_mean_vs_inv_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x        = 1 / np.sqrt(df_plot.shots),
             y        = mean_eig + df_plot.cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title    = r"Difference with mean cost function value vs $\frac{1}{\sqrt{Shots}}$",
             xlabel   = r"$1 / \sqrt{Shots}$",
             ylabel   = "Difference with mean cost function",
             y_err    = (brute_cost + df_plot.cost) * y_unc_rel,
             ylim     = (-brute_cost + mean_eig, 10),
             save_as  = save_name)


# Relative difference with optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots_o_dimH"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x        = np.sqrt(2**N_QBITS/df_plot.shots),
             y        = 1 + df_plot.cost/brute_cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title    = r"Relative difference with optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
             xlabel   = r"$\sqrt{\frac{dim(H)}{Shots}}$",
             ylabel   = "Relative difference with optimal cost function value",
             save_as  = save_name)

# Relative difference with optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots"
y_unc_rel = 1 / np.sqrt(N_repetitions)

scatter_plot(x        = 1 / np.sqrt(df_plot.shots),
             y        = 1 + df_plot.cost/brute_cost,
             #do_fit   = True,
             #fit_func = "1-exp",
             title    = r"Relative difference with optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
             xlabel   = r"$1 / \sqrt{Shots}$",
             ylabel   = "Relative difference with optimal cost function value",
             y_err    = (1 + df_plot.cost/brute_cost) * y_unc_rel,
             save_as  = save_name)


# Create new directory in upper folder
new_dir_command = "mkdir -p ../{0}".format(folder_name)
os.system(new_dir_command)

# Copy file there
copy_command = "cp {0}/* ../{1}/".format(folder_name, folder_name)
os.system(copy_command)

# Finally, delete the original output folder
delete_command = "rm -r {0}".format(folder_name)
os.system(delete_command)
