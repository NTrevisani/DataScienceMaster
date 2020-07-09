# python3 loop_scan.py cost 1
# python3 loop_scan.py cvar 0.5

import sys, os

if len(sys.argv) < 3:
    raise ValueError("Please insert number of shots, cost function type and CVaR alpha value")
cost  = sys.argv[1]
alpha = sys.argv[2]

shots_list = [1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128]

for shots in shots_list:
    command = "python3.7 scan_script.py {0} {1} {2} &".format(shots, cost, alpha)
    print(command)
    os.system(command)
