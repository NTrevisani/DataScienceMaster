import numpy as np
import pandas as pd
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit import IBMQ
import pickle
import sys
import matplotlib.pyplot as plt 


# The actual function
def qubo_to_ising(input_Q):
    n = len(input_Q)
    print("input:")
    print(input_Q)
    print("")
    
    # initialize H
    H = 0

    # compute the contribution of the i,j term to the Hamiltonian
    # i = left-side term = x_i (corresponds to sigma_z)
    for i in range(n):
        # j = right-side term = (1 - x_j) (corresponds to minus_z)
        for j in range(n):            
            # first term
            matrix_ij = 0
            if i == 0:
                matrix_ij = sigma_z
            elif j == 0:
                matrix_ij = minus_z
            else:
                matrix_ij = id_matrix
            
            # tensor product n times
            for k in range(1,n):
                if i == k:
                    new_term = sigma_z
                elif j == k:
                    new_term = minus_z
                else:
                    new_term = id_matrix                
                matrix_ij = np.kron(matrix_ij, new_term)

            # multiply by the i,j term of input_Q 
            matrix_ij = matrix_ij * input_Q[i,j]
            
            # sum
            H = H + matrix_ij
    
    return(-H)


# Compute the value of the cost function
# results: the results dictionary in the outcome of the circuit measurement
# weights: the original QUBO matrix
def cost_function_C(results, weights):
    
    # the eigenstates obtained by the evaluation of the circuit
    eigenstates = list(results.keys())
    
    # how many times each eigenstate has been sampled
    abundancies = list(results.values())
    
    # number of shots 
    shots = sum(results.values())
    
    # initialize the cost function
    cost = 0
    
    for k in range(len(eigenstates)):
        # ndarray of the digits extracted from the eigenstate string 
        x = np.array([int(num) for num in eigenstates[k]])
        # Cost function due to the k-th eigenstate
        cost = cost + x.dot(W.dot(1-x)) * abundancies[k]
    
    return -cost / shots


# Write the circuit as a parametric function
def VQE_circuit(theta, n, depth): 
    """Creates a variational-form RY ansatz.
    
    theta: (depth+1 x n) matrix of rotation angles,
    n: number of qbits,
    depth: number of layers.
    """
        
    if len(theta.ravel()) != ((depth+1) * n):        
        raise ValueError("Theta cannot be reshaped as a (depth+1 x n) matrix")

    theta.shape = (depth + 1, n)

    # Define the Quantum and Classical Registers
    q = QuantumRegister(n)
    c = ClassicalRegister(n)

    # Build the circuit for the ansatz
    circuit = QuantumCircuit(q, c)

    # Put all the qbits in the |+> state
    for i in range(n):
        circuit.ry(theta[0,i],q[i])
    circuit.barrier()
    
    # Now introduce the z-gates and RY-gates 'depth' times
    for j in range(depth):
        # Apply controlled-z gates
        for i in range(n-1):
            circuit.cz(q[i], q[i+1])

        # Introduce RY-gates
        for i in range(n):
            circuit.ry(theta[j+1,i],q[i])
        circuit.barrier()
    
    # Close the circuit with qbits measurements
    circuit.measure(q, c)
    
    return circuit    


