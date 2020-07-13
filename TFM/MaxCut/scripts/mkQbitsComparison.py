"""
python mkQbitsComparison.py mean
python mkQbitsComparison.py cvar_0.5
python mkQbitsComparison.py cvar_0.2
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

# Declare these variables in case they are not passed as input arguments
n_n     = 10
n_E     = 20
n_cost  = "mean"
n_alpha = 1

# Input arguments
if len(sys.argv) < 2:
    raise ValueError("""Please insert 
    cost function """)

n_cost  = sys.argv[1]
#n_alpha = sys.argv[2]

# Print input values
print("Cost function: {0}".format(n_cost))
#print("Alpha:         {0}".format(n_alpha))
    
# Create random Max-Cut problem
# Number of vertices
n = [10, 11, 12, 13]

# Number of edges
E = [20, 22, 24, 26]

# Random seed
seed = 2000

# Now create Max-Cut QUBO matrices
W2 = []
for i in range(len(n)):
    W = random_graph_producer(n[i], E[i], seed, verbosity=False)
    W2.append(W)
    
# Solve the Max-Cut problem using brute-force approach
# and save the solution
brute_solution = []
brute_cost     = [] 
for i in range(len(n)):
    bs, bc = brute_force_solver(W2[i], verbosity=False)
    brute_solution.append(bs)
    brute_cost.append(bc)
    
# Variables declaration
WEIGHTS       = W2
N_QBITS       = n
DEPTH         = 2
COST          = n_cost
N_repetitions = 100
shots_list    = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 256]


# Load results
df      = []
df_plot = []
for i in range(len(N_QBITS)):
    load_string = "../files/{0}qbits_{1}/Scan_{2}qbits".format(N_QBITS[i], COST, N_QBITS[i]) 
    results     = load_files(load_string, shots_list)
    df1, df2 = analyze_results(results, shots_list, W2[i], brute_solution[i], COST)
    df.append(df1)
    df_plot.append(df2)
    
# Create folder for figures
folder_name = "figures/{0}_comparison/".format(COST)
save_command = "mkdir -p {0}".format(folder_name)
os.system(save_command)


# Actual plotting

# Legend declaration - valid for all plots
# Still  too hard-coded
legend_list = ["10 qbits",
               "11 qbits",
               "12 qbits",
               "13 qbits"]

# Cost function evaluations vs shots/(Hilbert space dimension)
save_name = folder_name + "nfev_vs_shots_o_dimH"

plot_comparison(x       = [df_plot[i]["shots"]/2**N_QBITS[i] for i in range(len(N_QBITS))],
                y       = [df["nfevs"] for df in df_plot],
                legend  = legend_list,
                title   = "Number of cost function evaluations vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Cost function evaluations",
                leg_loc = "upper left",
                save_as = save_name)

# Cost function evaluations vs shots
save_name = folder_name + "nfev_vs_shots"

plot_comparison(x       = [df["shots"] for df in df_plot],
                y       = [df["nfevs"] for df in df_plot],
                legend  = legend_list,
                title   = "Number of cost function evaluations vs shots",
                xlabel  = "Shots",
                ylabel  = "Cost function evaluations",
                leg_loc = "upper left",
                save_as = save_name)


# Total circuit evaluations vs shots/(Hilbert space dimension)
save_name = folder_name + "nfev_x_shots_vs_shots_o_dimH"

plot_comparison(x       = [df_plot[i]["shots"]/2**N_QBITS[i] for i in range(len(N_QBITS))],
                y       = [df["shots"]*df["nfevs"] for df in df_plot],
                legend  = legend_list,
                title   = "Number of total circuit evaluations vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Total circuits evaluations",
                leg_loc = "upper left",
                save_as = save_name)

# Total circuit evaluations vs shots
save_name = folder_name + "nfev_x_shots_vs_shots"

plot_comparison(x       = [df["shots"] for df in df_plot],
                y       = [df["shots"]*df["nfevs"] for df in df_plot],
                legend  = legend_list,
                title   = "Number of total circuit evaluations vs shots",
                xlabel  = "Shots",
                ylabel  = "Total circuits evaluations",
                leg_loc = "upper left",
                save_as = save_name)


# Average solution cost function vs shots/(Hilbert space dimension)
save_name = folder_name + "cost_vs_shots_o_dimH"

plot_comparison(x       = [df_plot[i]["shots"]/2**N_QBITS[i] for i in range(len(N_QBITS))],
                y       = [df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = "Average solution cost function vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Cost function",
                ylim    = (-max(brute_cost), 0),
                leg_loc = "upper right",
                save_as = save_name)

# Average solution cost function vs shots
save_name = folder_name + "cost_vs_shots"

plot_comparison(x       = [df["shots"] for df in df_plot],
                y       = [df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = "Average solution cost function vs shots",
                xlabel  = "Shots",
                ylabel  = "Cost function",
                ylim    = (-max(brute_cost), 0),
                leg_loc = "upper right",
                save_as = save_name)


# Fraction of good solutions vs shots/(Hilbert space dimension)
save_name = folder_name + "frac_vs_shots_o_dimH"

plot_comparison(x       = [df_plot[i]["shots"]/2**N_QBITS[i] for i in range(len(N_QBITS))],
                y       = [df["frac"] for df in df_plot],
                legend  = legend_list,
                title   = "Fraction of good solutions vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Fraction of good solutions",
                leg_loc = "upper left",
                save_as = save_name)

# Fraction of good solutions vs shots
save_name = folder_name + "frac_vs_shots"

plot_comparison(x       = [df["shots"] for df in df_plot],
                y       = [df["frac"] for df in df_plot],
                legend  = legend_list,
                title   = "Fraction of good solutions vs shots",
                xlabel  = "Shots",
                ylabel  = "Fraction of good solutions",
                leg_loc = "upper left",
                save_as = save_name)


# Mean distance from optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots_o_dimH"

plot_comparison(x       = [np.sqrt(2**N_QBITS[i] / df_plot[i]["shots"]) for i in range(len(N_QBITS))],
                y       = [brute_cost[j] + df_plot[j]["cost"] for j in range(len(brute_cost))],
                legend  = legend_list,
                title   = r"Mean distance from optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
                xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
                ylabel  = "Distance from optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)

# Mean distance from optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots"

plot_comparison(x       = [1 / np.sqrt(df["shots"]) for df in df_plot],
                y       = [brute_cost[j] + df_plot[j]["cost"] for j in range(len(brute_cost))],
                legend  = legend_list,
                title   = r"Mean distance from optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
                xlabel  = r"$1 / \sqrt{Shots}$",
                ylabel  = "Distance from optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)


# Relative distance from optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots_o_dimH"

plot_comparison(x       = [np.sqrt(2**N_QBITS[i] / df_plot[i]["shots"]) for i in range(len(N_QBITS))],
                y       = [1 + df_plot[j]["cost"]/brute_cost[j] for j in range(len(brute_cost))],
                legend  = legend_list,
                title   = r"Relative distance from optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
                xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
                ylabel  = "Relative distance from optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)

# Relative distance from optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots"

plot_comparison(x       = [1 / np.sqrt(df["shots"]) for df in df_plot],
                y       = [1 + df_plot[j]["cost"]/brute_cost[j] for j in range(len(brute_cost))],
                legend  = legend_list,
                title   = r"Relative distance from optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
                xlabel  = r"$1 / \sqrt{Shots}$",
                ylabel  = "Relative distance from optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)


# Create new directory in upper folder
new_dir_command = "mkdir -p ../{0}".format(folder_name)
os.system(new_dir_command)

# Copy file there
copy_command = "cp {0}/* ../{1}/".format(folder_name, folder_name)
os.system(copy_command)

# Finally, delete the original output folder
delete_command = "rm -r {0}".format(folder_name)
os.system(delete_command)
