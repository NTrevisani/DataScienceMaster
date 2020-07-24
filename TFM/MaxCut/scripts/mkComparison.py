"""
python mkComparison.py 10 20
python mkComparison.py 11 22
python mkComparison.py 12 24
python mkComparison.py 13 26
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
n_n = 10
n_E = 20

# Input arguments
if len(sys.argv) < 3:
    raise ValueError("""Please insert 
    number of qbits 
    number of edges""")

n_n = sys.argv[1]
n_E = sys.argv[2]

# Print input values
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
COSTS         = ["mean","cvar_0.5","cvar_0.2"]
N_repetitions = 100
shots_list    = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 256]

# Load results
df      = []
df_plot = []
for i in range(len(COSTS)):
    load_string = "../files/{0}qbits_{1}/Scan_{2}qbits".format(N_QBITS, COSTS[i], N_QBITS) 
    results     = load_files(load_string, shots_list)
    df1, df2 = analyze_results(results, shots_list, W2, brute_solution, COSTS[i])
    df.append(df1)
    df_plot.append(df2)
    
# Create folder for figures
folder_name = "figures/{0}qbits_comparison/".format(n)
save_command = "mkdir -p {0}".format(folder_name)
os.system(save_command)


# Actual plotting

# Legend declaration - valid for all plots
# Still  too hard-coded
legend_list = ["Mean", "CVaR, a = 0.5", "CVaR, a = 0.2"]


# Cost function evaluations vs shots/(Hilbert space dimension)
save_name = folder_name + "nfev_vs_shots_o_dimH"

plot_comparison(x       = [df["shots"]/2**N_QBITS for df in df_plot],
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

plot_comparison(x       = [df["shots"]/2**N_QBITS for df in df_plot],
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

plot_comparison(x       = [df["shots"]/2**N_QBITS for df in df_plot],
                y       = [df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = "Average solution cost function vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Cost function",
                ylim    = (-brute_cost, 0),
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
                ylim    = (-brute_cost, 0),
                leg_loc = "upper right",
                save_as = save_name)


# Relative solution cost function vs shots/(Hilbert space dimension)
save_name = folder_name + "rel_cost_vs_shots_o_dimH"

plot_comparison(x       = [df["shots"]/2**N_QBITS for df in df_plot],
                y       = [df["cost"]/brute_cost for df in df_plot],
                legend  = legend_list,
                title   = "Relative solution cost function vs normalized shots",
                xlabel  = "Shots / dim(H)",
                ylabel  = "Relative cost function",
                ylim    = (-1, 0),
                leg_loc = "upper right",
                save_as = save_name)

# Relative solution cost function vs shots
save_name = folder_name + "rel_cost_vs_shots"

plot_comparison(x       = [df["shots"] for df in df_plot],
                y       = [df["cost"]/brute_cost for df in df_plot],
                legend  = legend_list,
                title   = "Relative solution cost function vs shots",
                xlabel  = "Shots",
                ylabel  = "Relative cost function",
                ylim    = (-1, 0),
                leg_loc = "upper right",
                save_as = save_name)


# Fraction of good solutions vs shots/(Hilbert space dimension)
save_name = folder_name + "frac_vs_shots_o_dimH"

plot_comparison(x       = [df["shots"]/2**N_QBITS for df in df_plot],
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


# Mean difference with optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots_o_dimH"

plot_comparison(x       = [np.sqrt(2**N_QBITS / df["shots"]) for df in df_plot],
                y       = [brute_cost + df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = r"Mean difference with optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
                xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
                ylabel  = "Difference with optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)

# Mean difference with optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "dist_vs_inv_shots"

plot_comparison(x       = [1 / np.sqrt(df["shots"]) for df in df_plot],
                y       = [brute_cost + df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = r"Mean difference with optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
                xlabel  = r"$1 / \sqrt{Shots}$",
                ylabel  = "Difference with optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)


# Difference with mean cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "diff_mean_vs_inv_shots_o_dimH"

plot_comparison(x       = [np.sqrt(2**N_QBITS / df["shots"]) for df in df_plot],
                y       = [mean_eig + df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = r"Difference with mean cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
                xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
                ylabel  = "Difference with mean cost function",
                leg_loc = "upper left",
                ylim    = (-brute_cost + mean_eig, 10),        
                save_as = save_name)

# Difference with mean cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "diff_mean_vs_inv_shots"
y_unc = [df["cost"] / np.sqrt(N_repetitions) for df in df_plot]

plot_comparison(x       = [1 / np.sqrt(df["shots"]) for df in df_plot],
                y       = [mean_eig + df["cost"] for df in df_plot],
                legend  = legend_list,
                title   = r"Difference with mean cost function value vs $\frac{1}{\sqrt{Shots}}$",
                xlabel  = r"$1 / \sqrt{Shots}$",
                ylabel  = "Difference with mean cost function",
		ylim    = (-brute_cost + mean_eig, 10),
                y_err   = [df["cost"] / np.sqrt(N_repetitions) for df in df_plot], #y_unc, 
                leg_loc = "upper left",
                save_as = save_name)


# Relative difference with optimal cost function value vs sqrt(Hilbert space dimension/shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots_o_dimH"

plot_comparison(x       = [np.sqrt(2**N_QBITS / df["shots"]) for df in df_plot],
                y       = [1 + df["cost"]/brute_cost for df in df_plot],
                legend  = legend_list,
                title   = r"Relative difference with optimal cost function value vs $\sqrt{\frac{dim(H)}{Shots}}$",
                xlabel  = r"$\sqrt{\frac{dim(H)}{Shots}}$",
                ylabel  = "Relative difference with optimal cost function value",
                leg_loc = "upper left",
                save_as = save_name)

# Relative difference with optimal cost function value vs 1/sqrt(shots)
# (Brute cost is positive)
save_name = folder_name + "rel_dist_vs_inv_shots"

plot_comparison(x       = [1 / np.sqrt(df["shots"]) for df in df_plot],
                y       = [1 + df["cost"]/brute_cost for df in df_plot],
                legend  = legend_list,
                title   = r"Relative difference with optimal cost function value vs $\frac{1}{\sqrt{Shots}}$",
                xlabel  = r"$1 / \sqrt{Shots}$",
                ylabel  = "Relative difference with optimal cost function value",
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