# In case you want to use a real quantum device as backend
def cost_function_cobyla(params, 
                         weights,   # = W, 
                         n_qbits,   # = 5, 
                         depth,     # = 2,
                         shots,     # = 1024
                         backend_name = 'qasm_simulator',
                         verbosity    = False):
    """Creates a circuit, executes it and computes the cost function.
    
    params: ndarray with the values of the parameters to be optimized,
    weights: the original QUBO matrix of the problem,
    n_qbits: number of qbits of the circuit,
    depth: number of layers of the ciruit,
    shots: number of evaluations of the circuit state,
    verbosity: activate/desactivate some control printouts.
    
    The function calls 'VQE_circuit' to create the circuit, then
    evaluates it and compute the cost function.
    """
    
    if (verbosity == True):
        print("Arguments:")
        print("params  = \n", params)
        print("weights = \n", weights)
        print("qbits   = ", n_qbits)
        print("depth   = ", depth)
        print("shots   = ", shots)
        print("backend = ", backend_name)
    
    circuit = VQE_circuit(params, n_qbits, depth)
    
    if backend_name == 'qasm_simulator':
        backend = Aer.get_backend('qasm_simulator')
    else:
        provider = IBMQ.load_account()
        backend = provider.get_backend(backend_name)
    
    # Execute the circuit on a simulator
    job = execute(circuit, 
                  backend = backend, 
                  shots   = shots)
    results = job.result()
    
    # the eigenstates obtained by the evaluation of the circuit
    eigenstates = list(results.get_counts().keys())
    
    # how many times each eigenstate has been sampled
    abundancies = list(results.get_counts().values())
    
    # number of shots 
    shots = sum(results.get_counts().values())
    
    # initialize the cost function
    cost = 0
    
    for k in range(len(eigenstates)):
        # ndarray of the digits extracted from the eigenstate string 
        x = np.array([int(num) for num in eigenstates[k]])
        # Cost function due to the k-th eigenstate
        cost = cost + x.dot(W.dot(1-x)) * abundancies[k]
    
    if (verbosity == True):
        print("cost = ", -cost/shots)

    return -cost / shots


# Is time a good figure of merit?
# https://stackoverflow.com/questions/27728483/understanding-the-output-of-scipy-optimize-basinhopping
import time
from scipy.optimize import minimize

def time_vs_shots(shots,
                  weights,
                  n_qbits,
                  depth,
                  backend_name,
                  final_eval_shots,
                  verbosity = False):
    """Returns the time taken to solve a VQE problem
    as a function of the shots.    
    
    Input parameters:
    shots: number of evaluations of the circuit state,
    weights: the original QUBO matrix of the problem,
    n_qbits: number of qbits of the circuit,
    depth: number of layers of the ciruit,
    backend_name: the name of the device where the optimization will be performed,
    final_eval_shots: number of shots for the evaluation of the optimized circuit,
    verbosity: activate/desactivate some control printouts.
    
    Output:
    elapsed_time: time taken for the optimization (in seconds)
    counts: the results of the optimization
    shots: the 'shots' input parameter (it may be useful for analysis)
    """
    
    # Create the rotation angles for the ansatz
    theta_0       = np.repeat(PI/2, n_qbits)
    theta_0.shape = (1, n_qbits)
    theta_1       = np.zeros((depth, n_qbits))
    theta         = np.concatenate((theta_0, theta_1), axis = 0) 
    
    # Time starts with the optimization
    start_time = time.time()

    # Classical optimizer tuning
    res = minimize(fun     = cost_function_cobyla, 
                   x0      = theta.ravel(),     # the 'params' argument of 'cost_function_cobyla'
                   method  = 'COBYLA',          # we want to use the COBYLA optimization algorithm
                   options = {'maxiter': 500},  # maximum number of iterations
                   tol     = 0.0001,            # tolerance or final accuracy in the optimization 
                   args    = (weights, 
                              n_qbits, 
                              depth, 
                              shots,
                              backend_name))    # the arguments of 'cost_function_cobyla', except 'params'

    # Time stops when the optimization stops
    end_time = time.time()
    
    # Total time taken for the optimization
    elapsed_time = end_time - start_time 

    # Number of cost function evaluations during the optimization
    n_func_evaluations = res.nfev

    # Obtain the output distribution using the final parameters
    optimal_circuit = VQE_circuit(res.x, 
                                  n_qbits, 
                                  depth)

    # Define the backend for the evaluation of the optimal circuit
    # - in case it is a simulator
    if backend_name == 'qasm_simulator':
        backend = Aer.get_backend('qasm_simulator')
    # - in case it is a real quantum device
    else:
        provider = IBMQ.load_account()
        backend = provider.get_backend(backend_name)

    # Get the results from the circuit with the optimized parameters    
    counts = execute(optimal_circuit, 
                     backend, 
                     shots = final_eval_shots).result().get_counts(optimal_circuit)
    
    return elapsed_time, counts, shots, n_func_evaluations, final_eval_shots


