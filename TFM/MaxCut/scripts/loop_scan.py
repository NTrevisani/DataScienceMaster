# 10-qbits problem
# python3 loop_scan.py cost 1   10 22
# python3 loop_scan.py cvar 0.5 10 22
# python3 loop_scan.py cvar 0.2 10 22

# 11-qbits problem
# python3 loop_scan.py cost 1   11 27
# python3 loop_scan.py cvar 0.5 11 27
# python3 loop_scan.py cvar 0.2 11 27

# 12-qbits problem
# python3 loop_scan.py cost 1   12 33
# python3 loop_scan.py cvar 0.5 12 33
# python3 loop_scan.py cvar 0.2 12 33

# 13-qbits problem
# python3 loop_scan.py cost 1   13 39
# python3 loop_scan.py cvar 0.5 13 39
# python3 loop_scan.py cvar 0.2 13 39

import sys, os

n_vertices = 10
n_edges    = 20

if len(sys.argv) < 5:
    raise ValueError("Please insert:\n cost function type\n CVaR alpha value\n number of vertices\n number of edges")
cost       = sys.argv[1]
alpha      = sys.argv[2]
n_vertices = sys.argv[3]
n_edges    = sys.argv[4]

# keep the ratio n_edges/max(n_edges) constant for all n_vertices values
n_edges = int(0.5*n_vertices*(n_vertices-1) * 0.5)

shots_list = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 192, 256, 512]

for shots in shots_list:
    command = "python3.7 scan_script.py {0} {1} {2} {3} {4} &".format(shots,
                                                                     cost,
                                                                     alpha,
                                                                     n_vertices,
                                                                     n_edges)
    print(command)
    os.system(command)
