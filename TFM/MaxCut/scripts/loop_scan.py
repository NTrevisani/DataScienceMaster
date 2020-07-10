# 10-qbits problem
# python3 loop_scan.py cost 1   10 20
# python3 loop_scan.py cvar 0.5 10 20
# python3 loop_scan.py cvar 0.2 10 20

# 11-qbits problem
# python3 loop_scan.py cost 1   11 22
# python3 loop_scan.py cvar 0.5 11 22
# python3 loop_scan.py cvar 0.2 11 22

# 12-qbits problem
# python3 loop_scan.py cost 1   12 24
# python3 loop_scan.py cvar 0.5 12 24
# python3 loop_scan.py cvar 0.2 12 24

import sys, os

n_vertices = 10
n_edges    = 20

if len(sys.argv) < 3:
    raise ValueError("Please insert number of shots, cost function type and CVaR alpha value")
cost  = sys.argv[1]
alpha = sys.argv[2]
if len(sys.argv) > 3:
    n_vertices  = sys.argv[3]
if len(sys.argv) > 4:
    n_edges     = sys.argv[4]


shots_list = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 256]

for shots in shots_list:
    command = "python3.7 scan_script.py {0} {1} {2} {3} {4}&".format(shots,
                                                                     cost,
                                                                     alpha,
                                                                     n_vertices,
                                                                     n_edges)
    print(command)
    os.system(command)