# Plot function definition
def scatter_plot(x, y, 
                 title = "", xlabel = "", ylabel = "", save_as = "", 
                 ylim = (-9999, -9999)):
    # Plot declaration
    fig, ax = plt.subplots()
    local_plot = ax.scatter(x = x,
                            y = y)

    # Title
    ax.set_title(title)

    # Cosmetics
    if ylim == (-9999, -9999):
        ax.set_ylim(0.0, 1.5*np.max(y))
    else:    
        ax.set_ylim(ylim)
    ax.set_xlim(0.0, 1.1*np.max(x))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # Save as png and pdf
    if save_as != "":
        plt.savefig(save_as + '.png')
        plt.savefig(save_as + '.pdf')


# Compute the value of the cost function of each eigenstate in a solution
# and returns to 'best candidate' eigenstate
# results_dict: the eigenstate-freq dictionary returned by 'time_vs_shots'
# weights: the original QUBO matrix
def best_candidate_finder(results_dict, 
                          weights):
        
    # the eigenstates obtained by the evaluation of the circuit
    eigenstates = list(results_dict.keys())
        
    # initialize the cost function
    min_cost = 0
    best_candidate = 0
    
    for k in range(len(eigenstates)):
        # ndarray of the digits extracted from the eigenstate string 
        x = np.array([int(num) for num in eigenstates[k]])
        # Cost function of to the k-th eigenstate
        cost = x.dot(W.dot(1-x))
        if cost > min_cost:
            min_cost = cost
            best_candidate = eigenstates[k]
    
    return best_candidate
        

# Function to compute F_opt
def F_opt_finder(results_obj,
                 n_shots,
                 W,
                 opt_sol,
                 n_eigenstates = 1000):
    """Returns the fraction of optimal solutions.
    
    Given the object returned by 'time_vs_shots',
    computes the fraction of best_candidates solutions
    which are optimal solutions.
    
    Inputs:
    results_obj: the object returned by 'time_vs_shots',
    n_shots: the 'number of shots' to investigate,
    W: the original QUBO matrix,
    opt_sol: list of the optimal solutions to the problem,
    n_eigenstates: maximum number of eigenstates in a solution.
    """
    # Initialize the counter of repetitions for the
    # selected number of shots
    N_rep = 0
    # Initialize the counter of best candidates which 
    # are optimal solutions    
    N_bc  = 0
    # Scan all the entries of the object
    for res in results_obj:
        # Select only the entries corresponding to 
        # the selected number of shots
        if res[2] == n_shots:
            # If the number of shots is the one we want to check,
            # sum 1 to the number of repetitions
            N_rep += 1
            # Find best candidate
            bc = best_candidate_finder(res[1], W)
            # best candidate must contain the optimal solution
            if bc in opt_sol:
                # best candidate must have less than 'n_eigenstates' eigenstates
                if len(res[1]) < n_eigenstates:
                    N_bc += 1
    # Initialize output value
    F_opt = 0
    # If N_rep is not 0, return the fraction of best candidates
    # which are also optimal solutions
    if N_rep != 0:
        F_opt = N_bc / N_rep
    else:
        print("The number of shots selected is not present")
    return F_opt


# We can save the results to produce them once and analyze them later
#https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
def save_object(obj, filename):
    with open(filename, 'wb') as output:  
        # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)   
        print("Object saved as", filename)


# This function is useful to check the memory usage
# https://stackoverflow.com/a/1094933/1870254
def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


# QUBO matrix used as example
W = np.array([[0, 1, 2, 0, 0],
              [1, 0, 2, 0, 0],
              [2, 2, 0, 2, 2],
              [0, 0, 2, 0, 1],
              [0, 0, 2, 1, 0]])

# PI declaration
PI = np.pi
